# 源码证据清单

基线：`774ce244b87cc0eb8d4b94ab9f5de2ab22049f01`；核对：2026-10-20。

类型：源码确认 / 官方文档描述 / 解释性简化。主图节点与连线完整映射见 `data/diagram-map.json`；图的抽象范围见各页正文。

## E01 · main → LLM.generate

- 类型：源码确认
- 结论：准备模型、输入与采样参数；调用 generate；示例把 token IDs 解码为文本。
- 文件：`examples/offline_inference.py:34-113`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/examples/offline_inference.py#L34-L113)
- 片段 SHA-256：`b0633c95a5ac4e4d6cd0c7ca27a5f036bf3a33fff573611cf58b1ac6661893e0`

## E02 · LLM.generate

- 类型：源码确认
- 结论：逐项 _add_request，然后运行 _run_engine；不是 HTTP 入口。
- 文件：`deepinfer/entrypoints/llm.py:90-142`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/entrypoints/llm.py#L90-L142)
- 片段 SHA-256：`ea9291343845d4b0c4025bd97c6093086411e2ba41eb51e216ef7aca46c89206`

## E03 · LLM._add_request

- 类型：源码确认
- 结论：必要时分词，复制 SamplingParams，传给引擎 add_request。
- 文件：`deepinfer/entrypoints/llm.py:144-166`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/entrypoints/llm.py#L144-L166)
- 片段 SHA-256：`9f4d27ce9ec562e70817c17a178c544f1e49bd9617fce39dc399139ed280275d`

## E04 · LLM._run_engine

- 类型：源码确认
- 结论：循环 step；结束前 flush；clone 池对象并按请求序聚合，可选解码。
- 文件：`deepinfer/entrypoints/llm.py:168-195`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/entrypoints/llm.py#L168-L195)
- 片段 SHA-256：`7b1272d27c9c51793fd1c38ea26015c3ef81d200e155e140a431bfe90f129610`

## E05 · LLMEngine.add_request / _enqueue

- 类型：源码确认
- 结论：把 Sequence 加入 C++ Scheduler；有结构化输出时需等待 matcher 构建。
- 文件：`deepinfer/engine/llm_engine.py:620-633`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L620-L633)
- 片段 SHA-256：`566c0da36922f3dbfdc256c1a0378237fc199d9863fed5f8c18bc4327b492b25`

## E06 · LLMEngine.step

- 类型：源码确认
- 结论：schedule 选出元数据与批次，再下发模型执行。
- 文件：`deepinfer/engine/llm_engine.py:860-960`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L860-L960)
- 片段 SHA-256：`817a0464e349dcc4192b8a8ddcd95f26684438d1794c57d678786b8676daf6aa`

## E07 · LLMEngine._execute_model_async_step / post_process

- 类型：源码确认
- 结论：通过 Worker.execute_model_step 执行；post_process 回调处理输出并反馈 MTP runtime。
- 文件：`deepinfer/engine/llm_engine.py:961-1016`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L961-L1016)
- 片段 SHA-256：`e5afa5c87c3477321ab95de7e1b1d0602b2a60f506e380185714457d2e6e1bd9`

## E08 · Scheduler._schedule

- 类型：源码确认
- 结论：在等待/运行队列、prefill 与 decode 之间组织批次，受块和计算预算约束。
- 文件：`csrc/engine/scheduler.hpp:275-558`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/scheduler.hpp#L275-L558)
- 片段 SHA-256：`5993f0740de902be171451fc04e1160f40f6e20f08dc555bf3e27180b12e356f`

## E09 · Scheduler._schedule_decode

- 类型：源码确认
- 结论：为 decode 追加槽、处理资源不足；MTPVarlen 分配 seqlens_q。
- 文件：`csrc/engine/scheduler.hpp:559-663`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/scheduler.hpp#L559-L663)
- 片段 SHA-256：`fcffd2cff540aed2c6796acef2c3b6267d051358cf7c6fd29558213699fe2801`

## E10 · Scheduler.schedule

