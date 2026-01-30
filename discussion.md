# 离线地图渲染方案

## 🧑‍💻 User

离线，把三维场景（其实是 2D）渲染成图片，数据大概是一个局部地图，有车道线，地面转向箭头等几何要素，是 geojson 格式。坐标都是 ENU 的。场景范围大概是 100m x 300m，像素化大概需要 5cm per pixel。

技术路线上，有啥选择？
现在已经有一个前端的 threejs 的渲染。但离线想输出的图片的话，有什么好的思路？

---
## 🤖 Assistant

需求拆成三件事：**(1) ENU→像素坐标的确定性投影**，**(2) 2D 矢量要素的线/面/符号渲染**，**(3) 离线批量输出图片（可控抗锯齿、线宽、虚线、贴图箭头）**。你现在 three.js 能画，离线就两条主路线：继续用 GPU/WebGL，或改成 CPU 矢量栅格化。

## 关键量先算清
- 范围 100m × 300m，5cm/px ⇒ 输出分辨率约 **2000 × 6000**（或旋转后 6000×2000）。
- 这已经是“高分辨率大画布”，对 **headless WebGL/浏览器**、**抗锯齿**、**内存** 有实际约束；CPU 栅格化反而稳定。

---

## 路线 A：继续 three.js，离线 headless 渲染（WebGL）
适用：已有 three.js 样式体系（材质、贴图箭头、虚线、图层）、想“所见即所得”复用。

实现方式：
1. **Node + headless-gl**（node-webgl / headless-gl）创建 WebGL context，three.js 渲染到 framebuffer，readPixels 导出 PNG。
   - 优点：不依赖整套浏览器，部署相对轻。
   - 风险点：WebGL 扩展/兼容、MSAA（多重采样抗锯齿）支持不稳；6k 长边 + 线条细节容易锯齿。
2. **Puppeteer/Playwright + Chromium headless**，打开你现有 three.js 页面，控制相机/投影参数，`page.screenshot()` 输出。
   - 优点：基本等同线上效果，字体/纹理/虚线表现更一致。
   - 风险点：更重；大分辨率截图时显存/内存压力；需要确保 deterministic（禁用动画、固定 DPR、固定时间步）。

工程要点（这条路线必须做）：
- 使用**正交相机**，相机视锥严格对应 ENU 区域：
  `left/right/top/bottom = bbox_meters`，然后 `meters -> pixels` 固定比例。
- 关闭任何随设备变化的 DPR：强制 `renderer.setPixelRatio(1)`，尺寸按像素给足。
- 抗锯齿策略：优先 **SSAA（超采样后缩小）**，例如按 2× 分辨率渲染再 downscale（代价是 4× 像素填充）。
- 线宽：WebGL 原生 linewidth 在多数实现上不可控；车道线建议用 **mesh strip（挤出成面）**，而不是 GL_LINE。

结论：如果你要完全复用 three.js 的视觉体系，这是最快，但要为抗锯齿和线宽付工程代价。

---

## 路线 B：不走 three.js，直接 2D 矢量→栅格（CPU，最稳）
适用：你的“3D 其实是 2D”，要的是地图符号学渲染：线、虚线、面填充、箭头标记、图层遮盖，且要高分辨率稳定输出。

可选技术栈（从“地图渲染”到“通用 2D”）：

### B1. Mapnik（经典离线制图）
- 读 GeoJSON，按样式（类似 CSS）渲染成 PNG。
- 强项：高质量抗锯齿、线型、虚线、复合符号、批量瓦片/大图输出都成熟。
- 代价：上手和部署比纯 JS/纯 Python 重一点，但稳定。

### B2. MapLibre GL Native / Mapbox GL（离线）
- 如果未来想走“地图样式规范”（style spec），可用离线渲染。
- 但你的数据是 ENU 局部坐标，不是经纬度/墨卡托；需要自己定义投影或做坐标适配，不如 Mapnik 直接用平面坐标来得直。

### B3. Skia / Cairo（通用 2D 图形库）
- 自己写渲染：ENU→像素后，把 LineString/Polygon 直接画到画布。
- Skia（C++/Rust/Node 绑定）质量高；Cairo（Python/Node）也行。
- 适合你这种要素类型固定（车道线、箭头、停止线、斑马线等）且样式规则明确的场景。
- 优点：最可控、确定性强、性能可预测。
- 代价：你要自己实现虚线、线帽、join、符号贴图沿线放置等规则（但这些库大多已有 dash/path effect）。

### B4. GDAL/OGR + rasterize（最省事的“能出图”）
- `gdal_rasterize` 直接把矢量栅格化到指定分辨率。
- 优点：最快搭起来。
- 缺点：符号化能力弱（复杂车道箭头/沿线符号/多层叠加的美术效果很难）。

