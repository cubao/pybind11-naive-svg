from __future__ import annotations
import numpy
import typing

__all__ = ["Circle", "Color", "Polygon", "Polyline", "SVG", "Text", "add"]

class Circle:
    def __copy__(self, arg0: dict) -> Circle:
        """
        Create a shallow copy of the Circle object
        """
    def __deepcopy__(self, memo: dict) -> Circle:
        """
        Create a deep copy of the Circle object
        """
    def __init__(
        self, center: numpy.ndarray[numpy.float64[2, 1]], r: float = 1.0
    ) -> None:
        """
        Initialize Circle with center point and radius
        """
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Circle: ...
    @typing.overload
    def center(self) -> numpy.ndarray[numpy.float64[2, 1]]:
        """
        Get the center of the Circle
        """
    @typing.overload
    def center(self, arg0: numpy.ndarray[numpy.float64[2, 1]]) -> Circle:
        """
        Set the center of the Circle
        """
    def clone(self) -> Circle:
        """
        Create a deep copy of the Circle object
        """
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
    def to_string(self) -> str:
        """
        Convert Circle to SVG string representation
        """
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
    def parse(arg0: str) -> Color:
        """
        Parse a color from a string representation
        """
    def __copy__(self, arg0: dict) -> Color:
        """
        Create a shallow copy of the Color object
        """
    def __deepcopy__(self, memo: dict) -> Color:
        """
        Create a deep copy of the Color object
        """
    @typing.overload
    def __init__(self, rgb: int = -1) -> None:
        """
        Initialize Color with RGB value
        """
    @typing.overload
    def __init__(self, r: int, g: int, b: int, a: float = -1.0) -> None:
        """
        Initialize Color with R, G, B, and optional Alpha values
        """
    def __repr__(self) -> str:
        """
        Return a string representation of the Color object
        """
    @typing.overload
    def a(self) -> float: ...
    @typing.overload
    def a(self, arg0: float) -> Color: ...
    @typing.overload
    def b(self) -> int: ...
    @typing.overload
    def b(self, arg0: int) -> Color: ...
    def clone(self) -> Color:
        """
        Create a deep copy of the Color object
        """
    @typing.overload
    def g(self) -> int: ...
    @typing.overload
    def g(self, arg0: int) -> Color: ...
    def invalid(self) -> bool:
        """
        Check if the color is invalid
        """
    @typing.overload
    def r(self) -> int: ...
    @typing.overload
    def r(self, arg0: int) -> Color: ...
    def to_string(self) -> str:
        """
        Convert color to string representation
        """

class Polygon:
    def __copy__(self, arg0: dict) -> Polygon:
        """
        Create a shallow copy of the Polygon object
        """
    def __deepcopy__(self, memo: dict) -> Polygon:
        """
        Create a deep copy of the Polygon object
        """
    def __init__(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> None:
        """
        Initialize Polygon with a set of points
        """
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Polygon: ...
    def clone(self) -> Polygon:
        """
        Create a deep copy of the Polygon object
        """
    @typing.overload
    def fill(self) -> Color: ...
    @typing.overload
    def fill(self, arg0: Color) -> Polygon: ...
    def from_numpy(
        self, arg0: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous]
    ) -> Polygon:
        """
        Set Polygon points from NumPy array
        """
    @typing.overload
    def stroke(self) -> Color: ...
    @typing.overload
    def stroke(self, arg0: Color) -> Polygon: ...
    @typing.overload
    def stroke_width(self) -> float: ...
    @typing.overload
    def stroke_width(self, arg0: float) -> Polygon: ...
    def to_numpy(self) -> numpy.ndarray[numpy.float64[m, 2]]:
        """
        Convert Polygon points to NumPy array
        """
    def to_string(self) -> str:
        """
        Convert Polygon to SVG string representation
        """

class Polyline:
    def __copy__(self, arg0: dict) -> Polyline:
        """
        Create a shallow copy of the Polyline object
        """
    def __deepcopy__(self, memo: dict) -> Polyline:
        """
        Create a deep copy of the Polyline object
        """
    def __init__(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> None:
        """
        Initialize Polyline with a set of points
        """
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Polyline: ...
    def clone(self) -> Polyline:
        """
        Create a deep copy of the Polyline object
        """
    @typing.overload
    def fill(self) -> Color: ...
    @typing.overload
    def fill(self, arg0: Color) -> Polyline: ...
    def from_numpy(
        self, arg0: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous]
    ) -> Polyline:
        """
        Set Polyline points from NumPy array
        """
    @typing.overload
    def stroke(self) -> Color: ...
    @typing.overload
    def stroke(self, arg0: Color) -> Polyline: ...
    @typing.overload
    def stroke_width(self) -> float: ...
    @typing.overload
    def stroke_width(self, arg0: float) -> Polyline: ...
    def to_numpy(self) -> numpy.ndarray[numpy.float64[m, 2]]:
        """
        Convert Polyline points to NumPy array
        """
    def to_string(self) -> str:
        """
        Convert Polyline to SVG string representation
        """

