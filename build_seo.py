#!/usr/bin/env python3
"""SEO-посадочные SHELESTFIT.COM: один компонент страницы, данные в seo/.

  seo/registry.json      реестр всех 80 кандидатов (status, index, cluster, productType, mergedInto…)
  seo/content/*.json     контент опубликованных страниц (по кластерам)
  index.html             источник истины для шапки, футера, аналитики и ЦЕН (тарифы/разовые услуги)

Запуск:  python3 build_seo.py          сборка + проверки (падает при ошибке)
         python3 build_seo.py --check  только проверки, без записи файлов

Результат:
  /<slug>/index.html     новые посадочные (URL вида /slug/)
  /<legacy>.html         существующие страницы, чей intent совпал с кандидатом (URL не меняется)
  sitemap.xml            существующие URL сайта + опубликованные SEO-URL (merged/disabled не попадают)
"""
import json, re, sys, os, glob, html, urllib.parse
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://shelestfit.com'
CHECK_ONLY = '--check' in sys.argv

def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- источник истины: index.html
INDEX = rd('index.html')
ANALYTICS = re.search(r'<!-- analytics begin -->.*?<!-- analytics end -->', INDEX, re.S).group(0)
HEADER = re.search(r'<header class="hdr".*?</header>', INDEX, re.S).group(0)
FOOTER = re.search(r'<footer class="ftr".*?</footer>', INDEX, re.S).group(0)

def absolutize(block):
    """Ссылки шапки/футера главной -> абсолютные (страницы лежат и в подпапках)."""
    block = block.replace('href="#"', 'href="/"')
    block = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', block)
    block = re.sub(r'href="(?!https?:|/|#|mailto:|tel:)([^"]+)"', r'href="/\1"', block)
    return block
HEADER = absolutize(HEADER)
FOOTER = absolutize(FOOTER)

def parse_prices():
    """Тарифы и разовые услуги берём из вёрстки главной, а не из второго списка цен."""
    prod = {}
    pr = re.search(r'<section id="pricing">.*?</section>', INDEX, re.S).group(0)
    for m in re.finditer(r'<div class="ptier[^"]*">(.*?)</ul>', pr, re.S):
        b = m.group(1)
        name = re.search(r'ptier__name[^>]*>([^<]+)<', b).group(1).strip()
        sub = re.search(r'ptier__sub[^>]*>([^<]+)<', b).group(1).strip()
        rub, usd = map(int, re.search(r'data-price="(\d+)\|(\d+)"', b).groups())
        items = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<li[^>]*>(.*?)</li>', b + '</ul>', re.S)]
        prod[name] = dict(name=name, sub=sub, rub=rub, usd=usd, monthly=True, items=items, src=f'index.html#pricing «{name}»')
    sv = re.search(r'<section id="services">.*?</section>', INDEX, re.S).group(0)
    for m in re.finditer(r'<div class="svc__c[^"]*">(.*?)</div>\s*(?=<div class="svc__c|</div>)', sv, re.S):
        b = m.group(1)
        t = re.search(r'<h4[^>]*>([^<]+)</h4>', b)
        p = re.search(r'data-price="(\d+)\|(\d+)"', b)
        d = re.search(r'<p data-i18n="sv\.s\d\.d">([^<]+)</p>', b)
        if t and p:
            name = t.group(1).strip()
            prod[name] = dict(name=name, sub=d.group(1).strip() if d else '', rub=int(p.group(1)), usd=int(p.group(2)), monthly=False, items=[],
                              src=f'index.html#services «{name}»')
    return prod

SITE_PRODUCTS = parse_prices()
# productType -> карточка на сайте. Названия как на сайте (источник истины по формулировкам).
PRODUCT_MAP = {
    'program_monthly': 'Программа',
    'full': 'Полное сопровождение',
    'vip': 'VIP-формат',
    'program_once': 'Индивидуальная программа тренировок',
    'nutrition': 'Разбор питания',
    'labs': 'Консультация с учётом анализов',
    'consult': 'Разовая консультация',
}
# Актуальная продуктовая логика из ТЗ: сверяем, что вёрстка главной ей соответствует.
TZ_PRICES = {'program_monthly': (10000, True), 'full': (15000, True), 'vip': (20000, True),
             'program_once': (10000, False), 'nutrition': (10000, False), 'labs': (10000, False), 'consult': (3000, False)}
