/* Оплата на сайте: карта/СБП через ЮKassa (сервер — Cloudflare Worker).
   Кнопки: любой элемент с data-plan="m9|m20|m30|m50|start|consult|program|food|labs". */
(function () {
  var API = 'https://shelestfit-bot.trenershelest.workers.dev/pay';

  var css = ''
    + '.paym{position:fixed;inset:0;z-index:1000;display:flex;align-items:center;justify-content:center;background:rgba(8,8,9,.82);backdrop-filter:blur(6px);}'
    + '.paym__c{background:#131315;border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:28px;max-width:420px;width:calc(100% - 40px);}'
    + '.paym__t{font-size:1.15rem;font-weight:600;margin:0 0 6px;color:#f2efe9;}'
    + '.paym__d{color:rgba(242,239,233,.65);font-size:.9rem;margin:0 0 18px;line-height:1.5;}'
    + '.paym input{width:100%;box-sizing:border-box;background:#1b1b1e;border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:13px 14px;color:#f2efe9;font-size:.95rem;margin-bottom:14px;}'
    + '.paym__row{display:flex;gap:10px;flex-wrap:wrap;}'
    + '.paym__err{color:#e08585;font-size:.84rem;margin:-6px 0 10px;display:none;}'
    + '.paym__alt{margin-top:14px;font-size:.85rem;color:rgba(242,239,233,.6);line-height:1.6;display:none;}'
    + '.paym__alt a{color:#d9b45f;}';
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  function openDialog(plan, title, price) {
    var m = document.createElement('div');
    m.className = 'paym';
    m.innerHTML = '<div class="paym__c">'
      + '<p class="paym__t">' + title + '</p>'
      + '<p class="paym__d">' + price + '. Оплата картой или через СБП на защищённой странице ЮKassa. Чек придёт на почту.</p>'
      + '<input type="email" placeholder="Почта для чека" autocomplete="email">'
      + '<p class="paym__err"></p>'
      + '<div class="paym__row">'
      + '<button class="btn btn--gold" type="button" data-go>Перейти к оплате</button>'
      + '<button class="btn btn--ghost" type="button" data-close>Отмена</button>'
      + '</div>'
      + '<p class="paym__alt">Онлайн-оплата подключается. Пока можно написать боту в Telegram: '
      + '<a href="https://t.me/ShelestFitBot" target="_blank" rel="noopener">@ShelestFitBot</a>, '
      + 'на почту <a href="mailto:trenershelest@icloud.com">trenershelest@icloud.com</a> '
      + 'или позвонить: <a href="tel:+79952723614">+7 995 272-36-14</a>.</p>'
      + '</div>';
    document.body.appendChild(m);
    var inp = m.querySelector('input');
    var err = m.querySelector('.paym__err');
    var alt = m.querySelector('.paym__alt');
    var go = m.querySelector('[data-go]');
    m.querySelector('[data-close]').onclick = function () { m.remove(); };
    m.addEventListener('click', function (e) { if (e.target === m) m.remove(); });
    inp.focus();

    go.onclick = function () {
      var email = (inp.value || '').trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        err.textContent = 'Укажите почту, на неё придёт чек. Например: ivan@mail.ru';
        err.style.display = 'block';
        return;
      }
      err.style.display = 'none';
      go.disabled = true;
      go.textContent = 'Секунду...';
      fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: plan, email: email })
      }).then(function (r) { return r.json(); }).then(function (j) {
        if (j && j.url) { location.href = j.url; return; }
        go.style.display = 'none';
        alt.style.display = 'block';
      }).catch(function () {
        go.disabled = false;
        go.textContent = 'Перейти к оплате';
        err.textContent = 'Не получилось связаться с сервером, попробуйте ещё раз.';
        err.style.display = 'block';
      });
    };
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-plan]');
    if (!b) return;
    e.preventDefault();
    openDialog(
      b.getAttribute('data-plan'),
      b.getAttribute('data-pay-title') || 'Оплата',
      b.getAttribute('data-pay-price') || ''
    );
  });
})();
