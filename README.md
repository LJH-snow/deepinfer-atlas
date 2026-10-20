# deepinfer-atlas

**DeepInfer 非官方可视化源码导读。**

[English](README.en.md) · [阅读站点](https://ljh-snow.github.io/deepinfer-atlas/index.html) · [源码阅读地图](https://ljh-snow.github.io/deepinfer-atlas/source-map.html) · [版本与证据](docs/evidence.md)

用约 10 分钟，建立从 `LLM.generate()` 到设备执行的源码地图。先看模块和请求流，再定位异步调度、DSpark 与开源边界；每个重要结论都能回到固定 commit 的源码或官方文档。

![deepinfer-atlas 阅读站点预览](site/assets/overview.png)

这是一个独立的社区导读项目，与 DeepSeek 无隶属关系。**[在线阅读](https://ljh-snow.github.io/deepinfer-atlas/) · [GitHub 仓库](https://github.com/LJH-snow/deepinfer-atlas)**。网站已通过 GitHub Pages 发布；也可下载仓库直接打开 `site/index.html`，或按下文启动本地服务。

## 从你的问题开始

| 想回答的问题 | 阅读入口 |
| --- | --- |
| DeepInfer 解决什么问题？模块怎样协作？ | [架构总览](https://ljh-snow.github.io/deepinfer-atlas/architecture.html) / [交互图](https://ljh-snow.github.io/deepinfer-atlas/diagrams/architecture.html) |
| 一次离线请求如何执行？ | [请求时序](https://ljh-snow.github.io/deepinfer-atlas/request.html) / [交互图](https://ljh-snow.github.io/deepinfer-atlas/diagrams/request.html) |
| 开源了什么，完整线上服务还缺什么？ | [开源边界](https://ljh-snow.github.io/deepinfer-atlas/scope.html) / [交互图](https://ljh-snow.github.io/deepinfer-atlas/diagrams/scope.html) |
| CPU / 设备异步、DSpark 怎样减少浪费？ | [性能优化](https://ljh-snow.github.io/deepinfer-atlas/performance.html) |
| 下一步从哪些文件、符号开始研究？ | [源码地图](https://ljh-snow.github.io/deepinfer-atlas/source-map.html) |
| 图里的箭头和结论是否可信？ | [版本与证据页](https://ljh-snow.github.io/deepinfer-atlas/evidence.html) / [机器可读证据](data/evidence.json) |

建议按“架构 2 分钟 → 请求 3 分钟 → 边界 2 分钟 → 优化 3 分钟”阅读。正文为中文，关键代码名保留英文；英文 README 可独立说明本项目价值与使用方式。

## 这份图谱怎样保证可核查

- 分析上游：[deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer)。
- 固定 commit：[`774ce244b87cc0eb8d4b94ab9f5de2ab22049f01`](https://github.com/deepseek-ai/DeepInfer/tree/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01)。
- 核对日期：**2026-10-20**（Asia/Shanghai）。这不是对后续版本的承诺。
- 46 条证据覆盖 24 个文件，记录符号、行号、内容摘要和固定版本链接。图的全部 **23 个节点、19 条关系**另有[逐项映射](data/diagram-map.json)。
- 区分“源码确认”“官方文档描述”“解释性简化”。逻辑阶段图不冒充默认 ZOS 的墙钟 trace；模拟验证预算不冒充性能测试。
- **设备 KV cache / 块管理已经存在；完整生产缓存存储、长期复用与跨 DP 请求负载均衡属于不同层次。** 不因存在缓存张量或扩展钩子就宣称完整服务已开源。

本项目做了静态源码核对、站点和图形验证，**没有运行 DeepInfer 模型，没有复测 GPU / NPU 性能**。详细结果与限制见[验证记录](docs/verification.md)。

## 本地阅读与构建

已有 `site/` 可直接打开，阅读不需要 GPU、NPU、Node.js、前端依赖或后台服务。

用 Python 3.10+ 标准库重新构建并预览：

```sh
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

打开 <http://127.0.0.1:4173/>。构建会生成八个中文页面，并把可部署内容复制到 `dist/`。相对资源路径支持域名根目录和项目子路径。

静态资源、图映射及交付摘要检查：

```sh
python3 scripts/verify.py
```

取得固定上游源码后核对全部证据片段：

```sh
python3 scripts/fetch_upstream.py
python3 scripts/verify.py --require-upstream
```

上游 checkout 保存在 `.upstream/DeepInfer/`，已被 Git 忽略。脚本只取固定 SHA，不会将已有 checkout 自动重置到新版本。

## 图形与维护

三张交互图均由 **Archify 2.16** 从 JSON 规格生成。独立 HTML 自带浅色/深色、缩放、搜索、节点检查、关系追踪和静态格式导出。默认无动效，WebM 不属于本次交付。导出与移动端的实际验证范围见[验证记录](docs/verification.md)。

| 源文件 | 作用 |
| --- | --- |
| `content/`、`templates/`、`site/assets/style.css` | 文章、公共页面结构与样式 |
| `diagrams/specs/` | 三张图的可编辑规格 |
| `diagrams/receipts/` | 9/9 showcase、原子交付与自动视觉检查收据 |
| `data/upstream.json`、`data/evidence.json` | 固定基线、证据与片段摘要 |
| `data/diagram-map.json` | 每个核心图节点/连线的证据 ID |
| `site/` | 预构建阅读站点和独立交互图 |
| `scripts/` | 构建、静态验证、上游获取与图形生成 |

更新拓扑需要安装相同版本 Archify（包未随仓库分发），然后运行：

```sh
ARCHIFY_HOME=/path/to/archify python3 scripts/diagrams.py
```

该命令按顺序运行 `validate → deliver → visual-check`，任一失败立即停止。**自动检查通过后仍需实际查看图形，并从最终 HTML 重新导出 PNG。** 完整流程见[维护说明](docs/maintenance.md)，图形摘要见[交付清单](docs/diagrams.md)。

## 部署与发布状态

`site/` 和 `dist/` 都可由静态托管平台提供。本仓库已启用 GitHub Pages；[部署工作流](.github/workflows/pages.yml) 基于官方静态站点模板，推送 `main` 后自动部署 `site/`，也可手动运行。

已于 **2026-10-21** 按所有者授权创建并推送至公开仓库 [LJH-snow/deepinfer-atlas](https://github.com/LJH-snow/deepinfer-atlas)，完成 Pages 部署并检查线上资源。没有覆盖已有同名仓库。在线入口为 [https://ljh-snow.github.io/deepinfer-atlas/](https://ljh-snow.github.io/deepinfer-atlas/)；原始推理源码分析版本保持不变。

[仓库简介、双语一句话、发布文案与技术文章选题](docs/release.md)已准备好。

## 归属与许可

上游 DeepInfer 采用 [Apache-2.0](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/LICENSE)。本项目原创文档、站点与图规格采用 [MIT](LICENSE)，不改变上游许可。生成的 Archify 查看器运行时保留其 MIT 归属，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。DeepSeek、DeepInfer 及相关名称归各自权利人。
