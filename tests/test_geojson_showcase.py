"""
GeoJSON 样式展示脚本

以北京为参考点，在 ENU 坐标系下构造各种几何要素，
展示 GeoJSON 到 SVG 的转换以及样式系统。

运行方式：
    pytest tests/test_geojson_showcase.py -v -s

输出：
    tests/output/showcase.geojson - GeoJSON 文件
    tests/output/showcase.svg - 转换后的 SVG 文件
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from pybind11_geobuf import tf

from naive_svg.geojson2svg import geojson2svg

# 北京参考点 (天安门广场附近)
BEIJING_LON, BEIJING_LAT = 116.4074, 39.9042

# 输出目录
OUTPUT_DIR = Path(__file__).parent / "output"


def enu_to_wgs84(enu_coords: list, anchor_lla: np.ndarray) -> list:
    """
    将 ENU 坐标 (米) 转换为 WGS84 坐标 (lon, lat)。

    Args:
        enu_coords: ENU 坐标列表，每个坐标为 [east, north] 或 [east, north, up]
        anchor_lla: 参考点的 WGS84 坐标 [lon, lat, alt]

    Returns:
        WGS84 坐标列表 [[lon, lat], ...]
    """
    # 确保是 3D 坐标
    coords = np.array(enu_coords)
    if coords.ndim == 1:
        coords = coords.reshape(1, -1)
    if coords.shape[1] == 2:
        coords = np.hstack([coords, np.zeros((len(coords), 1))])

    # 转换为 WGS84
    llas = tf.enu2lla(coords, anchor_lla=anchor_lla)
    return llas[:, :2].tolist()


def create_showcase_features() -> dict:
    """
    在 ENU 坐标系下构造展示要素，然后转换为 WGS84。

    所有坐标以米为单位，原点为北京参考点。
    """
    anchor = np.array([BEIJING_LON, BEIJING_LAT, 0.0])
    features = []

    # =========================================================================
    # 1. 建筑物 - 使用 Polygon
    # =========================================================================

    # 建筑A：红色半透明正方形 (100m x 100m)
    building_a_enu = [
        [0, 0],
        [100, 0],
        [100, 100],
        [0, 100],
        [0, 0],  # 闭合
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [enu_to_wgs84(building_a_enu, anchor)],
            },
            "properties": {
                "name": "建筑A",
                "type": "building",
                "paint": {
                    "fill-color": "#ff6b6b",  # 珊瑚红
                    "opacity": 0.7,
                    "line-width": 2,
                },
            },
        }
    )

    # 建筑B：蓝色半透明矩形 (150m x 80m)
    building_b_enu = [
        [150, 20],
        [300, 20],
        [300, 100],
        [150, 100],
        [150, 20],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [enu_to_wgs84(building_b_enu, anchor)],
            },
            "properties": {
                "name": "建筑B",
                "type": "building",
                "paint": {
                    "fill-color": "#4ecdc4",  # 青色
                    "opacity": 0.6,
                    "line-width": 1.5,
                },
            },
        }
    )

    # =========================================================================
    # 2. 道路 - 使用 LineString
    # =========================================================================

    # 主干道：深蓝色实线
    main_road_enu = [
        [-50, 50],
        [50, 50],
        [120, 60],
        [200, 60],
        [350, 50],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": enu_to_wgs84(main_road_enu, anchor),
            },
            "properties": {
                "name": "主干道",
                "type": "road",
                "paint": {
                    "fill-color": "navy",
                    "line-width": 4,
                    "line-type": "solid",
                },
            },
        }
    )

    # 辅路：橙色虚线
    secondary_road_enu = [
        [50, -30],
        [50, 50],
        [50, 150],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": enu_to_wgs84(secondary_road_enu, anchor),
            },
            "properties": {
                "name": "辅路",
                "type": "road",
                "paint": {
                    "fill-color": "orange",
                    "line-width": 2,
                    "line-type": "dashed",
                },
            },
        }
    )

    # 小径：灰色细虚线
    path_enu = [
        [200, 100],
        [220, 130],
        [250, 140],
        [280, 130],
        [300, 150],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": enu_to_wgs84(path_enu, anchor),
            },
            "properties": {
                "name": "小径",
                "type": "path",
                "paint": {
                    "fill-color": "gray",
                    "line-width": 1,
                    "line-type": "dashed",
                    "opacity": 0.8,
                },
            },
        }
    )

    # =========================================================================
    # 3. 兴趣点 - 使用 Point
    # =========================================================================

    # 餐厅：橙色圆点，带标注
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": enu_to_wgs84([[50, 120]], anchor)[0],
            },
            "properties": {
                "name": "餐厅",
                "type": "poi",
                "paint": {
                    "fill-color": "orange",
                    "radius": 8,
                    "text-field": "name",
                    "text-color": "#333333",
                },
            },
        }
    )

    # 地铁站：蓝色大圆点，带标注
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": enu_to_wgs84([[-30, 50]], anchor)[0],
            },
            "properties": {
                "name": "地铁站",
                "type": "poi",
                "paint": {
                    "fill-color": "#0066cc",
                    "radius": 10,
                    "text-field": "name",
                    "text-color": "#0066cc",
                },
            },
        }
    )

    # 停车场：灰色圆点
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": enu_to_wgs84([[320, 80]], anchor)[0],
            },
            "properties": {
                "name": "停车场",
                "type": "poi",
                "paint": {
                    "fill-color": "#666666",
                    "radius": 6,
                    "opacity": 0.9,
                },
            },
        }
    )

    # =========================================================================
    # 4. MultiPoint - 多个路灯
    # =========================================================================

    lamp_enu = [
        [0, 50],
        [40, 50],
        [80, 55],
        [160, 60],
        [240, 55],
        [320, 50],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": enu_to_wgs84(lamp_enu, anchor),
            },
            "properties": {
                "name": "路灯",
                "type": "infrastructure",
                "paint": {
                    "fill-color": "#ffcc00",  # 金黄色
                    "radius": 3,
                    "opacity": 0.9,
                },
            },
        }
    )

    # =========================================================================
    # 5. MultiLineString - 公交线路
    # =========================================================================

    bus_line_1_enu = [
        [-50, 30],
        [100, 30],
        [150, 40],
    ]
    bus_line_2_enu = [
        [150, 40],
        [200, 45],
        [350, 40],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [
                    enu_to_wgs84(bus_line_1_enu, anchor),
                    enu_to_wgs84(bus_line_2_enu, anchor),
                ],
            },
            "properties": {
                "name": "公交线路",
                "type": "transit",
                "paint": {
                    "fill-color": "#cc0066",  # 品红色
                    "line-width": 2,
                    "line-type": "dashed",
                    "opacity": 0.7,
                },
            },
        }
    )

    # =========================================================================
    # 6. MultiPolygon - 绿地区域
    # =========================================================================

    park_1_enu = [
        [100, 120],
        [140, 120],
        [140, 160],
        [100, 160],
        [100, 120],
    ]
    park_2_enu = [
        [160, 130],
        [190, 130],
        [190, 160],
        [160, 160],
        [160, 130],
    ]
    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [enu_to_wgs84(park_1_enu, anchor)],
                    [enu_to_wgs84(park_2_enu, anchor)],
                ],
            },
            "properties": {
                "name": "绿地",
                "type": "park",
                "paint": {
                    "fill-color": "green",
                    "opacity": 0.5,
                    "line-width": 1,
                },
            },
        }
    )

    # 构建 FeatureCollection
    geojson = {"type": "FeatureCollection", "features": features}

    return geojson


def test_geojson_showcase():
    """
    生成展示性 GeoJSON 和 SVG 文件。

    此测试会：
    1. 在 ENU 坐标系下构造各种几何要素
    2. 转换为 WGS84 坐标
    3. 保存为 GeoJSON 文件
    4. 调用 geojson2svg 生成 SVG 文件
    """
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 创建 GeoJSON
    geojson = create_showcase_features()

    # 保存 GeoJSON
    geojson_path = OUTPUT_DIR / "showcase.geojson"
    geojson_path.write_text(json.dumps(geojson, indent=2, ensure_ascii=False))
    print(f"\nGeoJSON 已保存至: {geojson_path}")

    # 生成 SVG
    svg_path = OUTPUT_DIR / "showcase.svg"
    geojson2svg(
        str(geojson_path),
        str(svg_path),
        with_label=False,
        with_grid=True,
        grid_step=50.0,  # 50米网格
        use_feature_style=True,
    )
    print(f"SVG 已保存至: {svg_path}")

    # 验证文件生成
    assert geojson_path.exists(), "GeoJSON 文件未生成"
    assert svg_path.exists(), "SVG 文件未生成"

    # 验证 GeoJSON 内容
    saved_geojson = json.loads(geojson_path.read_text())
    assert saved_geojson["type"] == "FeatureCollection"
    assert len(saved_geojson["features"]) > 0
    print(f"GeoJSON 包含 {len(saved_geojson['features'])} 个要素")

    # 验证 SVG 内容
    svg_content = svg_path.read_text()
    assert "<svg" in svg_content
    assert "<polygon" in svg_content  # 建筑物
    assert "<polyline" in svg_content  # 道路
    assert "<circle" in svg_content  # 兴趣点

    # 输出样式说明
    print("\n=== 样式说明 ===")
    print("建筑A: 珊瑚红 (#ff6b6b), 70% 透明度")
    print("建筑B: 青色 (#4ecdc4), 60% 透明度")
    print("主干道: 深蓝色 (navy), 4px 实线")
    print("辅路: 橙色 (orange), 2px 虚线")
    print("小径: 灰色 (gray), 1px 虚线")
    print("餐厅: 橙色圆点, 带文字标注")
    print("地铁站: 蓝色大圆点, 带文字标注")
    print("路灯: 金黄色小圆点 (MultiPoint)")
    print("公交线路: 品红色虚线 (MultiLineString)")
    print("绿地: 绿色半透明 (MultiPolygon)")


if __name__ == "__main__":
    test_geojson_showcase()
