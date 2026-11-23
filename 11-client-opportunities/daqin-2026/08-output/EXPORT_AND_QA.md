# 输出、复现与 QA
## 2026-11-23 已完成
- 在 `/mnt/data/daqin_env` Python 虚拟环境（复用宿主只读预装包）生成12页 A4 PDF；
- 源数据来自 `06-analysis/opportunity-matrix.csv`（研究假设）与 `06-analysis/evidence-register.md`；
- 产出6张矢量图（SVG）及对应高清PNG，内容：证据时间线/评分排序/筛选门禁/品牌保护流程/产品分工/90天计划；
- PDF用 WeasyPrint、SVGWrite/CairoSVG 渲染；逐页图片检查12页，PDF提取文本无替换字符，页脚12/12。
## 仓库现实约束
GitHub插件的纯文本文件 API 不能直接读取本地沙箱二进制路径，因此此分支存档可直接浏览/编辑的正文、来源、CSV、SVG与恢复状态；**PDF和PNG当前在会话沙箱供下载，不虚称已上传到GitHub。** 获得认证二进制上传通道时补 `08-output/*.pdf` 和 `04-assets/figures/*.png`，并生成SHA256。
## 可编辑矢量图导出PNG
本目录 `04-assets/figures/*.svg` 是独立可编辑矢量图。安装 CairoSVG 后执行：
```bash
python -m venv .venv
.venv/bin/python -m pip install cairosvg
for f in 04-assets/figures/*.svg; do .venv/bin/python -m cairosvg "$f" -o "${f%.svg}.png" -s 2; done
```
不运行时 SVG 本身可在浏览器直接打开和缩放。
## 真实性回归门禁
- 评分 ≠ 企业实测；历史损失 ≠ 2026现状；
- 第三方中标商 ≠ 大勤直接中标；
- 法院文书镜像 ≠ 法院原网站当前可访问；
- 品牌假货是目前最强外部证据，但不构成固定“必须做打假”的营销策略；
- 不用AI生图绘制含具体数据的咨询图或重绘真实产品UI，防止文字与数字漂移。
