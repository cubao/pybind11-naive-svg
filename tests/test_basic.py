from __future__ import annotations

import json
import tempfile
from pathlib import Path

from naive_svg import SVG, Circle, Color, Polygon, Polyline, Rect, Text, add
from naive_svg import Path as SvgPath


def test_add():
    assert add(1, 2) == 3


def test_color():
    assert Color().to_string() == "none"
    assert Color(0xFF0000).to_string() == "rgb(255,0,0)"
    assert Color(0xFF0000).a(0.5).to_string() == "rgba(255,0,0,0.5)"
    c = Color(0x00FF00)
    assert c.r() == 0
    assert c.g() == 255
    assert c.b() == 0
    assert c.a() == -1.0
    assert c.r(155) == c
    assert c.b(155).b() == 155
    assert c.to_string() == "rgb(155,255,155)"


def test_svg():
    svg = SVG(100, 100)
    print(svg)

    c = svg.add_circle([40, 30], r=50)
    assert isinstance(c, Circle)
    text = svg.to_string()
    print(text)
    assert "rgb(0,0,0)" in text

    c.stroke(Color(0xFF0000))
    text = svg.to_string()
    print(text)
    assert "rgb(255,0,0)" in text

    c.fill(Color(0x00FF00).a(0.2))

    svg.add_polyline([[0, 0], [30, 40], [40, 30], [50, 0]])
    assert svg.is_circle(0)
    assert not svg.is_circle(1)
    assert svg.is_polyline(1)
    p = svg.as_polyline(1)
    assert isinstance(p, Polyline)
    p.stroke(Color(0xFFAA00))
    svg.grid_step(10.0)

    svg.view_box([20, 20, 40, 40])
    t = svg.add_text([30, 40], text="hello")
    assert isinstance(t, Text)

    polygon = (
        svg.add_polygon([[20, 20], [20, 30], [40, 30], [40, 20], [20, 20]])
        .stroke(Color(0x0000FF))
        .fill(Color(0xFF0000).a(0.1))
    )
    assert isinstance(polygon, Polygon)

    text = svg.to_string()
    print(text)

    assert not svg.is_circle(10)


def test_dash_array():
    """Test stroke-dasharray support"""
    svg = SVG(400, 100)

    # Test dashed polyline
    p = svg.add_polyline([[10, 50], [390, 50]]).stroke(Color(0x000000)).stroke_width(2)
    p.dash_array("10,5")
    assert p.dash_array() == "10,5"

    text = svg.to_string()
    assert "stroke-dasharray:10,5" in text

    # Test complex dash pattern
    p2 = svg.add_polyline([[10, 70], [390, 70]]).stroke(Color(0xFF0000)).stroke_width(2)
    p2.dash_array("10,5,2,5")
    text = svg.to_string()
    assert "stroke-dasharray:10,5,2,5" in text


def test_stroke_linecap_linejoin():
    """Test stroke-linecap and stroke-linejoin support"""
    svg = SVG(200, 100)

    p = svg.add_polyline([[10, 50], [100, 10], [190, 50]])
    p.stroke(Color(0x000000)).stroke_width(10)
    p.stroke_linecap("round")
    p.stroke_linejoin("round")

    assert p.stroke_linecap() == "round"
    assert p.stroke_linejoin() == "round"

    text = svg.to_string()
    assert "stroke-linecap:round" in text
    assert "stroke-linejoin:round" in text


def test_transform():
    """Test transform attribute support"""
    svg = SVG(200, 200)

    c = svg.add_circle([100, 100], r=30)
    c.transform("rotate(45, 100, 100)")
    assert c.transform() == "rotate(45, 100, 100)"

    text = svg.to_string()
    assert "transform='rotate(45, 100, 100)'" in text


