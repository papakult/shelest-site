#!/usr/bin/env python3
"""Строит секцию 'Мои спортсмены' — горизонтальная лента карточек с фильтром
по дисциплине. Без имён/историй — только категория (нет данных для точной
атрибуции, чтобы не повторить прошлую ошибку с выдумыванием деталей)."""
import json, re

team = json.load(open('/root/shelest/team.json', encoding='utf-8'))
html = open('/root/shelest/index.html', encoding='utf-8').read()

CATS = {'bb': 'Бодибилдинг', 'pl': 'Пауэрлифтинг', 'gym': 'Зал', 'life': 'Спортивная жизнь'}
CATS_EN = {'bb': 'Bodybuilding', 'pl': 'Powerlifting', 'gym': 'Gym', 'life': 'Sporting life'}

cards = []
for it in team:
    wide = ' rail__c--w' if it.get('w') else ''
    cards.append(f'''      <div class="rail__c{wide}" data-cat="{it['cat']}">
        <img src="img/{it['img']}-440.jpg" srcset="img/{it['img']}-300.jpg 300w, img/{it['img']}-440.jpg 440w, img/{it['img']}-640.jpg 640w" sizes="260px" alt="{it['t']}" loading="lazy">
        <div class="rail__cap"><b>{it['t']}</b><span>{it['d']}</span></div>
      </div>''')

chips = ''.join(f'<button class="rail__chip" data-cat="{k}">{v}</button>' for k, v in CATS.items() if any(t['cat'] == k for t in team))

section = f'''
<!-- ================= МОИ СПОРТСМЕНЫ ================= -->
<section id="team">
  <div class="container">
    <p class="eyebrow" data-i18n="tm.eyebrow">Спортивная жизнь</p>
    <h2 class="h-sec" data-i18n="tm.title">Мои спортсмены</h2>
    <p class="lead" data-i18n="tm.lead">Соревнования, залы, подготовка — часть той же школы, по которой веду онлайн-клиентов.</p>
    <div class="rail__f" style="display:flex; gap:10px; margin:24px 0 4px; flex-wrap:wrap;">
      <button class="rail__chip is-active" data-cat="all" data-i18n="tm.all">Все</button>
      {chips}
    </div>
  </div>
  <div class="rail" style="display:flex; gap:16px; overflow-x:auto; padding:20px 24px 8px; scroll-snap-type:x proximity;">
{chr(10).join(cards)}
  </div>
</section>
'''

CSS = '''
/* ═══ team rail начало ═══ */
.rail__c{ flex:0 0 220px; scroll-snap-align:start; border-radius:var(--radius-sm); overflow:hidden; position:relative; background:var(--bg-2); border:1px solid var(--line); }
.rail__c--w{ flex-basis:340px; }
.rail__c img{ width:100%; aspect-ratio:3/4; object-fit:cover; display:block; }
.rail__c--w img{ aspect-ratio:16/10; }
.rail__cap{ position:absolute; left:0; right:0; bottom:0; padding:14px; background:linear-gradient(to top, rgba(0,0,0,.85), transparent); display:flex; flex-direction:column; gap:2px; }
.rail__cap b{ font-size:.88rem; }
.rail__cap span{ font-size:.74rem; color:var(--ink-mute); }
.rail__chip{ padding:8px 16px; border-radius:100px; border:1px solid var(--line-2); font-size:.82rem; color:var(--ink-dim); }
.rail__chip.is-active{ background:var(--gold); color:#100c02; border-color:var(--gold); }
.rail{ scrollbar-width:thin; }
/* ═══ team rail конец ═══ */
'''

JS = '''
/* ═══ team filter начало ═══ */
document.querySelectorAll('.rail__chip').forEach(chip=>{
  chip.addEventListener('click', ()=>{
    document.querySelectorAll('.rail__chip').forEach(c=>c.classList.remove('is-active'));
    chip.classList.add('is-active');
    const cat = chip.getAttribute('data-cat');
    document.querySelectorAll('.rail__c').forEach(card=>{
      card.style.display = (cat === 'all' || card.getAttribute('data-cat') === cat) ? '' : 'none';
    });
  });
});
/* ═══ team filter конец ═══ */
'''

if 'id="team"' in html:
    html = re.sub(r'\n<!-- ================= МОИ СПОРТСМЕНЫ.*?\n</section>\n', section, html, flags=re.S)
else:
    html = html.replace('<!-- ================= РАЗОВЫЕ УСЛУГИ', section.strip('\n') + '\n\n<!-- ================= РАЗОВЫЕ УСЛУГИ')

if '/* ═══ team rail начало ═══ */' not in html:
    html = html.replace('</style>', CSS + '</style>') if '</style>' in html else html

if '/* ═══ team filter начало ═══ */' not in html:
    html = html.replace('let LANG = ', JS + 'let LANG = ')

open('/root/shelest/index.html', 'w', encoding='utf-8').write(html)

# CSS идёт в core.css, не инлайн (у нас нет <style> в index.html)
core = open('/root/shelest/css/core.css', encoding='utf-8').read()
if '/* ═══ team rail начало ═══ */' not in core:
    core += CSS
    open('/root/shelest/css/core.css', 'w', encoding='utf-8').write(core)

print('готово. карточек спортсменов:', len(team))
