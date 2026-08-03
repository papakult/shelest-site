#!/usr/bin/env python3
"""Генерирует sport-nutrition.html, dietology.html, microbiome.html
из общего шаблона (шапка/футер как на index.html) + двуязычный контент по теме."""
import re, json

HEAD_FOOT = open('/root/shelest/index.html', encoding='utf-8').read()
HEADER = re.search(r'(<header class="hdr".*?</header>)', HEAD_FOOT, re.S).group(1)
FOOTER = re.search(r'(<footer class="ftr".*?</footer>)', HEAD_FOOT, re.S).group(1)
SCRIPTS = re.search(r'(<script>\s*document\.getElementById\(\'yr\'\).*?</script>\s*<script>\s*/\* ================= i18n.*?)Object\.assign\(I18N\.en, \{(.*?)\}\);(.*?</script>)', HEAD_FOOT, re.S)
SCRIPT_HEAD, EN_INDEX_BODY, SCRIPT_TAIL = SCRIPTS.group(1), SCRIPTS.group(2), SCRIPTS.group(3)

def fix_header_links(header):
    header = header.replace('href="#"', 'href="index.html"')
    header = re.sub(r'href="#(about|pricing|services|reviews|contact)"', r'href="index.html#\1"', header)
    return header

HEADER_SUB = fix_header_links(HEADER)

