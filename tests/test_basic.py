from __future__ import annotations

from naive_svg import SVG, Circle, Color, Path, Polygon, Polyline, Rect, Text, add


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
    assert isinstance(svg.as_path(0), Path)

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
    path = Path("M 10 10 L 50 50")
    added_path = svg.add(path)
    assert isinstance(added_path, Path)
    assert svg.is_path(0)

    # Create standalone Rect and add it
    rect = Rect(10, 20, 100, 80)
    added_rect = svg.add(rect)
    assert isinstance(added_rect, Rect)
    assert svg.is_rect(1)
