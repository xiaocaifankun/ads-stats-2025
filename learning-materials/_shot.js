const { chromium } = require('C:\\Users\\yangjh\\.workbuddy\\binaries\\node\\versions\\22.22.2-2\\node_modules\\agent-browser\\node_modules\\playwright-core');

(async () => {
  const target = 'file:///C:/Users/yangjh/Desktop/repos/ads-stats-2025/learning-materials/agent-memory.html';
  const exe = 'C:\\Users\\yangjh\\.agent-browser\\browsers\\chrome-153.0.8010.36\\chrome-win64\\chrome.exe';
  const browser = await chromium.launch({ executablePath: exe });
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 1 });
  await page.goto(target, { waitUntil: 'load' });
  await page.waitForTimeout(600);

  const out = 'C:/Users/yangjh/Desktop/repos/ads-stats-2025/learning-materials/_check';
  await page.screenshot({ path: out + '_full.png', fullPage: true });

  // 单独给三张图截图，便于细看
  const vizzes = await page.$$('.viz');
  for (let i = 0; i < vizzes.length; i++) {
    await vizzes[i].screenshot({ path: out + '_viz' + (i + 1) + '.png' });
  }

  // 结构探测
  const info = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll('*').forEach(el => {
      if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflowX === 'visible') {
        if (el.clientWidth > 0) bad.push(el.tagName + '.' + el.className + ' sw=' + el.scrollWidth + ' cw=' + el.clientWidth);
      }
    });
    return {
      title: document.title,
      sections: document.querySelectorAll('section').length,
      height: document.body.scrollHeight,
      overflowIssues: bad.slice(0, 8),
      vizCount: document.querySelectorAll('.viz').length,
      captionCount: document.querySelectorAll('.viz-caption').length,
      brokenAnchors: [...document.querySelectorAll('a')].filter(a => !a.href).length,
    };
  });
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
