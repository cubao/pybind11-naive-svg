from naive_svg import SVG, Circle, Polygon, Polyline, Text, add


def test_add():
    assert add(1, 2) == 3


def test_svg():
    svg = SVG(100, 100)
    print(svg)

    print(Polyline)
    print(Polygon)
    print(Circle)
    print(Text)