def test_path():
    """Test Path element"""
    svg = SVG(300, 200)

    # Test with direct d string
    path = svg.add_path("M 100 150 L 120 130 L 120 140 L 180 140 Z")
    path.fill(Color(0xFF0000)).stroke(Color(0x000000))

    assert svg.is_path(0)
    assert isinstance(svg.as_path(0), SvgPath)

    text = svg.to_string()
    assert "<path d='M 100 150 L 120 130 L 120 140 L 180 140 Z'" in text

    # Test with builder methods
    path2 = svg.add_path()
    path2.move_to(10, 10).line_to(50, 10).line_to(30, 50).close()
    path2.fill(Color(0x00FF00))

    text = svg.to_string()
    assert "M 1" in text  # move_to uses std::to_string which outputs decimal
    assert "L 5" in text
    assert "Z" in text


def test_path_bezier():
    """Test Path bezier curves"""
    svg = SVG(200, 200)

    # Quadratic bezier
    path = svg.add_path()
    path.move_to(10, 80).quadratic(95, 10, 180, 80)

    text = svg.to_string()
    assert "Q " in text

    # Cubic bezier
    path2 = svg.add_path()
    path2.move_to(10, 160).cubic(40, 100, 65, 100, 95, 160)

    text = svg.to_string()
    assert "C " in text


def test_path_arc():
    """Test Path arc command"""
    svg = SVG(200, 200)

    path = svg.add_path()
    path.move_to(50, 100).arc(50, 50, 0, 1, 1, 150, 100)

    text = svg.to_string()
    assert "A " in text


def test_rect():
    """Test Rect element"""
    svg = SVG(200, 200)

    rect = svg.add_rect(10, 20, 100, 80)
    rect.fill(Color(0xFF0000)).stroke(Color(0x000000)).stroke_width(2)

    assert svg.is_rect(0)
    assert isinstance(svg.as_rect(0), Rect)

    text = svg.to_string()
    assert "<rect x='10' y='20' width='100' height='80'" in text


def test_rect_rounded():
    """Test Rect with rounded corners"""
    svg = SVG(200, 200)

    rect = svg.add_rect(10, 20, 100, 80)
    rect.rx(10).ry(10)
    rect.fill(Color(0x00FF00))

    assert rect.rx() == 10
    assert rect.ry() == 10

    text = svg.to_string()
    assert "rx='10'" in text
    assert "ry='10'" in text


def test_element_chaining():
    """Test fluent API chaining with new attributes"""
    svg = SVG(200, 100)

    # Test chaining all new attributes
    p = (
        svg.add_polyline([[10, 50], [190, 50]])
        .stroke(Color(0x000000))
        .stroke_width(3)
        .dash_array("10,5")
        .stroke_linecap("round")
        .stroke_linejoin("round")
        .transform("translate(5, 5)")
    )

    assert p.dash_array() == "10,5"
    assert p.stroke_linecap() == "round"
    assert p.stroke_linejoin() == "round"
    assert p.transform() == "translate(5, 5)"


def test_path_and_rect_add():
    """Test adding Path and Rect via add() method"""
    svg = SVG(200, 200)

    # Create standalone Path and add it
    path = SvgPath("M 10 10 L 50 50")
    added_path = svg.add(path)
    assert isinstance(added_path, SvgPath)
    assert svg.is_path(0)

    # Create standalone Rect and add it
    rect = Rect(10, 20, 100, 80)
    added_rect = svg.add(rect)
    assert isinstance(added_rect, Rect)
    assert svg.is_rect(1)


# =============================================================================
# EGeoJSON Styling Tests
# =============================================================================


def test_parse_color():
    """Test color parsing function"""
    from naive_svg.geojson2svg import parse_color

    # Test hex colors (6 digits)
    c = parse_color("#ff0000")
    assert c.r() == 255
    assert c.g() == 0
    assert c.b() == 0

    c = parse_color("#00ff00")
    assert c.r() == 0
    assert c.g() == 255
    assert c.b() == 0

    # Test hex colors (3 digits)
    c = parse_color("#f00")
    assert c.r() == 255
    assert c.g() == 0
    assert c.b() == 0

    # Test named colors
    c = parse_color("red")
    assert c.r() == 255
    assert c.g() == 0
    assert c.b() == 0

    c = parse_color("blue")
    assert c.r() == 0
    assert c.g() == 0
    assert c.b() == 255

    # Test case insensitivity
    c = parse_color("RED")
    assert c.r() == 255

    c = parse_color("#FF0000")
    assert c.r() == 255

    # Test empty/invalid
    c = parse_color("")
    assert c.to_string() == "none"

    c = parse_color(None)
    assert c.to_string() == "none"


