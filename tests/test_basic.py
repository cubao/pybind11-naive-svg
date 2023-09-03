from naive_svg import SVG, Circle, Color, Polygon, Polyline, Text, add


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
    svg.as_polyline(1).stroke(Color(0xFFAA00))
    svg.grid_step(10.0)

    svg.view_box([20, 20, 40, 40])
    svg.add_text([30, 40], text="hello")

    text = svg.to_string()
    print(text)

    assert not svg.is_circle(10)