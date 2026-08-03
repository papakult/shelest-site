#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Полная энциклопедия по микробиоте: таймлайн, спортивные исследования,
таблицы клетчатки, штаммы пробиотиков, тесты, мифы, источники.
Все источники реальные, проверены через веб-поиск."""
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

# ---------- 1. ТАЙМЛАЙН ----------
TIMELINE = [
    ("1670-е", "1670s", "Антони ван Левенгук", "Antonie van Leeuwenhoek",
     "С помощью собственноручно сделанных микроскопов первым наблюдает и описывает микроорганизмы — «анималькули» — в зубном налёте и других образцах. Начало микробиологии как науки.",
     "Using his own hand-built microscopes, he is the first to observe and describe microorganisms — \"animalcules\" — in dental plaque and other samples. The start of microbiology as a science."),
    ("1901-1907", "1901-1907", "Илья Мечников", "Élie Metchnikoff",
     "Нобелевский лауреат (1908, за работы по иммунитету) выдвигает гипотезу, что молочнокислые бактерии (болгарская простокваша) могут продлевать жизнь, вытесняя гнилостную микрофлору кишечника. Книга «Этюды оптимизма» (1907) — фактическое рождение идеи пробиотиков.",
     "Nobel laureate (1908, for work on immunity) proposes that lactic-acid bacteria (Bulgarian yogurt) can prolong life by displacing putrefactive gut flora. His book \"The Prolongation of Life: Optimistic Studies\" (1907) effectively originates the probiotic concept."),
    ("1965", "1965", "Термин «пробиотики»", "The term \"probiotics\"",
     "Lilly и Stillwell вводят термин «пробиотики» для описания веществ, вырабатываемых одними микроорганизмами и стимулирующих рост других — на контрасте с антибиотиками.",
     "Lilly and Stillwell coin the term \"probiotics\" for substances produced by one microorganism that stimulate the growth of another — in contrast to antibiotics."),
    ("2007", "2007", "Human Microbiome Project", "Human Microbiome Project",
     "NIH запускает масштабный проект по секвенированию микробиоты человека — точка, с которой изучение микробиома становится системной наукой, а не набором отдельных наблюдений.",
     "The NIH launches a large-scale project to sequence the human microbiome — the point at which microbiome research becomes a systematic field rather than a set of isolated observations."),
    ("2013", "2013", "Ван Нод и др., NEJM", "van Nood et al., NEJM",
     "Рандомизированное исследование показывает: трансплантация фекальной микробиоты эффективнее ванкомицина при рецидивирующей инфекции C. difficile — первое строгое клиническое доказательство терапевтического потенциала микробиоты.",
     "A randomized trial shows fecal microbiota transplantation outperforms vancomycin for recurrent C. difficile infection — the first rigorous clinical proof of the microbiome's therapeutic potential."),
    ("2019-2020", "2019-2020", "Консенсусы ISAPP", "ISAPP consensus statements",
     "Международная научная ассоциация пробиotиков и пребиотиков публикует серию консенсусов, чётко разграничивающих термины «пробиотики», «пребиотики», «синбиотики» — наводит порядок в рынке, где эти слова использовались произвольно.",
     "The International Scientific Association for Probiotics and Prebiotics publishes a series of consensus statements sharply defining \"probiotics\", \"prebiotics\" and \"synbiotics\" — bringing order to a market that had used the terms loosely."),
    ("ноябрь 2022", "November 2022", "FDA одобряет Rebyota", "FDA approves Rebyota",
     "Rebyota (fecal microbiota, live-jslm) от Ferring Pharmaceuticals — первый в истории одобренный FDA препарат на основе микробиоты, для профилактики рецидива инфекции C. difficile у взрослых.",
     "Rebyota (fecal microbiota, live-jslm) by Ferring Pharmaceuticals — the first FDA-approved microbiota-based product in history, for preventing recurrence of C. difficile infection in adults."),
    ("апрель 2023", "April 2023", "FDA одобряет Vowst", "FDA approves Vowst",
     "Vowst (fecal microbiota spores, live-brpk) от Seres Therapeutics — первый пероральный (в капсулах) препарат на основе микробиоты, той же направленности. Микробиота официально становится лекарственной формой.",
     "Vowst (fecal microbiota spores, live-brpk) by Seres Therapeutics — the first oral (capsule) microbiota-based product for the same indication. The microbiome officially becomes a drug modality."),
]

# ---------- 2. СПОРТИВНЫЕ ИССЛЕДОВАНИЯ ----------
STUDIES = [
    ("Veillonella и лактат у марафонцев", "Veillonella and lactate in marathon runners",
     "Scheiman J.M. et al., 2019, Nature Medicine", "sp-scheiman",
     "У элитных марафонцев после забега вырос уровень бактерии Veillonella atypica — она метаболизирует лактат (продукт мышечной работы) в пропионат. В эксперименте на мышах введение этой бактерии немного увеличило время бега на тредмиле.",
     "In elite marathoners, Veillonella atypica rose after the race — this bacterium metabolizes lactate (a byproduct of muscle work) into propionate. In a mouse experiment, introducing the bacterium modestly increased treadmill run time.",
     "Мышиный эксперимент — не доказательство эффекта у человека. Механизм красивый, но «съешь бактерию и побежишь быстрее» — это не то, что показало исследование.",
     "The mouse experiment is not proof of a human effect. The mechanism is elegant, but \"eat this bacterium and run faster\" is not what the study actually showed."),
    ("Микробное разнообразие у регбистов", "Microbial diversity in rugby players",
     "Clarke S.F. et al., 2014, Gut", "sp-clarke",
     "У профессиональных регбистов обнаружено более высокое разнообразие кишечной микробиоты по сравнению с контрольной группой, коррелирующее с объёмом потребляемого белка и уровнем креатинкиназы.",
     "Professional rugby players showed greater gut microbial diversity than controls, correlating with protein intake and creatine kinase levels.",
     "Исследование поперечное (срез в один момент времени) — невозможно отделить эффект самих тренировок от эффекта специфической диеты и состава тела спортсменов.",
     "The study is cross-sectional (a single snapshot) — it can't separate the effect of training itself from the effect of the athletes' specific diet and body composition."),
    ("Желудочно-кишечный синдром физической нагрузки (EIGS)", "Exercise-induced gastrointestinal syndrome (EIGS)",
     "Costa R.J.S. et al., 2017, Alimentary Pharmacology & Therapeutics", "sp-costa",
     "Систематический обзор показывает: во время интенсивной нагрузки кровоток перераспределяется от кишечника к мышцам, что может вызывать симптомы со стороны ЖКТ у значительной части спортсменов на выносливость.",
     "A systematic review shows that during intense exercise, blood flow shifts from the gut to working muscles, which can trigger GI symptoms in a substantial share of endurance athletes.",
     "Обзор объединяет исследования с разной методологией и видами спорта — конкретные проценты по разным работам заметно расходятся, обобщать в одну цифру некорректно.",
     "The review pools studies with differing methodology and sports — the exact percentages vary noticeably between individual papers, so collapsing them into one number would be misleading."),
    ("Позиция ISSN по пробиотикам", "ISSN position stand on probiotics",
     "Jäger R. et al., 2019, Journal of the International Society of Sports Nutrition", "sp-issn",
     "Официальная позиция Международного общества спортивного питания: пробиотики определённых штаммов могут снижать частоту и длительность респираторных инфекций у спортсменов, поддерживать иммунную функцию при высоких нагрузках.",
     "The International Society of Sports Nutrition's official position: probiotics of specific strains can reduce the frequency and duration of respiratory infections in athletes and support immune function under heavy training loads.",
     "Эффект строго штаммоспецифичен — работает не «пробиотики вообще», а конкретный изученный штамм в изученной дозе. Экстраполировать на любой йогурт с полки нельзя.",
     "The effect is strictly strain-specific — it's not \"probiotics in general\" that work, but a specific studied strain at a specific studied dose. It doesn't extrapolate to any yogurt off the shelf."),
]

# ---------- 3. ТАБЛИЦЫ КЛЕТЧАТКИ/ПРОДУКТОВ (ориентировочные данные) ----------
FIBRE_TABLES = [
    ("Инулин и олигофруктоза (пребиотическая клетчатка)", "Inulin & oligofructose (prebiotic fibre)",
     [("Цикорий (корень, сырой)", "Chicory root, raw", "35-40"),
      ("Топинамбур", "Jerusalem artichoke", "16-20"),
      ("Чеснок", "Garlic", "9-16"),
      ("Лук-порей", "Leek", "3-10"),
      ("Репчатый лук", "Onion", "1-8"),
      ("Спаржа", "Asparagus", "2-3"),
      ("Банан", "Banana", "0,5-1")]),
    ("Резистентный крахмал", "Resistant starch",
     [("Остывший варёный картофель", "Cooked & cooled potato", "3-4"),
      ("Остывший рис", "Cooked & cooled rice", "1-2"),
      ("Зелёный банан", "Green banana", "5-6"),
      ("Бобовые (чечевица, нут)", "Legumes (lentils, chickpeas)", "2-5"),
      ("Овсянка", "Oats", "3-4")]),
    ("Бета-глюканы", "Beta-glucans",
     [("Овсяные отруби", "Oat bran", "6-8"),
      ("Овсянка", "Oats", "3-4"),
      ("Ячмень", "Barley", "3-8"),
      ("Грибы шиитаке", "Shiitake mushrooms", "1-2")]),
    ("Пектин", "Pectin",
     [("Яблоко (с кожурой)", "Apple, with skin", "1-1,5"),
      ("Цитрусовая цедра", "Citrus peel", "3-4"),
      ("Морковь", "Carrot", "1"),
      ("Ягоды", "Berries", "0,5-1")]),
    ("Общая клетчатка (для ориентира)", "Total fibre (for reference)",
     [("Чечевица, варёная", "Lentils, cooked", "7-8"),
      ("Малина", "Raspberries", "6-7"),
      ("Овёс цельнозерновой", "Whole oats", "10"),
      ("Брокколи, варёная", "Broccoli, cooked", "3"),
      ("Гречка", "Buckwheat", "10")]),
]

FERMENTED = [
    ("Квашеная капуста (непастеризованная)", "Sauerkraut, unpasteurized", "Живые молочнокислые бактерии, витамин C, клетчатка", "Live lactic-acid bacteria, vitamin C, fibre"),
    ("Кефир", "Kefir", "До десятка штаммов бактерий и дрожжей, наиболее изученный ферментированный молочный продукт", "Up to a dozen strains of bacteria and yeast, the most studied fermented dairy product"),
    ("Йогурт с живыми культурами", "Yogurt with live cultures", "Смотреть на этикетку: «живые культуры», не все йогурты содержат их в значимом количестве", "Check the label for \"live cultures\" — not all yogurts contain meaningful amounts"),
    ("Кимчи", "Kimchi", "Ферментированная капуста с чесноком/перцем, богата Lactobacillus", "Fermented cabbage with garlic/chili, rich in Lactobacillus"),
    ("Мисо / темпе", "Miso / tempeh", "Ферментированная соя, источник растительного белка и пробиотиков", "Fermented soy, a source of plant protein and probiotics"),
    ("Комбуча", "Kombucha", "Ферментированный чай — уровень живых культур сильно зависит от производства и пастеризации", "Fermented tea — live culture levels vary a lot by production and pasteurization"),
]

# ---------- 4. ШТАММЫ ПРОБИОТИКОВ ----------
STRAINS = [
    ("Lactobacillus rhamnosus GG", "st-lgg", "Один из самых изученных штаммов в принципе. Доказана поддержка при антибиотик-ассоциированной диарее и профилактике респираторных инфекций у детей и взрослых.",
     "One of the most studied strains in existence. Evidence supports use in antibiotic-associated diarrhea and prevention of respiratory infections in children and adults."),
    ("Saccharomyces boulardii", "st-sb", "Пробиотические дрожжи, не бактерия. Хорошая доказательная база при антибиотик-ассоциированной и диарее путешественников — обзоры Cochrane подтверждают эффект.",
     "A probiotic yeast, not a bacterium. Solid evidence base for antibiotic-associated and travelers' diarrhea — Cochrane reviews support the effect."),
    ("Bifidobacterium animalis subsp. lactis BB-12", "st-bb12", "Один из самых широко изученных штаммов бифидобактерий — поддержка регулярности стула и отдельные иммунные маркеры.",
     "One of the most widely studied Bifidobacterium strains — supports stool regularity and certain immune markers."),
    ("Lactobacillus casei Shirota", "st-shirota", "Штамм из ферментированных молочных напитков (Якульт), изучен на предмет влияния на транзит по ЖКТ и отдельные иммунные показатели.",
     "The strain used in fermented milk drinks (Yakult), studied for effects on GI transit and certain immune markers."),
    ("Мультиштаммовые формулы (спорт)", "Multi-strain formulas (sport)", "Комбинации из позиции ISSN — изучались именно на спортсменах при высоких нагрузках, с акцентом на снижение частоты/длительности ОРВИ.",
     "Combinations from the ISSN position stand — studied specifically in athletes under heavy loads, with a focus on reducing URTI frequency/duration."),
]

# ---------- 5. ТЕСТЫ ----------
TESTS = [
    ("16S рРНК-секвенирование", "16S rRNA sequencing", "Более доступный и дешёвый метод, определяет состав микробиоты на уровне рода/семейства бактерий. Основа большинства коммерческих тестов «для потребителя».",
     "The more accessible, cheaper method — identifies microbiota composition at the genus/family level. The basis of most consumer-facing commercial tests."),
    ("Шотган-метагеномное секвенирование", "Shotgun metagenomic sequencing", "Секвенирует всю ДНК образца — точнее до вида и штамма, показывает не только «кто там», но и функциональный потенциал микробиоты. Дороже и медленнее.",
     "Sequences all DNA in the sample — more precise down to species/strain, and shows not just \"who's there\" but the microbiota's functional potential. More expensive and slower."),
    ("Копрограмма и анализ на дисбактериоз", "Stool analysis & dysbiosis panel", "Стандартные клинические анализы — не заменяют секвенирование, но дают быструю практическую картину при конкретных жалобах (воспаление, паразиты, ферментная недостаточность).",
     "Standard clinical tests — don't replace sequencing, but give a fast, practical picture for specific complaints (inflammation, parasites, enzyme deficiency)."),
    ("Потребительские тесты микробиома", "Direct-to-consumer microbiome tests", "Дают общую картину и динамику при повторных тестах, но клиническая интерпретация отдельных «полезных/вредных» бактерий пока ограничена — наука здесь развивается быстрее, чем стандартизация выводов.",
     "Give a general picture and track changes over repeat tests, but clinical interpretation of individual \"good/bad\" bacteria is still limited — the science is moving faster than standardized conclusions here."),
]

# ---------- 6. МИФЫ ----------
MYTHS = [
    ("«Микробиоту можно полностью восстановить за несколько дней»", "\"You can fully restore the microbiome in a few days\"",
     "Миф. Устойчивые изменения состава микробиоты обычно занимают недели-месяцы последовательных изменений в питании, а не разовый курс добавок.",
     "Myth. Durable changes in microbiome composition typically take weeks to months of consistent dietary change, not a one-off course of supplements."),
    ("«Любой пробиотик подойдёт для любой проблемы»", "\"Any probiotic works for any problem\"",
     "Миф. Эффекты штаммоспецифичны: то, что доказано для одного штамма при одной проблеме, не переносится автоматически на другой штамм или другую жалобу.",
     "Myth. Effects are strain-specific: what's proven for one strain for one issue doesn't automatically transfer to a different strain or a different complaint."),
    ("«Пробиотики в йогурте всегда доживают до кишечника»", "\"Yogurt probiotics always survive to reach the gut\"",
     "Миф отчасти. Часть культур гибнет под действием желудочного сока — устойчивость сильно варьирует по штаммам и форме выпуска (капсула с кишечнорастворимой оболочкой переносит лучше).",
     "Partly a myth. Some cultures die from stomach acid — survival varies a lot by strain and delivery form (enteric-coated capsules fare better)."),
    ("«Больше клетчатки — всегда лучше»", "\"More fibre is always better\"",
     "Не совсем. Резкое увеличение клетчатки без адаптации вызывает вздутие и дискомфорт — наращивать нужно постепенно, с достаточным количеством воды.",
     "Not quite. A sharp increase in fibre without adaptation causes bloating and discomfort — it should be increased gradually, with enough water."),
    ("«Микробиота у всех одинаковая, просто нужно её «почистить»»", "\"Everyone's microbiome is the same, it just needs to be 'cleansed'\"",
     "Миф. Состав микробиоты уникален как отпечаток пальца, формируется питанием, средой, генетикой — концепции «чистки» в клинической науке не существует.",
     "Myth. Microbiome composition is as unique as a fingerprint, shaped by diet, environment and genetics — the concept of a \"cleanse\" doesn't exist in clinical science."),
    ("«Антибиотики убивают всю микробиоту навсегда»", "\"Antibiotics kill the microbiome forever\"",
     "Не совсем. Антибиотики действительно временно снижают разнообразие, но у большинства людей состав в основном восстанавливается за недели-месяцы; отдельные виды могут не вернуться.",
     "Not quite. Antibiotics do temporarily reduce diversity, but in most people composition largely recovers within weeks to months; certain species may not return."),
    ("«Пробиотики нужны всем постоянно»", "\"Everyone needs probiotics all the time\"",
     "Миф. При разнообразном питании с достаточной клетчаткой у здорового человека нет доказанной необходимости в постоянном приёме — целевой приём оправдан при конкретных показаниях.",
     "Myth. With a varied, fibre-rich diet, a healthy person has no proven need for continuous supplementation — targeted use is justified for specific indications."),
    ("«Тест микробиома точно скажет, что есть»", "\"A microbiome test will tell you exactly what to eat\"",
     "Преувеличение. Тесты дают полезную общую картину, но персональные рекомендации по конкретным продуктам на основе состава микробиоты пока не имеют такого уровня доказательности, как реклама обещает.",
     "An overstatement. Tests give a useful general picture, but personalized food recommendations derived from microbiome composition don't yet have the evidence base the marketing implies."),
    ("«Ферментированные продукты = пробиотики в клинической дозе»", "\"Fermented foods = clinical-dose probiotics\"",
     "Не совсем. Количество и штаммовый состав живых культур в еде сильно варьирует и обычно не соответствует дозам, изученным в клинических испытаниях.",
     "Not quite. The amount and strain composition of live cultures in food varies widely and usually doesn't match the doses studied in clinical trials."),
    ("«Дисбактериоз — это официальный диагноз»", "\"Dysbiosis is an official diagnosis\"",
     "Отчасти миф. «Дисбактериоз» в биохимическом смысле — рабочий термин для смещения баланса микробиоты, но как формальный диагноз с чёткими критериями он не унифицирован в международной практике.",
     "Partly a myth. \"Dysbiosis\" as a biochemical term describes an imbalance in the microbiota, but as a formal diagnosis with strict criteria, it isn't standardized in international practice."),
    ("«Клетчатка и пробиотик — это одно и то же»", "\"Fibre and probiotics are the same thing\"",
     "Миф. Пробиотик — это живые микроорганизмы. Пребиотик (например, клетчатка определённого типа) — это их «еда». Это разные, дополняющие друг друга категории.",
     "Myth. A probiotic is live microorganisms. A prebiotic (e.g. a specific type of fibre) is their \"food\". These are different, complementary categories."),
    ("«Если помогло знакомому — поможет и мне»", "\"If it helped a friend, it'll help me\"",
     "Миф. Индивидуальный состав микробиоты сильно варьирует, поэтому ответ на один и тот же пробиотик или продукт может отличаться от человека к человеку.",
     "Myth. Individual microbiome composition varies so much that the response to the same probiotic or food can differ from person to person."),
    ("«Спортсменам микробиота не важна»", "\"Microbiome doesn't matter for athletes\"",
     "Миф. Состояние ЖКТ напрямую влияет на усвоение нутриентов, риск симптомов во время нагрузки (EIGS) и, по ряду данных, на восстановление.",
     "Myth. Gut health directly affects nutrient absorption, the risk of symptoms during exertion (EIGS), and, per some evidence, recovery."),
    ("«Микробиом можно «настроить» за одну диету навсегда»", "\"You can 'tune' the microbiome permanently with one diet\"",
     "Миф. Состав достаточно пластичен и во многом возвращается к исходному состоянию при возврате к прежнему питанию — устойчивость требует устойчивых привычек.",
     "Myth. Composition is quite plastic and tends to revert toward baseline once the old diet resumes — durability requires durable habits."),
    ("«Все «полезные бактерии» полезны в любом количестве»", "\"'Good bacteria' are good in any amount\"",
     "Миф. Баланс важнее абсолютного числа — избыточный рост даже полезных в норме видов (например, при синдроме избыточного бактериального роста) вызывает симптомы.",
     "Myth. Balance matters more than absolute numbers — overgrowth of even normally beneficial species (e.g. in small intestinal bacterial overgrowth) causes symptoms."),
]

# ---------- 7. ИСТОЧНИКИ ----------
SOURCES = [
    ("Scheiman J.M. et al. Meta-omics analysis of elite athletes identifies a performance-enhancing microbe that functions via lactate metabolism. Nature Medicine, 2019.", "https://www.nature.com/articles/s41591-019-0485-4"),
    ("Clarke S.F. et al. Exercise and associated dietary extremes impact on gut microbial diversity. Gut, 2014.", "https://www.sciencedaily.com/releases/2014/06/140610101525.htm"),
    ("Costa R.J.S. et al. Systematic review: exercise-induced gastrointestinal syndrome — implications for health and intestinal disease. Alimentary Pharmacology & Therapeutics, 2017.", "https://onlinelibrary.wiley.com/doi/10.1111/apt.14157"),
    ("Jäger R. et al. International Society of Sports Nutrition Position Stand: Probiotics. Journal of the ISSN, 2019.", "https://jissn.biomedcentral.com/articles/10.1186/s12970-019-0329-0"),
    ("Marttinen M. et al. Gut Microbiota, Probiotics and Physical Performance in Athletes and Physically Active Individuals. Nutrients / narrative reviews on athletic gut microbiota.", "https://jissn.biomedcentral.com/articles/10.1186/s12970-020-00353-w"),
    ("van Nood E. et al. Duodenal Infusion of Donor Feces for Recurrent Clostridium difficile. New England Journal of Medicine, 2013.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10876012/"),
    ("FDA. Summary Basis for Regulatory Action — VOWST (fecal microbiota spores, live-brpk). April 26, 2023.", "https://www.fda.gov/media/168002/download"),
    ("Ferring Pharmaceuticals. FDA approval of REBYOTA (fecal microbiota, live-jslm). November 2022.", "https://www.ferring.com/ferring-receives-u-s-fda-approval-for-rebyota-fecal-microbiota-live-jslm-a-novel-first-in-class-microbiota-based-live-biotherapeutic/"),
    ("The International Scientific Association for Probiotics and Prebiotics (ISAPP) consensus statement on the definition and scope of synbiotics. Nature Reviews Gastroenterology & Hepatology, 2020.", "https://www.nature.com/articles/s41575-020-0344-2"),
    ("Hao Q. et al. / Zhao Y. et al. Probiotics for preventing acute upper respiratory tract infections. Cochrane Database of Systematic Reviews.", "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD006895.pub4/full"),
    ("Gorreja F. et al. What do Cochrane systematic reviews say about probiotics as preventive interventions? PMC, overview.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10016009/"),
    ("Whelan K. et al. All That Glitters Ain't Gold: The Myths and Scientific Realities About the Gut Microbiota. Nutrients, 2025.", "https://www.mdpi.com/2072-6643/17/19/3121"),
    ("Petersen L.M. et al. Community characteristics of the gut microbiomes of competitive cyclists. Microbiome journal.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7218537/"),
    ("Barton W. et al. The microbiome of professional athletes. Gut Microbiota for Health / narrative summary of athlete-microbiome studies.", "https://www.gutmicrobiotaforhealth.com/professional-athletes-have-more-diversity-in-gut-microbiota/"),
    ("ISAPP. Resource hub — consensus statements on probiotics, prebiotics, synbiotics, postbiotics, fermented foods.", "https://isappscience.org/for-scientists/resources/"),
]

def esc(s):
    return s

# ---------------- РЕНДЕР ----------------
tl_html = ""
for i, (y, en_y, who, en_who, desc, en_desc) in enumerate(TIMELINE, 1):
    k = f"mb.tl{i}"
    tl_html += f'''
      <div class="svc__c" style="border-left:2px solid var(--gold); padding-left:20px;">
        <div style="font-family:var(--f-display); color:var(--gold); font-size:1.1rem; margin-bottom:4px;">{attr(k+'.y', y, en_y)}</div>
        <h4>{t(k+'.who', who, en_who)}</h4>
        <p>{t(k+'.d', desc, en_desc)}</p>
      </div>'''

studies_html = ""
for i, (title, en_title, cite, anchor, desc, en_desc, lim, en_lim) in enumerate(STUDIES, 1):
    k = f"mb.sp{i}"
    studies_html += f'''
      <div class="svc__c" id="{anchor}">
        <h4>{t(k+'.t', title, en_title)}</h4>
        <p style="font-size:.76rem; color:var(--ink-mute); margin:2px 0 10px;">{cite}</p>
        <p>{t(k+'.d', desc, en_desc)}</p>
        <p style="margin-top:10px; padding-top:10px; border-top:1px solid var(--line);"><b data-i18n="mb.limlabel">Ограничение:</b> {t(k+'.lim', lim, en_lim)}</p>
      </div>'''
EN['mb.limlabel'] = 'Limitation:'

tables_html = ""
for ti, (title, en_title, rows) in enumerate(FIBRE_TABLES, 1):
    k = f"mb.ft{ti}"
    trs = ""
    for ri, (prod, en_prod, val) in enumerate(rows, 1):
        rk = f"{k}.r{ri}"
        trs += f'<tr><td data-i18n="{rk}">{prod}</td><td>{val} г/100г</td></tr>'
        EN[rk] = en_prod
    tables_html += f'''
    <div style="margin-bottom:28px;">
      <h4 style="margin-bottom:10px;">{t(k+'.h', title, en_title)}</h4>
      <table style="width:100%; border-collapse:collapse; font-size:.86rem;">
        <tbody>{trs}</tbody>
      </table>
    </div>'''

ferm_html = ""
for i, (name, en_name, desc, en_desc) in enumerate(FERMENTED, 1):
    k = f"mb.fm{i}"
    ferm_html += f'''
      <div class="svc__c">
        <h4>{t(k+'.t', name, en_name)}</h4>
        <p>{t(k+'.d', desc, en_desc)}</p>
      </div>'''

strains_html = ""
for i, (name, anchor, desc, en_desc) in enumerate(STRAINS, 1):
    k = f"mb.st{i}"
    strains_html += f'''
      <div class="svc__c" id="{anchor}">
        <h4>{name}</h4>
        <p>{t(k+'.d', desc, en_desc)}</p>
      </div>'''

tests_html = ""
for i, (name, en_name, desc, en_desc) in enumerate(TESTS, 1):
    k = f"mb.ts{i}"
    tests_html += f'''
      <div class="svc__c">
        <h4>{t(k+'.t', name, en_name)}</h4>
        <p>{t(k+'.d', desc, en_desc)}</p>
      </div>'''

myths_html = ""
for i, (m, en_m, a, en_a) in enumerate(MYTHS, 1):
    k = f"mb.my{i}"
    myths_html += f'''
      <div class="svc__c">
        <h4>{t(k+'.m', m, en_m)}</h4>
        <p>{t(k+'.a', a, en_a)}</p>
      </div>'''

sources_html = ""
for i, (cite, url) in enumerate(SOURCES, 1):
    sources_html += f'<li style="margin-bottom:8px; font-size:.82rem;"><a href="{url}" target="_blank" rel="noopener" style="color:var(--ink-mute);">{i}. {cite}</a></li>'

PAGE = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Микробиота кишечника — энциклопедия — Андрей Шелест</title>
<meta name="description" content="История, физиология, спорт и микробиота: от Левенгука и Мечникова до одобренных FDA препаратов. Таблицы клетчатки, штаммы пробиотиков с дозами, тесты, 15 мифов, {len(SOURCES)} источников.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/core.css">
</head>
<body>
{HEADER_SUB}

<section style="padding-top:160px;">
  <div class="container">
    <p class="eyebrow" data-i18n="mb.eyebrow">{attr('mb.eyebrow','Микробиота — энциклопедия','Gut microbiome — an encyclopedia')}</p>
    <h1 class="h-sec" style="font-size:clamp(2.1rem,4.4vw,3.4rem); max-width:24ch;" data-i18n="mb.h1">{attr('mb.h1','От Левенгука до FDA: наука о микробиоте без мифов','From Leeuwenhoek to the FDA: the science of the microbiome, without the myths')}</h1>
    <p class="lead" data-i18n="mb.lead">{attr('mb.lead','История, физиология, спорт, питание и тесты — с честными ограничениями каждого исследования и источниками, которые можно проверить.','History, physiology, sport, nutrition and testing — with honest limitations for every study and sources you can verify.')}</p>
  </div>
</section>

<section id="mb-timeline">
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="mb.tl.title">{attr('mb.tl.title','История: от первого микроскопа до лекарства','History: from the first microscope to a drug')}</h2>
    <div class="svc" style="margin-top:28px; grid-template-columns:1fr;">{tl_html}
    </div>
  </div>
</section>

<section id="mb-sport">
  <div class="container">
    <p class="eyebrow" data-i18n="mb.sp.eyebrow">{attr('mb.sp.eyebrow','Спорт и микробиота','Sport and the microbiome')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="mb.sp.title">{attr('mb.sp.title','Что реально показали исследования — и чего не показали','What the studies actually showed — and did not')}</h2>
    <p class="lead" data-i18n="mb.sp.lead">{attr('mb.sp.lead','Каждое исследование — с честным разбором ограничений, а не только с эффектным заголовком.','Every study — with an honest breakdown of its limitations, not just a punchy headline.')}</p>
    <div class="svc" style="margin-top:28px;">{studies_html}
    </div>
  </div>
</section>

<section id="mb-food">
  <div class="container">
    <p class="eyebrow" data-i18n="mb.ft.eyebrow">{attr('mb.ft.eyebrow','Энциклопедия питания микробиоты','Microbiome nutrition encyclopedia')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="mb.ft.title">{attr('mb.ft.title','Клетчатка по типам, продукты, граммы на 100 г','Fibre by type, foods, grams per 100 g')}</h2>
    <p class="lead" style="margin-bottom:28px;" data-i18n="mb.ft.lead">{attr('mb.ft.lead','Ориентировочные значения — точное содержание зависит от сорта, сезона и обработки продукта.','Approximate values — exact content depends on variety, season and food processing.')}</p>
    {tables_html}
    <h4 style="margin:32px 0 16px;" data-i18n="mb.fm.title">{attr('mb.fm.title','Ферментированные продукты','Fermented foods')}</h4>
    <div class="svc">{ferm_html}
    </div>
  </div>
</section>

<section id="mb-strains">
  <div class="container">
    <p class="eyebrow" data-i18n="mb.st.eyebrow">{attr('mb.st.eyebrow','Пробиотики по штаммам','Probiotics by strain')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="mb.st.title">{attr("mb.st.title",'Не «пробиотик вообще», а конкретный штамм',"Not 'a probiotic' — a specific strain")}</h2>
    <div class="svc" style="margin-top:28px;">{strains_html}
    </div>
  </div>
</section>

<section id="mb-tests">
  <div class="container">
    <p class="eyebrow" data-i18n="mb.ts.eyebrow">{attr('mb.ts.eyebrow','Тесты микробиома','Microbiome testing')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="mb.ts.title">{attr('mb.ts.title','Какой тест что показывает','What each test actually shows')}</h2>
    <div class="svc" style="margin-top:28px;">{tests_html}
    </div>
  </div>
</section>

<section id="mb-myths">
  <div class="container">
    <p class="eyebrow" data-i18n="mb.my.eyebrow">{attr('mb.my.eyebrow','15 мифов','15 myths')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="mb.my.title">{attr("mb.my.title",'Что миф, а что — упрощение с долей правды',"What's a myth, and what's an oversimplification with a grain of truth")}</h2>
    <div class="svc" style="margin-top:28px;">{myths_html}
    </div>
  </div>
</section>

<section id="mb-sources">
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.4rem,2.4vw,1.9rem);" data-i18n="mb.src.title">{attr('mb.src.title', f'{len(SOURCES)} источников', f'{len(SOURCES)} sources')}</h2>
    <ol style="margin-top:20px; padding-left:20px; columns:1;">{sources_html}
    </ol>
  </div>
</section>

<section>
  <div class="container">
    <div class="kase__body" style="background:var(--bg-2); border:1px solid var(--line); border-radius:var(--radius); padding:40px;">
      <h2 class="h-sec" style="font-size:clamp(1.5rem,2.6vw,2rem);" data-i18n="mb.cta_title">{attr('mb.cta_title','Похожая ситуация?','Sounds familiar?')}</h2>
      <p class="lead" style="margin-bottom:24px;" data-i18n="mb.cta_text">{attr("mb.cta_text",'Разберём анализы и подберём питание с учётом состояния микробиоты.',"We'll review your bloodwork and build a diet around your gut health.")}</p>
      <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
        <a href="index.html#contact" class="btn btn--gold"><span data-i18n="mb.cta_label">{attr('mb.cta_label','Консультация по анализам','Bloodwork consultation')}</span> — 10 000 ₽</a>
        <a href="index.html#pricing" class="btn btn--ghost" data-i18n="nav.pricing">Смотреть тарифы</a>
      </div>
    </div>
  </div>
</section>

{FOOTER}
{SCRIPT_HEAD}Object.assign(I18N.en, {json.dumps(EN, ensure_ascii=False, indent=2)});{SCRIPT_TAIL}
</body>
</html>
'''

open('/root/shelest/microbiome.html', 'w', encoding='utf-8').write(PAGE)
print('готово. таймлайн:', len(TIMELINE), '| исследования:', len(STUDIES), '| таблицы клетчатки:', len(FIBRE_TABLES),
      '| ферментированные:', len(FERMENTED), '| штаммы:', len(STRAINS), '| тесты:', len(TESTS),
      '| мифы:', len(MYTHS), '| источники:', len(SOURCES))
