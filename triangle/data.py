import os
import re
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np

from triangle.plot import plot


def remove_comments(s: str) -> str:
    return re.sub("#.*\n", "", s)


def split(tup: Sequence, pos: int) -> tuple:
    return tup[:pos], tup[pos:]


def loads(
    node: str | None = None,
    ele: str | None = None,
    poly: str | None = None,
    area: str | None = None,
    edge: str | None = None,
    neigh: str | None = None,
) -> dict[str, np.ndarray]:
    """
    Load a dictionary representing the triangle data from strings.
    """

    class var:
        start_at_zero = True

    data = {}

    def _vertices(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 4)
        N_vertices, dim, N_attr, N_bnd_markers = list(map(int, head))
        if N_vertices == 0:
            return tokens

        head, tokens = split(
            tokens,
            N_vertices * (1 + dim + N_attr + N_bnd_markers),
        )
        v = np.array(head).reshape(-1, 1 + dim + N_attr + N_bnd_markers)
        # check if starting at zero or one

        var.start_at_zero = v[0, 0] == "0"
        data["vertices"] = np.array(v[:, 1:3], dtype="double")
        if N_attr > 0:
            data["vertex_attributes"] = np.array(
                v[:, 3 : 3 + N_attr],
                dtype="double",
            )
        if N_bnd_markers > 0:
            data["vertex_markers"] = np.array(
                v[:, 3 + N_attr : 3 + N_attr + N_bnd_markers],
                dtype="intc",
            )

        return tokens

    def _ele(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 3)
        N_triangles, N_nodes, N_attr = list(map(int, head))
        if N_triangles == 0:
            return tokens

        head, tokens = split(tokens, N_triangles * (1 + N_nodes + N_attr))
        v = np.array(head).reshape(-1, 1 + N_nodes + N_attr)
        data["triangles"] = np.array(v[:, 1 : N_nodes + 1], dtype="intc")
        if not var.start_at_zero:
            data["triangles"] -= 1
        if N_attr > 0:
            data["triangle_attributes"] = np.array(
                v[:, N_nodes + 1 : N_nodes + 1 + N_attr],
                dtype="double",
            )

        return tokens

    def _segments(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 2)
        N_segments, N_bnd_markers = list(map(int, head))
        if N_segments == 0:
            return tokens

        head, tokens = split(tokens, N_segments * (3 + N_bnd_markers))
        v = np.array(head).reshape(-1, 3 + N_bnd_markers)
        data["segments"] = np.array(v[:, 1:3], dtype="intc")
        if not var.start_at_zero:
            data["segments"] -= 1
        if N_bnd_markers > 0:
            data["segment_markers"] = np.array(
                v[:, 3 : 3 + N_bnd_markers],
                dtype="intc",
            )

        return tokens

    def _holes(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 1)
        N_holes = int(head[0])
        if N_holes == 0:
            return tokens

        head, tokens = split(tokens, N_holes * 3)
        v = np.array(head).reshape(-1, 3)
        data["holes"] = np.array(v[:, 1:3], dtype="double")

        return tokens

    def _area(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 1)
        N_areas = int(head[0])
        if N_areas == 0:
            return tokens

        head, tokens = split(tokens, N_areas * 2)
        v = np.array(head).reshape(-1, 2)
        data["triangle_max_area"] = np.array(v[:, 1:2], dtype="double")
        return tokens

    def _edge(inpt: str) -> None:
        tokens = inpt.split("\n")
        head, tokens = split(tokens, 1)
        N_edges, N_bnd_markers = list(map(int, head[0].split()))
        if N_edges == 0:
            return

        tokens_split = [x.split() for x in tokens]
        edges = [x for x in tokens_split if len(x) == (3 + N_bnd_markers)]
        rays = [x for x in tokens_split if len(x) == (5 + N_bnd_markers)]
        edges_arr = np.array(edges)
        rays_arr = np.array(rays)
        data["edges"] = np.array(edges_arr[:, 1:3], dtype="intc")
        data["ray_origins"] = np.array(rays_arr[:, 1:2], dtype="intc")
        data["ray_directions"] = np.array(rays_arr[:, 3:], dtype="double")

        if not var.start_at_zero:
            data["edges"] -= 1
            data["ray_origins"] -= 1

    def _regions(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 1)
        N_areas = int(head[0])
        if N_areas == 0:
            return tokens

        # number of fields must be equal to 4 according to spec,
        # but it is only 3 in la.poly
        head, tokens = split(tokens, N_areas * 4)
        v = np.array(head).reshape(-1, 4)
        regs = np.array(v[:, 1:4], dtype="double")
        # add an extra column to make fields equal to 4
        regs = np.hstack(
            (
                regs[:, 0:2],
                np.zeros((regs.shape[0], 1)),
                regs[:, 2:3],
            )
        )
        data["regions"] = regs
        return tokens

    def _neigh(tokens: Sequence[str]) -> Sequence[str]:
        head, tokens = split(tokens, 2)
        N_triangles, N_neighs = list(map(int, head))
        if N_triangles == 0:
            return tokens

        head, tokens = split(tokens, N_triangles * (1 + N_neighs))
        v = np.array(head).reshape(-1, 1 + N_neighs)
        data["triangle_neighbors"] = np.array(v[:, 1:], dtype="intc")
        if not var.start_at_zero:
            data["triangle_neighbors"] -= 1
        return tokens

    if node:
        tok: Sequence[str] = remove_comments(node).split()
        _vertices(tok)
    if ele:
        tok = remove_comments(ele).split()
        _ele(tok)
    if poly:
        tok = remove_comments(poly).split()
        tok = _vertices(tok)
        tok = _segments(tok)
        tok = _holes(tok)
        if tok:
            _regions(tok)
    if area:
        tok = remove_comments(area).split()
        _area(tok)
    if edge:
        _edge(remove_comments(edge))
    if neigh:
        tok = remove_comments(neigh).split()
        _neigh(tok)

    return data


def load(directory: str, name: str) -> dict[str, np.ndarray]:
    """
    Load a dictionary representing the triangle data from `directory` and `name`.
    """

    data = {}
    for ext in ("node", "ele", "poly", "area", "edge", "neigh"):
        filename = os.path.join(directory, name + "." + ext)
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as f:
                data[ext] = f.read()
    return loads(**data)


def get_data_dir() -> str:
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, "data")


def get_data(name: str) -> dict[str, np.ndarray]:
    """
    Load data samples provided with the module.
    Examples: A, dots, ell, face, ...
    """
    return load(get_data_dir(), name)


def show_data(name: str) -> None:
    d = get_data(name)
    plot(plt.axes(), **d)
    plt.show()
