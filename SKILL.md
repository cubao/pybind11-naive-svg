# naive-svg: GeoJSON/Geometry to SVG Export Guide

This document teaches AI agents how to use `naive_svg` to export SVG files, with a focus on GeoJSON-to-SVG conversion for geospatial visualization.

## Core Concepts

### Coordinate Systems

GeoJSON data comes in three flavors, but the format is always standard GeoJSON:

| Coordinate System | Units | X axis | Y axis | Typical Use |
|---|---|---|---|---|
| WGS84 (LLA) | degrees | longitude | latitude | GPS data, web maps |
| ENU | meters | East | North | local tangent plane, metric analysis |
| EGO | meters | Forward (x) | Left (y) | vehicle/robot-centric perception |

SVG uses a screen coordinate system where **+x is right, +y is down**. This is a critical difference:

- **ENU/EGO** data has **+y pointing up** (North/Left), which is **inverted** relative to SVG.
- **WGS84** data must first be projected to a metric space (ENU) before rendering.

### The Y-Axis Problem and `svg.transform()`

When rendering ENU or EGO data, the Y axis is flipped relative to SVG convention. Use `svg.transform("scale(1,-1)")` to fix this globally:

```python
svg = SVG(width, height)
svg.view_box([xmin, -ymax, width, height])  # note: negate ymax for viewBox origin
svg.transform("scale(1,-1)")                # flip Y globally
```

This wraps all SVG content in `<g transform='scale(1,-1)'>`, making the coordinate system match ENU/EGO conventions where +y is up.

> **When NOT to flip**: If you pre-negate Y coordinates yourself (e.g., `points[:, 1] *= -1`), don't use `transform`. The `transform` approach is cleaner because it preserves the original coordinate values in the SVG source.

## Quick Start

### 1. Direct SVG Construction (Python)

```python
import numpy as np
from naive_svg import SVG, Color

svg = SVG(800, 600)
svg.view_box([0, 0, 800, 600])
svg.background(Color(255, 255, 255))

# Polyline (open path)
svg.add_polyline([[100, 100], [200, 150], [300, 100]]) \
   .stroke(Color(255, 0, 0)).stroke_width(2)

# Polygon (closed, filled)
svg.add_polygon([[400, 100], [500, 100], [450, 200], [400, 100]]) \
   .fill(Color(0, 128, 255, 0.3)).stroke(Color(0, 0, 255)).stroke_width(1)

# Circle
svg.add_circle([600, 150], r=30) \
   .fill(Color(0, 200, 0)).stroke(Color(0, 0, 0)).stroke_width(0.5)

# Text
svg.add_text([100, 50], text="Hello SVG", fontsize=16) \
   .fill(Color(0, 0, 0))

# Rect
svg.add_rect(50, 300, 200, 100) \
   .fill(Color(255, 200, 0, 0.5)).stroke(Color(0, 0, 0))

# Path (arbitrary shape)
svg.add_path().move_to(600, 300).line_to(700, 300) \
   .quadratic(750, 250, 700, 200).close() \
   .fill(Color(200, 0, 200, 0.4))

svg.dump("output.svg")
```

### 2. GeoJSON-to-SVG One-Liner

```python
from naive_svg.geojson2svg import geojson2svg

# WGS84 GeoJSON file -> SVG
geojson2svg("input.geojson", "output.svg")

# ENU/EGO GeoJSON -> SVG (skip coordinate conversion)
geojson2svg("input_enu.geojson", "output.svg", is_enu=True)
```

## GeoJSON Geometry → SVG Element Mapping

| GeoJSON Type | SVG Element | Notes |
|---|---|---|
| `Point` | `<circle>` | radius from `paint.radius` (default 5.0) |
| `MultiPoint` | multiple `<circle>` | one circle per coordinate |
| `LineString` | `<polyline>` | open path, no fill |
| `MultiLineString` | multiple `<polyline>` | each sub-line is a separate polyline |
| `Polygon` | `<polygon>` | uses outer ring only (first ring); closed, filled |
| `MultiPolygon` | multiple `<polygon>` | each sub-polygon rendered separately |