PRODUCTS = {}
for key, site_name in PRODUCT_MAP.items():
    p = SITE_PRODUCTS.get(site_name)
    if not p:
        sys.exit(f'Нет карточки «{site_name}» на index.html — проверьте вёрстку тарифов')
    rub, monthly = TZ_PRICES[key]
    if (p['rub'], p['monthly']) != (rub, monthly):
        sys.exit(f'Цена «{site_name}» на index.html ({p["rub"]}) расходится с ТЗ ({rub}); SEO-сборка остановлена')
    PRODUCTS[key] = dict(p, key=key)
# Подписи, чтобы не путать ежемесячную «Программу» и разовую «Индивидуальную программу»
LABEL = {'program_monthly': 'Программа тренировок', 'full': 'Полное сопровождение', 'vip': 'VIP-сопровождение',
         'program_once': 'Индивидуальная программа', 'nutrition': 'Разбор питания',
         'labs': 'Консультация с учётом предоставленных анализов', 'consult': 'Разовая консультация'}

def price_str(p):
    s = f'{p["rub"]:,}'.replace(',', ' ') + ' ₽'
    return s

def tg(text):
    # кириллица остаётся читаемой (браузер кодирует сам), экранируем только служебные символы URL
    enc = ''.join(urllib.parse.quote(ch, safe='') if ch in ' %&#+?"<>\'' else ch for ch in text)
    return 'https://t.me/ShelestF?text=' + enc

def tg_for(page_h1, key):
    p = PRODUCTS[key]
    per = ' в месяц' if p['monthly'] else ''
    rub = f'{p["rub"]:,}'.replace(',', ' ')
    return tg(f'Здравствуйте, Андрей! Пишу со страницы «{page_h1}». Интересует «{LABEL[key]}», {rub} ₽{per}.')

# ---------------------------------------------------------------- данные
REG = json.load(open(os.path.join(ROOT, 'seo/registry.json'), encoding='utf-8'))['pages']
BYID = {e['id']: e for e in REG}
CONTENT = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'seo/content/*.json'))):
    for k, v in json.load(open(f, encoding='utf-8')).items():
        if k in CONTENT: sys.exit(f'Контент {k} задан дважды ({f})')
        CONTENT[k] = v
PUB = [e for e in REG if e['status'] == 'published' and e['index']]
BA = {x['img']: x for x in json.load(open(os.path.join(ROOT, 'ba.json'), encoding='utf-8'))['items']}
CASES = {  # только реальные фото и подписи из ba.json
    'weightloss': ['ba-b65', 'ba-g116', 'ba-g117'],
    'general': ['ba-b65', 'ba-g116', 'ba-g21'],
    'competition': ['ba-g28', 'ba-g116', 'ba-b65'],
    'women': ['ba-g21', 'ba-g23', 'ba-b66'],
}
# Существующие страницы сайта, на которые можно ссылаться из related
EXTRA_LINKS = {
    'pitanie': ('/pitanie.html', 'Питание', 'Разбор рациона под цель и график'),
    'posle-travmy': ('/posle-travmy.html', 'Тренировки после травм', 'Нагрузка с учётом ограничений'),
    'podgotovka': ('/podgotovka-k-sorevnovaniyam.html', 'Подготовка к соревнованиям', 'Пауэрлифтинг, классик-физик, бикини'),
    'results': ('/results.html', 'Результаты клиентов', 'Фото до и после с согласиями'),
}
ARTICLES = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(ROOT, 'articles/*.html'))}
def article_title(slug):
    t = re.search(r'<title>(.*?)</title>', rd(f'articles/{slug}.html')).group(1)
    return html.unescape(t.split(' — ')[0].split(': Андрей')[0])

def url_of(e): return e['path']

# ---------------------------------------------------------------- рендер
def sec_title(t): return f'<h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);">{esc(t)}</h2>'