- 类型：源码确认
- 结论：构造每条 SequenceMetadata，记录在途长度和本轮 token 预算。
- 文件：`csrc/engine/scheduler.hpp:667-736`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/scheduler.hpp#L667-L736)
- 片段 SHA-256：`9b9d84b8ede5611ee7493f2637903435d4debf50387a1d3bc9d1b8cf4b60ab2a`

## E11 · BlockManager

- 类型：源码确认
- 结论：管理引擎缓存块编号的分配、固定与回收；不是分布式缓存服务。
- 文件：`csrc/engine/block_manager.hpp:119-187`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/block_manager.hpp#L119-L187)
- 片段 SHA-256：`5b5fd0ecefdd50d6422f355f5cd70b307dbfa0f62d0372f9767c26d947cbc312`

## E12 · CacheEngine.do_allocate_kv_cache

- 类型：源码确认
- 结论：分配设备 KV blocks、state blocks，形成 GPUCacheInterface；不能据此推断长期缓存服务已提供。
- 文件：`deepinfer/worker/cache_engine.py:851-973`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/cache_engine.py#L851-L973)
- 片段 SHA-256：`23e244f82fc4a5a9cd0fa45a66e769e6e3c50c7c7d7cc7555cfd4a67074ef906`

## E13 · Worker.execute_model_step

- 类型：源码确认
- 结论：先 launch 当前 forward，后处理上一轮，再采样当前轮；ZOS decode 延后当前后处理。
- 文件：`deepinfer/worker/worker.py:89-189`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/worker.py#L89-L189)
- 片段 SHA-256：`cf90c30dfedbca4799c1ba4ee3fd8e2e85840fa34f5a3ded8aefcda5df97c8fd`

## E14 · Worker._post_process_step / flush_inflight_reqs

- 类型：源码确认
- 结论：等待 sample_end_evt，再运行 ModelRunner 后处理和 Engine 回调；flush 排空在途结果。
- 文件：`deepinfer/worker/worker.py:248-283`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/worker.py#L248-L283)
- 片段 SHA-256：`30fc6349298cec43ed80bb9582acf8cd7373b795e008b67cec3610f2c136c2ba`

## E15 · ModelRunner.execute_main_model

- 类型：源码确认
- 结论：准备输入；CUDA graph replay 或 self.model forward；此方法禁止设备同步。
- 文件：`deepinfer/worker/model_runner.py:308-336`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/model_runner.py#L308-L336)
- 片段 SHA-256：`44445fa1661ea15dc39863a65824087a0d789d1999319d9f76a9973124de91be`

## E16 · ModelRunner.execute_sample

- 类型：源码确认
- 结论：准备 SamplerInputs 后调用 self.model.sample；此方法禁止设备同步。
- 文件：`deepinfer/worker/model_runner.py:337-368`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/model_runner.py#L337-L368)
- 片段 SHA-256：`c1707348cb3a54e98038d0b4c1511a1239e60ff04bb26267ecaa710953400ad7`

## E17 · DeepseekModel.forward

- 类型：源码确认
- 结论：模型执行承载 attention/MoE 等层；启用 DFlash 时更新其主模型缓存。
- 文件：`deepinfer/model_executor/models/deepseek.py:154-225`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/models/deepseek.py#L154-L225)
- 片段 SHA-256：`b61aefa9636247e78cc364453c6836181ee0acbcbcf153c146ea63a2c1b658da`

## E18 · DeepseekForCausalLM.sample

- 类型：源码确认
- 结论：将主模型输出交给 Sampler；EPLB 处理附着为后处理函数。
- 文件：`deepinfer/model_executor/models/deepseek.py:383-411`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/models/deepseek.py#L383-L411)
- 片段 SHA-256：`8e4efc7e6509445d5e6c789a54e6b2a212748b194085e66de1fb42531afd12e7`

## E19 · Sampler.forward decode 分支

