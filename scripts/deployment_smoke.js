async (page) => {
  const failures = [];
  const subpath = [];
  for (const slug of ['index','architecture','request','scope','performance','source-map','evidence','about']) {
    await page.goto(`http://127.0.0.1:4174/site/${slug}.html`);
    const result = await page.evaluate(() => ({
      pathname:location.pathname,
      styled:getComputedStyle(document.body).backgroundColor==='rgb(248, 249, 252)',
      missingImages:Array.from(document.images).filter(image=>!image.complete||!image.naturalWidth).map(image=>image.src),
    }));
    subpath.push({page:slug,...result});
    if (!result.styled||result.missingImages.length) failures.push({subpath:result});
  }
  await page.goto('http://127.0.0.1:4174/site/index.html');
  await page.getByRole('link',{name:/^开始阅读/}).click();
  if (new URL(page.url()).pathname!=='/site/architecture.html') failures.push({navigation:page.url()});
  const blockedFonts = [];
  const abortFont = route => {blockedFonts.push(route.request().url());return route.abort();};
  await page.route('https://fonts.googleapis.com/**',abortFont);
  await page.route('https://fonts.gstatic.com/**',abortFont);
  await page.setViewportSize({width:1440,height:900});
  await page.goto('http://127.0.0.1:4173/diagrams/architecture.html?theme=light');
  await page.evaluate(()=>document.fonts.ready);
  const nodes = await page.getByRole('button',{name:/^聚焦/}).count();
  await page.getByRole('button',{name:'放大',exact:true}).click();
  await page.screenshot({path:'output/playwright/font-fallback.png'});
  if (nodes!==9) failures.push({fontFallbackNodes:nodes});
  await page.unroute('https://fonts.googleapis.com/**',abortFont);
  await page.unroute('https://fonts.gstatic.com/**',abortFont);
  return {ok:failures.length===0,subpath,subpathNavigation:true,fontFallback:{blockedFonts,nodeCount:nodes,zoomClicked:true},failures};
}
