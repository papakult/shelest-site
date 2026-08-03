#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Встраивает ИИ-консультанта (чат, не калькулятор-форма) и блок
«Пресса / Куорум Медиа» в index.html."""
import re

html = open('/root/shelest/index.html', encoding='utf-8').read()
core = open('/root/shelest/css/core.css', encoding='utf-8').read()

# ---------------- ПРЕССА / КУОРУМ МЕДИА ----------------
PRESS_SECTION = '''
<!-- ================= ПРЕССА ================= -->
<section id="press">
  <div class="container">
    <p class="eyebrow" data-i18n="press.eyebrow">Публикации</p>
    <h2 class="h-sec" data-i18n="press.title">Пресса и упоминания</h2>
    <p class="lead" data-i18n="press.lead">Публикации и экспертные комментарии размещаются по мере выхода — раздел ведёт агентство Quorum Media.</p>
    <div class="svc" style="margin-top:28px;">
      <div class="svc__c" style="text-align:center; padding:40px 24px;">
        <p style="color:var(--ink-mute);" data-i18n="press.empty">Первые публикации появятся здесь в ближайшее время. Если у вас уже есть ссылка на статью — пришлите, добавим сразу с корректной разметкой для поисковиков.</p>
      </div>
    </div>
  </div>
</section>
'''

if 'id="press"' not in html:
    html = html.replace('<!-- ================= РАЗОВЫЕ УСЛУГИ', PRESS_SECTION.strip('\n') + '\n\n<!-- ================= РАЗОВЫЕ УСЛУГИ')

# ---------------- ИИ-КОНСУЛЬТАНТ (ЧАТ) ----------------
AI_WIDGET_HTML = '''
<!-- ================= ИИ-КОНСУЛЬТАНТ ================= -->
<button id="aiLauncher" class="ai-launcher" type="button" aria-label="ИИ-консультант">
  <span class="ai-launcher__dot"></span>
  <span data-i18n="ai.launcher">ИИ-консультант</span>
</button>

<div id="aiPanel" class="ai-panel" aria-hidden="true">
  <div class="ai-panel__head">
    <div>
      <b data-i18n="ai.title">ИИ-консультант Шелест</b>
      <span data-i18n="ai.subtitle">подбор питания и добавок под вас</span>
    </div>
    <button id="aiClose" type="button" aria-label="Закрыть">&times;</button>
  </div>
  <div id="aiLog" class="ai-panel__log"></div>
  <form id="aiForm" class="ai-panel__form">
    <input id="aiInput" type="text" autocomplete="off" data-i18n-ph="ai.placeholder" placeholder="Напишите ответ...">
    <button type="submit" class="btn btn--gold" data-i18n="ai.send">Отправить</button>
  </form>
</div>
'''

if 'id="aiPanel"' not in html:
    html = html.replace('</footer>', '</footer>' + AI_WIDGET_HTML)

AI_CSS = '''
/* ═══ ai widget начало ═══ */
.ai-launcher{ position:fixed; right:24px; bottom:24px; z-index:60; display:flex; align-items:center; gap:10px; padding:14px 22px; border-radius:100px; background:var(--gold); color:#100c02; font-weight:600; font-size:.92rem; box-shadow:0 12px 32px rgba(0,0,0,.4); }
.ai-launcher__dot{ width:8px; height:8px; border-radius:50%; background:#100c02; animation:aiPulse 1.6s ease-in-out infinite; }
@keyframes aiPulse{ 0%,100%{ opacity:1; } 50%{ opacity:.3; } }
.ai-panel{ position:fixed; right:24px; bottom:24px; z-index:70; width:380px; max-width:calc(100vw - 32px); height:520px; max-height:calc(100vh - 48px); background:var(--bg-2); border:1px solid var(--line-2); border-radius:var(--radius); display:flex; flex-direction:column; overflow:hidden; box-shadow:0 24px 64px rgba(0,0,0,.5); transform:translateY(16px) scale(.98); opacity:0; pointer-events:none; transition:.25s var(--e-out-expo, ease); }
.ai-panel.is-open{ transform:translateY(0) scale(1); opacity:1; pointer-events:auto; }
.ai-panel__head{ display:flex; align-items:flex-start; justify-content:space-between; padding:16px 18px; border-bottom:1px solid var(--line); }
.ai-panel__head b{ display:block; font-size:.94rem; }
.ai-panel__head span{ display:block; font-size:.74rem; color:var(--ink-mute); margin-top:2px; }
.ai-panel__head button{ background:none; border:none; color:var(--ink-mute); font-size:1.4rem; line-height:1; cursor:pointer; }
.ai-panel__log{ flex:1; overflow-y:auto; padding:16px 18px; display:flex; flex-direction:column; gap:12px; }
.ai-msg{ max-width:86%; padding:10px 14px; border-radius:14px; font-size:.86rem; line-height:1.45; white-space:pre-line; }
.ai-msg--bot{ align-self:flex-start; background:var(--bg-3); border:1px solid var(--line); border-bottom-left-radius:4px; }
.ai-msg--user{ align-self:flex-end; background:var(--gold); color:#100c02; border-bottom-right-radius:4px; }
.ai-msg--typing{ display:flex; gap:4px; padding:14px; }
.ai-msg--typing span{ width:6px; height:6px; border-radius:50%; background:var(--ink-mute); animation:aiTyping 1s infinite; }
.ai-msg--typing span:nth-child(2){ animation-delay:.15s; }
.ai-msg--typing span:nth-child(3){ animation-delay:.3s; }
@keyframes aiTyping{ 0%,60%,100%{ opacity:.3; transform:translateY(0);} 30%{ opacity:1; transform:translateY(-3px);} }
.ai-panel__form{ display:flex; gap:8px; padding:14px; border-top:1px solid var(--line); }
.ai-panel__form input{ flex:1; background:var(--bg-3); border:1px solid var(--line-2); border-radius:100px; padding:10px 16px; color:var(--ink); font-size:.86rem; }
.ai-panel__form button{ padding:10px 18px; font-size:.82rem; white-space:nowrap; }
@media (max-width:520px){ .ai-panel{ right:16px; left:16px; width:auto; bottom:88px; } .ai-launcher{ right:16px; bottom:16px; padding:12px 18px; } }
/* ═══ ai widget конец ═══ */
'''

if '/* ═══ ai widget начало ═══ */' not in core:
    core += AI_CSS
    open('/root/shelest/css/core.css', 'w', encoding='utf-8').write(core)

AI_JS = r'''
/* ═══ ai widget начало ═══ */
(function(){
  const launcher = document.getElementById('aiLauncher');
  const panel = document.getElementById('aiPanel');
  const closeBtn = document.getElementById('aiClose');
  const log = document.getElementById('aiLog');
  const form = document.getElementById('aiForm');
  const input = document.getElementById('aiInput');
  if (!launcher || !panel) return;

  let opened = false;
  const state = { step: 0, data: {} };

  const STEPS = [
    { key: 'goal', ask: 'Привет! Я разберу ваш рацион и подскажу, что реально нужно из питания и добавок. Начнём с цели — что вам ближе: снижение веса, набор массы или поддержание формы?' },
    { key: 'weight', ask: 'Понял. Сколько вы сейчас весите (в кг)?' },
    { key: 'height', ask: 'Какой у вас рост (в см)?' },
    { key: 'age', ask: 'Сколько вам лет?' },
    { key: 'sex', ask: 'Вы мужчина или женщина?' },
    { key: 'activity', ask: 'Как часто тренируетесь: почти не тренируюсь, 2-3 раза в неделю, или почти каждый день?' },
    { key: 'budget', ask: 'И последнее — какой бюджет на добавки в месяц вам комфортен: до 3000 ₽, до 7000 ₽, или бюджет не главное?' },
  ];

  function scrollLog(){ log.scrollTop = log.scrollHeight; }

  function addMsg(text, who){
    const div = document.createElement('div');
    div.className = 'ai-msg ai-msg--' + who;
    div.textContent = text;
    log.appendChild(div);
    scrollLog();
  }

  function addTyping(){
    const div = document.createElement('div');
    div.className = 'ai-msg ai-msg--bot ai-msg--typing';
    div.innerHTML = '<span></span><span></span><span></span>';
    div.id = 'aiTypingNow';
    log.appendChild(div);
    scrollLog();
  }
  function removeTyping(){
    const t = document.getElementById('aiTypingNow');
    if (t) t.remove();
  }

  function botSay(text, delay){
    addTyping();
    setTimeout(()=>{ removeTyping(); addMsg(text, 'bot'); }, delay || 550);
  }

  function extractNumber(s){
    const m = s.replace(',', '.').match(/[\d]+(\.\d+)?/);
    return m ? parseFloat(m[0]) : null;
  }

  function parseGoal(s){
    s = s.toLowerCase();
    if (/сниж|худе|похуд|минус/.test(s)) return 'loss';
    if (/набор|масс|плюс/.test(s)) return 'gain';
    return 'maintain';
  }
  function parseSex(s){ return /жен/i.test(s) ? 'f' : 'm'; }
  function parseActivity(s){
    s = s.toLowerCase();
    if (/кажд|ежедн|6|7/.test(s)) return 1.7;
    if (/2|3|нескол/.test(s)) return 1.5;
    return 1.3;
  }
  function parseBudget(s){
    s = s.toLowerCase();
    if (/3000|3 000|мал/.test(s)) return 3000;
    if (/7000|7 000/.test(s)) return 7000;
    return 15000;
  }

  function computeAndReply(){
    const d = state.data;
    const weight = d.weight, height = d.height, age = d.age;
    const sexK = d.sex === 'f' ? -161 : 5;
    const bmr = 10*weight + 6.25*height - 5*age + sexK;
    const tdee = bmr * d.activity;
    let targetCal = tdee;
    if (d.goal === 'loss') targetCal = tdee - 450;
    if (d.goal === 'gain') targetCal = tdee + 350;
    const protein = Math.min(2.2*weight, (targetCal*0.35)/4);
    const fat = (targetCal*0.27)/9;
    const carbs = Math.max((targetCal - protein*4 - fat*9)/4, 0);
    const fibre = Math.max(14*targetCal/1000, 25);
    const water = Math.round(weight*32);

    let stack = [];
    stack.push('Креатин моногидрат — 5 г/день, постоянно');
    if (d.goal !== 'loss') stack.push('Протеин — 1-2 порции, если не закрываете белок едой');
    if (d.budget >= 7000) stack.push('Омега-3 — 1-2 г/день, если рыба в рационе редко');
    if (d.budget >= 7000 && d.goal === 'loss') stack.push('Витамин D — по анализам, часто актуален зимой в Новосибирске');
    if (d.budget < 3000) stack.push('При таком бюджете креатина и, при нехватке белка в еде, протеина обычно достаточно');

    const goalRu = {loss:'снижение веса', gain:'набор массы', maintain:'поддержание формы'}[d.goal];

    const summary =
`Готово. Вот ориентир под вашу цель — ${goalRu}:

Калории: ~${Math.round(targetCal)} ккал/день
Белки: ~${Math.round(protein)} г · Жиры: ~${Math.round(fat)} г · Углеводы: ~${Math.round(carbs)} г
Клетчатка: от ${Math.round(fibre)} г · Вода: ~${water} мл

Из добавок под ваш бюджет:
${stack.map(s=>'• '+s).join('\n')}

Это ориентир по формулам (Mifflin-St Jeor), не диагноз. Чтобы собрать точный план с учётом анализов и образа жизни — жду в разборе питания.`;

    botSay(summary, 700);
    setTimeout(()=>{
      const div = document.createElement('div');
      div.className = 'ai-msg ai-msg--bot';
      div.innerHTML = 'Записаться на разбор питания: <a href="index.html#contact" style="color:var(--gold);">открыть контакты →</a>';
      log.appendChild(div);
      scrollLog();
    }, 1400);
  }

  function askNext(){
    if (state.step >= STEPS.length){ computeAndReply(); return; }
    botSay(STEPS[state.step].ask, state.step === 0 ? 300 : 550);
  }

  function handleAnswer(text){
    const key = STEPS[state.step].key;
    if (key === 'goal') state.data.goal = parseGoal(text);
    else if (key === 'weight') state.data.weight = extractNumber(text) || 75;
    else if (key === 'height') state.data.height = extractNumber(text) || 175;
    else if (key === 'age') state.data.age = extractNumber(text) || 30;
    else if (key === 'sex') state.data.sex = parseSex(text);
    else if (key === 'activity') state.data.activity = parseActivity(text);
    else if (key === 'budget') state.data.budget = parseBudget(text);
    state.step++;
    askNext();
  }

  launcher.addEventListener('click', ()=>{
    panel.classList.toggle('is-open');
    opened = true;
    if (log.children.length === 0) askNext();
  });
  closeBtn.addEventListener('click', ()=> panel.classList.remove('is-open'));

  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    const val = input.value.trim();
    if (!val) return;
    addMsg(val, 'user');
    input.value = '';
    handleAnswer(val);
  });
})();
/* ═══ ai widget конец ═══ */
'''

if '/* ═══ ai widget начало ═══ */' not in html:
    html = html.replace('let LANG = ', AI_JS + 'let LANG = ')

open('/root/shelest/index.html', 'w', encoding='utf-8').write(html)
print('готово: пресса + ИИ-консультант (чат) встроены')
