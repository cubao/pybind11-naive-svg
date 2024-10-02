from __future__ import annotations

import typing

import numpy

__all__ = ["Circle", "Color", "Polygon", "Polyline", "SVG", "Text", "add"]

class Circle:
    def __copy__(self, arg0: dict) -> Circle: ...
    def __deepcopy__(self, memo: dict) -> Circle: ...
    def __init__(
        self, center: numpy.ndarray[numpy.float64[2, 1]], r: float = 1.0
    ) -> None: ...
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Circle: ...
    @typing.overload
    def center(self) -> numpy.ndarray[numpy.float64[2, 1]]: ...
    @typing.overload
    def center(self, arg0: numpy.ndarray[numpy.float64[2, 1]]) -> Circle: ...
    def clone(self) -> Circle: ...
    @typing.overload
    def fill(self) -> Color: ...
    @typing.overload
    def fill(self, arg0: Color) -> Circle: ...
    @typing.overload
    def r(self) -> float: ...
    @typing.overload
    def r(self, arg0: float) -> Circle: ...
    @typing.overload
    def stroke(self) -> Color: ...
    @typing.overload
    def stroke(self, arg0: Color) -> Circle: ...
    @typing.overload
    def stroke_width(self) -> float: ...
    @typing.overload
    def stroke_width(self, arg0: float) -> Circle: ...
    def to_string(self) -> str: ...
    @typing.overload
    def x(self) -> float: ...
    @typing.overload
    def x(self, arg0: float) -> Circle: ...
    @typing.overload
    def y(self) -> float: ...
    @typing.overload
    def y(self, arg0: float) -> Circle: ...

class Color:
    @staticmethod
    def parse(arg0: str) -> Color: ...
    def __copy__(self, arg0: dict) -> Color: ...
    def __deepcopy__(self, memo: dict) -> Color: ...
    @typing.overload
    def __init__(self, rgb: int = -1) -> None: ...
    @typing.overload
    def __init__(self, r: int, g: int, b: int, a: float = -1.0) -> None: ...
    def __repr__(self) -> str: ...
    @typing.overload
    def a(self) -> float: ...
    @typing.overload
    def a(self, arg0: float) -> Color: ...
    @typing.overload
    def b(self) -> int: ...
    @typing.overload
    def b(self, arg0: int) -> Color: ...
    def clone(self) -> Color: ...
    @typing.overload
    def g(self) -> int: ...
    @typing.overload
    def g(self, arg0: int) -> Color: ...
    def invalid(self) -> bool: ...
    @typing.overload
    def r(self) -> int: ...
    @typing.overload
    def r(self, arg0: int) -> Color: ...
    def to_string(self) -> str: ...

class Polygon:
    def __copy__(self, arg0: dict) -> Polygon: ...
    def __deepcopy__(self, memo: dict) -> Polygon: ...
    def __init__(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> None: ...
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Polygon: ...
    def clone(self) -> Polygon: ...
    @typing.overload
    def fill(self) -> Color: ...
    @typing.overload
    def fill(self, arg0: Color) -> Polygon: ...
    def from_numpy(
        self, arg0: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous]
    ) -> Polygon: ...
    @typing.overload
    def stroke(self) -> Color: ...
    @typing.overload
    def stroke(self, arg0: Color) -> Polygon: ...
    @typing.overload
    def stroke_width(self) -> float: ...
    @typing.overload
    def stroke_width(self, arg0: float) -> Polygon: ...
    def to_numpy(self) -> numpy.ndarray[numpy.float64[m, 2]]: ...
    def to_string(self) -> str: ...

class Polyline:
    def __copy__(self, arg0: dict) -> Polyline: ...
    def __deepcopy__(self, memo: dict) -> Polyline: ...
    def __init__(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> None: ...
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Polyline: ...
    def clone(self) -> Polyline: ...
    @typing.overload
    def fill(self) -> Color: ...
    @typing.overload
    def fill(self, arg0: Color) -> Polyline: ...
    def from_numpy(
        self, arg0: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous]
    ) -> Polyline: ...
    @typing.overload
    def stroke(self) -> Color: ...
    @typing.overload
    def stroke(self, arg0: Color) -> Polyline: ...
    @typing.overload
    def stroke_width(self) -> float: ...
    @typing.overload
    def stroke_width(self, arg0: float) -> Polyline: ...
    def to_numpy(self) -> numpy.ndarray[numpy.float64[m, 2]]: ...
    def to_string(self) -> str: ...

