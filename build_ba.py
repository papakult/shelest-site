#!/usr/bin/env python3
"""Вставляет реальное фото Олега в блок 'Главный случай' и строит секцию
'До и после' с остальными диптихами из ba.json."""
import json, re

ba = json.load(open('/root/shelest/ba.json', encoding='utf-8'))
html = open('/root/shelest/index.html', encoding='utf-8').read()

# 1) кейс Олега — заменяем плейсхолдер на реальное фото
html = re.sub(
    r'<div class="ba vgn" style="background:var\(--bg-3\);.*?</div>\s*(?=<div class="kase__body">)',
    '<div class="ba vgn"><img src="img/case-oleg-700.jpg" srcset="img/case-oleg-480.jpg 480w, img/case-oleg-700.jpg 700w, img/case-oleg-1100.jpg 1100w" sizes="(max-width:860px) 100vw, 42vw" alt="Олег — до и после" loading="lazy"></div>\n      ',
    html, flags=re.S
)

# 2) секция "До и после"
more = ba.get('more', 9)
cards = []
en_pairs = []
for i, it in enumerate(ba['items'], 1):
    extra = ' data-extra' if i > more else ''
    cards.append(f'''      <div class="svc__c bac" style="padding:0; overflow:hidden;"{extra}>
        <img src="img/{it['img']}-500.jpg" srcset="img/{it['img']}-360.jpg 360w, img/{it['img']}-500.jpg 500w, img/{it['img']}-700.jpg 700w" sizes="(max-width:860px) 50vw, 30vw" alt="{it['t']}" loading="lazy" style="width:100%; aspect-ratio:3/4; object-fit:cover;">
        <div style="padding:18px;">
          <h4 data-i18n="bp.{i}.t" style="font-size:.98rem;">{it['t']}</h4>
          <p data-i18n="bp.{i}.d" style="font-size:.82rem; color:var(--ink-mute); margin-top:4px;">{it['d']}</p>
        </div>
      </div>''')
    en_pairs.append(f"  'bp.{i}.t': {json.dumps(it['en_t'], ensure_ascii=False)}, 'bp.{i}.d': {json.dumps(it['en_d'], ensure_ascii=False)},")

more_btn = ''
if len(ba['items']) > more:
    more_btn = f'''
    <div style="text-align:center; margin-top:28px;">
      <button class="btn btn--ghost" id="baMore" type="button" data-i18n="bp.more">Показать ещё ({len(ba['items']) - more})</button>
    </div>'''

section = f'''
<!-- ================= ДО И ПОСЛЕ ================= -->
<section id="before-after">
  <div class="container">
    <p class="eyebrow" data-i18n="bp.eyebrow">Реальные трансформации</p>
    <h2 class="h-sec" data-i18n="bp.title">До и после</h2>
    <p class="lead" data-i18n="bp.lead">Настоящие клиенты, их фотографии и результаты — со всеми письменными согласиями.</p>
    <div class="svc bag" style="margin-top:28px;">
{chr(10).join(cards)}
    </div>{more_btn}
  </div>
</section>
'''

if 'id="before-after"' in html:
    html = re.sub(r'\n<!-- ================= ДО И ПОСЛЕ.*?</section>\n', section, html, flags=re.S)
else:
    html = html.replace('<!-- ================= РАЗОВЫЕ УСЛУГИ', section.strip('\n') + '\n\n<!-- ================= РАЗОВЫЕ УСЛУГИ')

MORE_CSS = '''
/* ═══ ba show-more начало ═══ */
.bag .bac[data-extra]{ display:none; }
.bag.is-open .bac[data-extra]{ display:block; }
/* ═══ ba show-more конец ═══ */
'''
MORE_JS = '''
/* ═══ ba show-more начало ═══ */
const baMoreBtn = document.getElementById('baMore');
if (baMoreBtn) {
  baMoreBtn.addEventListener('click', () => {
    document.querySelector('.bag').classList.add('is-open');
    baMoreBtn.style.display = 'none';
  });
}
/* ═══ ba show-more конец ═══ */
'''
if '/* ═══ ba show-more начало ═══ */' not in html:
    html = html.replace('let LANG = ', MORE_JS + 'let LANG = ')

open('/root/shelest/index.html', 'w', encoding='utf-8').write(html)

core = open('/root/shelest/css/core.css', encoding='utf-8').read()
if '/* ═══ ba show-more начало ═══ */' not in core:
    core += MORE_CSS
    open('/root/shelest/css/core.css', 'w', encoding='utf-8').write(core)

print('готово. карточек до/после:', len(ba['items']), '(показано сразу:', more, ')')
print("EN-ключи (добавить в Object.assign(I18N.en, {...})):")
print("  'bp.eyebrow': 'Real transformations', 'bp.title': 'Before & after', 'bp.lead': 'Real clients, their photos and results — with written consent on file.', 'bp.more': 'Show more (%d)'," % (len(ba['items']) - more))
print('\n'.join(en_pairs))
