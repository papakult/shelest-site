#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Апгрейд №1 по мотивам премиальных фитнес-сайтов ОАЭ (The Warehouse Gym,
GymNation): выпадающее меню «Энциклопедии» в шапке на всех страницах +
статус-бар с честными цифрами сразу под hero на главной. Ничего не копирует
дословно — только общие приёмы (dropdown-меню, contrast stat-bar)."""
import re, json

FILES = ['index.html', 'sport-nutrition.html', 'dietology.html', 'microbiome.html']

DROP_EN = {
    'nav.enc': 'Encyclopedias',
    'nav.enc.sn': 'Sport nutrition', 'nav.enc.sn.d': 'AIS ABCD supplement ratings',
    'nav.enc.di': 'Dietology', 'nav.enc.di.d': '5 evidence-based diets compared',
    'nav.enc.mb': 'Gut microbiome', 'nav.enc.mb.d': 'History, sport, testing, myths',
}

STAT_EN = {
    'stat.1.n': 'World champion', 'stat.1.l': 'Powerlifting',
    'stat.2.n': 'Medical background', 'stat.2.l': 'Degree in medicine',
    'stat.3.n': '27+', 'stat.3.l': 'Before/after transformations',
    'stat.4.n': 'Online only', 'stat.4.l': 'Coaching worldwide',
}

def make_drop(prefix):
    return f'''<div class="hdr__drop">
        <a href="{prefix}sport-nutrition.html" data-i18n="nav.enc">Энциклопедии</a>
        <div class="hdr__panel">
          <a href="{prefix}sport-nutrition.html"><b data-i18n="nav.enc.sn">Спортивное питание</b><span data-i18n="nav.enc.sn.d">Рейтинг добавок AIS ABCD</span></a>
          <a href="{prefix}dietology.html"><b data-i18n="nav.enc.di">Диетология</b><span data-i18n="nav.enc.di.d">5 доказательных диет</span></a>
          <a href="{prefix}microbiome.html"><b data-i18n="nav.enc.mb">Микробиота</b><span data-i18n="nav.enc.mb.d">История, спорт, тесты, мифы</span></a>
        </div>
      </div>
      '''

STAT_BAR = '''<section class="stat-bar">
  <div class="container stat-bar__row">
    <div class="stat-bar__item"><span class="stat-bar__n" data-i18n="stat.1.n">Чемпион мира</span><span class="stat-bar__l" data-i18n="stat.1.l">по пауэрлифтингу</span></div>
    <div class="stat-bar__item"><span class="stat-bar__n" data-i18n="stat.2.n">Медицинское образование</span><span class="stat-bar__l" data-i18n="stat.2.l">высшее, врачебное</span></div>
    <div class="stat-bar__item"><span class="stat-bar__n" data-i18n="stat.3.n">27+</span><span class="stat-bar__l" data-i18n="stat.3.l">трансформаций «до/после»</span></div>
    <div class="stat-bar__item"><span class="stat-bar__n" data-i18n="stat.4.n">Только онлайн</span><span class="stat-bar__l" data-i18n="stat.4.l">ведение из любой точки мира</span></div>
  </div>
</section>

'''

for fname in FILES:
    html = open(fname, encoding='utf-8').read()
    prefix = '' if fname == 'index.html' else 'index.html' if False else ''
    prefix = '' if fname == 'index.html' else ''
    # subpages sit alongside sport-nutrition.html etc, so relative links have no prefix either way
    if 'class="hdr__drop"' not in html:
        html = html.replace(
            '<a href="#services" data-i18n="nav.services">Услуги</a>' if fname == 'index.html' else '<a href="index.html#services" data-i18n="nav.services">Услуги</a>',
            ('<a href="#services" data-i18n="nav.services">Услуги</a>\n      ' if fname == 'index.html' else '<a href="index.html#services" data-i18n="nav.services">Услуги</a>\n      ')
            + make_drop(''),
            1
        )
    if fname == 'index.html' and 'class="stat-bar"' not in html:
        html = html.replace(
            '</section>\n\n<!-- ================= О МНЕ ================= -->',
            '</section>\n\n' + STAT_BAR + '<!-- ================= О МНЕ ================= -->',
            1
        )
    m = re.search(r'(Object\.assign\(I18N\.en, \{)(.*?)(\}\);)', html, re.S)
    if m:
        existing = html.split("Object.assign(I18N.en", 1)[1][:3000]
        need = {}
        if "'nav.enc'" not in existing:
            need.update(DROP_EN)
        if fname == 'index.html' and "'stat.1.n'" not in existing:
            need.update(STAT_EN)
        if need:
            head = html[:m.end(2)].rstrip()
            if head.endswith(','):
                head = head[:-1]
            extra_en = ',\n  ' + ',\n  '.join(f"'{k}': {json.dumps(v, ensure_ascii=False)}" for k, v in need.items()) + '\n'
            html = head + extra_en + html[m.end(2):]
    open(fname, 'w', encoding='utf-8').write(html)
    print(fname, 'patched')