- 类型：源码确认
- 结论：先验证上一轮候选，再用确认 token 生成下一轮 draft 与置信度。
- 文件：`deepinfer/model_executor/layers/sampler.py:214-301`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/layers/sampler.py#L214-L301)
- 片段 SHA-256：`f9357100455535b951b90e01434533509d3b590beb79013a2654da1e4a51f4a7`

## E20 · LLMEngine._process_model_outputs

- 类型：源码确认
- 结论：处理 MTP 信息，scheduler.process_outputs 推进状态，再 build_request_outputs。
- 文件：`deepinfer/engine/llm_engine.py:687-763`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L687-L763)
- 片段 SHA-256：`705cf66d2a9b478bfa02e7e590e31642ca8caee65ff221da995521831a5b05b7`

## E21 · Scheduler._check_stop

- 类型：源码确认
- 结论：按 EOS、最大模型长度和 max_tokens 等停止生成；错误/中止另有分支。
- 文件：`csrc/engine/scheduler.hpp:1035-1053`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/scheduler.hpp#L1035-L1053)
- 片段 SHA-256：`f958261f12d4c77e3f0649981449289553b0c3f6e316febdf9bf7de79eec1ea0`

## E22 · EngineArgs.__post_init__

- 类型：源码确认
- 结论：根据 EngineType 注入 ZOS 默认值，且尊重显式环境覆盖。
- 文件：`deepinfer/engine/arg_utils.py:48-61`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/arg_utils.py#L48-L61)
- 片段 SHA-256：`26a71dde3e84c96b6e75abcc9fc680d02cd4077a07dac86172307eaf223cac15`

## E23 · EngineType.default_zero_overhead_scheduling

- 类型：源码确认
- 结论：NORMAL 同时执行 prompt/completion；NORMAL 和 COMPLETION 默认 ZOS。
- 文件：`deepinfer/engine/engine_type.py:4-17`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/engine_type.py#L4-L17)
- 片段 SHA-256：`975e9e67462cb3eb966e16aca828e1793266c7185c6815af9c6440855cfb7821`

## E24 · MTPVarlen.schedule

- 类型：源码确认
- 结论：根据历史接受率、forward 性能曲线和 sampler 时间估计选择总预算；无曲线回退到现有草稿长度。
- 文件：`csrc/engine/mtp_varlen.hpp:150-275`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/mtp_varlen.hpp#L150-L275)
- 片段 SHA-256：`365411e43a845c512dae11f6d6da322c7d862b19096fce0b251a856fda190e2d`

## E25 · ConfidenceHead

- 类型：源码确认
- 结论：预测各 draft 位置的接受概率；置信度是估计，不是验证的替代品。
- 文件：`deepinfer/model_executor/models/mtp/dflash.py:46-81`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/models/mtp/dflash.py#L46-L81)
- 片段 SHA-256：`4922327a864d7b50be2922ec47d42840d5fc565633f52e202691a80f3dceb38c`

## E26 · DFlash.sample_drafts / run_drafts

- 类型：源码确认
- 结论：生成 draft token 与置信度，写回候选状态；DSpark 方案的当前实现入口类名为 DFlash。
- 文件：`deepinfer/model_executor/models/mtp/dflash.py:279-387`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/models/mtp/dflash.py#L279-L387)
- 片段 SHA-256：`6cdf1d8cb2cbd49b3664d97b44bdc534897280fe204a8e0b0df2055889f5db8c`

## E27 · compute_seqlens_q_by_confidence_rates

- 类型：源码确认
- 结论：在设备端将总预算按最新置信度重新分配给请求；融合 remap scatter。
- 文件：`deepinfer/model_executor/layers/tilelang_ops/schedule_mtp_varlen.py:11-33`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/layers/tilelang_ops/schedule_mtp_varlen.py#L11-L33)
- 片段 SHA-256：`854290772a5ddc44b9ace31192292ce18ee9af5d6e2a081692a02e17c640ff41`

## E28 · Worker._correct_seqlens_qk

