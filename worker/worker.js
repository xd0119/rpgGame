/**
 * 暴雨孤岛 - 评分 Worker
 * Cloudflare Workers + KV
 *
 * 绑定 KV namespace 名为 RATING_KV
 * key: "rating" → value: {"sum":74,"count":8}
 *
 * GET  → 返回 {sum, count, avg}
 * POST → body: {"score":8} → 更新 sum/count → 返回新的 {sum, count, avg}
 */

// 简单 CORS 头
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};

export default {
  async fetch(request, env) {
    // 处理预检
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS });
    }

    try {
      // 读当前值
      const raw = await env.RATING_KV.get('rating');
      let data = raw ? JSON.parse(raw) : { sum: 74, count: 8 };

      if (request.method === 'POST') {
        const body = await request.json();
        const score = Number(body.score);
        if (score < 1 || score > 10 || isNaN(score)) {
          return new Response(JSON.stringify({ error: 'score must be 1-10' }), {
            status: 400, headers: { ...CORS, 'Content-Type': 'application/json' }
          });
        }
        data.sum += score;
        data.count += 1;
        await env.RATING_KV.put('rating', JSON.stringify(data));
      }

      const avg = (data.sum / data.count).toFixed(1);
      return new Response(JSON.stringify({ sum: data.sum, count: data.count, avg: parseFloat(avg) }), {
        headers: { ...CORS, 'Content-Type': 'application/json' }
      });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500, headers: { ...CORS, 'Content-Type': 'application/json' }
      });
    }
  }
};
