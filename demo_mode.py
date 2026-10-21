"""Static demo boundary, applied to existing pages and every SEO build.

Run python3 demo_mode.py after editing a legacy HTML page.
No browser-side patching: intake links are removed from delivered HTML.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSP = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' blob:; connect-src 'none'; frame-src 'none'; object-src 'none'; form-action 'none'; base-uri 'self'; upgrade-insecure-requests"
NOTICE = '<a class="demo-mode-note" href="/privacy-policy.html">Демонстрационный проект · Прием заявок отключен</a>'
CONTACT = '''<section id="contact" class="sec-bg" style="--bgimg:url(/img/andrey-suit-800.webp);"><div class="container">
<p class="eyebrow">SHELESTFIT · демоверсия</p><h2 class="h-sec">Пример сайта из портфолио</h2>
<p class="lead">Здесь можно посмотреть дизайн и структуру сайта тренера. Запись на тренировки, консультации и прием заявок отключены. Описания услуг и цены показаны как элементы макета.</p>
<p style="margin-top:24px"><a class="btn btn--gold" href="/privacy-policy.html">О демонстрационном проекте</a></p></div></section>'''
DEMO_COPY = 'В демоверсии прием заявок отключен.'

def demo_html(source):
    if 'data-demo-legal' in source:
        return source
    if not re.search(r'<body\b', source, re.I) or 'Verification: ' in source:
        return source  # preserve search-engine verification documents
    h = source
    h = h.replace('Демонстрационный пример. Через этот сайт нельзя записаться, заказать услугу или отправить заявку.', DEMO_COPY)
    h = re.sub(r'<!-- analytics begin -->.*?<!-- analytics end -->', '<!-- analytics begin --><!-- analytics end -->', h, flags=re.S)
    h = re.sub(r'<script\b[^>]*src=["\'][^"\']*analytics-consent[^"\']*["\'][^>]*>\s*</script>', '', h, flags=re.I)
    h = re.sub(r'<script\b[^>]*>.*?</script>', lambda m: '' if re.search(r'\b(?:ym|gtag)\s*\(', m.group()) else m.group(), h, flags=re.S|re.I)
    h = re.sub(r'<section\b[^>]*\bid="contact"[^>]*>.*?</section>', lambda m: CONTACT, h, flags=re.S)
    h = re.sub(r'<!-- =+ ИИ-КОНСУЛЬТАНТ =+ -->.*?(?=<script>)', '', h, flags=re.S)
    h = re.sub(r'/\* Contact panel:.*?\}\)\(\);', '', h, flags=re.S)
    # No form submission / free-text collection, even when a legacy page returns.
    h = re.sub(r'<form\b[^>]*>.*?</form>', '<p>'+DEMO_COPY+'</p>', h, flags=re.S|re.I)
    h = re.sub(r'<(?:input|textarea|iframe)\b[^>]*>(?:.*?</(?:textarea|iframe)>)?', '', h, flags=re.S|re.I)
    chunks = re.split(r'(<script\b.*?</script>)', h, flags=re.S|re.I)
    for i in range(0, len(chunks), 2):
        block = chunks[i]
        def label(m):
            if re.search(r'почт(?:а|у|е|ы|ой)|\bemail\b|напишите|пришлите|свяжитесь|присылайте', m.group(3), re.I):
                attrs = re.sub(r'\s+data-i18n="[^"]*"', '', m.group(2))
                return '<'+m.group(1)+attrs+'>Демонстрационный пример</'+m.group(1)+'>'
            return m.group()
        block = re.sub(r'<(h[2-6]|li|span|strong|b)([^>]*)>([^<]*)</\1>', label, block, flags=re.I)
        # Reword invitations, including texts without a button.
        block = re.sub(r'<p\b[^>]*>.*?</p>', lambda m: '<p>'+DEMO_COPY+'</p>' if re.search(r'почт(?:а|у|е|ы|ой)|\bemail\b|напишите|пришлите|свяжитесь|присылайте', re.sub(r'<[^>]+>', ' ', m.group()), re.I) else m.group(), block, flags=re.S|re.I)
        def anchor(m):
            a, body = m.group(1), m.group(2)
            href = re.search(r'\bhref=["\']([^"\']+)', a, re.I)
            dest = html.unescape(href.group(1)) if href else ''
            text = re.sub(r'<[^>]+>', '', body).strip()
            intake = dest.lower().startswith(('mailto:', 'tel:', 'https://t.me/', 'http://t.me/', 'https://wa.me/')) or bool(re.search(r'(?:^|/)index\.html#contact$|^/?#contact$', dest))
            if intake or re.search(r'(?:privacy-policy|soglasie)\.html', dest):
                classes = re.search(r'\bclass="([^"]+)"', a)
                cls = ' class="'+html.escape(classes.group(1), quote=True)+'"' if classes else ''
                return '<a'+cls+' href="/privacy-policy.html">О демоверсии</a>'
            return m.group()
        block = re.sub(r'<a\b([^>]*)>(.*?)</a>', anchor, block, flags=re.S|re.I)
        block = re.sub(r'(<span\b[^>]*data-i18n="ftr.pay"[^>]*>).*?</span>', '<span>Демонстрационный проект, услуги не оказываются</span>', block, flags=re.S)
        block = re.sub(r'(<p\b[^>]*data-i18n="ftr.bio"[^>]*>).*?</p>', '<p>Демонстрационный сайт тренера из портфолио разработки.</p>', block, flags=re.S)
        chunks[i] = block
    h = ''.join(chunks)
    demo_link = r'<a\b[^>]*href="/privacy-policy\.html"[^>]*>О демоверсии</a>'
    h = re.sub('('+demo_link+r')\s*(?:·\s*)?'+demo_link, r'\1', h)
    h = re.sub(r'<title>(?!Демоверсия)(.*?)</title>', r'<title>Демоверсия | \1</title>', h, flags=re.S)
    # Remove commercial/identity schema; retain navigation and educational FAQ.
    def schema(m):
        data = json.loads(m.group(1))
        if data.get('@type') not in ('BreadcrumbList', 'Article', 'CollectionPage'):
            return ''
        return m.group()
    h = re.sub(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', schema, h, flags=re.S)
    h = re.sub(r'\n?<meta\b[^>]*(?:http-equiv="Content-Security-Policy"|name="referrer")[^>]*>', '', h, flags=re.I)
    boundary = '<meta http-equiv="Content-Security-Policy" content="'+CSP+'">\n<meta name="referrer" content="no-referrer">'
    h = re.sub(r'(<meta charset="utf-8">)', lambda m: m.group(1)+'\n'+boundary, h, count=1, flags=re.I)
    if '/css/demo-mode.css' not in h:
        h = h.replace('</head>', '<link rel="stylesheet" href="/css/demo-mode.css">\n</head>')
    h = re.sub(r'<a class="demo-mode-note".*?</a>\n?', '', h, flags=re.S)
    h = h.replace('</body>', NOTICE+'\n</body>')
    # Theme controls are local to the current document, without browser storage.
    h = h.replace("localStorage.getItem('sh-theme')", "document.documentElement.getAttribute('data-theme')")
    h = h.replace("localStorage.getItem('sh-font')", "document.documentElement.getAttribute('data-font')")
    h = h.replace("localStorage.setItem('sh-theme', d.dataset.theme)", "document.documentElement.setAttribute('data-theme', d.dataset.theme)")
    h = h.replace("localStorage.setItem('sh-font', d.dataset.font)", "document.documentElement.setAttribute('data-font', d.dataset.font)")
    h = re.sub(r'\s+data-ev="[^"]*"', '', h)
    return h

if __name__ == '__main__':
    changed = 0
    for p in sorted(ROOT.rglob('*.html')):
        old = p.read_text(encoding='utf-8')
        new = demo_html(old)
        if new != old:
            p.write_text(new, encoding='utf-8'); changed += 1
    print('Demo pages updated:', changed)