PAGES = {
    'sport-nutrition.html': dict(
        title='Спортивное питание — Андрей Шелест', en_title='Sport Nutrition — Andrey Shelest',
        desc='Как разобраться в спортивном питании: что реально работает, а что маркетинг. Подбор спортпита от тренера с медицинским образованием.',
        en_desc='How to make sense of sports supplements: what actually works and what is marketing. Supplement selection from a coach with a medical background.',
        eyebrow='Спортивное питание', en_eyebrow='Sport nutrition',
        h1='Спортпит без мифов', en_h1='Supplements without the myths',
        lead='Большая часть рынка спортивного питания — маркетинг. Разбираю, что реально влияет на результат, что просто трата денег, а что может быть небезопасно при ваших анализах и лекарствах.',
        en_lead='Most of the sports nutrition market is marketing. I break down what actually affects your results, what is just wasted money, and what could be unsafe given your bloodwork or medications.',
        sections=[
            ('Как я подбираю спортпит', 'How I put together a supplement plan', [
                ('Шаг 1. Смотрю на рацион и цель', 'Step 1. Diet and goal first', 'Спортпит имеет смысл только на фоне уже выстроенного питания — сперва разбираю, чего конкретно не хватает в рационе и под какую задачу подбираем добавки.',
                 'Supplements only make sense on top of a diet that already works — first I check what your current diet is actually missing and what goal we\'re building the plan around.'),
                ('Шаг 2. Проверяю совместимость', 'Step 2. Checking compatibility', 'Медицинское образование позволяет учитывать, что вы уже принимаете — лекарства, БАДы, хронические состояния — прежде чем что-то советовать.',
                 'A medical background means I can factor in what you already take — medication, supplements, chronic conditions — before recommending anything.'),
                ('Шаг 3. Даю конкретную схему', 'Step 3. A concrete schedule, not a list', 'Не «список того, что купить», а точная дозировка, время приёма и на сколько недель — с корректировкой по ходу, если что-то не подходит.',
                 'Not just "here\'s what to buy" — an exact dosage, timing, and duration, adjusted along the way if something doesn\'t suit you.'),
            ]),
            ('Что имеет смысл', 'What actually helps', [
                ('Белок', 'Protein', 'Сывороточный или любой другой протеин закрывает суточную норму белка, когда это неудобно сделать едой. Не «сжигает жир» и не «строит мышцы» сам по себе — работает как добавка к рациону.',
                 'Whey or any other protein powder fills your daily protein target when food alone is inconvenient. It doesn\'t "burn fat" or "build muscle" on its own — it works as a supplement to your diet.'),
                ('Креатин', 'Creatine', 'Один из немногих видов спортпита с доказанной эффективностью — рост силовых показателей и объёма тренировочной работы. Дозировка и схема приёма подбираются индивидуально.',
                 'One of the few supplements with solid evidence behind it — it increases strength and training volume. Dosage and timing are set individually.'),
                ('Витамины и минералы', 'Vitamins and minerals', 'Имеет смысл только по результатам анализов, а не «на всякий случай» — учитывая тренировочные нагрузки и объём вашей еды.',
                 'Only makes sense based on bloodwork, not "just in case" — accounting for your training load and how much you actually eat.'),
                ('Омега-3', 'Omega-3', 'Актуальна, если в рационе мало жирной рыбы — влияет на воспаление, восстановление и липидный профиль, что особенно важно при силовых нагрузках.',
                 'Relevant if your diet is low in fatty fish — affects inflammation, recovery and lipid profile, which matters a lot under heavy training loads.'),
            ]),
            ('Что чаще всего лишнее', 'What is usually unnecessary', [
                ('BCAA отдельно от белка', 'BCAAs on top of protein', 'При достаточном количестве белка в рационе аминокислоты организм получает и без отдельной добавки.',
                 'With enough protein in your diet, you already get these amino acids without a separate supplement.'),
                ('Жиросжигатели', 'Fat burners', 'Эффект в большинстве случаев держится на стимуляторах и эффекте плацебо, а не на реальном влиянии на жировой обмен.',
                 'In most cases the effect comes from stimulants and the placebo effect, not any real impact on fat metabolism.'),
                ('Предтрены с высокими дозами кофеина', 'High-caffeine pre-workouts', 'Кратковременный бодрящий эффект, который легко получить дешевле и безопаснее — и который со временем требует всё большей дозы.',
                 'A short-lived energy boost you can get more cheaply and safely elsewhere — and one that demands ever-higher doses over time.'),
            ]),
            ('Мифы о спортпите', 'Common myths', [
                ('«Протеин — это химия»', '"Protein powder is a chemical"', 'Миф. Это концентрированный молочный или растительный белок — тот же нутриент, что и в еде, просто в удобной форме.',
                 'Myth. It\'s concentrated milk or plant protein — the same nutrient you get from food, just in a convenient form.'),
                ('«Без спортпита результата не будет»', '"No results without supplements"', 'Миф. База — это тренировки и питание. Добавки в лучшем случае докручивают то, что уже работает, на 5–10%.',
                 'Myth. Training and diet are the foundation. Supplements, at best, add another 5–10% on top of what\'s already working.'),
                ('«Чем больше доза — тем быстрее эффект»', '"More is always better"', 'Миф. У большинства добавок есть потолок эффективности — превышение дозы просто лишняя нагрузка на организм без дополнительного результата.',
                 'Myth. Most supplements have a ceiling — going past it just adds strain on your body without extra benefit.'),
            ]),
            ('Частые вопросы', 'Frequently asked', [
                ('Сколько нужно белка в день?', 'How much protein do I need daily?', 'Ориентировочно 1,6–2,2 г на кг веса тела при регулярных силовых тренировках — точная цифра зависит от цели и состава тела.',
                 'Roughly 1.6–2.2 g per kg of body weight with regular strength training — the exact number depends on your goal and body composition.'),
                ('Можно ли принимать спортпит без консультации тренера?', 'Can I take supplements without a consultation?', 'Можно, но на практике большинство переплачивают за то, что им не нужно именно сейчас — здесь и есть смысл разбора.',
                 'You can, but in practice most people overpay for things they don\'t actually need right now — that\'s exactly where a review helps.'),
                ('Спортпит и лекарства — это совместимо?', 'Is it safe with medication?', 'Обязательно уточняю, что клиент уже принимает, прежде чем что-то рекомендовать — при медицинском образовании это стандартная практика.',
                 'I always check what you\'re already taking before recommending anything — standard practice given my medical background.'),
                ('Нужен ли спортпит, если тренируюсь для себя, а не на соревнования?', 'Do I need supplements if I train just for myself?', 'Не обязательно — часто рацион можно закрыть обычной едой, и это ещё и дешевле.',
                 'Not necessarily — regular food often covers it just fine, and it\'s cheaper too.'),
            ]),
        ],
        cta_title='Нужен подбор под вашу задачу?', en_cta_title='Need a plan built for you?',
        cta_text='Разберу текущий рацион и добавки, уберу лишнее, подскажу, что реально нужно именно вам.',
        en_cta_text='I\'ll review your current diet and supplements, cut what\'s unnecessary, and tell you what you actually need.',
        cta_price='5 000 ₽', usd='53',
        cta_label='Подбор спортивного питания', en_cta_label='Supplement plan',
    ),
    'dietology.html': dict(
        title='Питание и диетология — Андрей Шелест', en_title='Nutrition & Dietology — Andrey Shelest',
        desc='Разбор питания и построение рациона под цель — снижение веса, набор массы, поддержание формы — с учётом анализов и образа жизни.',
        en_desc='Nutrition review and diet planning for your goal — weight loss, muscle gain, or maintenance — based on bloodwork and lifestyle.',
        eyebrow='Питание', en_eyebrow='Nutrition',
        h1='Питание строится под вас, а не наоборот', en_h1='Your diet is built around you, not the other way around',
        lead='Не диета «на 1200 калорий», а рацион, который реально можно соблюдать: с учётом вашего графика, привычек, вкусовых предпочтений и того, что показывают анализы.',
        en_lead='Not a generic "1200 calorie" diet, but a plan you can actually stick to — built around your schedule, habits, food preferences, and what your bloodwork shows.',
        sections=[
            ('Как проходит разбор питания', 'How a nutrition review works', [
                ('Шаг 1. Анкета и текущий рацион', 'Step 1. Questionnaire and current diet', 'Присылаете, что и как едите сейчас, обычный день — без прикрас, это основа для дальнейшей работы.',
                 'You send over what a normal day of eating actually looks like — no cleanup version, this is the starting point.'),
                ('Шаг 2. Смотрю анализы, если есть', 'Step 2. Bloodwork review, if available', 'Гликемический профиль, гормоны, липидный профиль, дефициты витаминов и микроэлементов — если анализы есть, они напрямую влияют на итоговый рацион.',
                 'Glycemic markers, hormones, lipid profile, vitamin and mineral deficiencies — if you have recent bloodwork, it directly shapes the final plan.'),
                ('Шаг 3. Собираю рацион', 'Step 3. Building the plan', 'Конкретные продукты, порции и время приёма пищи — под ваш холодильник и график, а не абстрактная схема «БЖУ на бумаге».',
                 'Specific foods, portions and meal timing — built around your actual kitchen and schedule, not an abstract macro spreadsheet.'),
                ('Шаг 4. Сопровождение', 'Step 4. Ongoing support', 'Корректировка по ходу — вес, самочувствие и результаты анализов со временем меняются, и рацион меняется вместе с ними.',
                 'Adjustments along the way — weight, wellbeing and bloodwork shift over time, and the plan shifts with them.'),
            ]),
            ('Под какую задачу', 'What kind of goal', [
                ('Снижение веса', 'Weight loss', 'Дефицит калорий без потери мышечной массы и без постоянного чувства голода — рацион держится долго именно поэтому.',
                 'A calorie deficit without losing muscle and without constant hunger — that\'s exactly why it holds up long-term.'),
                ('Набор массы', 'Muscle gain', 'Профицит калорий с акцентом на качество продуктов, а не просто «есть больше» — чтобы масса шла, а не только цифра на весах.',
                 'A calorie surplus with a focus on food quality, not just "eat more" — so it\'s actual mass, not just a bigger number on the scale.'),
                ('Поддержание формы', 'Maintenance', 'Рацион, который не требует постоянного контроля — база выстроена так, что держать форму можно на автопилоте.',
                 'A diet that doesn\'t need constant tracking — the foundation is set up so staying in shape runs on autopilot.'),
                ('Подготовка к соревнованиям', 'Contest prep', 'Питание под конкретную дату — сушка или набор к весовой категории, с более частой корректировкой и контролем.',
                 'Nutrition built around a specific date — cutting or gaining into a weight class, with tighter, more frequent adjustments.'),
            ]),
            ('Как я работаю с питанием', 'How I approach nutrition', [
                ('Отталкиваюсь от анализов', 'I start from bloodwork', 'Гликемический индекс продуктов, гормональный фон, дефициты — всё это видно по анализам и напрямую влияет на то, какой рацион будет работать именно у вас.',
                 'Glycemic index tolerance, hormone levels, deficiencies — bloodwork shows all of this, and it directly shapes which diet will actually work for you.'),
                ('Учитываю реальную жизнь', 'I account for real life', 'Рацион строится под ваш график, а не наоборот — иначе он не продержится дольше пары недель.',
                 'The diet is built around your schedule, not the other way around — otherwise it won\'t last more than a couple of weeks.'),
                ('Считаем не только калории', 'It\'s not just about calories', 'Баланс белков, жиров и углеводов и качество продуктов важны не меньше общей калорийности.',
                 'The balance of protein, fat and carbs, and food quality, matter just as much as total calories.'),
            ]),
            ('Частые вопросы', 'Frequently asked', [
                ('Это диета с жёсткими ограничениями?', 'Is this a strict, restrictive diet?', 'Нет — рацион строится так, чтобы его можно было соблюдать долго, без срывов на ровном месте.',
                 'No — the plan is built so you can actually stick to it long-term, without random breakdowns.'),
                ('Нужно ли сдавать анализы заранее?', 'Do I need bloodwork beforehand?', 'Не обязательно, но с ними разбор точнее — видно дефициты и гормональный фон, а не только цифры на весах.',
                 'Not required, but it makes the review more precise — it shows deficiencies and hormone levels, not just the number on the scale.'),
                ('Сколько длится сопровождение?', 'How long does the program run?', 'Зависит от тарифа — от разовой консультации до постоянного ведения с регулярными корректировками.',
                 'Depends on the plan you choose — from a one-off consultation to ongoing coaching with regular adjustments.'),
                ('Что если есть аллергии или непереносимости?', 'What about allergies or intolerances?', 'Учитывается сразу при составлении рациона — план подбирается под то, что вам подходит, а не наоборот.',
                 'It\'s factored in from the start — the plan is built around what works for you, not the other way around.'),
            ]),
        ],
        cta_title='Разбор вашего рациона', en_cta_title='A review of your diet',
        cta_text='Смотрю, что вы едите сейчас, и выстраиваю питание под цель — без резких ограничений и срывов.',
        en_cta_text='I look at what you\'re eating now and build a plan toward your goal — without extreme restriction or burnout.',
        cta_price='10 000 ₽', usd='105',
        cta_label='Разбор питания', en_cta_label='Nutrition review',
    ),
    'microbiome.html': dict(
        title='Микробиота кишечника — Андрей Шелест', en_title='Gut Microbiome — Andrey Shelest',
        desc='Как микробиота кишечника влияет на срывы в питании, отёки и снижение веса — и что можно сделать, чтобы это изменить.',
        en_desc='How gut microbiome affects diet breakdowns, bloating and weight loss — and what can actually be done about it.',
        eyebrow='Микробиота', en_eyebrow='Gut microbiome',
        h1='Иногда дело не в силе воли', en_h1='Sometimes it isn\'t about willpower',
        lead='Постоянные срывы в питании, отёки, вес, который не двигается несмотря на дефицит калорий — часто причина не в дисциплине, а в состоянии микробиоты кишечника.',
        en_lead='Constant diet breakdowns, bloating, weight that won\'t move despite a calorie deficit — the cause is often not discipline, but the state of your gut microbiome.',
        sections=[
            ('Как это проверяется', 'How it\'s checked', [
                ('Шаг 1. Симптомы и история', 'Step 1. Symptoms and history', 'Отёки, срывы, стабильность стула, самочувствие после еды — сперва собираю полную картину, а не только жалобу «не худею».',
                 'Bloating, breakdowns, stool patterns, how you feel after eating — I start by building the full picture, not just "I\'m not losing weight."'),
                ('Шаг 2. Анализы', 'Step 2. Bloodwork and testing', 'По показаниям — копрограмма, анализ на дисбактериоз, иногда расширенные тесты микробиоты, в зависимости от картины.',
                 'Based on the symptoms — a stool analysis, dysbiosis testing, sometimes extended microbiome panels, depending on the picture.'),
                ('Шаг 3. Коррекция', 'Step 3. Correction', 'Питание, точечные добавки и отслеживание динамики — микробиоту выравнивают постепенно, а не одной таблеткой.',
                 'Diet, targeted supplements, and tracking progress over time — the microbiome is rebalanced gradually, not with a single pill.'),
            ]),
            ('Признаки, на которые стоит обратить внимание', 'Signs worth paying attention to', [
                ('Вздутие после еды', 'Bloating after meals', 'Регулярное вздутие даже после привычной еды — частый признак дисбаланса, а не просто «съел что-то не то».',
                 'Regular bloating even after your usual food is often a sign of imbalance, not just "ate something off."'),
                ('Нестабильный стул', 'Irregular digestion', 'Постоянные перепады без явной причины в питании стоит разбирать отдельно, а не списывать на стресс.',
                 'Constant swings with no clear dietary cause are worth investigating separately, not just blaming on stress.'),
                ('Тяга к сладкому и мучному', 'Cravings for sugar and carbs', 'Навязчивая тяга к определённым продуктам может быть не про слабую волю, а про состояние микробиоты.',
                 'A persistent craving for specific foods can be less about willpower and more about your gut microbiome.'),
                ('Вес не двигается при дефиците калорий', 'Weight stuck despite a calorie deficit', 'Если дефицит есть, а весы стоят на месте неделями — часто дело не в арифметике, а в том, как усваивается еда.',
                 'If there\'s a real deficit but the scale hasn\'t moved for weeks, it\'s often not about the math — it\'s about how food is being absorbed.'),
                ('Высыпания и проблемы с кожей', 'Skin issues', 'Кожа нередко реагирует на состояние кишечника раньше, чем меняется вес — стоит обращать внимание на такие сигналы.',
                 'Skin often reacts to gut health before weight even shifts — worth paying attention to these signals.'),
            ]),
            ('Почему это важно', 'Why this matters', [
                ('Тяга к сахару и срывы', 'Sugar cravings and breakdowns', 'Дисбаланс микробиоты может напрямую провоцировать тягу к определённым продуктам — и это не про слабую волю.',
                 'An imbalanced microbiome can directly drive cravings for specific foods — and that\'s not a willpower problem.'),
                ('Отёки и самочувствие', 'Bloating and how you feel', 'Состояние кишечника влияет на воспаление и задержку жидкости — а значит, и на то, как вы выглядите и чувствуете себя на диете.',
                 'Gut health affects inflammation and fluid retention — which shapes how you look and feel while dieting.'),
                ('Связь с тренировками', 'Connection to training', 'Усвоение белка и углеводов, восстановление после нагрузок, общий уровень энергии — всё это тоже завязано на состояние микробиоты.',
                 'Protein and carb absorption, recovery after training, overall energy levels — all of this ties back to gut health too.'),
            ]),
            ('Частые вопросы', 'Frequently asked', [
                ('Это то же самое, что просто пить пробиотики?', 'Is this just about taking probiotics?', 'Нет — без анализа и разбора рациона это часто просто трата денег. Пробиотики работают точечно, под конкретную картину.',
                 'No — without testing and reviewing your diet, this is often just wasted money. Probiotics work best when targeted to your specific situation.'),
                ('Может ли микробиота влиять на тренировки и результат?', 'Can gut health affect training results?', 'Да, косвенно — через самочувствие, воспаление и то, насколько хорошо усваивается еда.',
                 'Yes, indirectly — through how you feel, inflammation, and how well your food is actually absorbed.'),
                ('Это долго восстанавливается?', 'Does it take long to fix?', 'По-разному — первые изменения обычно заметны за несколько недель, но многое зависит от исходного состояния.',
                 'It varies — the first changes are usually noticeable within a few weeks, but a lot depends on the starting point.'),
            ]),
        ],
        cta_title='Похожая ситуация?', en_cta_title='Sounds familiar?',
        cta_text='Разберём анализы и подберём питание с учётом состояния микробиоты.',
        en_cta_text='We\'ll review your bloodwork and build a diet around your gut health.',
        cta_price='10 000 ₽', usd='105',
        cta_label='Консультация по анализам', en_cta_label='Bloodwork consultation',
    ),
}

