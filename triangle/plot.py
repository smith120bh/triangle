from typing import TYPE_CHECKING, Union

import numpy as np

try:
    from matplotlib import pyplot as plt
except ImportError:
    from .null_matplotlib import plt  # type: ignore

if TYPE_CHECKING:
    from matplotlib.axes import Axes as ax
    from matplotlib.figure import Figure, SubFigure

    from .null_matplotlib import Axes as ax_null

    Axes = Union[ax, ax_null]


def compare(
    fig: "Figure|SubFigure",
    A: dict[str, np.ndarray],
    B: dict[str, np.ndarray],
    figsize: tuple[float, float] = (6, 3),
) -> None:
    plt.figure(num=fig, figsize=figsize)
    ax1 = plt.subplot(121)
    plot(ax1, **A)
    lim = ax1.axis()
    ax2 = plt.subplot(122, sharey=ax1)
    plot(ax2, **B)
    ax2.axis(lim)
    plt.tight_layout()


def comparev(
    fig: "Figure|SubFigure",
    A: dict[str, np.ndarray],
    B: dict[str, np.ndarray],
    figsize: tuple[float, float] = (3, 6),
) -> None:
    plt.figure(num=fig, figsize=figsize)
    ax1 = plt.subplot(211)
    plot(ax1, **A)
    lim = ax1.axis()
    ax2 = plt.subplot(212, sharex=ax1)
    plot(ax2, **B)
    ax2.axis(lim)
    plt.tight_layout()


def plot(ax: "Axes", **kw: np.ndarray) -> None:
    assert ax.axes is not None
    ax.axes.set_aspect("equal")
    vertices(ax, **kw)
    if "segments" in kw:
        segments(ax, **kw)
    if "triangles" in kw:
        triangles(ax, **kw)
    if "holes" in kw:
        holes(ax, **kw)
    if "edges" in kw:
        edges(ax, **kw)
    if "regions" in kw:
        regions(ax, **kw)
    if "triangle_attributes" in kw:
        triangle_attributes(ax, **kw)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


def vertices(ax: "Axes", **kw: np.ndarray) -> None:
    verts = np.array(kw["vertices"])
    ax.scatter(*verts.T, color="k")
    if "labels" in kw:
        for i in range(verts.shape[0]):
            ax.text(verts[i, 0], verts[i, 1], str(i))
    if "markers" in kw:
        vm = kw["vertex_markers"]
        for i in range(verts.shape[0]):
            ax.text(verts[i, 0], verts[i, 1], str(vm[i]))


def segments(ax: "Axes", **kw: np.ndarray) -> None:
    verts = np.array(kw["vertices"])
    segs = np.array(kw["segments"])
    for beg, end in segs:
        x0, y0 = verts[beg, :]
        x1, y1 = verts[end, :]
        ax.fill(
            [x0, x1],
            [y0, y1],
            facecolor="none",
            edgecolor="r",
            linewidth=3,
            zorder=0,
        )


def triangles(ax: "Axes", **kw: np.ndarray) -> None:
    verts = np.array(kw["vertices"])
    ax.triplot(verts[:, 0], verts[:, 1], kw["triangles"], "ko-")


def holes(ax: "Axes", **kw: np.ndarray) -> None:
    holes_arr = np.array(kw["holes"])
    ax.scatter(*holes_arr.T, marker="x", color="r")  # type: ignore


def edges(ax: "Axes", **kw: np.ndarray) -> None:
    """
    Plot regular edges and rays (edges whose one endpoint is at infinity)
    """
    verts_arr = kw["vertices"]
    edges_arr = kw["edges"]
    for beg, end in edges_arr:
        x0, y0 = verts_arr[beg, :]
        x1, y1 = verts_arr[end, :]
        ax.fill(
            [x0, x1],
            [y0, y1],
            facecolor="none",
            edgecolor="k",
            linewidth=0.5,
        )

    if ("ray_origins" not in kw) or ("ray_directions" not in kw):
        return

    lim = ax.axis()
    ray_origin = kw["ray_origins"]
    ray_direct = kw["ray_directions"]
    for beg, (vx, vy) in zip(ray_origin.flatten(), ray_direct):
        x0, y0 = verts_arr[beg, :]
        scale = 100.0  # some large number
        x1, y1 = x0 + scale * vx, y0 + scale * vy
        ax.fill(
            [x0, x1],
            [y0, y1],
            facecolor="none",
            edgecolor="k",
            linewidth=0.5,
        )
    ax.axis(lim)  # make sure figure is not rescaled by ifinite ray


def regions(ax: "Axes", **kw: np.ndarray) -> None:
    """
    Plot regions labeled by region
    """
    regions_arr = np.array(kw["regions"])
    ax.scatter(regions_arr[:, 0], regions_arr[:, 1], marker="*", color="b")
    for x, y, r, _ in regions_arr:
        ax.text(x, y, f" {r}", color="b", va="center")


def triangle_attributes(ax: "Axes", **kw: np.ndarray) -> None:
    """
    Plot triangle attributes labeled by region
    """
    verts = np.array(kw["vertices"])
    tris = np.array(kw["triangles"])
    attrs = np.array(kw["triangle_attributes"]).flatten()
    centroids = verts[tris].mean(axis=1)
    ax.scatter(
        centroids[:, 0],
        centroids[:, 1],
        marker=".",
        color="m",
        zorder=1,
    )
    for (x, y), r in zip(centroids, attrs):
        ax.text(x, y, f" {r}", color="m", zorder=1, va="center")
