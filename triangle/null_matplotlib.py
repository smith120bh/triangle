# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    import numpy as np
    from matplotlib.axes import Axes as ax
    from matplotlib.figure import Figure, SubFigure


class fake_axes:
    def __init__(self) -> None:
        self.axes = self

    @staticmethod
    def axis(lim: Optional[tuple[float, float, float, float]] = None) -> None:
        pass

    @staticmethod
    def set_aspect(aspect: str) -> None:
        pass

    @staticmethod
    def get_xaxis() -> "Axes":
        return fake_axes()

    @staticmethod
    def get_yaxis() -> "Axes":
        return fake_axes()

    @staticmethod
    def set_visible(visible: bool) -> None:
        pass

    @staticmethod
    def scatter(x: "np.ndarray", y: "np.ndarray", **kw: Any) -> None:
        pass

    @staticmethod
    def text(x: float, y: float, s: str, **kw: Any) -> None:
        pass

    @staticmethod
    def fill(x: list, y: list, **kw: Any) -> None:
        pass

    @staticmethod
    def triplot(
        x: "np.ndarray", y: "np.ndarray", triangles: "np.ndarray", color: str
    ) -> None:
        pass


if TYPE_CHECKING:
    Axes = Union[ax, fake_axes]


class plt:
    @staticmethod
    def figure(num: "Figure|SubFigure", figsize: tuple[float, float]) -> "Axes":
        return fake_axes()

    @staticmethod
    def subplot(
        num: int, sharex: Optional["Axes"] = None, sharey: Optional["Axes"] = None
    ) -> "Axes":
        return fake_axes()

    @staticmethod
    def tight_layout() -> None:
        pass

    @staticmethod
    def axes() -> "Axes":
        return fake_axes()

    @staticmethod
    def show() -> None:
        pass
