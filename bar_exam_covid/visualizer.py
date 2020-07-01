"""
.. module:: visualizer
:synopsis: visualizes COVID-19 and bar exam data
:author: Corey Rayburn Yung
:copyright: 2020
:license: Apache-2.0
"""

import pathlib
from typing import Any, Callable, ClassVar, Iterable, Mapping, Sequence, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def category_plot(data: pd.DataFrame, first: str, second: str) -> object:
    return sns.catplot(
        x = 'state', 
        y = first, 
        hue = second,
        data = data,
        kind = 'bar')

def visualize_combinations(data: pd.DataFrame) -> Sequence[object]:
    visuals = []
    dates = [
        ('policy_date_total', 'current_date_total'),
        ('policy_date_weekly', 'current_date_weekly')]
    measures = ['cases', 'deaths']
    for measure in measures:
        for categories in dates:
            visual = category_plot(
                data = data,
                first = f'{categories[0]}_{measure}',
                second = f'{categories[1]}_{measure}')
            visuals.append(visual)
    return visuals

def visualize(data: pd.DataFrame) -> Sequence[object]:
    sns.set(style = 'whitegrid')
    visual_data = data.loc[
        (data['diploma_privilege'] == 0)
         & (data['remote_testing'] == 0)]
    visual_data = visual_data[visual_data['state'] != 'Guam']
    visual_data = visual_data[visual_data['state'] != 'Virgin Islands']
    return visualize_combinations(data = visual_data)