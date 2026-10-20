async (page) => {
  const records = [];
  const failures = [];
  for (const [slug,query,id] of [['architecture','BlockManager','blocks'],['request','Model / Sampler','executor'],['scope','完整在线服务','missing-service']]) {
    await page.setViewportSize({width:390,height:844});
    await page.goto(`http://127.0.0.1:4173/diagrams/${slug}.html?theme=light`);
    await page.getByRole('button',{name:/重置图表视图/}).click();
    await page.getByRole('button',{name:'查找节点',exact:true}).click();
    await page.getByRole('searchbox',{name:'搜索图表节点',exact:true}).fill(query);
    const dialog = page.getByRole('dialog');
    const result = dialog.getByRole('button',{name:/^聚焦/});
    const count = await result.count();
    if (count!==1) throw new Error(`${slug}: expected one search result, got ${count}`);
    await result.click();
    await page.waitForFunction(() => {
      const element = document.querySelector('[data-node-id][aria-pressed="true"]');
      if (!element) return false;
      const box = element.getBoundingClientRect();
      return box.x + box.width/2 > 0 && box.x + box.width/2 < innerWidth;
    }, null, {timeout:3000});
    const selected = page.getByRole('button',{name:/^聚焦/,pressed:true});
    const box = await selected.boundingBox();
    const name = await selected.getAttribute('aria-label');
    const hash = new URL(page.url()).hash;
    const dimensions = await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
    const isReachable = box !== null && box.x+box.width/2>0 && box.x+box.width/2<390;
    if (hash!==`#focus=${id}` || !isReachable || dimensions.scrollWidth>390) failures.push({diagram:slug,hash,box,dimensions});
    await page.screenshot({path:`output/playwright/search-${slug}-390.png`,fullPage:true});
    await page.getByRole('button',{name:'关闭语义护照',exact:true}).click();
    const closed = (await page.getByRole('button',{name:'关闭语义护照',exact:true}).count())===0;
    if (!closed) failures.push({diagram:slug,passport:'did not close'});
    records.push({diagram:slug,query,hash,selectedName:name,selectedCenterVisible:isReachable,passportClosed:closed,...dimensions});
  }
  return {ok:failures.length===0,records,failures};
}