def render(slug, d):
    key_base = slug.split('.')[0].replace('-', '_')
    secs = ''
    en_dict = {}
    for si, (h, en_h, items) in enumerate(d['sections'], 1):
        sk = f'{key_base}.s{si}'
        en_dict[f'{sk}.h'] = en_h
        cards = ''
        for ii, (t, en_t, p, en_p) in enumerate(items, 1):
            ik = f'{sk}.i{ii}'
            en_dict[f'{ik}.t'] = en_t
            en_dict[f'{ik}.p'] = en_p
            cards += f'''
          <div class="svc__c">
            <h4 data-i18n="{ik}.t">{t}</h4>
            <p data-i18n="{ik}.p">{p}</p>
          </div>'''
        secs += f'''
<section>
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="{sk}.h">{h}</h2>
    <div class="svc" style="margin-top:28px;">{cards}
    </div>
  </div>
</section>
'''
    en_dict[f'{key_base}.eyebrow'] = d['en_eyebrow']
    en_dict[f'{key_base}.h1'] = d['en_h1']
    en_dict[f'{key_base}.lead'] = d['en_lead']
    en_dict[f'{key_base}.cta_title'] = d['en_cta_title']
    en_dict[f'{key_base}.cta_text'] = d['en_cta_text']
    en_dict[f'{key_base}.cta_label'] = d['en_cta_label']

    en_js = ',\n  '.join(f"'{k}': {json.dumps(v, ensure_ascii=False)}" for k, v in en_dict.items())
    page_scripts = SCRIPT_HEAD + f'Object.assign(I18N.en, {{\n  {en_js}\n}});' + SCRIPT_TAIL

    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{d['title']}</title>
