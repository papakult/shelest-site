#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Приводит АНГЛИЙСКИЕ формулировки об образовании к точным.
Первый скрипт правил только русский, английский словарь остался со словом
"medical". Здесь чиним его.

Факт: НГМУ (Novosibirsk State Medical University), 2004-2009,
специальность «Биоэкология», специализация «Экология человека»,
квалификация биолог-эколог. Диплома врача нет.

Английский канон: "degree in human ecology (Novosibirsk State Medical University)"

Запуск:
    cd ~/Desktop/shelest-site
    python3 fix-en.py            # предпросмотр
    python3 fix-en.py --apply    # применить
"""
import io, os, re, sys

APPLY = '--apply' in sys.argv

EXACT = [
    # Шапка главной
    ("World Champion · Medical degree · Competing athlete",
     "World Champion · Degree in human ecology · Competing athlete"),

    # Врезка «обо мне»
    ("I combine what few in online fitness can: a medical degree, a World Champion title, and status as a competing athlete.",
     "I combine what few in online fitness can: a degree in human ecology from a medical university, a World Champion title, and status as a competing athlete."),

    # Подвал
    ("World Champion, medical degree, competing athlete. Online coaching across Russia.",
     "World Champion, degree in human ecology, competing athlete. Online coaching across Russia."),
    ("World Champion, coach with a medical background. Online coaching for training, nutrition and bloodwork.",
     "World Champion, coach with a science background. Online coaching for training, nutrition and bloodwork."),

    # Полоска статистики и блок регалий
    ("Higher medical education", "Degree in human ecology"),
    ("NSMU — I understand how the body works under load",
     "Novosibirsk State Medical University, 2004–2009 — physiology, biochemistry, human ecology"),

    # FAQ и «подходит ли вам»
    ("My medical background lets me adapt the load to your limitations.",
     "My science background lets me adapt the load to your limitations."),
    ("A combination of competitive experience as a world champion and a medical background — programs are built on an understanding of your physiology, not a template.",
     "A combination of competitive experience as a world champion and a background in physiology and biochemistry — programs are built on an understanding of your body, not a template."),
    ("You want your load built by someone with a medical background, not a template",
     "You want your load built by someone who understands physiology, not a template"),

    # Спортпит
    ("A medical background means I can factor in what you already take — medication, supplements, chronic conditions — before recommending anything.",
     "A background in physiology and biochemistry means I can factor in what you already take — medication, supplements, chronic conditions — before recommending anything."),
    ("I always check what you're already taking before recommending anything — standard practice given my medical background.",
     "I always check what you're already taking before recommending anything — that is basic diligence, not an optional extra."),
]

GENERIC = [
    (r"a medical degree",        "a degree in human ecology"),
    (r"[Mm]edical degree",       "degree in human ecology"),
    (r"a medical background",    "a science background"),
    (r"my medical background",   "my science background"),
    (r"[Hh]igher medical education", "Degree in human ecology"),
]

EXTS = ('.html', '.md', '.js')
SKIP_DIRS = {'.git', 'node_modules', '.github'}

changed_files = 0
report = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fn in sorted(files):
        if not fn.endswith(EXTS):
            continue
        path = os.path.join(root, fn)
        try:
            src = io.open(path, encoding='utf-8').read()
        except Exception:
            continue
        out = src
        for old, new in EXACT:
            out = out.replace(old, new)
        for pat, new in GENERIC:
            out = re.sub(pat, new, out)
        if out != src:
            changed_files += 1
            for a, b in zip(src.splitlines(), out.splitlines()):
                if a != b:
                    report.append((path, a.strip()[:120], b.strip()[:120]))
            if APPLY:
                io.open(path, 'w', encoding='utf-8').write(out)

for path, a, b in report:
    print('\n%s' % path)
    print('  was: %s' % a)
    print('  now: %s' % b)

print('\n' + '=' * 60)
print('Файлов: %d, строк: %d' % (changed_files, len(report)))
print('ПРИМЕНЕНО' if APPLY else 'предпросмотр, ничего не записано')
