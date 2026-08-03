#!/usr/bin/env python3
"""Заполняет #revGrid карточками из reviews.json. Пропускает записи со статусом PENDING_RESEND."""
import json, re

with open('/root/shelest/reviews.json', encoding='utf-8') as f:
    reviews = json.load(f)

cards = []
en_pairs = []
i = 0
for r in reviews:
    if r['t'].startswith('PENDING_RESEND'):
        continue
    i += 1
    res_html = f'<span class="rev__res">{r["res"]}</span>' if r.get('res') else ''
    cards.append(f'''      <div class="rev__c">
        <div class="rev__q">"</div>
        <p class="rev__t" data-i18n="rv.{i}.t">{r['t']}</p>
        <div class="rev__foot">
          <div class="rev__av rev__av--ph">{r['av']}</div>
          <div>
            <div class="rev__n" data-i18n="rv.{i}.n">{r['n'] or '&nbsp;'}</div>
            <div class="rev__r" data-i18n="rv.{i}.r">{r['r']}</div>
          </div>
          {res_html}
        </div>
      </div>''')
    en_pairs.append(f"  'rv.{i}.t': {json.dumps(r['en_t'], ensure_ascii=False)},")
    if r['en_n']:
        en_pairs.append(f"  'rv.{i}.n': {json.dumps(r['en_n'], ensure_ascii=False)},")
    en_pairs.append(f"  'rv.{i}.r': {json.dumps(r['en_r'], ensure_ascii=False)},")

block = '\n'.join(cards)

html = open('/root/shelest/index.html', encoding='utf-8').read()
html = re.sub(
    r'(<div class="rev__grid" id="revGrid">).*?(</div>\s*</div>\s*</section>)',
    lambda m: m.group(1) + '\n' + block + '\n    ' + m.group(2),
    html, flags=re.S
)
open('/root/shelest/index.html', 'w', encoding='utf-8').write(html)

print(f'Вставлено отзывов: {i} (пропущено ожидающих пересылки: {len(reviews)-i})')
print('EN-ключи для i18n:')
print('\n'.join(en_pairs))
