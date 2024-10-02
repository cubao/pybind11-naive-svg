from __future__ import annotations

import colorsys
import os
import random

import numpy as np
from pybind11_geobuf import geojson, tf

from naive_svg import SVG, Color


def random_stroke():
    h, s, v = random.uniform(0, 1), random.uniform(0.4, 1), random.uniform(0.7, 1)
    r, g, b = (np.array(colorsys.hsv_to_rgb(h, s, v)) * 255).astype(np.uint8)
    # return f'#{r:02x}{g:02x}{b:02x}'
    return r, g, b


def geojson2svg(
    input_path: str,
    output_path: str,
    *,
    with_label: bool = False,
    with_grid: bool = True,
):
    fc = geojson.FeatureCollection()
    assert fc.load(input_path), f"failed to load {input_path}"

    strokes = {}
    bbox = None
    svg = SVG(-1, -1)
    anchor = None
    gtypes = set()
    for idx, f in enumerate(fc):
        geom = f.geometry()
        if not geom.is_line_string() and not geom.is_polygon():
            continue
        llas = f.as_numpy()
        gtypes.add(f.geometry().type())
        if anchor is None:
            anchor = np.copy(llas[0])
        props = f.properties()
        ftype = str(props["type"]()) if "type" in props else "unknown"
        if ftype not in strokes:
            strokes[ftype] = random_stroke()
        r, g, b = strokes[ftype]
        enus = tf.lla2enu(llas, anchor_lla=anchor)
        if geom.is_line_string():
            svg.add_polyline(enus[:, :2]).stroke(Color(r, g, b)).stroke_width(0.2)
        else:
            svg.add_polygon(enus[:, :2]).stroke(Color(r, g, b)).fill(
                Color(r, g, b, 0.2)
            ).stroke_width(0.2)
        if with_label:
            fid = str(props["id"]()) if "id" in props else f"f#{idx}"
            svg.add_text(enus[0, :2], text=fid, fontsize=1.0).lines(
                [f"type:{ftype}", f"index={idx}"]
            )
        emin = enus.min(axis=0)[:2]
        emax = enus.max(axis=0)[:2]
        if bbox is None:
            bbox = np.array([*emin, *emax])
        else:
            bbox[:2] = np.min([bbox[:2], emin], axis=0)
            bbox[2:] = np.max([bbox[2:], emax], axis=0)
    bbox[:2] -= 10.0
    bbox[2:] -= 10.0
    width, height = bbox[2:] - bbox[:2]

    llas = tf.enu2lla([[*bbox[:2], 0.0], [*bbox[2:], 0.0]], anchor_lla=anchor)
    llas = llas.round(5)[:, :2]
    svg.width(width).height(height)
    if with_grid:
        svg.grid_step(100.0)
    svg.view_box([*bbox[:2], width, height])
    svg.attrs(f"bbox='{llas.reshape(-1).tolist()}'")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    return svg.dump(output_path)


if __name__ == "__main__":
    import fire

    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(geojson2svg)
