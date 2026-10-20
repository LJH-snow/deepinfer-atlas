# 发布材料

## 仓库简介

An unofficial visual source guide to DeepSeek DeepInfer: architecture, request flow, DSpark, async scheduling, and release boundaries.

## 中文一句话

DeepInfer 非官方可视化源码导读，用约 10 分钟建立从 `LLM.generate()` 到设备执行的源码地图。

## English tagline

An unofficial visual guide to DeepInfer, from `LLM.generate()` to device execution in about ten minutes.

## 主预览图

`site/assets/overview.png`：从真实首页截图生成，适合 README 与项目介绍。

`site/assets/architecture.png`：与固定 JSON 规格和交付 HTML 对应的清晰整图，适合技术分享。

## 简短中文发布文案

我整理了 deepinfer-atlas：一份 DeepInfer 非官方可视化源码导读。

先用三张交互图看清模块协作、一次离线请求的生成循环，以及开源引擎与完整线上服务的边界；再沿源码地图进入 CPU / 设备异步调度、DSpark 置信度与验证预算。

所有关键结论固定到 `774ce244b87cc0eb8d4b94ab9f5de2ab22049f01`，附文件、符号和行号；明确区分源码确认、官方描述和解释性简化。尤其把设备 KV cache 与生产级长期缓存存储、跨 DP 负载均衡分开说明。

站点轻量、无后台，提供双语 README、可重新生成的图规格和验证记录。没有运行模型或复测官方性能数据。项目独立整理，与 DeepSeek 无隶属关系。

发布时在此文案后加入已经核验的真实仓库与在线站点地址。

## Short English launch copy

Meet deepinfer-atlas, an unofficial visual source guide to DeepInfer. Three interactive diagrams cover architecture, the offline generation loop, and the release boundary. Deeper reading routes explain CPU/device overlap and DSpark verification scheduling, with immutable source links and explicit simplification notes.

The guide is pinned to commit `774ce244b87cc0eb8d4b94ab9f5de2ab22049f01`, checked on October 20, 2026. It distinguishes device KV caches from a complete production cache service and DP request routing. No model benchmarks were reproduced. This is an independent community guide, not an official DeepSeek project.

## 三个可以延伸的技术文章

1. **默认异步 decode 中，`step()` 到底返回了哪一轮结果？** 从 Worker.prev_step_state、采样 event、元数据修正和最后的 flush 解释 CPU / 设备的跨步协作。
2. **DSpark 怎样把固定长度候选变成变长验证预算？** 从 ConfidenceHead、process_MTPInfo 到 MTPVarlen 和 GPU 分配内核，区分预测、预算、验证和实际接受 token。
3. **为什么 DeepInfer 有 KV cache，官方却说完整服务还缺缓存系统？** 用设备张量、块管理、缓存扩展点、长期复用和跨 DP 负载均衡划清引擎与服务的边界。

## 发布状态

当前为本地可审阅、可部署版本。没有创建公开远程仓库、没有推送、没有部署公网 Pages。缺少本会话对公开发布的明确授权；凭据是否可用未作为完成本地工作的前提，也没有借此提前停止。授权后仍需检查同名仓库和真实 Pages 结果。