结论：如果离线要“稳定批量出 2000×6000 且线条好看”，CPU 2D（Mapnik 或 Skia/Cairo）通常比 headless WebGL 更省坑。

---

## 路线 C：混合：three.js 只负责几何生成，最终用 2D 栅格器画
做法：
- three.js 里你可能已经有“车道线挤出面/箭头 mesh”的生成逻辑；把它输出成 2D path（多边形集合）或简单三角网。
- 离线用 Skia/Cairo 把这些面填充/描边到像素。
优势：复用几何规则，但抛弃 WebGL 的抗锯齿/linewidth 不确定性。

---

## 选型结论（按你的描述最匹配）
- 你是 **平面 ENU 局部地图**、要 **5cm/px 大图**、要素是 **线/面/符号**：优先 **路线 B（Mapnik 或 Skia/Cairo）**。
- 只有在“必须与现有 three.js 视觉完全一致”时，才优先 **路线 A（Puppeteer/Chromium headless）**，并用 SSAA 解决锯齿与线宽。

---

## 最小落地方案（可直接工程化）
1. 固定一个渲染坐标系：ENU bbox → 像素 bbox（线性变换矩阵）。
2. GeoJSON 逐要素按 layer 分类（lane boundary / centerline / arrows / stopline / crosswalk）。
3. 用 Mapnik 或 Skia/Cairo：
   - LineString：stroke（dash、cap、join、miter limit）。
   - Polygon：fill + optional outline。
   - 箭头：用贴图 stamp（按点放置）或用矢量符号（SVG path）按朝向旋转绘制。
4. 输出 PNG（需要透明就 RGBA），保证可重复生成（无随机、无依赖 DPI）。

如果你坚持复用 three.js：Puppeteer headless + 正交相机 + SSAA downscale + 线全部用 mesh strip，不用 GL_LINE。

---
## 🧑‍💻 User

我直接把我的数据，以 svg 格式的形式导出。这样可行吗？

---
## 🤖 Assistant

可行，而且对你这种“2D 几何要素 + 高分辨率静态出图”通常是最省坑的路线。核心是两步：**ENU→SVG 坐标**，**SVG→PNG（或直接用 SVG）**。

## 1) ENU → SVG 的确定性映射
设定渲染范围 bbox：`[Emin,Emax] × [Nmin,Nmax]`（米），分辨率 5cm/px。
- `Wpx = round((Emax-Emin)/0.05)`
- `Hpx = round((Nmax-Nmin)/0.05)`

SVG 以左上为原点、y 向下。ENU 的 N 通常向上，所以需要翻转：
- `x = (E - Emin) / 0.05`
- `y = (Nmax - N) / 0.05`

然后输出：
- `<svg width="{Wpx}" height="{Hpx}" viewBox="0 0 {Wpx} {Hpx}">`

## 2) 要素如何表达成 SVG
- 车道线/中心线：`<path d="M ... L ...">` + `stroke`、`stroke-width`、`stroke-dasharray`、`stroke-linecap`、`stroke-linejoin`
  - `stroke-width` 用“像素”定义：例如 10cm 线宽 ⇒ `0.10/0.05 = 2px`
- 面（停止区、斑马线块等）：`<path ... fill=...>`
- 地面箭头：
  - 最稳：预定义一个箭头的 path（或 `<symbol>`），按 ENU 朝向旋转平移：`transform="translate(x y) rotate(deg) scale(s)"`
  - 如果是沿线重复符号，用 `<pattern>` 或分段 stamp（更可控）

## 3) SVG → 离线图片（PNG）
两类实现最常用：
- **rsvg-convert（librsvg）/ Inkscape CLI**：对 SVG 支持完整，文本/路径/变换稳定。
- **Cairo/Skia**：你自己控制渲染管线时用；但“直接把 SVG 转 PNG”用 librsvg 最省事。

注意点（否则会踩坑）：
- 大图尺寸：你约 2000×6000，SVG 本身没问题；转 PNG 时要确认工具不会默认缩放或改 DPI。
- 线条对齐：细线在偶数/奇数像素上会糊；可用 0.5px 对齐策略（例如让线中心落在半像素）或统一用面（把线挤出成 polygon）避免对齐问题。
- 虚线在不同渲染器可能略有差异；如果必须完全一致，改成显式几何（把虚线拆成短线段）最确定。
- 字体：如果有文字，嵌入字体或转 path，避免环境差异。

结论：SVG 作为中间格式非常合适；你把 GeoJSON → SVG（路径/符号）做成确定性输出，再用标准离线渲染器转 PNG，稳定性通常优于 headless WebGL。