- 类型：源码确认
- 结论：ZOS 的 CPU 元数据滞后，使用上一轮设备采样结果修正 q/k；变长 q 回传 pinned buffer。
- 文件：`deepinfer/worker/worker.py:191-246`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/worker.py#L191-L246)
- 片段 SHA-256：`5eaa70ddb296d45989d1982fd7cb2d82b5ab377b556b42ef63ae68d93e4a0e0a`

## E29 · WorkerBase.warm_up_model

- 类型：源码确认
- 结论：CUDA graph 启用时捕获图；varlen 开启才采集 decode 性能曲线。
- 文件：`deepinfer/worker/base.py:274-289`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/base.py#L274-L289)
- 片段 SHA-256：`0b2df399cf1d3e9c42afb9e9cdf81e0e5be1686be57fd3784806e2dc37057dc9`

## E30 · UserBuffer 的依赖

- 类型：源码确认
- 结论：通信与矩阵计算缓冲对接 DeepEP / DeepGEMM；仅展示依赖关系。
- 文件：`deepinfer/model_executor/parallel_utils/userbuffer.py:7-24`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/parallel_utils/userbuffer.py#L7-L24)
- 片段 SHA-256：`41c4062dc1306b9c629232997ee631914acfaeb2e375401966ba5e432f317b74`

## E31 · prefill_attn_varlen_sparse / decode_mla_mqa_sparse

- 类型：源码确认
- 结论：attention backend 调用 FlashMLA；后端细节超出主图。
- 文件：`deepinfer/model_executor/layers/attention_backend.py:2-128`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/layers/attention_backend.py#L2-L128)
- 片段 SHA-256：`358a3c6b20686cded07ca9cabff1e248b4acf1d0afe11510d929bc5209433444`

## E32 · bf16_gemm

- 类型：源码确认
- 结论：矩阵乘后端直接调用 DeepGEMM。
- 文件：`deepinfer/model_executor/layers/linear.py:3-36`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/layers/linear.py#L3-L36)
- 片段 SHA-256：`b5d0fd64e3a9666c971e64181952a214db3996aaf01efdbc8c33ffc2d5f5959f`

## E33 · gather / cp_broadcast

- 类型：源码确认
- 结论：rank 间 gather/broadcast 使用 torch.distributed；不是线上请求负载均衡。
- 文件：`deepinfer/model_executor/parallel_utils/communication_op.py:12-47`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/model_executor/parallel_utils/communication_op.py#L12-L47)
- 片段 SHA-256：`e0725c3032f274f11f0c44089f0032ad232f71aeab784e50857d62076940f0a8`

## D01 · 官方支持表

- 类型：官方文档描述
- 结论：该版本支持 DeepSeek-V4.1-Flash、SM100 / Ascend 950，并列出特性与启用条件。
- 文件：`README.md:5-36`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/README.md#L5-L36)
- 片段 SHA-256：`f75bc6dd445c191158a1b987ddf7ff066eb2bfd37da954743b0e2c72d49e58cf`

## D02 · 官方发布范围

- 类型：官方文档描述
- 结论：完整 KV cache system、VE/Prefill/Decode 分离部署、跨 DP 副本负载均衡未包含在发布中。
- 文件：`README.md:38-42`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/README.md#L38-L42)
- 片段 SHA-256：`4c82689c7a992dc21a746ea3faa02c5f579a5113a7dc4bae8e762c18c9c94200`

## E34 · LLMEngine 分阶段与缓存钩子

- 类型：源码确认
- 结论：init_pd_split / do_save_kvcache 等是扩展钩子；存在钩子不等于完整生产集成。
- 文件：`deepinfer/engine/llm_engine.py:801-829`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L801-L829)
- 片段 SHA-256：`37607eb6c4d4128a9bfa61148a336b076263f43199cc575ef2519232d8202807`

## D03 · 生产 KVCache 与基础设施

- 类型：官方文档描述
- 结论：长期上下文复用是官方生产系统目标；缓存管理及负载均衡耦合内部设施，未完全开源。
- 文件：`doc/inference_deployment_qa.md:13-27`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/doc/inference_deployment_qa.md#L13-L27)
- 片段 SHA-256：`395ddaf7b6dab38e7b72f14f242b55770050f3d97b99be497f33ccc6e32ab1e2`

