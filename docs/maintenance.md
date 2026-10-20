# 本地构建、更新与重新生成

阅读与构建不要求推理硬件。`site/` 为已提交的成品；`content/`、`templates/` 与 `site/assets/style.css` 是站点源文件。默认八个阅读页无 JavaScript 依赖，交互图各自带 Archify 运行时。

## 构建与预览

```sh
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

需要 Python 3.10+；访问 http://127.0.0.1:4173/。`site/` 可直接打开，HTTP 预览便于检查下载与部署行为。`dist/` 是可重新生成的托管目录，已 Git 忽略。构建不访问网络，不下载字体、脚本或图片；图片均本地提供。阅读页使用系统字体。Archify 生成查看器自带可选 Google Fonts 请求，阻断该请求时系统字体回退已检查；不把它描述为绝对无网络请求。

## 固定上游与证据检查

```sh
python3 scripts/fetch_upstream.py
python3 scripts/verify.py --require-upstream
```

fetch 脚本只获取 `data/upstream.json` 中的 SHA。已存在 checkout 若版本不同或包含修改会拒绝覆盖。证据检查核对全部记录的行号、锚点、关键调用、文件摘要和片段摘要，并核对图节点/关系与证据的完备映射。

`verify.py` 无本地上游时仍能检查站点和图形收据，但会清楚报告跳过了源码片段核对；正式维护请用 `--require-upstream`。

## 修改内容

1. 编辑 `content/*.html`；公共结构编辑 `templates/base.html`；样式编辑 `site/assets/style.css`。
2. `{{src:E02}}` 这种源链接标记由 `scripts/build.py` 从证据 JSON 生成，禁止手工把引用改成上游浮动分支。
3. 新增结论时更新 `data/evidence.json`，写清符号、起止行、anchor、checks、file_sha256、excerpt_sha256；引用类型限定为 `source` 或 `official-doc`。解释性简化在正文明确写出。
4. 更新基线中的 evidence_count / source_files、双语 README 的数量，以及 `docs/evidence.md` 的发布清单。
5. 执行构建和验证；实际查看桌面与移动端。内容改变可能影响长链接、标题换行和阅读宽度。

## 更新分析版本

不要只替换 SHA。先保留旧基线，在独立 checkout 分析目标版本，再逐条重审：入口、配置默认值、调度策略、同步边界、采样、缓存、开源范围和硬件条件。对每个证据重新计算范围和摘要，之后再修改基线及正文。官方 Q&A 的线上性能数据与开源示例的条件不可混用。

SHA-256 计算示例使用 Python 标准库：文件摘要为原始 bytes；片段摘要为 `"\n".join(lines[start-1:end]).encode()`。更新脚本不能把旧文案的语义核对替换成摘要更新。

## 图规格和 Archify 版本

- 工具：Archify skill **2.16**（MIT；规格 schema_version 1）。工具包不在仓库中，站点使用者无需安装。
- 规格：`diagrams/specs/architecture.json`、`request.json`、`scope.json`。
- 输出：`site/diagrams/*.html`，保持自包含；不要直接修改已验收 HTML。
- 证据：`data/diagram-map.json`；主图最多 9 个模块节点。
- 主题：zh-CN、classic、无动效、showcase。

安装相同版本的 Archify skill 后设置其包路径：

```sh
ARCHIFY_HOME=/path/to/archify python3 scripts/diagrams.py
```

默认也查找用户 `.agents/skills/archify` 或 `.codex/skills/archify`。需要 Node.js 18+；视觉检查还需要 Chrome/Chromium。工具命令是：

```sh
node "$ARCHIFY_HOME/bin/archify.mjs" validate architecture diagrams/specs/architecture.json --quality showcase --json
node "$ARCHIFY_HOME/bin/archify.mjs" deliver architecture diagrams/specs/architecture.json site/diagrams/architecture.html --quality showcase --json
node "$ARCHIFY_HOME/bin/archify.mjs" visual-check site/diagrams/architecture.html --json
```

request 的类型是 `sequence`；scope 是 `architecture`。任何非零退出均不算通过；依赖步骤立即停止，避免检查旧 HTML。必须包含 9 项 artifact 检查、0 composition errors / warnings。最终收据冻结规格与 HTML 的 SHA-256。

## 视觉检查与预览导出

1. 自动截图之后实际查看 1440×900、1600×1000、1920×1080、2048×1320，并看最小/最大尺寸的浅色和深色图。
2. 确认桌面没有横向或纵向溢出，文字/标签/线条无重叠，最大屏幕没有不合理的空白底带。禁止以隐藏溢出或缩小字号伪造通过。
3. 另外检查 390×844 和 320×740；移动端允许纵向阅读，完整标签可用放大与搜索查看。
4. 在最终 HTML 中点“导出 → PNG”保存整图预览，覆盖 `site/assets/architecture.png`、`request.png`、`scope.png`。同时检查 SVG；图片要清晰、无查看器面板或焦点状态残留。
5. HTML 里的 img 宽高比要与真实 PNG 一致；构建并运行验证。需要改尺寸时修改 `content/` 的声明，不能用 CSS 拉伸。
6. 首页浏览器截图为 `site/assets/overview.png`，用于双语 README 和发布材料；截图需来自真实构建页面。

自动 visual-check 收据仍保持 `visualReview: pending` 是工具的诚实约定。人工完成后把实际检查结果写入 `docs/diagrams.md` / `docs/verification.md`，不要篡改工具自动收据。

## 发布

`site/` 或 `dist/` 可上传到任意静态托管平台。所有路径相对引用，已准备 GitHub Pages 子路径部署。`.github/workflows/pages.yml` 参考 2026-10-20 获取的官方 `actions/starter-workflows` 静态模板，目标是 `site/`。

本项目已于2026-10-21按所有者追加授权发布到https://github.com/LJH-snow/deepinfer-atlas，在线地址为https://ljh-snow.github.io/deepinfer-atlas/，Pages采用GitHub Actions。后续更新提交后推送main即可触发部署；必须检查实际工作流和线上资源，不能仅凭工作流文件宣称发布成功。Fork到其他账号时，更新双语README地址并在Settings → Pages选择GitHub Actions。

## 可重复的浏览器检查

仓库保存了普通 Playwright CLI 的 `run-code` 脚本（不依赖测试 runner）：

- `scripts/browser_audit.js`：八页 × 三种尺寸、skip link、页内导航、主题/缩放及移动端容纳。
- `scripts/interaction_smoke.js`：390px 三图的节点搜索、焦点 URL、信息面板关闭。检查会等待查看器的平滑定位完成，再测元素是否进入视口。
- `scripts/deployment_smoke.js`：`/site/` 子路径及 Google Fonts 阻断回退；需要另开 `python3 -m http.server 4174 --bind 127.0.0.1 --directory .`。
- `scripts/export_previews.js`：三图 PNG/SVG 及架构 JPEG/WebP 真正下载，返回源 HTML 摘要。

示例（已安装 `@playwright/cli` 的环境）：

```sh
playwright-cli -s=atlas open http://127.0.0.1:4173/
playwright-cli -s=atlas run-code --filename scripts/browser_audit.js
```

使用 CLI 的 `### Result` JSON 保存验证报告；不要将仅打印的执行代码视为通过。导出脚本结果保存为 `output/exports.json` 后，运行 `python3 scripts/record_previews.py`，绑定 PNG/SVG 摘要并更新文章图像宽高比。Python 脚本只整理真正导出的文件，不自行伪造导出结果。

生成SVG保留导出器原始字节及摘要；其CSS自带少量行尾空白，`.gitattributes`仅对三份生成SVG关闭空白风格检查。不要为格式化这些产物而破坏预览来源绑定。
