async (page) => {
  const records = [];
  for (const slug of ['architecture','request','scope']) {
    await page.setViewportSize({width:1440,height:900});
    await page.goto(`http://127.0.0.1:4173/diagrams/${slug}.html`);
    const theme = page.getByRole('button',{name:'切换颜色主题',exact:true});
    if ((await theme.innerText()).includes('深色')) await theme.click();
    await page.getByRole('button',{name:/重置图表视图/}).click();
    const artifactSha = await page.evaluate(async () => {
      const bytes = await (await fetch(location.href)).arrayBuffer();
      const hash = await crypto.subtle.digest('SHA-256',bytes);
      return Array.from(new Uint8Array(hash),value=>value.toString(16).padStart(2,'0')).join('');
    });
    const formats = slug==='architecture' ? [['PNG 无损图像','png'],['SVG 可编辑矢量图','svg'],['JPEG 紧凑图像','jpg'],['WebP 现代图像格式','webp']] : [['PNG 无损图像','png'],['SVG 可编辑矢量图','svg']];
    for (const [label,extension] of formats) {
      await page.getByRole('button',{name:'导出图表',exact:true}).click();
      const pending = page.waitForEvent('download');
      await page.getByRole('menuitem',{name:label,exact:true}).click();
      const download = await pending;
      const destination = extension==='png' || extension==='svg' ? `site/assets/${slug}.${extension}` : `output/playwright/${slug}.${extension}`;
      await download.saveAs(destination);
      const failure = await download.failure();
      if (failure) throw new Error(`${slug}/${extension}: ${failure}`);
      records.push({diagram:slug,format:extension,path:destination,artifactSha,suggestedName:download.suggestedFilename()});
    }
  }
  return {ok:true,records};
}
