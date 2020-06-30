"""
.. module:: munger
:synopsis: munges COVID-19 and bar exam data
:author: Corey Rayburn Yung
:copyright: 2020
:license: Apache-2.0
"""

import datetime
from typing import Any, Callable, ClassVar, Iterable, Mapping, Sequence, Tuple

import pandas as pd

import bar_exam_covid


def get_previous_day(
        date: datetime.datetime,
        difference: int) -> datetime.datetime:
    return datetime.datetime.strftime(
         date - datetime.timedelta(difference), '%Y-%m-%d')

def get_covid_data(
        covid_data: pd.DataFrame,
        state: str,
        date: datetime.datetime,
        return_column: str) -> int:
    match = covid_data[
        (covid_data['date'] == date) & (covid_data['state'] == state)]
    return match[return_column]

def add_covid_data(
        row: pd.Series, 
        covid_data: pd.DataFrame) -> pd.Series:
    dates = {
        'policy_date_total': row['policy_date'], 
        'current_date_total': get_previous_day(
            date = datetime.datetime.now(), difference = 1),
        'policy_date_previous_week': get_previous_day(
            date = row['policy_date'], difference = 7),
        'current_date_previous_week': get_previous_day(
            date = datetime.datetime.now(), difference = 8)}
    return_columns = ['cases', 'deaths']
    for return_column in return_columns:
        for key, date in dates.items():
            column_name = f'{key}_{return_column}'
            row[column_name] = get_covid_data(
                covid_data = covid_data,
                state = row['state'],
                date = date,
                return_column = return_column)
        row[f'current_weekly_{return_column}'] = (
            row[f'current_date_total_{return_column}']
            - row[f'current_date_previous_week_{return_column}'])
        row[f'policy_date_weekly_{return_column}'] = (
            row[f'policy_date_total_{return_column}']
            - row[f'policy_date_previous_week_{return_column}'])
    return row
