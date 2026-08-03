const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  await page.goto('file://' + path.resolve(__dirname, 'index.html'));
  await page.waitForTimeout(300);
  const h = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h; y += 700) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(100);
  }
  await page.evaluate(() => document.getElementById('baMore') && document.getElementById('baMore').click());
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'shot_v3_full.png', fullPage: true });
  await browser.close();
})();