## Styling System

### Paint Dictionary

Styling is controlled via a `paint` dictionary in feature properties:

```json
{
  "properties": {
    "paint": {
      "fill-color": "#ff6b6b",
      "opacity": 0.7,
      "line-width": 2.0,
      "line-type": "solid",
      "radius": 8.0,
      "text-field": "name",
      "text-color": "#333333"
    }
  }
}
```

| Paint Key | Type | Default | Applies To | Description |
|---|---|---|---|---|
| `fill-color` | string | `"#4a9e54"` | all | Hex (`#ff0000`, `#f00`) or named color (`red`, `navy`) |
| `opacity` | float | `1.0` | all | 0.0–1.0, applied as fill-opacity/stroke-opacity |
| `line-width` | float | `1.0` | LineString, Polygon | stroke-width in SVG units |
| `line-type` | string | `"solid"` | LineString | `"solid"` or `"dashed"` (renders as `stroke-dasharray:5,5`) |
| `radius` | float | `5.0` | Point, MultiPoint | circle radius in SVG units |
| `text-field` | string | — | Point | property key to use as label text |
| `text-color` | string | `"#000000"` | Point | color of label text |

### How Styling is Applied Per Geometry Type

**LineString/MultiLineString:**
- `fill-color` → `stroke` color (not fill — polylines have no fill)
- `line-width` → `stroke-width`
- `line-type: "dashed"` → `stroke-dasharray: 5,5`
- `opacity < 1.0` → `stroke-opacity`

**Polygon/MultiPolygon:**
- `fill-color` → both `fill` and `stroke` color
- `line-width` → `stroke-width`
- `opacity < 1.0` → both `fill-opacity` and `stroke-opacity`

**Point/MultiPoint:**
- `fill-color` → both `fill` and `stroke` color
- `radius` → circle `r`
- `opacity < 1.0` → `fill-opacity`
- `text-field` → if set, looks up the key in `properties` and adds a `<text>` label

### Paint Priority (Layered Format)

```
feature.properties.paint  >  layer.meta.paint  >  DEFAULT_PAINT
```

## Coordinate Conversion Workflow

### Scenario A: WGS84 GeoJSON (most common)

WGS84 data (lon/lat in degrees) must be projected to a flat metric space for SVG rendering. The library uses **ENU (East-North-Up)** projection with an auto-detected anchor point.

```python
# Automatic: geojson2svg handles WGS84 → ENU internally
geojson2svg("wgs84_data.geojson", "output.svg")

# Or convert manually for more control:
from naive_svg.geojson2svg import geojson_to_enu

fc_enu = geojson_to_enu("wgs84_data.geojson", anchor=[116.4074, 39.9042, 0.0])
# Now fc_enu has ENU coordinates in meters, use with is_enu=True
```

Pipeline: `WGS84 GeoJSON → lla2enu(anchor) → ENU coords (meters) → SVG (with Y-flip via viewBox)`

### Scenario B: ENU GeoJSON

Data is already in meters (East, North). Common in robotics, surveying, and perception systems.

```python
geojson2svg("enu_data.geojson", "output.svg", is_enu=True)
```

Pipeline: `ENU GeoJSON (meters) → SVG directly (with Y-flip via viewBox)`

### Scenario C: EGO GeoJSON (vehicle-centric)

EGO coordinates are in the vehicle's frame: X = forward, Y = left. This is conceptually the same as ENU (both metric, Y-up in the math sense), so treat it the same way:

```python
geojson2svg("ego_data.geojson", "output.svg", is_enu=True)
```

> If you need to rotate EGO to match a specific heading, apply the rotation before rendering or use per-element `transform("rotate(...)")`.

## Building SVG from GeoJSON Programmatically

