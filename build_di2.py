#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Расширяет dietology.html: таймлайн истории нутрициологии, сравнение
реальных доказательных диет (Средиземноморская/DASH/низкоуглеводная/ИГ/
растительная), таблица нутриентов (DRI), клинический блок с красными
флагами, мифы, источники. Все источники реальные, проверены через веб-поиск."""
import re, json

EN = {}
def t(key, ru, en):
    EN[key] = en
    return f'<span data-i18n="{key}">{ru}</span>'
def attr(key, ru, en):
    EN[key] = en
    return ru

# ---------- 1. ТАЙМЛАЙН ----------
TIMELINE = [
    ("1780-е", "1780s", "Антуан Лавуазье", "Antoine Lavoisier",
     "Первым измеряет расход энергии человека с помощью калориметра — закладывает основу представления о еде как об источнике энергии, а не просто наборе вкусов.",
     "First measures human energy expenditure with a calorimeter — laying the foundation for food as a source of energy, not just taste."),
    ("1860-1900-е", "1860s-1900s", "Карл фон Фойт и Уилбур Этуотер", "Carl von Voit and Wilbur Atwater",
     "Фойт с учениками измеряет обмен веществ у людей в разных условиях; Этуотер на основе этих данных выводит калорийность белков, жиров и углеводов (4-9-4 ккал/г) — систему, которой пользуются до сих пор.",
     "Voit and his students measure human metabolism under varied conditions; Atwater uses this data to derive the caloric values of protein, fat and carbohydrate (4-9-4 kcal/g) — the system still used today."),
    ("1912", "1912", "Казимир Функ и «витамины»", "Casimir Funk and \"vitamines\"",
     "Вводит термин «vitamine» для веществ, дефицит которых вызывает болезни (цинга, бери-бери, пеллагра) — питание впервые официально признаётся не только источником энергии, но и незаменимых микронутриентов.",
     "Coins the term \"vitamine\" for substances whose deficiency causes disease (scurvy, beriberi, pellagra) — nutrition is formally recognized as more than just energy, but also essential micronutrients."),
    ("1937", "1937", "Ганс Кребс, цикл трикарбоновых кислот", "Hans Krebs, the citric acid cycle",
     "Описывает биохимический цикл, через который клетки извлекают энергию из белков, жиров и углеводов — фундамент современной биохимии питания. Нобелевская премия 1953 года.",
     "Describes the biochemical cycle through which cells extract energy from protein, fat and carbohydrate — the foundation of modern nutritional biochemistry. 1953 Nobel Prize."),
    ("1958-1970", "1958-1970", "Энсел Кис, Seven Countries Study", "Ancel Keys, Seven Countries Study",
     "Первое крупное межнациональное когортное исследование связи питания с сердечно-сосудистыми заболеваниями — заложило основу представлений о защитном эффекте средиземноморского типа питания.",
     "The first large multinational cohort study linking diet to cardiovascular disease — laid the groundwork for the idea of a protective Mediterranean-style diet."),
    ("1980-1997", "1980-1997", "От RDA к DRI", "From RDA to DRI",
     "США переходят от единых норм RDA (Recommended Dietary Allowances) к системе Dietary Reference Intakes — диапазонам норм по возрасту и полу, регулярно обновляемым Национальной академией наук.",
     "The US moves from single RDA (Recommended Dietary Allowances) figures to the Dietary Reference Intakes system — ranges by age and sex, regularly updated by the National Academy of Sciences."),
    ("1997", "1997", "Исследование DASH, NEJM", "The DASH trial, NEJM",
     "Рандомизированное контролируемое исследование показывает: диета, богатая овощами, фруктами и нежирными молочными продуктами, снижает систолическое давление почти как отдельные препараты — без единого «запрещённого» продукта.",
     "A randomized controlled trial shows a diet rich in vegetables, fruit and low-fat dairy lowers systolic blood pressure almost as much as single medications — without banning any one food."),
    ("2013", "2013", "PREDIMED, NEJM", "PREDIMED, NEJM",
     "Крупное испанское РКИ: средиземноморская диета с оливковым маслом или орехами снижает частоту крупных сердечно-сосудистых событий у людей высокого риска. Версия 2018 года — с исправленной методологией рандомизации, эффект подтверждён.",
     "A large Spanish RCT: a Mediterranean diet with olive oil or nuts reduces major cardiovascular events in high-risk adults. The corrected 2018 re-analysis, fixing a randomization issue, confirms the effect."),
    ("2019", "2019", "EAT-Lancet Commission", "EAT-Lancet Commission",
     "Международная комиссия впервые формулирует единые границы «планетарной диеты» — рацион, одновременно полезный для здоровья человека и совместимый с пределами возможностей планеты.",
     "An international commission formulates unified boundaries for a \"planetary health diet\" — one that is simultaneously healthy for people and compatible with planetary limits."),
    ("2020-е", "2020s", "Эра персонализированного питания", "The era of personalized nutrition",
     "Развитие непрерывного мониторинга глюкозы, генетического тестирования и данных о микробиоте формирует переход от универсальных рекомендаций к индивидуальному подбору — наука пока отстаёт от маркетинга направления.",
     "Continuous glucose monitoring, genetic testing and microbiome data drive a shift from one-size-fits-all guidance to individualized recommendations — the science still lags behind the marketing of this field."),
]

# ---------- 2. СРАВНЕНИЕ ДИЕТ ----------
DIETS = [
    ("Средиземноморская диета", "Mediterranean diet",
     "Овощи, фрукты, цельные злаки, бобовые, оливковое масло, рыба, умеренно — молочные продукты и вино, минимум красного мяса и сладкого.",
     "Vegetables, fruit, whole grains, legumes, olive oil, fish, moderate dairy and wine, minimal red meat and sweets.",
     "PREDIMED (NEJM, 2013/2018) — снижение крупных сердечно-сосудистых событий на ~30% у людей высокого риска на оливковом масле или орехах. Один из наиболее устойчиво воспроизводимых результатов в диетологии.",
     "PREDIMED (NEJM, 2013/2018) — roughly a 30% reduction in major cardiovascular events in high-risk adults on olive oil or nuts. One of the most consistently replicated findings in nutrition science.",
     "Исследование проводилось на людях уже высокого сердечно-сосудистого риска в Испании — перенос эффекта на здоровых людей и другие культуры питания требует осторожности.",
     "The trial was run in high-cardiovascular-risk Spanish adults — extrapolating the effect to healthy people and other food cultures needs caution."),
    ("DASH", "DASH",
     "Овощи, фрукты, нежирные молочные продукты, цельные злаки, ограничение натрия и насыщенных жиров — изначально разработана против гипертонии.",
     "Vegetables, fruit, low-fat dairy, whole grains, limited sodium and saturated fat — originally designed against hypertension.",
     "Оригинальное РКИ (NEJM, 1997) и метаанализы РКИ подтверждают клинически значимое снижение систолического давления — эффект сопоставим с монотерапией отдельными препаратами у части пациентов.",
     "The original RCT (NEJM, 1997) and later meta-analyses of RCTs confirm a clinically meaningful drop in systolic blood pressure — comparable to single-drug therapy in some patients.",
     "Эффект на давление изучен лучше всего; данные по долгосрочному влиянию на вес и другие исходы менее однородны между исследованиями.",
     "The blood-pressure effect is the best studied; evidence on long-term weight and other outcomes is less consistent across trials."),
    ("Низкоуглеводная / кетогенная", "Low-carb / ketogenic",
     "Резкое ограничение углеводов (обычно до 20-50 г/день на кето), акцент на жиры и белок — организм переходит в состояние кетоза.",
     "Sharp carbohydrate restriction (typically 20-50 g/day for keto), emphasis on fat and protein — the body shifts into ketosis.",
     "Метаанализы РКИ показывают сопоставимую с низкожировыми диетами потерю веса в первые 6-12 месяцев, у части людей — более выраженное снижение через полгода; данные по сердечно-сосудистым факторам риска смешанные.",
     "Meta-analyses of RCTs show weight loss comparable to low-fat diets over 6-12 months, with a somewhat larger early effect in some studies; evidence on cardiovascular risk factors is mixed.",
     "Разница с другими диетами по итоговому весу через 12+ месяцев обычно невелика и статистически неустойчива; долгосрочные данные по сердечно-сосудистым исходам ограничены.",
     "The difference from other diets in final weight after 12+ months is usually small and statistically fragile; long-term cardiovascular outcome data remain limited."),
    ("Интервальное голодание / ограничение по времени", "Intermittent fasting / time-restricted eating",
     "Приём пищи ограничивается определённым временным окном (например, 8 часов) или чередованием дней с ограничением калорий — без обязательного изменения состава рациона.",
     "Eating is confined to a specific time window (e.g. 8 hours) or alternated with calorie-restricted days — without necessarily changing what you eat.",
     "Систематические обзоры и метаанализы РКИ 2024-2025 годов показывают снижение веса и улучшение отдельных кардиометаболических показателей — в среднем сопоставимое с классическим ограничением калорий, а не превосходящее его.",
     "Systematic reviews and meta-analyses of RCTs from 2024-2025 show weight loss and improved cardiometabolic markers — on average comparable to, not superior to, classic calorie restriction.",
     "Ключевой работающий механизм — фактическое снижение общего калоража за счёт более короткого окна питания, а не «магия» самого голодания как такового.",
     "The key working mechanism is an actual drop in total calorie intake from the shorter eating window, not any \"magic\" of fasting itself."),
    ("Растительная / EAT-Lancet", "Plant-forward / EAT-Lancet",
     "Основа рациона — овощи, фрукты, цельные злаки, бобовые и орехи, животный белок — в небольшом количестве или отсутствует.",
     "The base of the diet is vegetables, fruit, whole grains, legumes and nuts, with animal protein minimal or absent.",
     "Комиссия EAT-Lancet (2019) связывает такой рацион со снижением риска хронических заболеваний и меньшей нагрузкой на экосистему; последующие индексы Planetary Health Diet Index коррелируют с более низкой смертностью в когортных исследованиях.",
     "The EAT-Lancet Commission (2019) links this pattern to lower chronic disease risk and reduced ecological burden; subsequent Planetary Health Diet Index studies correlate with lower mortality in cohort research.",
     "Часть критики (Lancet Planetary Health, 2024) указывает на риск дефицита железа, B12, цинка и омега-3 при строгом соблюдении без планирования — рацион требует грамотного замещения животных источников.",
     "Some criticism (Lancet Planetary Health, 2024) flags a risk of iron, B12, zinc and omega-3 shortfalls under strict, unplanned adherence — the diet needs deliberate substitution of animal-source nutrients."),
]

# ---------- 3. ТАБЛИЦА НУТРИЕНТОВ (DRI, ориентировочно для взрослых) ----------
NUTRIENTS = [
    ("Белок", "Protein", "0,8 г/кг — минимальная норма; 1,2-2,2 г/кг — при регулярных тренировках", "0.8 g/kg minimum RDA; 1.2-2.2 g/kg with regular training"),
    ("Клетчатка", "Fibre", "25 г/день (женщины), 38 г/день (мужчины), или ориентир 14 г на 1000 ккал", "25 g/day (women), 38 g/day (men), or a 14 g per 1000 kcal target"),
    ("Витамин D", "Vitamin D", "600-800 МЕ (15-20 мкг)/день — выше при подтверждённом дефиците по анализам", "600-800 IU (15-20 mcg)/day — higher with a confirmed deficiency on bloodwork"),
    ("Витамин B12", "Vitamin B12", "2,4 мкг/день — риск дефицита выше при растительном питании без добавок", "2.4 mcg/day — deficiency risk is higher on a plant-based diet without supplementation"),
    ("Железо", "Iron", "8 мг/день (мужчины), 18 мг/день (женщины репродуктивного возраста)", "8 mg/day (men), 18 mg/day (women of reproductive age)"),
    ("Омега-3 (ALA)", "Omega-3 (ALA)", "1,1-1,6 г/день; EPA+DHA — обычно из рыбы 2 раза в неделю или добавки", "1.1-1.6 g/day; EPA+DHA usually from fish twice a week or a supplement"),
    ("Натрий", "Sodium", "менее 2300 мг/день (ВОЗ рекомендует менее 2000 мг)", "under 2300 mg/day (WHO recommends under 2000 mg)"),
    ("Кальций", "Calcium", "1000 мг/день (взрослые), 1200 мг/день (женщины 51+)", "1000 mg/day (adults), 1200 mg/day (women 51+)"),
]

# ---------- 4. КЛИНИЧЕСКИЙ БЛОК / КРАСНЫЕ ФЛАГИ ----------
CLINICAL = [
    ("Резкое и быстрое похудение без цели", "Rapid, unintended weight loss",
     "Потеря более 5% веса за месяц без сознательного дефицита калорий — повод для обследования, а не для похвалы диете.",
     "Losing more than 5% of body weight in a month without a deliberate calorie deficit warrants medical evaluation, not praise for the diet."),
    ("Признаки расстройства пищевого поведения", "Signs of disordered eating",
     "Жёсткие ритуалы вокруг еды, тревога при отклонении от плана, компенсаторное поведение после еды — это повод обратиться к специалисту, а не «просто дисциплина».",
     "Rigid food rituals, anxiety around deviating from a plan, compensatory behavior after eating — this calls for a specialist, not just \"more discipline\"."),
    ("Кето и сахароснижающие препараты/инсулин", "Keto with glucose-lowering drugs / insulin",
     "Резкое снижение углеводов на фоне инсулина или сульфонилмочевины требует пересмотра дозировки врачом — иначе высок риск гипогликемии.",
     "Sharply cutting carbs while on insulin or a sulfonylurea requires a physician to re-titrate dosage — otherwise the hypoglycemia risk is high."),
    ("Голодание и беременность/кормление", "Fasting during pregnancy / breastfeeding",
     "Интервальное голодание и строгие ограничительные диеты не рекомендуются без сопровождения врача в период беременности и лактации.",
     "Intermittent fasting and strict restrictive diets are not recommended without physician supervision during pregnancy and breastfeeding."),
    ("История расстройств пищевого поведения", "History of an eating disorder",
     "Любая диета со строгими правилами и подсчётом — известный триггер рецидива у людей с историей РПП; таким клиентам нужен другой, более гибкий подход.",
     "Any diet with strict rules and counting is a known relapse trigger for people with a history of an eating disorder — they need a different, more flexible approach."),
    ("Хроническая усталость, выпадение волос, нарушение цикла", "Chronic fatigue, hair loss, cycle disruption",
     "Частые признаки затяжного дефицита калорий или конкретных нутриентов (железо, B12, белок) — сигнал пересмотреть рацион и сдать анализы, а не «перетерпеть».",
     "Common signs of a prolonged calorie or specific nutrient deficit (iron, B12, protein) — a signal to revise the diet and get bloodwork, not to \"push through\"."),
]

MYTHS_DI = [
    ("«Углеводы после шести — это жир»", "\"Carbs after 6pm turn into fat\"",
     "Миф. Организм не считает часы — имеет значение суммарный баланс калорий за день/неделю, а не время последнего приёма пищи.",
     "Myth. The body doesn't watch the clock — total calorie balance over the day/week matters, not the time of the last meal."),
    ("«Детокс-диеты выводят токсины»", "\"Detox diets flush out toxins\"",
     "Миф. За выведение продуктов метаболизма отвечают печень и почки — работая при обычном, а не «детокс», питании; специального ускорения эта функция не требует.",
     "Myth. Metabolic waste removal is the liver's and kidneys' job — they do it during ordinary eating, not just on a \"detox\"; that function doesn't need special acceleration."),
    ("«Чем меньше калорий, тем быстрее результат»", "\"Fewer calories always means faster results\"",
     "Не совсем. Слишком резкий дефицит замедляет обмен веществ, повышает риск срыва и потери мышечной массы вместо жировой.",
     "Not quite. Too aggressive a deficit slows metabolism and raises the risk of a binge-relapse and losing muscle instead of fat."),
    ("«Один суперфуд решает всё»", "\"One superfood fixes everything\"",
     "Миф. Ни один отдельный продукт не компенсирует несбалансированный рацион в целом — работает совокупность, а не единичный ингредиент.",
     "Myth. No single food compensates for an unbalanced diet overall — it's the whole pattern that matters, not one ingredient."),
    ("«Голодание переводит организм в режим накопления жира»", "\"Fasting puts the body into fat-storage mode\"",
     "Преувеличение. Метаболизм действительно замедляется при длительном и сильном дефиците, но кратковременное интервальное голодание в рамках протокола к этому обычно не приводит.",
     "An overstatement. Metabolism does slow with a prolonged, severe deficit, but short-term intermittent fasting within a normal protocol usually doesn't cause this."),
    ("«Растительный белок неполноценный»", "\"Plant protein is incomplete\"",
     "Не совсем. Отдельные растительные источники могут не покрывать все незаменимые аминокислоты, но при разнообразном рационе за день баланс легко достигается.",
     "Not quite. Individual plant sources may lack some essential amino acids, but a varied diet across the day easily achieves balance."),
    ("«Глютен вреден всем»", "\"Gluten is harmful for everyone\"",
     "Миф. Доказанный вред глютен несёт только при целиакии и подтверждённой чувствительности — для остальных отказ от него не даёт клинического преимущества.",
     "Myth. Gluten is only proven harmful in celiac disease and confirmed sensitivity — for everyone else, avoiding it gives no clinical benefit."),
    ("«Чем позже последний приём пищи, тем хуже сон»", "\"A late last meal always wrecks sleep\"",
     "Не универсально. Влияет состав и объём порции и индивидуальная чувствительность, а не сам факт позднего приёма пищи.",
     "Not universal. Meal composition, portion size and individual sensitivity matter more than the mere fact of eating late."),
    ("«Диета без срывов работает только у сильных духом»", "\"A diet without slip-ups only works if you're strong-willed\"",
     "Миф. Устойчивость рациона определяется в первую очередь его реалистичностью и соответствием образу жизни, а не силой воли конкретного человека.",
     "Myth. A diet's staying power comes mainly from how realistic it is and how well it fits your life, not from one person's willpower."),
    ("«БЖУ важнее, чем качество продуктов»", "\"Macros matter more than food quality\"",
     "Не совсем. Баланс белков/жиров/углеводов важен, но источник (цельные продукты против ультра-обработанных) тоже независимо влияет на сытость, микронутриенты и здоровье кишечника.",
     "Not quite. Macro balance matters, but the source (whole foods vs. ultra-processed) independently affects satiety, micronutrients and gut health too."),
]

SOURCES_DI = [
    ("Estruch R. et al. Primary Prevention of Cardiovascular Disease with a Mediterranean Diet Supplemented with Extra-Virgin Olive Oil or Nuts (PREDIMED). New England Journal of Medicine, 2018 (corrected re-analysis).", "https://www.nejm.org/doi/full/10.1056/NEJMoa1800389"),
    ("Appel L.J. et al. A Clinical Trial of the Effects of Dietary Patterns on Blood Pressure (DASH). New England Journal of Medicine, 1997.", "https://www.nejm.org/doi/full/10.1056/NEJM199704173361601"),
    ("Siervo M. et al. Effects of the Dietary Approaches to Stop Hypertension (DASH) diet on cardiovascular risk factors: a systematic review and meta-analysis. British Journal of Nutrition / PubMed.", "https://pubmed.ncbi.nlm.nih.gov/25149893/"),
    ("Bueno N.B. et al. Very-low-carbohydrate ketogenic diet v. low-fat diet for long-term weight loss: a meta-analysis of randomised controlled trials. British Journal of Nutrition.", "https://www.cambridge.org/core/journals/british-journal-of-nutrition/article/verylowcarbohydrate-ketogenic-diet-v-lowfat-diet-for-longterm-weight-loss-a-metaanalysis-of-randomised-controlled-trials/6FD9F975BAFF1D46F84C8BA9CE860783"),
    ("Impact of very low carbohydrate ketogenic diets on cardiovascular risk factors among patients with type 2 diabetes: GRADE-assessed systematic review and meta-analysis. Nutrition & Metabolism, 2024.", "https://link.springer.com/article/10.1186/s12986-024-00824-w"),
    ("The impact of intermittent fasting on body composition and cardiometabolic outcomes in overweight and obese adults: systematic review and meta-analysis of RCTs. Nutrition Journal, 2025.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC12309044/"),
    ("Intermittent fasting and health outcomes: an umbrella review of systematic reviews and meta-analyses of randomised controlled trials. eClinicalMedicine / ScienceDirect, 2024.", "https://www.sciencedirect.com/science/article/pii/S2589537024000981"),
    ("EAT-Lancet Commission. Food in the Anthropocene: the EAT-Lancet Commission on healthy diets from sustainable food systems. The Lancet, 2019.", "https://eatforum.org/knowledge/diets-for-a-better-future/2019-eat-lancet-commission/"),
    ("Recommendations to address the shortfalls of the EAT-Lancet planetary health diet from a plant-forward perspective. The Lancet Planetary Health, 2024.", "https://www.thelancet.com/journals/lanplh/article/PIIS2542-5196(24)00305-X/fulltext"),
    ("Institute of Medicine (National Academies). Dietary Reference Intakes: Reference Tables. NCBI Bookshelf.", "https://www.ncbi.nlm.nih.gov/books/NBK208874/"),
    ("NIH Office of Dietary Supplements. Nutrient Recommendations and Databases (Dietary Reference Intakes).", "https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx"),
    ("World Health Organization. Sodium intake for adults and children — Guideline.", "https://www.who.int/publications/i/item/9789241504836"),
]

def render_diet(i, name, en_name, comp, en_comp, ev, en_ev, lim, en_lim):
    k = f"di.d{i}"
    return f'''
      <div class="svc__c">
        <h4>{t(k+'.n', name, en_name)}</h4>
        <p style="font-size:.76rem; color:var(--ink-mute); margin:4px 0 10px;">{t(k+'.c', comp, en_comp)}</p>
        <p><b data-i18n="di.evlabel">Что показывает наука:</b> {t(k+'.ev', ev, en_ev)}</p>
        <p style="margin-top:10px; padding-top:10px; border-top:1px solid var(--line);"><b data-i18n="di.limlabel">Ограничение:</b> {t(k+'.lim', lim, en_lim)}</p>
      </div>'''

diets_html = "".join(render_diet(i, *d) for i, d in enumerate(DIETS, 1))
EN['di.evlabel'] = 'What the science shows:'
EN['di.limlabel'] = 'Limitation:'

tl_html = ""
for i, (y, en_y, who, en_who, desc, en_desc) in enumerate(TIMELINE, 1):
    k = f"di.tl{i}"
    tl_html += f'''
      <div class="svc__c" style="border-left:2px solid var(--gold); padding-left:20px;">
        <div style="font-family:var(--f-display); color:var(--gold); font-size:1.1rem; margin-bottom:4px;">{attr(k+'.y', y, en_y)}</div>
        <h4>{t(k+'.who', who, en_who)}</h4>
        <p>{t(k+'.d', desc, en_desc)}</p>
      </div>'''

nutrients_rows = ""
for i, (name, en_name, val, en_val) in enumerate(NUTRIENTS, 1):
    k = f"di.nt{i}"
    nutrients_rows += f'<tr><td data-i18n="{k}.n" style="padding:10px 0; border-bottom:1px solid var(--line);">{name}</td><td data-i18n="{k}.v" style="padding:10px 0; border-bottom:1px solid var(--line); color:var(--ink-mute); font-size:.86rem;">{val}</td></tr>'
    EN[f'{k}.n'] = en_name
    EN[f'{k}.v'] = en_val

clinical_html = ""
for i, (title, en_title, desc, en_desc) in enumerate(CLINICAL, 1):
    k = f"di.cl{i}"
    clinical_html += f'''
      <div class="svc__c">
        <h4>{t(k+'.t', title, en_title)}</h4>
        <p>{t(k+'.d', desc, en_desc)}</p>
      </div>'''

myths_html = ""
for i, (m, en_m, a, en_a) in enumerate(MYTHS_DI, 1):
    k = f"di.my{i}"
    myths_html += f'''
      <div class="svc__c">
        <h4>{t(k+'.m', m, en_m)}</h4>
        <p>{t(k+'.a', a, en_a)}</p>
      </div>'''

sources_html = "".join(f'<li style="margin-bottom:8px; font-size:.82rem;"><a href="{u}" target="_blank" rel="noopener" style="color:var(--ink-mute);">{i}. {c}</a></li>' for i,(c,u) in enumerate(SOURCES_DI,1))

EXTRA = f'''
<section id="di-timeline">
  <div class="container">
    <p class="eyebrow" data-i18n="di.tl.eyebrow">{attr('di.tl.eyebrow','История нутрициологии','History of nutrition science')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="di.tl.title">{attr("di.tl.title","От калориметра Лавуазье до персонализированного питания","From Lavoisier's calorimeter to personalized nutrition")}</h2>
    <div class="svc" style="margin-top:28px; grid-template-columns:1fr;">{tl_html}
    </div>
  </div>
</section>

<section id="di-diets">
  <div class="container">
    <p class="eyebrow" data-i18n="di.d.eyebrow">{attr('di.d.eyebrow','Энциклопедия диет','Diet encyclopedia')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="di.d.title">{attr('di.d.title','5 доказательных подходов — с честными ограничениями','5 evidence-based approaches — with honest limitations')}</h2>
    <p class="lead" data-i18n="di.d.lead">{attr("di.d.lead","Не «какая диета лучшая», а что конкретно показало каждое исследование и кому это не подходит.","Not 'which diet is best', but what each study actually showed, and who it isn't right for.")}</p>
    <div class="svc" style="margin-top:28px;">{diets_html}
    </div>
  </div>
</section>

<section id="di-nutrients">
  <div class="container">
    <p class="eyebrow" data-i18n="di.nt.eyebrow">{attr('di.nt.eyebrow','Ориентиры','Reference values')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="di.nt.title">{attr('di.nt.title','Таблица нутриентов: суточные нормы для взрослых','Nutrient table: daily reference intakes for adults')}</h2>
    <p class="lead" style="margin-bottom:24px;" data-i18n="di.nt.lead">{attr('di.nt.lead','Общие ориентиры DRI/RDA (NIH, ВОЗ) — индивидуальная норма зависит от возраста, пола, состояния здоровья и уровня активности.','General DRI/RDA reference values (NIH, WHO) — your individual target depends on age, sex, health status and activity level.')}</p>
    <table style="width:100%; border-collapse:collapse; font-size:.92rem;">
      <tbody>{nutrients_rows}
      </tbody>
    </table>
  </div>
</section>

<section id="di-clinical">
  <div class="container">
    <p class="eyebrow" data-i18n="di.cl.eyebrow">{attr('di.cl.eyebrow','Когда пора к врачу','When to see a doctor')}</p>
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="di.cl.title">{attr('di.cl.title','Клинические красные флаги в питании','Clinical red flags in nutrition')}</h2>
    <p class="lead" data-i18n="di.cl.lead">{attr("di.cl.lead","Любая диета подбирается с учётом состояния здоровья — вот когда самостоятельные эксперименты стоит остановить.","Any diet should account for your health status — here's when to stop self-experimenting.")}</p>
    <div class="svc" style="margin-top:28px;">{clinical_html}
    </div>
  </div>
</section>

<section id="di-myths2">
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.6rem,2.8vw,2.2rem);" data-i18n="di.my.title">{attr('di.my.title','Мифы о питании','Nutrition myths')}</h2>
    <div class="svc" style="margin-top:28px;">{myths_html}
    </div>
  </div>
</section>

<section id="di-sources">
  <div class="container">
    <h2 class="h-sec" style="font-size:clamp(1.4rem,2.4vw,1.9rem);" data-i18n="di.src.title">{attr('di.src.title', f'{len(SOURCES_DI)} источников', f'{len(SOURCES_DI)} sources')}</h2>
    <ol style="margin-top:20px; padding-left:20px;">{sources_html}
    </ol>
  </div>
</section>
'''

html = open('/root/shelest/dietology.html', encoding='utf-8').read()

if 'id="di-timeline"' not in html:
    html = html.replace('<section>\n  <div class="container">\n    <div class="kase__body"', EXTRA.strip('\n') + '\n\n<section>\n  <div class="container">\n    <div class="kase__body"')

m = re.search(r'(Object\.assign\(I18N\.en, \{)(.*?)(\}\);)', html, re.S)
if m and "'di.tl" not in html.split("Object.assign(I18N.en")[1][:2000]:
    extra_en = ',\n  ' + ',\n  '.join(f"'{k}': {json.dumps(v, ensure_ascii=False)}" for k, v in EN.items())
    html = html[:m.end(2)] + extra_en + html[m.end(2):]

open('/root/shelest/dietology.html', 'w', encoding='utf-8').write(html)
print('готово: таймлайн:', len(TIMELINE), '| диеты:', len(DIETS), '| нутриенты:', len(NUTRIENTS),
      '| клинический блок:', len(CLINICAL), '| мифы:', len(MYTHS_DI), '| источники:', len(SOURCES_DI))
