#!/usr/bin/env python3
"""Одноразовый помощник: собирает seo/registry.json из таблицы ТЗ (80 кандидатов)
и решений по intent. После генерации registry.json правится руками/этим скриптом."""
import json
# id, slug, h1, primaryKeyword, cluster, product(ТЗ)
ROWS = """A01|personalny-trener-online|Персональный тренер онлайн|персональный тренер онлайн|A|full
A02|online-trener|Онлайн-тренер|онлайн тренер|A|full
A03|fitnes-trener-online|Фитнес-тренер онлайн|фитнес тренер онлайн|A|full
A04|online-soprovozhdenie|Онлайн-сопровождение по тренировкам|онлайн сопровождение тренировки|A|full
A05|online-soprovozhdenie-trenirovki-pitanie|Онлайн-сопровождение по тренировкам и питанию|онлайн сопровождение тренировки питание|A|full
A06|personalnoe-online-vedenie|Персональное онлайн-ведение|персональное онлайн ведение тренер|A|full
A07|online-trener-dlya-muzhchin|Онлайн-тренер для мужчин|онлайн тренер для мужчин|A|full
A08|online-trener-dlya-zhenshchin|Онлайн-тренер для женщин|онлайн тренер для женщин|A|full
A09|online-trener-dlya-nachinayushchih|Онлайн-тренер для начинающих|онлайн тренер для начинающих|A|full
A10|online-trener-dlya-zala|Онлайн-тренер для тренировок в зале|онлайн тренер тренажерный зал|A|full
A11|online-trener-dlya-doma|Онлайн-тренер для домашних тренировок|онлайн тренер дома|A|full
A12|vip-online-soprovozhdenie|VIP онлайн-сопровождение|vip онлайн сопровождение тренер|A|vip
B01|programma-trenirovok|Индивидуальная программа тренировок|индивидуальная программа тренировок|B|program_monthly
B02|personalnaya-programma-trenirovok|Персональная программа тренировок|персональная программа тренировок|B|program_monthly
B03|sostavlenie-programmy-trenirovok|Составление программы тренировок|составление программы тренировок|B|program_once
B04|programma-trenirovok-s-trenerom|Программа тренировок от тренера|программа тренировок от тренера|B|program_once
B05|programma-trenirovok-dlya-muzhchin|Программа тренировок для мужчин|программа тренировок для мужчин|B|program_monthly
B06|programma-trenirovok-dlya-zhenshchin|Программа тренировок для женщин|программа тренировок для женщин|B|program_monthly
B07|programma-trenirovok-dlya-nachinayushchih|Программа тренировок для начинающих|программа тренировок для начинающих|B|program_monthly
B08|programma-trenirovok-dlya-opytnyh|Программа тренировок для опытных|программа тренировок для опытных|B|program_monthly
B09|programma-trenirovok-na-mesyac|Программа тренировок на месяц|программа тренировок на месяц|B|program_monthly
B10|programma-trenirovok-3-raza-v-nedelyu|Программа тренировок 3 раза в неделю|программа тренировок 3 раза в неделю|B|program_monthly
B11|programma-trenirovok-4-raza-v-nedelyu|Программа тренировок 4 раза в неделю|программа тренировок 4 раза в неделю|B|program_monthly
B12|programma-trenirovok-v-zale|Программа тренировок в тренажёрном зале|программа тренировок в тренажерном зале|B|program_monthly
B13|individualnaya-programma-v-zale|Индивидуальная программа тренировок в зале|индивидуальная программа тренировок в зале|B|program_monthly
B14|programma-trenirovok-doma|Программа тренировок дома|программа тренировок дома|B|program_monthly
B15|individualnaya-programma-doma|Индивидуальная программа тренировок дома|индивидуальная программа тренировок дома|B|program_monthly
B16|programma-trenirovok-s-gantelyami|Программа тренировок с гантелями|программа тренировок с гантелями|B|program_monthly
B17|programma-trenirovok-bez-inventarya|Программа тренировок без инвентаря|программа тренировок без инвентаря|B|program_monthly
B18|programma-silovyh-trenirovok|Индивидуальная программа силовых тренировок|программа силовых тренировок|B|program_monthly
C01|programma-trenirovok-dlya-pohudeniya|Программа тренировок для похудения|программа тренировок для похудения|C|program_monthly
C02|programma-pohudeniya-v-zale|Программа тренировок для похудения в зале|программа тренировок для похудения в зале|C|program_monthly
C03|programma-pohudeniya-doma|Программа тренировок для похудения дома|программа тренировок для похудения дома|C|program_monthly
C04|programma-pohudeniya-dlya-muzhchin|Программа тренировок для похудения мужчинам|программа тренировок для похудения мужчинам|C|program_monthly
C05|programma-pohudeniya-dlya-zhenshchin|Программа тренировок для похудения женщинам|программа тренировок для похудения женщинам|C|program_monthly
C06|trener-dlya-pohudeniya-online|Тренер для похудения онлайн|тренер для похудения онлайн|C|full
C07|online-trener-dlya-pohudeniya|Онлайн-тренер для похудения|онлайн тренер для похудения|C|full
C08|personalny-trener-dlya-snizheniya-vesa|Персональный тренер для снижения веса|персональный тренер для снижения веса|C|full
C09|trenirovki-dlya-snizheniya-vesa|Тренировки для снижения веса|тренировки для снижения веса|C|program_monthly
C10|silovye-trenirovki-dlya-pohudeniya|Силовые тренировки для похудения|силовые тренировки для похудения|C|program_monthly
C11|programma-trenirovok-i-pitaniya-dlya-pohudeniya|Программа тренировок и рекомендации по питанию для похудения|программа тренировок и питания для похудения|C|full
C12|pohudenie-s-personalnym-trenerom-online|Похудение с персональным тренером онлайн|похудение с тренером онлайн|C|full
D01|programma-trenirovok-na-massu|Программа тренировок на массу|программа тренировок на массу|D|program_monthly
D02|programma-nabora-myshechnoy-massy|Программа тренировок на набор мышечной массы|программа тренировок на набор мышечной массы|D|program_monthly
D03|programma-na-massu-dlya-muzhchin|Программа тренировок на массу для мужчин|программа тренировок на массу для мужчин|D|program_monthly
D04|programma-na-massu-v-zale|Программа тренировок на массу в зале|программа тренировок на массу в зале|D|program_monthly
D05|programma-na-massu-3-raza-v-nedelyu|Программа тренировок на массу 3 раза в неделю|программа тренировок на массу 3 раза в неделю|D|program_monthly
D06|trener-dlya-nabora-massy|Персональный тренер для набора мышечной массы|тренер для набора мышечной массы|D|full
D07|online-trener-dlya-nabora-massy|Онлайн-тренер для набора мышечной массы|онлайн тренер для набора мышечной массы|D|full
D08|nabor-myshechnoy-massy-s-trenerom|Набор мышечной массы с тренером|набор мышечной массы с тренером|D|full
D09|trenirovki-na-silu-i-massu|Тренировки на силу и массу|тренировки на силу и массу|D|program_monthly
D10|programma-trenirovok-i-pitaniya-na-massu|Программа тренировок и рекомендации по питанию для набора массы|программа тренировок и питания для набора массы|D|full
E01|trener-dlya-muzhchin-posle-40|Тренер для мужчин после 40 лет|тренер для мужчин после 40|E|full
E02|online-trener-dlya-muzhchin-posle-40|Онлайн-тренер для мужчин после 40|онлайн тренер для мужчин после 40|E|full
E03|trenirovki-dlya-muzhchin-posle-40|Тренировки для мужчин после 40|тренировки для мужчин после 40|E|program_monthly
E04|programma-trenirovok-dlya-muzhchin-posle-40|Программа тренировок для мужчин после 40|программа тренировок для мужчин после 40|E|program_monthly
E05|silovye-trenirovki-posle-40|Силовые тренировки после 40|силовые тренировки после 40|E|program_monthly
E06|nabor-myshechnoy-massy-posle-40|Набор мышечной массы после 40|набор мышечной массы после 40|E|full
E07|nachat-trenirovatsya-posle-40|Как начать тренироваться после 40|как начать тренироваться после 40|E|program_monthly
E08|vozvrashchenie-v-zal-posle-40|Возвращение в тренажёрный зал после 40|возвращение в зал после 40|E|full
E09|programma-posle-dolgogo-pereryva|Программа тренировок после долгого перерыва|программа тренировок после перерыва|E|program_monthly
E10|trener-dlya-muzhchin-posle-50|Тренер для мужчин после 50 лет|тренер для мужчин после 50|E|full
F01|trener-po-pauerliftingu-online|Тренер по пауэрлифтингу онлайн|тренер по пауэрлифтингу онлайн|F|full
F02|online-trener-po-silovym-trenirovkam|Онлайн-тренер по силовым тренировкам|онлайн тренер силовые тренировки|F|full
F03|programma-trenirovok-po-pauerliftingu|Программа тренировок по пауэрлифтингу|программа тренировок по пауэрлифтингу|F|program_monthly
F04|podgotovka-k-sorevnovaniyam-po-pauerliftingu|Подготовка к соревнованиям по пауэрлифтингу|подготовка к соревнованиям по пауэрлифтингу|F|full
F05|programma-trenirovok-na-silu|Программа тренировок на силу|программа тренировок на силу|F|program_monthly
F06|uvelichenie-silovyh-pokazateley|Тренировки для увеличения силовых показателей|увеличение силовых показателей|F|full
F07|tehnika-prisedaniy|Разбор техники приседаний|техника приседаний тренер|F|consult
F08|tehnika-zhima-lezha|Разбор техники жима лёжа|техника жима лежа тренер|F|consult
F09|tehnika-stanovoy-tyagi|Разбор техники становой тяги|техника становой тяги тренер|F|consult
F10|razbor-tehniki-uprazhneniy-online|Разбор техники упражнений онлайн|разбор техники упражнений онлайн|F|consult
G01|personalny-trener-sochi|Персональный тренер в Сочи|персональный тренер сочи|G|full
G02|fitnes-trener-sochi|Фитнес-тренер в Сочи|фитнес тренер сочи|G|full
G03|online-trener-sochi|Онлайн-тренер в Сочи|онлайн тренер сочи|G|full
G04|programma-trenirovok-sochi|Индивидуальная программа тренировок в Сочи|программа тренировок сочи|G|program_monthly
G05|personalny-trener-adler|Персональный тренер в Адлере|персональный тренер адлер|G|full
G06|fitnes-trener-adler|Фитнес-тренер в Адлере|фитнес тренер адлер|G|full
G07|online-trener-adler|Онлайн-тренер в Адлере|онлайн тренер адлер|G|full
G08|programma-trenirovok-adler|Индивидуальная программа тренировок в Адлере|программа тренировок адлер|G|program_monthly"""

