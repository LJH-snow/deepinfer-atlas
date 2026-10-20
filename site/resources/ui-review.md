# 页面质量审阅

使用技能：design-taste-frontend、web-design-guidelines；阅读站点为中文技术编辑式页面，不是营销图片页。

指南来源：2026-10-21再次抓取 `vercel-labs/web-interface-guidelines` 的 `main/command.md`。内容 SHA-256：`d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234`。

## 已修复的可操作发现

- `site/assets/style.css`：移动文章栏被代码/表格的intrinsic width撑大；显式width:100%，保留内部代码块滚动。
- `site/assets/style.css`：证据h3的长函数符号造成窄屏横向溢出；overflow-wrap:anywhere，保留完整标识符与正常字号。
- `content/index.html`：首页简介末尾孤字换行；缩短为清晰的一句说明。
- `content/architecture.html`与图规格：默认“数据库”含义容易与完整缓存服务混淆；架构图例改为“缓存与块管理”，正文明确张量提供者与服务区别。

当前范围内没有尚未处理的站点源代码问题。以下是适用项核查与限制，不代表上游查看器的每项功能均接受了完整可访问性审计。

## 适用前端检查

- 设计判断：面向初读源码的开发者，使用原生CSS、单蓝强调、浅色主题、系统中文/无衬线字体。VARIANCE=5、MOTION=1、DENSITY=4；图形使用Archify自身语义配色。
- 静态页面有lang、description、一个h1、分级标题、semantic nav、main/skip link和明确图注。
- 图像有alt与实际宽高比；首页关键预览高优先加载。核心图是实际输出资产，不是装饰图或假截图。
- 导航用a，折叠目录用原生details/summary，交互有focus-visible和hover，正文链接保留可见下划线。
- 正文和按钮配色实算：白色/蓝色CTA 6.74:1、次要正文/背景 6.04:1、正文/背景 14.95:1、链接/背景 6.41:1；长标识符、SHA和源码路径可换行；移动布局逐区域折叠；不以overflow:hidden掩盖宽度问题。
- 站点无连续动画；CSS尊重prefers-reduced-motion；Archify静态无动效。
- 首页非官方身份、上游commit和来源清晰。版本信息是读者核对技术内容的必要上下文，不套用营销页“版本页脚禁用”规则。
- 阅读页无需状态表单、登录、异步API、React状态或后端，因此这些技能条目不适用。没有引入第三方前端框架依赖；依照用户轻量约束采用原生实现。
- PNG/SVG是真实图表；技术导读不需要无关摄影或生成装饰图片。没有为满足营销模板规则引入无意义素材。

## 检查限制

没有真实设备、全套assistive technology或线上Core Web Vitals数据。站点自身导航和跳转正文键盘路径已实测；查看器的搜索、聚焦、面板关闭、主题、缩放和部分导出已实测。其他高级功能如实列为未逐项验证。