def render_tariffs(e, c):
    keys = c['tariffs']
    cards = []
    for i, k in enumerate(keys):
        p = PRODUCTS[k]
        mid = ' ptier--mid' if i == 0 else ''
        badge = '<span class="ptier__badge">Под этот запрос</span>' if i == 0 and len(keys) > 1 else ''
        per = '<small> / мес</small>' if p['monthly'] else '<small> разово</small>'
        items = p['items'] or ([p['sub']] if p['sub'] else [])
        sub = p['sub'] if p['monthly'] else ('Разовая услуга, без ежемесячного ведения')
        lis = ''.join(f'<li>{esc(x)}</li>' for x in items)
        btn = 'btn--gold' if i == 0 else 'btn--ghost'
        cards.append(f'''<div class="ptier{mid}">{badge}
        <div class="ptier__name">{esc(LABEL[k])}</div>
        <div class="ptier__sub">{esc(sub)}</div>
        <div class="ptier__price" data-price="{p['rub']}|{p['usd']}"><span class="pv">{price_str(p)}</span>{per}</div>
        <ul class="ptier__list">{lis}</ul>
        <a class="btn {btn}" href="{esc(tg_for(e['h1'], k))}" target="_blank" rel="noopener">Обсудить в Telegram</a>
      </div>''')
    note = c.get('tariffNote', '')
    note_html = f'<p class="lead" style="font-size:.95rem; margin-top:14px;">{note}</p>' if note else ''
    return f'''<section id="pricing">
  <div class="container">
    <p class="eyebrow">Формат и цена</p>
    {sec_title(c.get('tariffTitle', 'Какой формат подходит'))}{note_html}
    <div class="pricing__grid">{''.join(cards)}</div>
    <p style="margin-top:22px; font-size:.86rem; color:var(--ink-mute);">Все форматы и разовые услуги: <a href="/#pricing" style="color:var(--gold-2);">тарифы на главной</a>.</p>
  </div>
</section>'''

def render_cases(kind):
    if not kind or kind == 'none': return ''
    cards = []
    for img in CASES[kind]:
        x = BA[img]
        cards.append(f'''<a class="art-card" href="/results.html" style="padding:0; overflow:hidden;">
        <img src="/img/{img}-500.webp" srcset="/img/{img}-360.webp 360w, /img/{img}-500.webp 500w" sizes="(max-width:860px) 90vw, 30vw" alt="{esc(x['t'])}" loading="lazy" style="width:100%; aspect-ratio:3/4; object-fit:cover;">
        <div style="padding:16px 20px 20px;"><b class="art-card__title" style="font-size:1.05rem;">{esc(x['t'])}</b><p class="art-card__desc" style="margin-top:6px;">{esc(x['d'])}</p></div>
      </a>''')
    return f'''<section id="case">
  <div class="container">
    <p class="eyebrow">Реальные клиенты</p>
    {sec_title('Результаты')}
    <p class="lead" style="font-size:1rem;">Фото клиентов публикуются с их письменного согласия. Результат у каждого свой и зависит от исходных данных и регулярности.</p>
    <div class="art-grid">{''.join(cards)}</div>
    <p style="margin-top:20px;"><a class="btn btn--ghost" href="/results.html">Все результаты</a></p>
  </div>
</section>'''

def related_cards(e, c):
    out = []
    for r in c.get('related', []):
        if r in EXTRA_LINKS:
            href, t, s = EXTRA_LINKS[r]
        else:
            t_e = BYID[r]; tc = CONTENT.get(r, {'eyebrow': ''})
            href, t, s = url_of(t_e), tc.get('breadcrumb', t_e['h1']), tc.get('cardSub', tc['eyebrow'])
        out.append(f'<a class="dir-card" href="{href}"><h3 class="dir-card__t">{esc(t)}</h3><p class="dir-card__s">{esc(s)}</p><span class="dir-card__m">Подробнее →</span></a>')
    arts = ''
    if c.get('articles'):
        links = ''.join(f'<a href="/articles/{a}.html" style="color:var(--ink); font-weight:600;">{esc(article_title(a))} →</a>' for a in c['articles'])
        arts = f'<p style="font-size:.78rem; color:var(--ink-mute); text-transform:uppercase; letter-spacing:.06em; margin:34px 0 14px;">Читать по теме</p><div style="display:flex; flex-direction:column; gap:12px;">{links}</div>'
    return f'''<section id="more">
  <div class="container">
    <p class="eyebrow">Другие направления</p>
    {sec_title(c.get('relatedTitle', 'Смотрите также'))}
    <div class="dir-grid" style="margin-top:28px;">{''.join(out)}</div>{arts}
  </div>
</section>'''

def paras(ps): return ''.join(f'<p>{x}</p>' for x in ps)  # допускаются <a>/<b> из контента

