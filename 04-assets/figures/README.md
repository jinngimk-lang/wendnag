# BP 图表源文件说明

本目录是 BP 图表的正式事实源。

## 可编辑 SVG

- `svg/`：8 张独立 SVG 矢量源文件（图1、图2、图3、图10、图11、图12、图15、图16）。
- SVG 中的文字保留为 `<text>` 文本节点，没有转成轮廓；矩形、线条、箭头等也都是矢量元素。
- SVG 不嵌入 PNG/JPG，放大不会模糊。
- 可直接使用 Figma、Adobe Illustrator、Inkscape 等矢量编辑器修改文字、数字、框体和线条。
- 图表名称统一使用 `AegisClaw`，不再保留“曾用名 InkClaw”字样。

## Word 中的编辑边界

Word 把插入的 SVG 当作一个图形对象，因此 SVG 嵌入 DOCX 后，通常不能像 Word 原生表格/形状那样逐个编辑 SVG 内部文字和框体。需要修改图表内容时，应直接编辑本目录下的 SVG 源文件，或修改 `src/draw_bp_figures.py` 后重新生成，再替换进 DOCX。

如果后续要求“在 Word 内部直接逐个编辑框、文字、箭头”，则应把图表改成 Office 原生 DrawingML 形状，而不是 SVG。

## 生成代码

- `src/draw_bp_figures.py`：确定性绘图代码。
- `.github/workflows/build-bp-figures.yml`：云端校验流程，检查 SVG 保留文本节点、没有旧产品名，并核对输出尺寸。