## D04 · 官方 DSpark 描述

- 类型：官方文档描述
- 结论：Confidence Head 与变长验证的设计说明，及其和异步调度的配合。
- 文件：`doc/inference_deployment_qa.md:239-265`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/doc/inference_deployment_qa.md#L239-L265)
- 片段 SHA-256：`2247309e3f06881d56fef54bd9f98020d24cb41b11cab9e05c94818bdfb800ed`

## D05 · 官方异步调度说明

- 类型：官方文档描述
- 结论：调度与后处理是 CPU 工作；目标是重叠执行以减少设备空闲。
- 文件：`doc/inference_deployment_qa.md:266-276`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/doc/inference_deployment_qa.md#L266-L276)
- 片段 SHA-256：`78a533c261f276901f3f23813e3e536ccf5a29aa55a239fe225075e789b2f688`

## E35 · nextn / varlen 配置

- 类型：源码确认
- 结论：最大草稿长度默认 5；ENABLE_MTP_VARLEN 描述器默认 False。
- 文件：`deepinfer/environ.py:129-132`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/environ.py#L129-L132)
- 片段 SHA-256：`4860215f2eb603611f7c23c1d419552cf7930ecb7356e7401774466362f7a608`

## E36 · WorkerBase.run_workers

- 类型：源码确认
- 结论：driver 对 CP group 广播方法，再在本地调用；主图省略 follower 执行与通信。
- 文件：`deepinfer/worker/base.py:290-304`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/base.py#L290-L304)
- 片段 SHA-256：`cf407e955baf933738c8e3d7ecc7cee85f2bd7ef12a24f6dbc271ebdcf93e4fe`

## E37 · LLMEngine 初始化缓存管理与调度器

- 类型：源码确认
- 结论：设备缓存已初始化后建立块/状态槽管理器，注入 decode 性能曲线。
- 文件：`deepinfer/engine/llm_engine.py:265-270`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L265-L270)
- 片段 SHA-256：`a22de26ade86eb28dc2357550d58eb693fa9768478bdd5622e14e2cd72b1a353`

## E38 · ModelRunner.load_model

- 类型：源码确认
- 结论：get_model 得到模型对象，并检查 SWA bounded replay 保留长度覆盖 window + backtracking。
- 文件：`deepinfer/worker/model_runner.py:96-112`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/worker/model_runner.py#L96-L112)
- 片段 SHA-256：`364deb4676beb8a3df6ba45b4cc8627440025abfab44669e77244d9c73892d56`

## E39 · LLMEngine 类说明

- 类型：源码确认
- 结论：当前发布不含 online-serving wrapper，LLM 包装用于离线批量推理。
- 文件：`deepinfer/engine/llm_engine.py:130-142`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/engine/llm_engine.py#L130-L142)
- 片段 SHA-256：`dbc187db8cb18119f3237029ac9d726fb8bca0ab53f6436e6fc49e6941069429`

## E40 · MMProcessor

- 类型：源码确认
- 结论：存在多模态片段处理基础；不意味着视觉编码器分离部署服务已交付。
- 文件：`deepinfer/ve/processor/mm_processor.py:10-30`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/deepinfer/ve/processor/mm_processor.py#L10-L30)
- 片段 SHA-256：`b0c9df6907ed9c8c1dba1e2d2bccb882c90275e8ccbf82c953d17f3ed7a95c28`

## E41 · process_MTPInfo

- 类型：源码确认
- 结论：对各位置置信度做累乘，移位保存历史预测接受率；不是直接把真实接受率当预测值。
- 文件：`csrc/engine/scheduler.hpp:1196-1271`
- [固定 commit 源码](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/csrc/engine/scheduler.hpp#L1196-L1271)
- 片段 SHA-256：`7cdb1d578f0378608ee1b4ba20221172d8ff9a53c21d7d506e4f4e1a34aa4cb4`