def test_merge_paint():
    """Test paint merging with priority"""
    from naive_svg.geojson2svg import DEFAULT_PAINT, merge_paint

    # Test default values
    result = merge_paint({}, {})
    assert result["fill-color"] == DEFAULT_PAINT["fill-color"]
    assert result["opacity"] == 1.0

    # Test layer paint override
    result = merge_paint({}, {"fill-color": "#ff0000"})
    assert result["fill-color"] == "#ff0000"

    # Test feature paint override (takes priority)
    result = merge_paint({"fill-color": "#00ff00"}, {"fill-color": "#ff0000"})
    assert result["fill-color"] == "#00ff00"

    # Test partial override
    result = merge_paint({"opacity": 0.5}, {"fill-color": "#ff0000", "line-width": 2})
    assert result["fill-color"] == "#ff0000"
    assert result["opacity"] == 0.5
    assert result["line-width"] == 2


def test_apply_line_style():
    """Test line style application"""
    from naive_svg.geojson2svg import apply_line_style

    svg = SVG(100, 100)
    polyline = svg.add_polyline([[0, 0], [50, 50], [100, 0]])

    paint = {
        "fill-color": "#ff0000",
        "line-width": 3.0,
        "line-type": "dashed",
        "opacity": 0.5,
    }
    apply_line_style(polyline, paint)

    text = svg.to_string()
    assert "rgb(255,0,0)" in text
    assert "stroke-width:3" in text
    assert "stroke-dasharray:5,5" in text
    assert "stroke-opacity='0.5'" in text


def test_apply_polygon_style():
    """Test polygon style application"""
    from naive_svg.geojson2svg import apply_polygon_style

    svg = SVG(100, 100)
    polygon = svg.add_polygon([[0, 0], [50, 50], [100, 0], [0, 0]])

    paint = {
        "fill-color": "#00ff00",
        "opacity": 0.7,
    }
    apply_polygon_style(polygon, paint)

    text = svg.to_string()
    assert "rgb(0,128,0)" in text or "rgb(0,255,0)" in text  # green color
    assert "fill-opacity='0.7'" in text


def test_apply_point_style():
    """Test point style application"""
    from naive_svg.geojson2svg import apply_point_style

    svg = SVG(100, 100)
    circle = svg.add_circle([50, 50], r=10)

    paint = {
        "fill-color": "#0000ff",
        "opacity": 0.8,
    }
    apply_point_style(circle, paint)

    text = svg.to_string()
    assert "rgb(0,0,255)" in text
    assert "fill-opacity='0.8'" in text


def test_add_text_annotation():
    """Test text annotation from text-field"""
    import numpy as np

    from naive_svg.geojson2svg import add_text_annotation

    svg = SVG(100, 100)
    properties = {"name": "Test Point", "id": "123"}
    paint = {"text-field": "name", "text-color": "#ff0000"}

    text_elem = add_text_annotation(
        svg, np.array([50.0, 50.0]), properties, paint, fontsize=10
    )

    assert text_elem is not None
    text = svg.to_string()
    assert "Test Point" in text
    assert "rgb(255,0,0)" in text

    # Test with missing field
    svg2 = SVG(100, 100)
    paint2 = {"text-field": "nonexistent"}
    text_elem2 = add_text_annotation(svg2, np.array([50.0, 50.0]), properties, paint2)
    assert text_elem2 is None


def test_geojson2svg_standard_geojson():
    """Test conversion of standard GeoJSON format"""
    from naive_svg.geojson2svg import geojson2svg

    # Create a simple GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[121.48, 31.24], [121.49, 31.25]],
                },
                "properties": {
                    "id": "line1",
                    "paint": {"fill-color": "#ff0000", "line-width": 2},
                },
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [121.485, 31.245]},
                "properties": {
                    "name": "Test",
                    "paint": {
                        "fill-color": "#00ff00",
                        "radius": 10,
                        "text-field": "name",
                    },
                },
            },
        ],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.geojson"
        output_path = Path(tmpdir) / "output.svg"

        input_path.write_text(json.dumps(geojson_data))

        geojson2svg(str(input_path), str(output_path), with_grid=False)

        assert output_path.exists()
        svg_content = output_path.read_text()

        # Check that SVG was generated with styling
        assert "<svg" in svg_content
        assert "<polyline" in svg_content
        assert "<circle" in svg_content
        assert "rgb(255,0,0)" in svg_content  # red line
        assert "stroke-width:2" in svg_content


