"""
.. module:: visualizer
:synopsis: visualizes COVID-19 and bar exam data
:author: Corey Rayburn Yung
:copyright: 2020
:license: Apache-2.0
"""

import pathlib
from typing import Any, Callable, ClassVar, Iterable, Mapping, Sequence, Tuple

import pandas as pd


def visualize(data: pd.DataFrame) -> Sequence[object]:
    visuals = []
    return visuals