class SVG:
    def __copy__(self, arg0: dict) -> SVG:
        """
        Create a shallow copy of the SVG object
        """
    def __deepcopy__(self, memo: dict) -> SVG:
        """
        Create a deep copy of the SVG object
        """
    def __init__(self, width: float, height: float) -> None:
        """
        Initialize SVG with width and height
        """
    @typing.overload
    def add(self, polyline: Polyline) -> Polyline:
        """
        Add a Polyline to the SVG
        """
    @typing.overload
    def add(self, polygon: Polygon) -> Polygon:
        """
        Add a Polygon to the SVG
        """
    @typing.overload
    def add(self, circle: Circle) -> Circle:
        """
        Add a Circle to the SVG
        """
    @typing.overload
    def add(self, text: Text) -> Text:
        """
        Add a Text to the SVG
        """
    def add_circle(
        self, center: numpy.ndarray[numpy.float64[2, 1]], *, r: float = 1.0
    ) -> Circle:
        """
        Add a Circle to the SVG
        """
    def add_polygon(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> Polygon:
        """
        Add a Polygon to the SVG using NumPy array of points
        """
    def add_polyline(
        self,
        points: numpy.ndarray[numpy.float64[m, 2], numpy.ndarray.flags.c_contiguous],
    ) -> Polyline:
        """
        Add a Polyline to the SVG using NumPy array of points
        """
    def add_text(
        self,
        position: numpy.ndarray[numpy.float64[2, 1]],
        *,
        text: str,
        fontsize: float = 10.0,
    ) -> Text:
        """
        Add a Text to the SVG
        """
    def as_circle(self, index: int) -> Circle:
        """
        Get the element at the given index as a Circle
        """
    def as_polygon(self, index: int) -> Polygon:
        """
        Get the element at the given index as a Polygon
        """
    def as_polyline(self, index: int) -> Polyline:
        """
        Get the element at the given index as a Polyline
        """
    def as_text(self, index: int) -> Text:
        """
        Get the element at the given index as a Text
        """
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> SVG: ...
    @typing.overload
    def background(self) -> Color: ...
    @typing.overload
    def background(self, arg0: Color) -> SVG: ...
    def clone(self) -> SVG:
        """
        Create a deep copy of the SVG object
        """
    def dump(self, path: str) -> None:
        """
        Save the SVG to a file
        """
    def empty(self) -> bool:
        """
        Check if the SVG is empty
        """
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
    def is_circle(self, arg0: int) -> bool:
        """
        Check if the element at the given index is a Circle
        """
    def is_polygon(self, arg0: int) -> bool:
        """
        Check if the element at the given index is a Polygon
        """
    def is_polyline(self, arg0: int) -> bool:
        """
        Check if the element at the given index is a Polyline
        """
    def is_text(self, arg0: int) -> bool:
        """
        Check if the element at the given index is a Text
        """
    def num_elements(self) -> int:
        """
        Get the number of elements in the SVG
        """
    def pop(self) -> None:
        """
        Remove the last added element from the SVG
        """
    def to_string(self) -> str:
        """
        Convert the SVG to a string representation
        """
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
    def html_escape(text: str) -> str:
        """
        Escape special characters in the text for HTML
        """
    def __copy__(self, arg0: dict) -> Text:
        """
        Create a shallow copy of the Text object
        """
    def __deepcopy__(self, memo: dict) -> Text:
        """
        Create a deep copy of the Text object
        """
    def __init__(
        self,
        position: numpy.ndarray[numpy.float64[2, 1]],
        text: str,
        fontsize: float = 10.0,
    ) -> None:
        """
        Initialize Text with position, content, and font size
        """
    @typing.overload
    def attrs(self) -> str: ...
    @typing.overload
    def attrs(self, arg0: str) -> Text: ...
    def clone(self) -> Text:
        """
        Create a deep copy of the Text object
        """
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
    def position(self) -> numpy.ndarray[numpy.float64[2, 1]]:
        """
        Get the position of the Text
        """
    @typing.overload
    def position(self, arg0: numpy.ndarray[numpy.float64[2, 1]]) -> Text:
        """
        Set the position of the Text
        """
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
    def to_string(self) -> str:
        """
        Convert Text to SVG string representation
        """

def add(arg0: int, arg1: int) -> int:
    """
    Add two numbers

    Some other explanation about the add function.
    """

__version__: str = "0.0.3"