When the `geojson2svg()` one-liner doesn't meet your needs (custom styling, mixed coordinate systems, additional annotations), build the SVG yourself:

```python
import json
import numpy as np
from naive_svg import SVG, Color
from naive_svg.geojson2svg import parse_color

# Load GeoJSON
with open("data.geojson") as f:
    data = json.load(f)

# --- Step 1: Collect coordinates and compute bounding box ---
all_points = []
for feature in data["features"]:
    geom = feature["geometry"]
    coords = np.array(geom["coordinates"])
    if coords.ndim == 1:
        coords = coords.reshape(1, -1)
    # Flatten nested structures (Polygon outer ring, etc.)
    if geom["type"] == "Polygon":
        coords = np.array(geom["coordinates"][0])
    all_points.append(coords[:, :2])

all_points = np.vstack(all_points)
bbox_min = all_points.min(axis=0)
bbox_max = all_points.max(axis=0)
padding = 10.0
bbox_min -= padding
bbox_max += padding
width, height = bbox_max - bbox_min

# --- Step 2: Create SVG with proper coordinate setup ---
svg = SVG(width, height)
svg.view_box([bbox_min[0], -bbox_max[1], width, height])
svg.transform("scale(1,-1)")  # flip Y for ENU/EGO
svg.grid_step(50.0)           # optional grid

# --- Step 3: Add elements per geometry type ---
for feature in data["features"]:
    geom = feature["geometry"]
    props = feature.get("properties", {})
    paint = props.get("paint", {})
    color = parse_color(paint.get("fill-color", "#4a9e54"))

    if geom["type"] == "LineString":
        pts = np.array(geom["coordinates"])[:, :2]
        svg.add_polyline(pts) \
           .stroke(color) \
           .stroke_width(paint.get("line-width", 1.0))

    elif geom["type"] == "Polygon":
        pts = np.array(geom["coordinates"][0])[:, :2]
        svg.add_polygon(pts) \
           .fill(Color(color.r(), color.g(), color.b(), paint.get("opacity", 0.3))) \
           .stroke(color) \
           .stroke_width(paint.get("line-width", 1.0))

    elif geom["type"] == "Point":
        pt = np.array(geom["coordinates"])[:2]
        r = paint.get("radius", 5.0)
        svg.add_circle(pt, r=r) \
           .fill(color) \
           .stroke(Color(0, 0, 0)).stroke_width(0.5)

svg.dump("output.svg")
```

## Layered GeoJSON Format

Beyond standard FeatureCollection, the library supports a layered format where each layer carries its own default paint:

```json
{
  "layers": [
    {
      "name": "Roads",
      "meta": {
        "paint": { "fill-color": "navy", "line-width": 3, "line-type": "solid" }
      },
      "data": {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "geometry": { "type": "LineString", "coordinates": [[...], [...]] },
            "properties": {
              "paint": { "line-width": 5 }
            }
          }
        ]
      }
    },
    {
      "name": "POIs",
      "meta": {
        "paint": { "fill-color": "#0066cc", "radius": 8 }
      },
      "data": {
        "type": "FeatureCollection",
        "features": [...]
      }
    }
  ]
}
```

Feature-level `paint` overrides layer-level `paint`, which overrides defaults.

## SVG API Reference (Cheatsheet)

### SVG Container

```python
svg = SVG(width, height)
svg.width(w)                            # set width
svg.height(h)                           # set height
svg.view_box([x, y, w, h])             # set viewBox (controls visible area)
svg.transform("scale(1,-1)")           # wrap all content in <g transform="...">
svg.background(Color(255, 255, 255))   # background rect
svg.grid_step(50.0)                    # enable grid with spacing
svg.grid_x([xmin, xmax, xstep])       # custom grid X range
svg.grid_y([ymin, ymax, ystep])       # custom grid Y range
svg.grid_color(Color(200, 200, 200))  # grid line color
svg.attrs("data-name='my-map'")       # custom SVG attributes
svg.to_string()                        # get SVG as string
svg.dump("file.svg")                   # write to file
```