class SVG:
    def __copy__(self, arg0: dict) -> SVG: ...
    def __deepcopy__(self, memo: dict) -> SVG: ...
    def __init__(self, width: float, height: float) -> None: ...
    @typing.overload
    def add(self, polyline: Polyline) -> Polyline: ...
    @typing.overload
    def add(self, polygon: Polygon) -> Polygon: ...
    @typing.overload
    def add(self, circle: Circle) -> Circle: ...
    @typing.overload
    def add(self, text: Text) -> Text: ...
    def add_circle(
        self, center: numpy.ndarray[numpy.float64[2, 1]], *, r: float = 1.0
    ) -> Circle: ...
    def add_polygon(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> Polygon: ...
    def add_polyline(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> Polyline: ...
    def add_text(
        self,
        position: numpy.ndarray[numpy.float64[2, 1]],
        *,
        text: str,
        fontsize: float = 10.0,
    ) -> Text: ...
    def as_circle(self, index: int) -> Circle: ...
    def as_polygon(self, index: int) -> Polygon: ...
    def as_polyline(self, index: int) -> Polyline: ...
    def as_text(self, index: int) -> Text: ...
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> SVG: ...
    @typing.overload
    def background(self) -> Color: ...
    @typing.overload
    def background(self, arg0: Color) -> SVG: ...
    def clone(self) -> SVG: ...
    def dump(self, path: str) -> None: ...
    def empty(self) -> bool: ...
    @typing.overload
    def grid_color(self) -> Color: ...
    @typing.overload
    def grid_color(self, arg0: Color) -> SVG: ...
    @typing.overload
    def grid_step(self) -> float: ...
    @typing.overload
    def grid_step(self, arg0: float) -> SVG: ...
    @typing.overload
    def grid_x(self) -> list[float]: ...
    @typing.overload
    def grid_x(self, arg0: list[float]) -> SVG: ...
    @typing.overload
    def grid_y(self) -> list[float]: ...
    @typing.overload
    def grid_y(self, arg0: list[float]) -> SVG: ...
    @typing.overload
    def height(self) -> float: ...
    @typing.overload
    def height(self, arg0: float) -> SVG: ...
    def is_circle(self, arg0: int) -> bool: ...
    def is_polygon(self, arg0: int) -> bool: ...
    def is_polyline(self, arg0: int) -> bool: ...
    def is_text(self, arg0: int) -> bool: ...
    def num_elements(self) -> int: ...
    def pop(self) -> None: ...
    def to_string(self) -> str: ...
    @typing.overload
    def view_box(self) -> list[float]: ...
    @typing.overload
    def view_box(self, arg0: list[float]) -> SVG: ...
    @typing.overload
    def width(self) -> float: ...
    @typing.overload
    def width(self, arg0: float) -> SVG: ...

class Text:
    @staticmethod
    def html_escape(text: str) -> str: ...
    def __copy__(self, arg0: dict) -> Text: ...
    def __deepcopy__(self, memo: dict) -> Text: ...
    def __init__(
        self,
        position: numpy.ndarray[numpy.float64[2, 1]],
        text: str,
        fontsize: float = 10.0,
    ) -> None: ...
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Text: ...
    def clone(self) -> Text: ...
    @typing.overload
    def fill(self) -> Color: ...
    @typing.overload
    def fill(self, arg0: Color) -> Text: ...
    @typing.overload
    def fontsize(self) -> float: ...
    @typing.overload
    def fontsize(self, arg0: float) -> Text: ...
    @typing.overload
    def lines(self) -> list[str]: ...
    @typing.overload
    def lines(self, arg0: list[str]) -> Text: ...
    @typing.overload
    def position(self) -> numpy.ndarray[numpy.float64[2, 1]]: ...
    @typing.overload
    def position(self, arg0: numpy.ndarray[numpy.float64[2, 1]]) -> Text: ...
    @typing.overload
    def stroke(self) -> Color: ...
    @typing.overload
    def stroke(self, arg0: Color) -> Text: ...
    @typing.overload
    def stroke_width(self) -> float: ...
    @typing.overload
    def stroke_width(self, arg0: float) -> Text: ...
    @typing.overload
    def text(self) -> str: ...
    @typing.overload
    def text(self, arg0: str) -> Text: ...
    def to_string(self) -> str: ...

def add(arg0: int, arg1: int) -> int:
    """
    Add two numbers

    Some other explanation about the add function.
    """

__version__: str = "0.0.3"