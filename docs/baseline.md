# 上游分析基线

- 仓库：https://github.com/deepseek-ai/DeepInfer.git
- Commit：`774ce244b87cc0eb8d4b94ab9f5de2ab22049f01`
- Commit 时间：2026-10-20T19:03:13+08:00
- 核对日期：2026-10-20（Asia/Shanghai）
- 上游获取：本地独立、忽略的 `.upstream/DeepInfer/` checkout；分析时 `git rev-parse HEAD` 与 SHA 一致。
- 分析范围：离线示例、LLM.generate / LLMEngine、C++ Scheduler / BlockManager、Worker / ModelRunner、模型/采样主路径、设备 KV/state 布局、异步调度、DSpark 预算/置信度/验证及官方文档发布范围。
- 证据：46 条记录，24 个文件；文件与片段 SHA-256 见 `data/evidence.json`。

本次以实际源码重新核对，没有使用未经本次复核的其他会话结论。主路径调用与所有图节点/连线有显式映射。静态分析不等同于覆盖所有配置、抢占、错误、并行或后端组合。

## 尚未执行

没有运行模型推理、编译 DeepInfer 扩展、使用支持的 SM100 / Ascend 950 运行基准，也没有部署实际推理服务。所有性能讨论为机制说明，没有本项目实测数据。

## 尚未公开的生产细节

官方 README / Q&A 说明完整缓存服务与跨 DP 负载均衡不在本次发布范围。未公开的协议、长期持久化布局或生产服务拓扑不以猜测补全。设备 CacheEngine、BlockManager 和缓存保存钩子不是这些组件已经交付的证据。

## 工具限制

本环境没有可调用 codebase-memory-mcp 或 Context7 MCP，已先检查可用工具和资源。源码发现改用本地检索及函数/调用点逐项核对；工具使用与 GitHub Pages 准备采用技能本身的 CLI 帮助或官方源文件。项目站点避免引入前端库，以减少不必要的文档及依赖漂移。