### Elements

All setters return `self` for method chaining. Common properties on every element:

```python
.stroke(Color(r, g, b))       # outline color
.stroke_width(2.0)            # outline thickness
.fill(Color(r, g, b, alpha))  # fill color (alpha: 0.0-1.0, or -1 for none)
.dash_array("5,5")            # dashed line pattern
.stroke_linecap("round")      # "butt" | "round" | "square"
.stroke_linejoin("round")     # "miter" | "round" | "bevel"
.transform("rotate(45)")      # per-element SVG transform
.attrs("data-id='x'")         # custom attributes
```

### Color

```python
Color()                    # invalid/none (renders as "none")
Color(0xFF0000)            # from hex int: red
Color(255, 0, 0)           # from RGB
Color(255, 0, 0, 0.5)     # from RGBA (alpha 0.0-1.0)
color.r(), .g(), .b()     # get channels
color.a(0.5)               # set alpha, returns self
Color.parse("#ff0000")     # parse hex string
```

### Element-Specific

```python
# Polyline / Polygon — take Nx2 numpy array or list-of-lists
svg.add_polyline([[x1,y1], [x2,y2], ...])
svg.add_polygon([[x1,y1], [x2,y2], ...])

# Circle — center as [x, y], radius as r
svg.add_circle([cx, cy], r=10.0)

# Text — position, text content, font size
svg.add_text([x, y], text="label", fontsize=12.0)
   .lines(["line2", "line3"])    # additional lines (multi-line text)

# Rect — x, y, width, height
svg.add_rect(x, y, w, h).rx(5).ry(5)  # with rounded corners

# Path — SVG path commands
svg.add_path("M 0 0 L 100 0 L 100 100 Z")
svg.add_path().move_to(0, 0).line_to(100, 0).quadratic(150, 50, 100, 100).close()
```

## Common Patterns

### Auto-fit viewBox from data

```python
points = np.vstack([...all coordinate arrays...])
pad = 10.0
xmin, ymin = points.min(axis=0) - pad
xmax, ymax = points.max(axis=0) + pad
w, h = xmax - xmin, ymax - ymin

svg = SVG(w, h)
svg.view_box([xmin, -ymax, w, h])   # -ymax because of Y-flip
svg.transform("scale(1,-1)")
```

### Directional arrows on polylines

Use SVG `Path` to draw arrowheads at segment endpoints:

```python
def add_arrow(svg, p0, p1, size=3.0, color=Color(0, 0, 0)):
    """Draw an arrowhead at p1, pointing from p0 to p1."""
    d = p1 - p0
    d = d / np.linalg.norm(d) * size
    perp = np.array([-d[1], d[0]]) * 0.5
    svg.add_polygon([p1, p1 - d + perp, p1 - d - perp]) \
       .fill(color).stroke(color).stroke_width(0.5)
```

### Overlay multiple GeoJSON layers

```python
svg = SVG(w, h)
svg.view_box([...]).transform("scale(1,-1)")

# Layer 1: road network (polylines)
for feature in roads["features"]:
    pts = np.array(feature["geometry"]["coordinates"])[:, :2]
    svg.add_polyline(pts).stroke(Color(0, 0, 128)).stroke_width(2)

# Layer 2: buildings (polygons)
for feature in buildings["features"]:
    pts = np.array(feature["geometry"]["coordinates"][0])[:, :2]
    svg.add_polygon(pts).fill(Color(200, 200, 200, 0.5)).stroke(Color(100, 100, 100))

# Layer 3: POIs (circles + labels)
for feature in pois["features"]:
    pt = np.array(feature["geometry"]["coordinates"])[:2]
    name = feature["properties"].get("name", "")
    svg.add_circle(pt, r=5).fill(Color(255, 0, 0))
    if name:
        svg.add_text(pt, text=name, fontsize=3).fill(Color(0, 0, 0))

svg.dump("map.svg")
```
