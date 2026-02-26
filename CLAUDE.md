# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**naive-svg** is a C++/Python hybrid library for SVG generation with GeoJSON-to-SVG conversion. C++ core (`src/naive_svg.hpp`) provides SVG primitives via a fluent API, exposed to Python through pybind11 bindings (`src/pybind11_naive_svg.cpp`). A pure-Python module (`src/naive_svg/geojson2svg.py`) handles GeoJSON conversion with WGS84/ENU coordinate transforms.

## Build & Development Commands

```bash
# Build (editable install with C++ compilation)
make build

# Run tests
make pytest                    # runs pytest tests/test_basic.py
pytest tests/test_basic.py     # core tests
pytest tests/test_geojson_showcase.py -v -s  # showcase with SVG output

# Lint (runs pre-commit hooks: ruff, clang-format, cmake-format, mypy)
make lint

# Regenerate type stubs after changing C++ bindings
make restub    # runs pybind11-stubgen, copies to src/naive_svg/_core.pyi
```

## Architecture

### Two-layer design

1. **C++ layer** (`src/naive_svg.hpp`): All SVG types live in `namespace cubao` under `struct SVG`. Element types: `Color`, `Polyline`, `Polygon`, `Circle`, `Text`, `Path`, `Rect`. The `SVG` class is the container that holds elements and produces SVG XML via `write()`/`to_string()`/`dump()`.

2. **Python layer** (`src/naive_svg/`): `_core` is the compiled pybind11 module. `geojson2svg.py` adds GeoJSON parsing, coordinate conversion (via `pybind11_geobuf`), and layered styling.

### Fluent API pattern

The C++ macro `SETUP_FLUENT_API(Klass, VarType, VarName)` generates getter/setter pairs where setters return `Klass&` for chaining. A corresponding pybind11 macro `SETUP_FLUENT_API_PYBIND` mirrors this in Python bindings. When adding new element properties, update both macros.

### Key conventions

- All Python files require `from __future__ import annotations` (enforced by ruff isort).
- C++ formatted with `.clang-format`; Python with `ruff format`.
- Type stubs in `stubs/naive_svg/_core.pyi` are auto-generated — edit the C++ bindings, then `make restub`.
- The C++ header is canonical and synced upstream to `cubao-headers` via `make sync_headers`.

## Source Layout

- `src/naive_svg.hpp` — C++ SVG library (single header)
- `src/pybind11_naive_svg.cpp` — pybind11 bindings
- `src/main.cpp` — PYBIND11_MODULE entry point
- `src/naive_svg/geojson2svg.py` — GeoJSON-to-SVG converter (pure Python)
- `src/naive_svg/_core.pyi` — auto-generated type stubs
- `tests/test_basic.py` — unit tests for C++ bindings and geojson2svg
- `tests/test_geojson_showcase.py` — integration test generating showcase SVG
