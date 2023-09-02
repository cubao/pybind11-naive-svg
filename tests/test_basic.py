from naive_svg import add, SVG, Polyline, Polygon, Circle, Text


def test_add():
    assert add(1, 2) == 3

def test_svg():
    svg = SVG(100, 100)
    print(svg)