def test_geojson2svg_egeojson_format():
    """Test conversion of EGeoJSON v2.0 format with layers"""
    from naive_svg.geojson2svg import geojson2svg

    # Create EGeoJSON with layers
    egeojson_data = {
        "version": 2.0,
        "layers": [
            {
                "name": "DashedLines",
                "meta": {
                    "paint": {
                        "fill-color": "#ff0000",
                        "line-width": 2,
                        "line-type": "dashed",
                        "opacity": 0.8,
                    }
                },
                "data": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [[121.29, 31.25], [121.30, 31.26]],
                            },
                            "properties": {},
                        }
                    ],
                },
            },
            {
                "name": "Points",
                "meta": {"paint": {"fill-color": "#0000ff", "radius": 5}},
                "data": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [121.295, 31.255],
                            },
                            "properties": {
                                "name": "Waypoint",
                                "paint": {
                                    "fill-color": "#00ff00",  # Override layer color
                                    "text-field": "name",
                                    "text-color": "#000000",
                                },
                            },
                        }
                    ],
                },
            },
        ],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.egeojson"
        output_path = Path(tmpdir) / "output.svg"

        input_path.write_text(json.dumps(egeojson_data))

        geojson2svg(str(input_path), str(output_path), with_grid=False)

        assert output_path.exists()
        svg_content = output_path.read_text()

        # Check SVG structure
        assert "<svg" in svg_content
        assert "<polyline" in svg_content
        assert "<circle" in svg_content

        # Check dashed line style
        assert "stroke-dasharray:5,5" in svg_content

        # Check that feature-level paint overrides layer-level
        # The point should be green (#00ff00), not blue (#0000ff)
        assert "rgb(0,255,0)" in svg_content or "rgb(0,128,0)" in svg_content

        # Check text annotation
        assert "Waypoint" in svg_content


def test_geojson2svg_polygon():
    """Test polygon conversion with styling"""
    from naive_svg.geojson2svg import geojson2svg

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [121.48, 31.24],
                            [121.49, 31.24],
                            [121.49, 31.25],
                            [121.48, 31.25],
                            [121.48, 31.24],
                        ]
                    ],
                },
                "properties": {"paint": {"fill-color": "#ff0000", "opacity": 0.5}},
            }
        ],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.geojson"
        output_path = Path(tmpdir) / "output.svg"

        input_path.write_text(json.dumps(geojson_data))

        geojson2svg(str(input_path), str(output_path), with_grid=False)

        assert output_path.exists()
        svg_content = output_path.read_text()

        assert "<polygon" in svg_content
        assert "fill-opacity='0.5'" in svg_content


def test_geojson2svg_use_feature_style_false():
    """Test that use_feature_style=False ignores paint styles"""
    from naive_svg.geojson2svg import geojson2svg

    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[121.48, 31.24], [121.49, 31.25]],
                },
                "properties": {"paint": {"fill-color": "#ff0000", "line-width": 10}},
            }
        ],
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "test.geojson"
        output_path = Path(tmpdir) / "output.svg"

        input_path.write_text(json.dumps(geojson_data))

        geojson2svg(
            str(input_path), str(output_path), with_grid=False, use_feature_style=False
        )

        assert output_path.exists()
        svg_content = output_path.read_text()

        # Should not have the specified red color or line-width 10
        # Instead should have random color and default width
        assert "stroke-width:10" not in svg_content
        assert "stroke-width:0.2" in svg_content


def test_egeojson2svg_alias():
    """Test that egeojson2svg is an alias for geojson2svg"""
    from naive_svg.geojson2svg import egeojson2svg, geojson2svg

    assert egeojson2svg is geojson2svg