# Существующие страницы сайта, которые покрывают тот же intent: URL сохраняем,
# страницу перегенерируем через общий компонент (не создаём дубль).
LEGACY = {
  'A04': ('onlayn-vedenie.html', 'Существующая страница «Онлайн-ведение» отвечает на тот же intent (сопровождение). URL не меняем, страница собирается общим компонентом.'),
  'A08': ('zhenskiy-trening.html', 'Существующая страница «Женский тренинг» = intent «онлайн-тренер для женщин». URL сохранён.'),
  'B01': ('programma-trenirovok.html', 'Существующий URL /programma-trenirovok.html уже отвечает на этот запрос; создавать /programma-trenirovok/ = прямой дубль. URL сохранён.'),
  'B14': ('trenirovki-doma.html', 'Существующая страница «Тренировки дома» = intent «программа тренировок дома». URL сохранён.'),
  'E01': ('muzhchiny-40plus.html', 'Существующая страница «Мужчинам 40+» = intent «тренер для мужчин после 40». URL сохранён.'),
}

MERGED = {
  'A02': ('A01', 'Та же потребность: найти тренера, который работает дистанционно. «Онлайн-тренер» использован как вторичный ключ A01.'),
  'A03': ('A01', '«Фитнес-тренер онлайн» и «персональный тренер онлайн» ведут на один и тот же продукт; отличие в одном слове.'),
  'A05': ('A04', 'Полное сопровождение и так включает питание; отдельная страница повторила бы A04.'),
  'A06': ('A04', '«Персональное онлайн-ведение» и «онлайн-сопровождение» синонимы; оба закрыты страницей онлайн-ведения.'),
  'B02': ('B01', '«Персональная» и «индивидуальная» программа — синонимы, один продукт.'),
  'B04': ('B03', '«Программа от тренера» и «составление программы» — один запрос на разовое составление.'),
  'B09': ('B01', 'Тариф «Программа» и есть месячная программа; B01 закрывает «на месяц» как вторичный ключ.'),
  'B13': ('B12', '«Индивидуальная программа в зале» и «программа в тренажёрном зале» — один intent.'),
  'B15': ('B14', 'Программа дома у нас всегда индивидуальная; дубль B14.'),
  'B17': ('B14', 'Страница тренировок дома уже включает вариант без инвентаря (собственный вес); отдельная страница была бы почти копией.'),
  'C07': ('C06', 'Перестановка слов «тренер для похудения онлайн» / «онлайн-тренер для похудения».'),
  'C08': ('C06', '«Снижение веса» = «похудение», тот же продукт (сопровождение).'),
  'C09': ('C01', '«Тренировки для снижения веса» и «программа тренировок для похудения» закрывают одну потребность.'),
  'C12': ('C06', '«Похудение с тренером онлайн» = запрос на тренера для похудения, тот же продукт.'),
  'D02': ('D01', '«На массу» и «на набор мышечной массы» — одно и то же.'),
  'D03': ('D01', 'Запрос «на массу» по факту и так мужской; отдельная страница заменила бы одно слово.'),
  'D04': ('D01', 'Программа на массу по умолчанию строится для зала; зальный вариант раскрыт внутри D01.'),
  'D07': ('D06', '«Онлайн-тренер для набора массы» = D06, работа и так только онлайн.'),
  'D08': ('D06', '«Набор массы с тренером» = запрос на тренера для набора массы.'),
  'D09': ('F05', 'Сила и масса раскрыты на странице программы на силу (блок про гипертрофию).'),
  'E02': ('E01', 'Работа только онлайн, «онлайн-тренер после 40» = «тренер после 40».'),
  'E03': ('E01', 'Существующая страница называется «Тренировки для мужчин после 40»; это тот же intent.'),
  'E05': ('E04', '«Силовые тренировки после 40» закрыты программой для мужчин после 40 (силовая база).'),
  'E08': ('E09', 'Возвращение в зал после 40 = возвращение после перерыва; возраст раскрыт внутри E09.'),
  'F06': ('F02', '«Увеличение силовых показателей» = задача, под которую ищут онлайн-тренера по силовым.'),
  'G04': ('G03', 'Одна честная страница для Сочи; программа тренировок онлайн не зависит от города.'),
  'G07': ('G03', 'Адлер — район Сочи; работа только онлайн, отдельная страница была бы doorway.'),
  'G08': ('G03', 'Адлер — район Сочи; программа онлайн, отдельная страница была бы doorway.'),
}

