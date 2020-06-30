"""
.. module:: loader
:synopsis: loads COVID-19 and bar exam data
:author: Corey Rayburn Yung
:copyright: 2020
:license: Apache-2.0
"""

import pathlib
from typing import Any, Callable, ClassVar, Iterable, Mapping, Sequence, Union

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

GOOGLE_API_KEY = pathlib.Path('..') / '..' / 'keys' / 'barexamcovid.json'

BAR_EXAM_FILE = 'Bar Exams and COVID 2020'
BAR_EXAM_COLUMNS = {
    'state': str,
    'abbreviation': str,
    'diploma_privilege': bool, 
    'summer_exam': bool,
    'fall_exam': bool,
    'remote_testing': bool,
    'masks_required': bool,
    'masks_not_required': bool,
    'no_mask_policy': bool,
    'separation_policy': bool,	
    'door_screening': bool,	
    'internship_policy': bool,
    'policy_date': str}

COVID_URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
COVID_COLUMNS = {
    'date': str,
    'state': str,
    'fips': int,
    'cases': int,
    'deaths': int}


def fix_columns(
        df: pd.DataFrame, 
        datatypes: Mapping[str, Any]) -> pd.DataFrame:
    for key, value in datatypes.items():
        df[key] = df[key].astype(value)
    df = df[list(datatypes.keys())]
    df['state'] = df['state'].str.strip()
    return df

def get_covid_data() -> pd.DataFrame:
    df = pd.read_csv(COVID_URL)
    df = fix_columns(df = df, datatypes = COVID_COLUMNS)
    df['date'] = pd.to_datetime(
        df['date'], 
        infer_datetime_format = True)
    return df

def get_bar_exam_data() -> pd.DataFrame:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_API_KEY, 
        scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(BAR_EXAM_FILE).sheet1
    data = worksheet.get_all_values()
    header = data.pop(0)
    df = pd.DataFrame(data, columns = header)
    df = fix_columns(df = df, datatypes = BAR_EXAM_COLUMNS)
    df['policy_date'] = pd.to_datetime(
        df['policy_date'],  
        infer_datetime_format = True)
    return df