def render(e):
    c = CONTENT[e['id']]
    url = SITE + url_of(e)
    title = f'{c["title"]} · Андрей Шелест'
    main = PRODUCTS[c['tariffs'][0]]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', q['a'])}} for q in c['faq']]}
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "serviceType": LABEL[main['key']], "name": e['h1'],
              "description": c['description'],
              "provider": {"@type": "Person", "name": "Андрей Шелест", "jobTitle": "Онлайн-тренер, чемпион мира", "url": SITE + '/'},
              "areaServed": "RU", "url": url}
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + '/'}]
    parent = c.get('parent')
    if parent:
        pe = BYID[parent]; crumbs.append({"@type": "ListItem", "position": 2, "name": CONTENT[parent].get('breadcrumb', pe['h1']), "item": SITE + url_of(pe)})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": c.get('breadcrumb', e['h1']), "item": url})
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}
    J = lambda o: json.dumps(o, ensure_ascii=False)

    blocks = []
    if c.get('answer'):
        blocks.append(f'''<section>
  <div class="container art-body" style="max-width:820px;">
    {sec_title(c['answer']['h2'])}
    <div style="margin-top:20px;">{paras(c['answer']['p'])}</div>
  </div>
</section>''')
    blocks.append(f'''<section class="sec-bg sec-bg--soft" style="--bgimg:url(/img/{c.get('bg', 'team-6')}-640.webp);">
  <div class="container art-body" style="max-width:820px;">
    {sec_title(c['task']['h2'])}
    <div style="margin-top:20px;">{paras(c['task']['p'])}</div>
  </div>
</section>''')
    no = ''
    if c.get('notFor'):
        no = f'''<div class="fit-col fit-col--no"><h3>Не подходит, если</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in c['notFor'])}</ul></div>'''
    blocks.append(f'''<section>
  <div class="container">
    {sec_title(c['audience']['h2'])}
    <div class="fit-grid" style="margin-top:24px;">
      <div class="fit-col fit-col--yes"><h3>Подходит, если</h3><ul>{''.join(f"<li>{esc(x)}</li>" for x in c['audience']['items'])}</ul></div>
      {no}
    </div>
  </div>
</section>''')
    steps = ''.join(f'<div class="step"><span class="step__n">{i}</span><p>{esc(s)}</p></div>' for i, s in enumerate(c['process']['steps'], 1))
    blocks.append(f'''<section class="sec-bg sec-bg--soft" style="--bgimg:url(/img/{c.get('bg', 'team-6')}-640.webp);">
  <div class="container">
    {sec_title(c['process']['h2'])}
    <div class="steps" style="margin-top:28px;">{steps}</div>
  </div>
</section>''')
    ben = ''.join(f'<div class="svc__c"><h4>{esc(b["t"])}</h4><p>{esc(b["d"])}</p></div>' for b in c['benefits']['items'])
    blocks.append(f'''<section>
  <div class="container">
    {sec_title(c['benefits']['h2'])}
    <div class="svc">{ben}</div>
  </div>
</section>''')
    blocks.append(f'''<section>
  <div class="container art-body" style="max-width:820px;">
    {sec_title(c['why']['h2'])}
    <div style="margin-top:20px;">{paras(c['why']['p'])}</div>
  </div>
</section>''')
    blocks.append(render_tariffs(e, c))
    blocks.append(render_cases(c.get('cases')))
    faq = ''.join(f'''<div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false"><span>{esc(q['q'])}</span><i class="faq__ic" aria-hidden="true"></i></button>
        <div class="faq__a"><p>{q['a']}</p></div>
      </div>''' for q in c['faq'])
    blocks.append(f'''<section id="faq">
  <div class="container">
    {sec_title('Частые вопросы')}
    <div class="faq__list" style="margin-top:24px;">{faq}</div>
  </div>
</section>''')
    blocks.append(f'''<section class="seg-cta sec-bg sec-bg--soft" style="--bgimg:url(/img/{c.get('bg', 'team-6')}-640.webp);">
  <div class="container" style="text-align:center;">
    <h2 class="h-sec" style="font-size:clamp(1.7rem,3vw,2.4rem);">{esc(c['ctaTitle'])}</h2>
    <p class="lead" style="margin:14px auto 28px;">{esc(c['ctaText'])}</p>
    <a class="btn btn--gold" href="{esc(tg_for(e['h1'], main['key']))}" target="_blank" rel="noopener" style="font-size:1.02rem;">Написать в Telegram</a>
  </div>
</section>''')
    blocks.append(related_cards(e, c))

    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(c['description'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/core.css">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta name="theme-color" content="#0b0b0c">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(c['title'])}">
<meta property="og:description" content="{esc(c['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="ru_RU">
<meta property="og:image" content="{SITE}/img/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/img/og-cover.jpg">
<script type="application/ld+json">{J(svc_ld)}</script>
<!-- seo:breadcrumbs -->
<script type="application/ld+json">{J(bc_ld)}</script>
<!-- seo:faq-schema -->
<script type="application/ld+json">{J(faq_ld)}</script>
{ANALYTICS}
</head>
<body>
<!-- generated by build_seo.py from seo/registry.json ({e['id']}); правки вносить в seo/content, не в этот файл -->
{HEADER}

<section class="seg-hero sec-bg" style="padding-top:150px; --bgimg:url(/img/{c.get('bg', 'team-6')}-640.webp);">
  <div class="container">
    <p class="eyebrow">{esc(c['eyebrow'])}</p>
    <h1 class="h-sec" style="font-size:clamp(2rem,4.4vw,3.4rem); max-width:22ch;">{esc(e['h1'])}</h1>
    <p class="lead" style="font-size:1.1rem; margin-top:18px;">{esc(c['lead'])}</p>
    <div style="display:flex; gap:14px; margin-top:30px; flex-wrap:wrap;">
      <a class="btn btn--gold" href="{esc(tg_for(e['h1'], main['key']))}" target="_blank" rel="noopener">Написать в Telegram</a>
      <a class="btn btn--ghost" href="#pricing">Формат и цена</a>
    </div>
  </div>
</section>

{chr(10).join(b for b in blocks if b)}

{FOOTER}
<script src="/js/seo-landing.js" defer></script>
<script src="/js/premium.js" defer></script>
</body>
</html>
'''

def out_path(e):
    p = e['path']
    return p.strip('/') + '/index.html' if p.endswith('/') else p.lstrip('/')

# ---------------------------------------------------------------- проверки
ALLOWED_RUB = {'10 000', '15 000', '20 000', '3 000'}
BAD_PHRASES = ['гарантирую', 'гарантированн', 'уникальная авторская', 'авторская методика', 'минус 10 кг',
               'лучшей версией', 'поставлю диагноз', 'вылечу', 'лечу ', 'не просто', 'не только', '«', '»']
def text_of(h):
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(re.sub(r'\s+', ' ', h))

def validate(pages):
    errs, warns = [], []
    ids = {e['id'] for e in PUB}
    for e in PUB:
        if e['id'] not in CONTENT: errs.append(f'{e["id"]}: нет контента')
    for e in REG:
        if e['status'] == 'merged' and BYID[e['mergedInto']]['status'] != 'published':
            errs.append(f'{e["id"]}: mergedInto {e["mergedInto"]} не опубликована')
    seen_t, seen_d, seen_h = Counter(), Counter(), Counter()
    sent_pages = defaultdict(set)
    for e, h in pages:
        c = CONTENT[e['id']]
        seen_t[c['title']] += 1; seen_d[c['description']] += 1; seen_h[e['h1']] += 1
        if h.count('<h1') != 1: errs.append(f'{e["id"]}: H1 != 1')
        if 'noindex' in h: errs.append(f'{e["id"]}: noindex')
        if len(c['title']) > 62: warns.append(f'{e["id"]}: title {len(c["title"])} симв.')
        if not 110 <= len(c['description']) <= 175: warns.append(f'{e["id"]}: description {len(c["description"])} симв.')
        if not 4 <= len(c['faq']) <= 7: errs.append(f'{e["id"]}: FAQ {len(c["faq"])}')
        if not 3 <= len(c['audience']['items']) <= 6: errs.append(f'{e["id"]}: audience {len(c["audience"]["items"])}')
        rel = c.get('related', [])
        if not 3 <= len(rel) <= 8: errs.append(f'{e["id"]}: related {len(rel)}')
        for r in rel:
            if r not in EXTRA_LINKS and (r not in ids): errs.append(f'{e["id"]}: related {r} не опубликована')
            if r == e['id']: errs.append(f'{e["id"]}: ссылка на себя')
        for a in c.get('articles', []):
            if a not in ARTICLES: errs.append(f'{e["id"]}: статьи {a} нет')
        kw = e['primaryKeyword'].split()[0][:5].lower()
        body = text_of(h)
        for m in re.findall(r'(\d[\d\s ]*)\s?₽', body):
            v = re.sub(r'[\s ]+', ' ', m).strip()
            if v not in ALLOWED_RUB: errs.append(f'{e["id"]}: недопустимая цена «{v} ₽»')
        content_text = text_of(json.dumps(c, ensure_ascii=False))
        for b in BAD_PHRASES:
            if b.lower() in content_text.lower(): errs.append(f'{e["id"]}: запрещённое «{b}»')
        if '—' in content_text or ' – ' in content_text: errs.append(f'{e["id"]}: тире в тексте')
        for href in re.findall(r'href="(/[^"#?]*)', h):
            p = href.lstrip('/')
            if p == '': continue
            f = os.path.join(ROOT, p + ('index.html' if p.endswith('/') else ''))
            if not os.path.exists(f) and not any(out_path(x) == (p + 'index.html' if p.endswith('/') else p) for x in PUB):
                errs.append(f'{e["id"]}: битая ссылка {href}')
        # повторяющиеся предложения между страницами
        for s in re.split(r'(?<=[.!?])\s+', ' '.join(
                c['task']['p'] + c['why']['p'] + (c.get('answer') or {}).get('p', []) + [c['lead']] +
                [q['a'] for q in c['faq']] + [b['d'] for b in c['benefits']['items']])):
            s = re.sub(r'<[^>]+>', '', s).strip()
            if len(s) > 50: sent_pages[s].add(e['id'])
    for k, n in seen_t.items():
        if n > 1: errs.append(f'дубль title: {k}')
    for k, n in seen_d.items():
        if n > 1: errs.append(f'дубль description: {k}')
    for k, n in seen_h.items():
        if n > 1: errs.append(f'дубль H1: {k}')
    for s, ps in sent_pages.items():
        if len(ps) > 2: errs.append(f'предложение на {len(ps)} страницах ({",".join(sorted(ps))}): {s[:80]}')
        elif len(ps) == 2: warns.append(f'предложение на 2 страницах ({",".join(sorted(ps))}): {s[:70]}')
    return errs, warns

# ---------------------------------------------------------------- sitemap
def build_sitemap():
    """sitemap = базовые URL сайта (seo/sitemap_base.json) + published/index SEO-страницы из реестра.
    Идемпотентно: не читает собственный предыдущий результат."""
    base = json.load(open(os.path.join(ROOT, 'seo/sitemap_base.json'), encoding='utf-8'))['urls']
    blocked = {SITE + '/' + e['slug'] + '/' for e in REG if not e['index']}
    rows, seen = [], set()
    for u in base:
        if u['loc'] in blocked or u['loc'] in seen: continue
        seen.add(u['loc']); rows.append((u['loc'], u['changefreq'], u['priority']))
    for e in PUB:
        u = SITE + e['path']
        if u in seen: continue
        seen.add(u); rows.append((u, 'monthly', '0.7'))
    body = ''.join(f'  <url>\n    <loc>{l}</loc>\n    <changefreq>{c}</changefreq>\n    <priority>{p}</priority>\n  </url>\n' for l, c, p in rows)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n'

# ---------------------------------------------------------------- main
if __name__ == '__main__':
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    todo = [e for e in PUB if e['id'] in CONTENT and (not only or e['id'] in only)]
    pages = [(e, render(e)) for e in todo]
    errs, warns = validate(pages)
    if only:  # частичная проверка: игнорируем отсутствие контента у чужих страниц
        errs = [x for x in errs if 'нет контента' not in x]
    for w in warns: print('WARN', w)
    for x in errs: print('ERR ', x)
    missing = [e['id'] for e in PUB if e['id'] not in CONTENT]
    print(f'published={len(PUB)} rendered={len(pages)} missing_content={missing}')
    if errs: sys.exit(1)
    if CHECK_ONLY: sys.exit(0)
    for e, h in pages:
        p = os.path.join(ROOT, out_path(e))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(h)
    if not missing and not only:
        open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(build_sitemap())
        print('sitemap.xml обновлён')
