# 核心图交付记录

工具：Archify skill 2.16，生成器标识 `archify 2.16.0-dev.0`；schema_version 1；locale zh-CN；classic；静态模式；质量 showcase。

三张最终 HTML 都经过 validate → deliver → visual-check。自动 visual-check 的 `visualReview: pending` 是工具约定；本文件另行记录已实际查看截图后的人工状态，不修改自动收据。

| 图 | 类型 | Artifact 检查 | Composition | 桌面四尺寸 | 人工视觉状态 | 视觉修正轮次 |
| --- | --- | --- | --- | --- | --- | --- |
| architecture | architecture | 9/9 | 0 errors / 0 warnings | 通过 | passed | 1 |
| request | sequence | 9/9 | 0 errors / 0 warnings | 通过 | passed | 2 |
| scope | architecture | 9/9 | 0 errors / 0 warnings | 通过 | passed | 0 |

尺寸：1440×900、1600×1000、1920×1080、2048×1320，全部 `scrollWidth <= innerWidth` 且 `scrollHeight <= innerHeight`。小/大尺寸的浅色和深色 PNG 与 contact sheet 保存在 `site/diagrams/*.visual-check.*`。

实际视觉审阅确认：节点与标签无明显遮挡；架构图关系方向明确、控制/资源/依赖标识一致；时序图已压缩多余留白、去除会相互干扰的冗余阶段框，保留重复 step 与异步边界说明；范围图三栏边界清晰；最大屏幕下图形与说明区域分布合理。移动端使用独立打开、缩放/搜索及正文的模块说明进行阅读，结果详见验证记录。

静态 PNG / SVG 由最终 HTML 的导出菜单生成。架构图另测 JPEG / WebP。主预览来自真实首页截图，未以手工绘图模拟站点。默认无动效，WebM 未交付；剪贴板导出、语义雷达等高级功能未逐一验证。

## 冻结摘要

下列摘要来自最终原子交付收据。重新生成后需同步更新，不能把旧收据与新 HTML 混用。

### architecture

- 规格：`diagrams/specs/architecture.json`
- HTML：`site/diagrams/architecture.html`
- specification_sha256：`a6e1b35df58dcde3e71a9e0a5ef995db61c215960754c1ddb1d8ab5f6960637b`
- artifact_sha256：`d18e61258c6770bd3a5b2d79d32c5ce406b01ed214a87c4c102173a942606391`
- artifact_bytes：711671
- validate / deliver / visual-check 收据：`diagrams/receipts/architecture.*.json`

### request

- 规格：`diagrams/specs/request.json`
- HTML：`site/diagrams/request.html`
- specification_sha256：`d75de908981ef6e69fd0c3043f7871934268f59fb3ea0b36ea34d79861e49351`
- artifact_sha256：`8b2504f026f30581c602d6d24cc55d2f4f9b7c0620555b61626c03951889308c`
- artifact_bytes：709178
- validate / deliver / visual-check 收据：`diagrams/receipts/request.*.json`

### scope

- 规格：`diagrams/specs/scope.json`
- HTML：`site/diagrams/scope.html`
- specification_sha256：`b13c75066ac37990f5de799a8ac33adc0e878dab7129ea73cb8df7b38f7be5f2`
- artifact_sha256：`35a4948c05e931199b8dad3d2c36ce5ff0005dc3a836129a940bb0f27d64146e`
- artifact_bytes：709404
- validate / deliver / visual-check 收据：`diagrams/receipts/scope.*.json`
