#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Расширяет sport-nutrition.html: система рейтинга AIS ABCD (реальная
классификация Австралийского института спорта), таймлайн, разбор по группам,
мифы, источники — вместо прежних 4 карточек."""
import re, json

HEAD_FOOT = open('/root/shelest/index.html', encoding='utf-8').read()
HEADER = re.search(r'(<header class="hdr".*?</header>)', HEAD_FOOT, re.S).group(1)
FOOTER = re.search(r'(<footer class="ftr".*?</footer>)', HEAD_FOOT, re.S).group(1)
SCRIPTS = re.search(r'(<script>\s*document\.getElementById\(\'yr\'\).*?</script>\s*<script>\s*/\* ================= i18n.*?)Object\.assign\(I18N\.en, \{(.*?)\}\);(.*?</script>)', HEAD_FOOT, re.S)
SCRIPT_HEAD, _, SCRIPT_TAIL = SCRIPTS.group(1), SCRIPTS.group(2), SCRIPTS.group(3)

def fix_header_links(header):
    header = header.replace('href="#"', 'href="index.html"')
    header = re.sub(r'href="#(about|pricing|services|reviews|contact)"', r'href="index.html#\1"', header)
    return header
HEADER_SUB = fix_header_links(HEADER)

EN = {}
def t(key, ru, en):
    EN[key] = en
    return f'<span data-i18n="{key}">{ru}</span>'
def attr(key, ru, en):
    EN[key] = en
    return ru

GROUPS = [
    ("A", "Группа A — доказательства работают на вас", "Group A — evidence supports use",
     "Достаточно качественных исследований, показывающих реальный эффект при правильной дозировке.",
     "Solid research showing a real effect at the correct dosage.",
     [
        ("Креатин моногидрат", "Creatine monohydrate", "3-5 г/день, постоянно", "3-5 g/day, ongoing",
         "Самая изученная добавка в спортивном питании — рост силовых показателей и объёма тренировочной работы, подтверждено GRADE-обзорами.",
         "The most studied sports supplement — increases strength and training volume, confirmed by GRADE-assessed reviews."),
        ("Кофеин", "Caffeine", "3-6 мг/кг за 30-60 мин до нагрузки", "3-6 mg/kg 30-60 min pre-exercise",
         "Метаанализ метаанализов подтверждает эффект на силу и выносливость. Индивидуальная переносимость сильно различается.",
         "A meta-analysis of meta-analyses confirms effects on strength and endurance. Individual tolerance varies widely."),
        ("Протеин (сывороточный/казеин/растительный)", "Protein (whey/casein/plant)", "по недостающему количеству белка в рационе", "to cover the protein gap in your diet",
         "Не «строит мышцы» сам по себе — закрывает суточную норму белка, когда это неудобно сделать едой.",
         "Doesn't \"build muscle\" on its own — fills your daily protein target when food alone is inconvenient."),
        ("Бета-аланин", "Beta-alanine", "3-6 г/день, курсом от 4 недель", "3-6 g/day, over a 4+ week course",
         "Повышает внутримышечный карнозин, буферизует закисление при работе 1-4 минуты — спринт, интервалы, кроссфит.",
         "Raises intramuscular carnosine, buffering acidosis during 1-4 minute efforts — sprints, intervals, CrossFit-style work."),
        ("Гидрокарбонат натрия (сода)", "Sodium bicarbonate", "0,2-0,3 г/кг за 60-90 мин до нагрузки", "0.2-0.3 g/kg 60-90 min pre-exercise",
         "Буферизует закисление при коротких интенсивных усилиях. Частый побочный эффект — расстройство ЖКТ, нужна индивидуальная отработка протокола.",
         "Buffers acidosis during short, intense efforts. GI upset is a common side effect — the protocol needs individual testing."),
        ("Нитраты (свекольный сок)", "Nitrates (beetroot juice)", "~6-8 ммоль нитрата за 2-3 часа до старта", "~6-8 mmol nitrate 2-3 hours pre-event",
         "Улучшает эффективность работы мышц на выносливость через путь оксида азота — эффект заметнее у менее тренированных атлетов.",
         "Improves muscular efficiency in endurance work via the nitric oxide pathway — the effect is more noticeable in less-trained athletes."),
        ("Витамин D", "Vitamin D", "по результатам анализов", "based on bloodwork",
         "Работает как добавка, только если есть реальный дефицит — актуально для Сибири в осенне-зимний период. Без дефицита эффекта на результат нет.",
         "Only works as a supplement if there's an actual deficiency — relevant for Siberia in autumn-winter. With no deficiency, there's no effect on performance."),
     ]),
    ("B", "Группа B — многообещающе, но рано ставить точку", "Group B — promising, but not settled",
     "Есть исследования в пользу эффекта, но их пока меньше или они менее однозначны, чем в группе A.",
     "Studies point toward an effect, but there are fewer of them, or they're less conclusive, than group A.",
     [
        ("HMB", "HMB", "3 г/день", "3 g/day",
         "Возможна защита мышечной массы при дефиците калорий, но данные смешанные и часто спонсированы производителями.",
         "May help preserve muscle mass in a calorie deficit, but evidence is mixed and often industry-funded."),
        ("Омега-3", "Omega-3", "1-2 г EPA+DHA/день", "1-2 g EPA+DHA/day",
         "Противовоспалительный эффект и поддержка восстановления правдоподобны, прямое влияние на силовые результаты доказано слабее.",
         "The anti-inflammatory, recovery-support effect is plausible; a direct effect on strength outcomes is less well proven."),
        ("Терпкая вишня (тart cherry)", "Tart cherry juice", "по протоколу конкретного исследования", "per the specific study's protocol",
         "Небольшие исследования показывают снижение болезненности мышц после нагрузки — выборки пока маленькие.",
         "Small studies show reduced muscle soreness after exertion — sample sizes remain small."),
        ("Коллаген + витамин C", "Collagen + vitamin C", "15 г коллагена + витамин C за 30-60 мин до нагрузки", "15 g collagen + vitamin C 30-60 min pre-exercise",
         "Теоретически поддерживает синтез коллагена в сухожилиях/связках при приёме перед нагрузкой — направление активно изучается.",
         "Theoretically supports tendon/ligament collagen synthesis when taken before loading exercise — an actively researched area."),
     ]),
    ("C", "Группа C — недостаточно доказательств для общего применения", "Group C — insufficient evidence for general use",
     "Либо исследований мало, либо они не показывают значимого эффекта сверх плацебо для большинства людей.",
     "Either there's too little research, or it shows no meaningful effect beyond placebo for most people.",
     [
        ("BCAA отдельно от белка", "BCAAs on top of protein", "—", "—",
         "При достаточном общем белке в рационе отдельный приём BCAA не даёт измеримого преимущества по синтезу мышечного белка.",
         "With adequate total dietary protein, separate BCAA intake shows no measurable advantage for muscle protein synthesis."),
        ("Жиросжигатели / термогеники", "Fat burners / thermogenics", "—", "—",
         "Эффект в основном держится на стимуляторах и плацебо, а не на доказанном влиянии на жировой обмен.",
         "The effect largely rests on stimulants and placebo, not a proven impact on fat metabolism."),
        ("Травяные «бустеры тестостерона»", "Herbal \"testosterone boosters\"", "—", "—",
         "Устойчивой доказательной базы влияния на реальный уровень тестостерона у здоровых мужчин нет.",
         "There's no solid evidence base for an effect on actual testosterone levels in healthy men."),
     ]),
    ("D", "Группа D — под запретом или высокий риск", "Group D — banned or high risk",
     "Запрещённые вещества или добавки с высоким риском загрязнения запрещёнными субстанциями.",
     "Banned substances, or supplements with a high risk of contamination with banned substances.",
     [
        ("Стимуляторы типа DMAA", "DMAA-type stimulants", "—", "—",
         "Запрещённое вещество в большинстве антидопинговых кодексов — встречается в нерегулируемых «жиросжигателях» и предтренах.",
         "A banned substance under most anti-doping codes — turns up in unregulated \"fat burners\" and pre-workouts."),
        ("Предтрены без сертификации на чистоту", "Uncertified pre-workout blends", "—", "—",
         "«Проприетарные формулы» без независимого тестирования — реальный риск примесей запрещённых веществ, особенно важно для соревнующихся атлетов.",
         "\"Proprietary blends\" without independent testing — a real risk of banned-substance contamination, especially relevant for competing athletes."),
     ]),
]

MYTHS_SN = [
    ("«Без спортпита результата не будет»", "\"No results without supplements\"", "Миф. База — тренировки и питание. Добавки в лучшем случае докручивают 5-10% сверху.", "Myth. Training and diet are the foundation. Supplements add, at best, another 5-10% on top."),
    ("«Чем больше доза — тем быстрее эффект»", "\"More dose means faster results\"", "Миф. У большинства добавок есть потолок эффективности — превышение просто лишняя нагрузка на организм.", "Myth. Most supplements have an effectiveness ceiling — exceeding it just adds strain on the body."),
    ("«Протеин — это химия»", "\"Protein powder is a chemical\"", "Миф. Концентрированный молочный или растительный белок — тот же нутриент, что и в еде.", "Myth. It's concentrated milk or plant protein — the same nutrient as in food."),
    ("«Спортпит нужен всем, кто тренируется»", "\"Everyone who trains needs supplements\"", "Миф. При достаточном и разнообразном питании многое закрывается едой.", "Myth. With enough varied food, much of it is covered by diet alone."),
    ("«Группа A — это гарантия результата лично для вас»", "\"Group A guarantees results for you personally\"", "Не совсем. Групповые данные — это средний эффект по выборке, индивидуальный ответ варьирует.", "Not quite. Group-level data is an average effect across a sample — individual response varies."),
]

SOURCES_SN = [
    ("Australian Institute of Sport. AIS Sports Supplement Framework — ABCD Classification System.", "https://www.ausport.gov.au/ais/nutrition/supplements/about-the-ais-sports-supplement-framework"),
    ("Creatine supplementation protocols with or without training interventions on body composition: a GRADE-assessed systematic review. J Int Soc Sports Nutr, 2024.", "https://www.tandfonline.com/doi/full/10.1080/15502783.2024.2380058"),
    ("The effect of caffeine supplementation on muscular strength and endurance: a meta-analysis of meta-analyses. 2024.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC11336343/"),
    ("Effects of Caffeine Intake on Endurance Running Performance and Time to Exhaustion: A Systematic Review and Meta-Analysis.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC9824573/"),
    ("Dosing strategies for β-alanine supplementation in strength and power performance: a systematic review.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC12466178/"),
    ("The Muscle Carnosine Response to Beta-Alanine Supplementation: A Systematic Review with Bayesian Meta-Analysis.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7456894/"),
    ("The effects of branched-chain amino acids on muscle protein synthesis and breakdown: an update. Nutr Res Rev, 2023.", "https://pubmed.ncbi.nlm.nih.gov/37681443/"),
    ("Does BCAA Supplementation Attenuate Muscle Damage Markers and Soreness after Resistance Exercise? Meta-Analysis of RCTs.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8230327/"),
]

def render_group(letter, title, en_title, desc, en_desc, items):
    k = f"sn.g{letter}"
    cards = ""
    for i, (name, en_name, dose, en_dose, d, en_d) in enumerate(items, 1):
        ik = f"{k}.i{i}"
        cards += f'''
      <div class="svc__c">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
          <h4>{t(ik+'.n', name, en_name)}</h4>
          <span style="flex:0 0 auto; font-size:.7rem; padding:3px 9px; border-radius:100px; background:var(--gold); color:#100c02; font-weight:700;">{letter}</span>
        </div>
        {f'<p style="font-size:.76rem; color:var(--ink-mute); margin:4px 0;">{t(ik+".dose", dose, en_dose)}</p>' if dose != '—' else ''}
        <p>{t(ik+'.d', d, en_d)}</p>
      </div>'''
    return f'''
<section id="sn-group-{letter.lower()}">
  <div class="container">
    <p class="eyebrow">{t(k+'.eyebrow', title, en_title)}</p>
    <p class="lead" style="margin-bottom:24px;">{t(k+'.lead', desc, en_desc)}</p>
    <div class="svc">{cards}
    </div>
  </div>
</section>'''

groups_html = "".join(render_group(*g) for g in GROUPS)

myths_html = ""
for i, (m, en_m, a, en_a) in enumerate(MYTHS_SN, 1):
    k = f"sn.my{i}"
    myths_html += f'''
      <div class="svc__c">
        <h4>{t(k+'.m', m, en_m)}</h4>
        <p>{t(k+'.a', a, en_a)}</p>
      </div>'''

sources_html = "".join(f'<li style="margin-bottom:8px; font-size:.82rem;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-mute);">{i}. {c}</a></li>' for i,(c,u) in enumerate(SOURCES_SN,1))

EXTRA = f'''
<section id="sn-framework">
  <div class="container">
    <p class="eyebrow" data-i18n="sn.fw.eyebrow">{attr('sn.fw.eyebrow','Система классификации','Classification system')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="sn.fw.title">{attr('sn.fw.title','AIS ABCD — та же система, что использует Австралийский институт спорта','AIS ABCD — the same framework used by the Australian Institute of Sport')}</h2>
    <p class="lead" data-i18n="sn.fw.lead">{attr('sn.fw.lead','Международный стандарт классификации спортивных добавок по уровню доказательности — от «работает» до «под запретом».','An international standard for classifying sports supplements by evidence level — from working to banned.')}</p>
  </div>
</section>
{groups_html}
<section id="sn-myths2">
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="sn.my.title">{attr('sn.my.title','Мифы','Myths')}</h2>
    <div class="svc" style="margin-top:28px;">{myths_html}
    </div>
  </div>
</section>
<section id="sn-sources">
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.4rem,2.4vw,1.9rem);" data-i18n="sn.src.title">{attr('sn.src.title', f'{len(SOURCES_SN)} источников', f'{len(SOURCES_SN)} sources')}</h2>
    <ol style="margin-top:20px; padding-left:20px;">{sources_html}
    </ol>
  </div>
</section>
'''

html = open('/root/shelest/sport-nutrition.html', encoding='utf-8').read()

# вставляем перед финальным CTA-блоком (kase__body)
if 'id="sn-framework"' not in html:
    html = html.replace('<section>\n  <div class="container">\n    <div class="kase__body"', EXTRA.strip('\n') + '\n\n<section>\n  <div class="container">\n    <div class="kase__body"')

# добавляем EN-ключи в существующий Object.assign(I18N.en, {...})
m = re.search(r'(Object\.assign\(I18N\.en, \{)(.*?)(\}\);)', html, re.S)
if m and "'sn.g" not in html.split("Object.assign(I18N.en")[1][:2000]:
    extra_en = ',\n  ' + ',\n  '.join(f"'{k}': {json.dumps(v, ensure_ascii=False)}" for k, v in EN.items())
    html = html[:m.end(2)] + extra_en + html[m.end(2):]

open('/root/shelest/sport-nutrition.html', 'w', encoding='utf-8').write(html)
print('готово: группы AIS ABCD добавлены, добавок:', sum(len(g[5]) for g in GROUPS), '| мифов:', len(MYTHS_SN), '| источников:', len(SOURCES_SN))