<meta name="description" content="{d['desc']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/core.css">
</head>
<body>
{HEADER_SUB}

<section style="padding-top:160px;">
  <div class="container">
    <p class="eyebrow" data-i18n="{key_base}.eyebrow">{d['eyebrow']}</p>
    <h1 class="h-sec" style="font-size:clamp(2.1rem,4.4vw,3.4rem); max-width:20ch;" data-i18n="{key_base}.h1">{d['h1']}</h1>
    <p class="lead" data-i18n="{key_base}.lead">{d['lead']}</p>
  </div>
</section>
{secs}
<section>
  <div class="container">
    <div class="kase__body" style="background:var(--bg-2); border:1px solid var(--line); border-radius:var(--radius); padding:40px;">
      <h2 class="h-sec" style="font-size:clamp(1.5rem,2.6vw,2rem);" data-i18n="{key_base}.cta_title">{d['cta_title']}</h2>
      <p class="lead" style="margin-bottom:24px;" data-i18n="{key_base}.cta_text">{d['cta_text']}</p>
      <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
        <a href="index.html#contact" class="btn btn--gold"><span data-i18n="{key_base}.cta_label">{d['cta_label']}</span> — {d['cta_price']}</a>
        <a href="index.html#pricing" class="btn btn--ghost" data-i18n="nav.pricing">Смотреть тарифы</a>
      </div>
    </div>
  </div>
</section>

{FOOTER}
{page_scripts}
</body>
</html>
'''

for slug, d in PAGES.items():
    open(f'/root/shelest/{slug}', 'w', encoding='utf-8').write(render(slug, d))
    print('написано:', slug)
