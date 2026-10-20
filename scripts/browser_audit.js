async (page) => {
  const origin = 'http://127.0.0.1:4173';
  const slugs = ['index','architecture','request','scope','performance','source-map','evidence','about'];
  const sizes = [{width:1440,height:900},{width:390,height:844},{width:320,height:740}];
  const records = [];
  const failures = [];
  const runtimeErrors = [];
  const networkErrors = [];
  page.on('pageerror', error => runtimeErrors.push(String(error)));
  page.on('response', response => { if (response.status() >= 400) networkErrors.push({url:response.url(),status:response.status()}); });
  for (const size of sizes) {
    await page.setViewportSize(size);
    for (const slug of slugs) {
      await page.goto(`${origin}/${slug}.html`);
      await page.evaluate(() => document.fonts.ready);
      const result = await page.evaluate(() => ({
        title: document.title,
        width: innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        missingImages: Array.from(document.images).filter(image => !image.complete || image.naturalWidth === 0).map(image => image.src),
        navigationLinks: document.querySelectorAll('.primary-nav a').length,
        heading: document.querySelector('h1')?.textContent,
      }));
      records.push({page:slug,...size,...result});
      if (result.scrollWidth > size.width || result.missingImages.length || result.navigationLinks !== 6) failures.push({page:slug,...size,result});
      if (slug === 'index' || (size.width === 390 && ['architecture','performance'].includes(slug))) {
        await page.screenshot({path:`output/playwright/${slug}-${size.width}.png`,fullPage:size.width===390});
      }
    }
  }
  await page.setViewportSize({width:1440,height:900});
  await page.goto(`${origin}/index.html`);
  await page.keyboard.press('Tab');
  const skipFocused = await page.evaluate(() => document.activeElement?.classList.contains('skip-link'));
  await page.keyboard.press('Enter');
  const skipWorks = await page.evaluate(() => document.activeElement?.id === 'main');
  if (!skipFocused || !skipWorks) failures.push({keyboardSkipLink:{skipFocused,skipWorks}});
  await page.getByRole('link',{name:/^开始阅读/}).click();
  if (!page.url().endsWith('/architecture.html')) failures.push({primaryNavigation:page.url()});
  await page.getByRole('link',{name:'沿职责理解九个节点',exact:true}).click();
  if (!page.url().endsWith('#modules')) failures.push({tocNavigation:page.url()});
  for (const slug of ['architecture','request','scope']) {
    await page.setViewportSize({width:1440,height:900});
    await page.goto(`${origin}/diagrams/${slug}.html`);
    const theme = page.getByRole('button',{name:'切换颜色主题',exact:true});
    const beforeTheme = await theme.innerText();
    await theme.click();
    const afterTheme = await theme.innerText();
    if (beforeTheme === afterTheme) failures.push({diagram:slug,theme:'did not change'});
    await theme.click();
    const reset = page.getByRole('button',{name:/重置图表视图/});
    const beforeZoom = await reset.innerText();
    await page.getByRole('button',{name:'放大',exact:true}).click();
    const afterZoom = await reset.innerText();
    if (beforeZoom === afterZoom) failures.push({diagram:slug,zoom:'did not change'});
    await reset.click();
    records.push({diagram:slug,themeToggle:true,zoomChanged:true});
    for (const size of sizes.slice(1)) {
      await page.setViewportSize(size);
      const dimensions = await page.evaluate(() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:innerHeight,scrollHeight:document.documentElement.scrollHeight}));
      if (dimensions.scrollWidth > size.width) failures.push({diagram:slug,...size,dimensions});
      records.push({diagram:slug,...size,...dimensions});
      if (size.width===390) await page.screenshot({path:`output/playwright/diagram-${slug}-390.png`,fullPage:true});
    }
  }
  if (runtimeErrors.length || networkErrors.length) failures.push({runtimeErrors,networkErrors});
  const report = {ok:failures.length===0,records,failures,runtimeErrors,networkErrors};
  return report;
}
