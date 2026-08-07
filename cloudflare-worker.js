/**
 * ИИ-консультант для shelestfit.com — Cloudflare Worker.
 *
 * Что делает: принимает сообщения чата с сайта и проксирует их в Anthropic API.
 * Ключ API хранится ТОЛЬКО в секретах Cloudflare (Settings → Variables → Secrets,
 * имя: ANTHROPIC_API_KEY) — в коде его нет и в браузер он не попадает.
 *
 * Деплой: dash.cloudflare.com → Workers & Pages → Create Worker →
 * вставить этот код → Deploy → добавить секрет ANTHROPIC_API_KEY.
 */

const ALLOWED_ORIGINS = [
  'https://shelestfit.com',
  'https://www.shelestfit.com',
  'https://papakult.github.io',
];

const SYSTEM_PROMPT = `Ты — ИИ-консультант на сайте персонального тренера Андрея Шелеста (shelestfit.com).
Андрей — чемпион мира по пауэрлифтингу с биологическим образованием, ведёт клиентов только онлайн.

Твоя роль:
- Отвечаешь на вопросы о тренировках, питании, спортивных добавках, восстановлении — доброжелательно, коротко и по делу, на языке собеседника (русский или английский).
- Можешь дать общие ориентиры по калориям/белку и по выбору добавок с доказанной эффективностью (креатин, кофеин, белок и т.п.), ссылаясь на энциклопедии сайта: /sport-nutrition.html, /dietology.html, /microbiome.html.
- Ты НЕ ставишь диагнозы, не назначаешь лечение и не заменяешь врача. При вопросах о болезнях, травмах, лекарствах — советуешь очную консультацию врача.
- Не обещаешь конкретных результатов ("минус N кг за месяц").
- Если человеку нужна персональная программа, план питания или разбор анализов — предлагаешь написать Андрею напрямую: бот @ShelestFitBot в Telegram, Telegram-чат или email trenershelest@icloud.com (все ссылки — в разделе «Контакты» на главной странице). Тарифы — в разделе «Тарифы» на главной странице.
- Отвечай кратко: 2–6 предложений, без markdown-заголовков.`;

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders(origin) });
    }
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405, headers: corsHeaders(origin) });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) } });
    }

    // messages: [{role:'user'|'assistant', content:'...'}, ...] — история чата с фронтенда
    const messages = Array.isArray(body.messages) ? body.messages.slice(-20) : null;
    if (!messages || !messages.length) {
      return new Response(JSON.stringify({ error: 'no messages' }), { status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) } });
    }

    // простая защита: ограничение длины
    for (const m of messages) {
      if (typeof m.content !== 'string' || m.content.length > 4000) {
        return new Response(JSON.stringify({ error: 'message too long' }), { status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) } });
      }
    }

    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5',
        max_tokens: 600,
        system: SYSTEM_PROMPT,
        messages: messages.map(m => ({
          role: m.role === 'assistant' ? 'assistant' : 'user',
          content: m.content,
        })),
      }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      console.log('anthropic error', resp.status, errText);
      return new Response(JSON.stringify({ error: 'upstream', status: resp.status }), { status: 502, headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) } });
    }

    const data = await resp.json();
    const text = (data.content && data.content[0] && data.content[0].text) || '';
    return new Response(JSON.stringify({ reply: text }), {
      headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
    });
  },
};
