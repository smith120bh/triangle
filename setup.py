from typing import Optional

from setuptools import Extension, setup

define_macros: list[tuple[str, Optional[str]]] = [
    ("VOID", "void"),
    ("REAL", "double"),
    ("NO_TIMER", "1"),
    ("TRILIBRARY", "1"),
    ("ANSI_DECLARATORS", "1"),
]

ext_modules: list[Extension] = [
    Extension(
        "triangle.core",
        ["triangle-c/triangle.c", "triangle/core.c"],
        include_dirs=["triangle-c"],
        define_macros=define_macros,
        # extra_compile_args=['-g'],
    ),
]

# see pyproject.toml for other metadata
setup(
    name="triangle",
    ext_modules=ext_modules,
)