DISABLED = {
  'G01': 'На сайте прямо указано «я работаю только онлайн» (onlayn-vedenie.html) — очных тренировок в Сочи нет, коммерческая страница персонального тренера в Сочи была бы неправдой.',
  'G02': 'Как G01: очный формат не оказывается. Если появится — объединить с G01.',
  'G05': 'Очная работа в Адлере не подтверждена сайтом («работаю только онлайн»).',
  'G06': 'Как G05.',
}

PRODUCT_NAMES = {'full':'Полное сопровождение','vip':'VIP-формат','program_monthly':'Программа (ежемесячно)',
 'program_once':'Индивидуальная программа (разово)','consult':'Разовая консультация','nutrition':'Разбор питания','labs':'Консультация с учётом анализов'}

reg = []
for line in ROWS.splitlines():
    i, slug, h1, kw, cl, prod = line.split('|')
    e = dict(id=i, slug=slug, cluster=cl, productType=prod, primaryKeyword=kw, h1=h1)
    if i in LEGACY:
        path, why = LEGACY[i]
        e.update(status='published', index=True, path='/'+path, canonicalSlug=path, legacyPage=True, decision=why)
    elif i in MERGED:
        tgt, why = MERGED[i]
        e.update(status='merged', index=False, mergedInto=tgt, decision=why)
    elif i in DISABLED:
        e.update(status='disabled', index=False, decision=DISABLED[i])
    else:
        e.update(status='published', index=True, path=f'/{slug}/', canonicalSlug=slug, decision='Самостоятельный intent.')
    reg.append(e)
# canonical для merged = страница, куда перенесён intent
byid = {e['id']: e for e in reg}
for e in reg:
    if e['status'] == 'merged':
        e['canonicalSlug'] = byid[e['mergedInto']]['canonicalSlug']
json.dump({'_about': 'Единый реестр SEO-посадочных. build_seo.py читает его + seo/content/*.json. '
           'Сайт: только published + index:true попадают в HTML и sitemap. merged/disabled URL не создаются.',
           'pages': reg}, open('seo/registry.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(e['status'] for e in reg))
