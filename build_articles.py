#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Портал статей для shelestfit.com.

Читает Markdown-файлы из articles/src/*.md (с front-matter) и генерирует:
  • articles/<slug>.html  — отдельную SEO-страницу на каждую статью
                            (canonical на свой сайт, og, JSON-LD Article)
  • articles.html          — витрину со всеми статьями (карточки, поиск по тегу)
  • дополняет sitemap.xml   — все URL статей

Добавить статью: положить .md в articles/src/ и запустить `python3 build_articles.py`.
Формат front-matter:
---
title: Заголовок
description: Короткое описание для поисковика (1-2 предложения)
date: 2026-08-04
tags: спортпит, добавки
external_url: https://dzen.ru/...   (необязательно — где ещё опубликовано)
---
Текст статьи в Markdown.
"""
import os, re, glob, html as htmlmod
import markdown as md

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'articles', 'src')
OUTDIR = os.path.join(ROOT, 'articles')
SITE = 'https://shelestfit.com'
AUTHOR = 'Андрей Шелест'

TEMPLATE_FILE = os.path.join(ROOT, 'sport-nutrition.html')
tpl = open(TEMPLATE_FILE, encoding='utf-8').read()

HEAD = re.search(r'^(.*?)</head>', tpl, re.S).group(1)
HEADER = re.search(r'(<header class="hdr".*?</header>)', tpl, re.S).group(1)
BOTTOM = re.search(r'(<footer class="ftr".*?</html>)', tpl, re.S).group(1)

# --- голова: общие asset-ссылки (шрифты, css) без страничных мета ---
HEAD_ASSETS = re.search(r'(<link rel="preconnect".*?<link rel="stylesheet" href="css/core\.css">)', HEAD, re.S).group(1)

def add_prefix(text):
    """Добавляет ../ к относительным ссылкам (для страниц в /articles/)."""
    return re.sub(r'(href|src)="(?!https?://|#|\.\./|/|mailto:|tel:|data:)([^"]+)"',
                  r'\1="../\2"', text)

HEADER_SUB = add_prefix(HEADER)
BOTTOM_SUB = add_prefix(BOTTOM)
HEAD_ASSETS_SUB = add_prefix(HEAD_ASSETS)

def parse_front_matter(raw):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', raw, re.S)
    if not m:
        return {}, raw
    meta_block, body = m.group(1), m.group(2)
    meta = {}
    for line in meta_block.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, body

def esc(s):
    return htmlmod.escape(s or '', quote=True)

def ru_date(iso):
    months = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
    try:
        y, m, d = iso.split('-')
        return f'{int(d)} {months[int(m)-1]} {y}'
    except Exception:
        return iso

articles = []
for path in sorted(glob.glob(os.path.join(SRC, '*.md'))):
    raw = open(path, encoding='utf-8').read()
    meta, body = parse_front_matter(raw)
    slug = os.path.splitext(os.path.basename(path))[0]
    title = meta.get('title', slug)
    desc = meta.get('description', '')
    date = meta.get('date', '')
    tags = [t.strip() for t in meta.get('tags', '').split(',') if t.strip()]
    external = meta.get('external_url', '').strip()
    body_html = md.markdown(body, extensions=['extra'])
    articles.append(dict(slug=slug, title=title, desc=desc, date=date,
                         tags=tags, external=external, body=body_html))

# новые статьи — сверху
articles.sort(key=lambda a: a['date'], reverse=True)

# ---------- страница одной статьи ----------
def render_article(a):
    url = f'{SITE}/articles/{a["slug"]}.html'
    cover_rel = f'img/covers/{a["slug"]}.jpg'
    has_cover = os.path.exists(os.path.join(ROOT, cover_rel))
    cover = f'{SITE}/{cover_rel}' if has_cover else f'{SITE}/img/og-cover.jpg'
    cover_block = (f'<img src="../{cover_rel}" width="1200" height="630" loading="eager" '
                   f'alt="{esc(a["title"])}" '
                   f'style="width:100%; height:auto; border-radius:var(--radius-sm); '
                   f'margin-top:26px; border:1px solid var(--line);">') if has_cover else ''
    ext_block = ''
    if a['external']:
        ext_block = (f'<p style="margin-top:28px; padding:16px 20px; border:1px solid var(--line); '
                     f'border-radius:var(--radius-sm); font-size:.9rem; color:var(--ink-dim);">'
                     f'Эта статья также опубликована во внешнем издании: '
                     f'<a href="{esc(a["external"])}" target="_blank" rel="noopener" '
                     f'style="color:var(--gold-2);">читать там →</a></p>')
    tags_block = ''
    if a['tags']:
        chips = ' '.join(f'<span style="font-size:.74rem; color:var(--ink-mute); border:1px solid var(--line); '
                         f'border-radius:100px; padding:3px 12px;">{esc(t)}</span>' for t in a['tags'])
        tags_block = f'<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:16px;">{chips}</div>'

    faq_ld = build_faq(a['body'])

    jsonld = (
        '{"@context":"https://schema.org","@type":"Article",'
        f'"headline":{md_json(a["title"])},'
        f'"description":{md_json(a["desc"])},'
        f'"datePublished":"{a["date"]}",'
        '"author":{"@type":"Person","name":"Андрей Шелест","url":"https://shelestfit.com/"},'
        '"publisher":{"@type":"Person","name":"Андрей Шелест"},'
        f'"image":"{cover}",'
        f'"mainEntityOfPage":"{url}"'
        '}'
    )

    head = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(a["title"])} — {AUTHOR}</title>
<meta name="description" content="{esc(a["desc"])}">
{HEAD_ASSETS_SUB}
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(a["title"])}">
<meta property="og:description" content="{esc(a["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="ru_RU">
<meta property="og:image" content="{cover}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{cover}">
<script type="application/ld+json">{jsonld}</script>
{faq_ld}
</head>
<body>
{HEADER_SUB}

<article>
<section style="padding-top:150px; padding-bottom:24px;">
  <div class="container" style="max-width:760px;">
    <a href="../articles.html" style="font-size:.84rem; color:var(--ink-mute);">← Все статьи</a>
    <h1 class="h-sec" style="font-size:clamp(1.9rem,4vw,3rem); margin-top:18px;">{esc(a["title"])}</h1>
    <p style="color:var(--ink-mute); font-size:.86rem; margin-top:10px;">{ru_date(a["date"])} · {AUTHOR}</p>
    {tags_block}
    {cover_block}
  </div>
</section>
<section style="padding-top:0;">
  <div class="container art-body" style="max-width:760px;">
    {a["body"]}
    {ext_block}
    <div style="margin-top:40px; padding-top:28px; border-top:1px solid var(--line);">
      <a class="btn btn--gold" href="../index.html#contact">Записаться на разбор</a>
    </div>
  </div>
</section>
</article>

{BOTTOM_SUB}'''
    return head

def md_json(s):
    import json
    return json.dumps(s or '', ensure_ascii=False)

QUESTION_RE = re.compile(
    r'^(правда ли|можно ли|нужна ли|нужно ли|сколько|как |что |чем |почему|зачем|кому|когда|'
    r'опасн|вреди|станет ли|будет ли|стоит ли|а что|какой|какая|какие|где )', re.I)

def build_faq(body_html):
    """Собирает FAQPage из H2-вопросов и первого абзаца под каждым."""
    pairs = re.findall(r'<h2[^>]*>(.*?)</h2>\s*<p>(.*?)</p>', body_html, re.S)
    qa = []
    for q, ans in pairs:
        q = re.sub(r'<[^>]+>', '', q).strip()
        ans = re.sub(r'<[^>]+>', '', ans).strip()
        if not q or not ans or not QUESTION_RE.match(q):
            continue
        if len(ans) < 40:
            continue
        qa.append((q, ans[:600]))
    if not qa:
        return ''
    items = ','.join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (md_json(q), md_json(a)) for q, a in qa)
    return '<script type="application/ld+json">{"@context":"https://schema.org",' \
           '"@type":"FAQPage","mainEntity":[' + items + ']}</script>'

os.makedirs(OUTDIR, exist_ok=True)
for a in articles:
    out = os.path.join(OUTDIR, a['slug'] + '.html')
    open(out, 'w', encoding='utf-8').write(render_article(a))

# ---------- витрина articles.html ----------
def render_index():
    cards = []
    for a in articles:
        tag = a['tags'][0] if a['tags'] else ''
        cards.append(f'''      <a class="art-card" href="articles/{a['slug']}.html" data-tags="{esc(' '.join(a['tags']))}">
        <div class="art-card__date">{ru_date(a['date'])}</div>
        <h3 class="art-card__title">{esc(a['title'])}</h3>
        <p class="art-card__desc">{esc(a['desc'])}</p>
        <span class="art-card__more">Читать →</span>
      </a>''')
    all_tags = sorted({t for a in articles for t in a['tags']})
    chips = ['<button class="art-chip is-active" data-tag="all">Все</button>']
    for t in all_tags:
        chips.append(f'<button class="art-chip" data-tag="{esc(t)}">{esc(t)}</button>')

    page = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Статьи — {AUTHOR}</title>
<meta name="description" content="Статьи Андрея Шелеста о тренировках, питании, добавках и восстановлении — по доказательной базе.">
{HEAD_ASSETS}
<link rel="canonical" href="{SITE}/articles.html">
<meta property="og:type" content="website">
<meta property="og:title" content="Статьи — {AUTHOR}">
<meta property="og:description" content="Статьи о тренировках, питании, добавках и восстановлении — по доказательной базе.">
<meta property="og:url" content="{SITE}/articles.html">
<meta property="og:locale" content="ru_RU">
</head>
<body>
{HEADER}

<section style="padding-top:150px;">
  <div class="container">
    <p class="eyebrow">Блог</p>
    <h1 class="h-sec" style="font-size:clamp(2.1rem,4.4vw,3.4rem);">Статьи</h1>
    <p class="lead">Разборы по тренировкам, питанию, добавкам и восстановлению — коротко и по доказательной базе.</p>
    <div class="art-filter">{''.join(chips)}</div>
    <div class="art-grid" id="artGrid">
{chr(10).join(cards)}
    </div>
  </div>
</section>

<script>
(function(){{
  var chips = document.querySelectorAll('.art-chip');
  var cards = document.querySelectorAll('.art-card');
  chips.forEach(function(chip){{
    chip.addEventListener('click', function(){{
      chips.forEach(function(c){{ c.classList.remove('is-active'); }});
      chip.classList.add('is-active');
      var tag = chip.getAttribute('data-tag');
      cards.forEach(function(card){{
        var tags = (card.getAttribute('data-tags') || '').split(' ');
        card.style.display = (tag === 'all' || tags.indexOf(tag) !== -1) ? '' : 'none';
      }});
    }});
  }});
}})();
</script>

{BOTTOM}'''
    # витрина на корне — без ../ префиксов, но HEADER/BOTTOM берём корневые
    return page

open(os.path.join(ROOT, 'articles.html'), 'w', encoding='utf-8').write(render_index())

# ---------- sitemap ----------
sm_path = os.path.join(ROOT, 'sitemap.xml')
urls = [f'{SITE}/', f'{SITE}/articles.html',
        f'{SITE}/sport-nutrition.html', f'{SITE}/dietology.html', f'{SITE}/microbiome.html']
urls += [f'{SITE}/articles/{a["slug"]}.html' for a in articles]
entries = []
for u in urls:
    pr = '1.0' if u.endswith('/') else ('0.7' if '/articles/' in u else '0.8')
    cf = 'weekly'
    entries.append(f'  <url>\n    <loc>{u}</loc>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>')
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(entries) + '\n</urlset>\n'
open(sm_path, 'w', encoding='utf-8').write(sitemap)

print(f'Собрано статей: {len(articles)}')
for a in articles:
    print('  •', a['slug'], '—', a['title'])
print('Сгенерировано: articles.html + articles/*.html + обновлён sitemap.xml')
