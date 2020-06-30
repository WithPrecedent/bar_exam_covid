"""
.. module:: main entry point for bar_exam_covid
:synopsis: executes bar_exam_covid loading, munging, and visualizing functions.
:author: Corey Rayburn Yung
:copyright: 2020
:license: Apache-2.0
"""

import pathlib
import sys
from typing import Any, Callable, ClassVar, Iterable, Mapping, Sequence, Tuple
import warnings

import bar_exam_covid


def _args_to_dict() -> Mapping[str, str]:
    """Converts command line arguments into 'arguments' dict.
    
    The dictionary conversion is more forgiving than the typical argparse
    construction. It allows the package to check default options and give
    clearer error coding.
    This handy bit of code, as an alternative to argparse, was found here:
        https://stackoverflow.com/questions/54084892/how-to-convert-commandline-key-value-args-to-dictionary
    
    Returns:
        arguments(dict): dictionary of command line options when the options
            are separated by '='.
            
    """
    arguments = {}
    for argument in sys.argv[1:]:
        if '=' in argument:
            separated = argument.find('=')
            key, value = argument[:separated], argument[separated + 1:]
            arguments[key] = value
    return arguments

def main(folder: str = None) -> None:
    """Loads, munges, plots, and exports bar exam and COVID-19 data.
    
    Args:
        folder (str): name of folder to export visualizations to. Defaults to
            None. If not passed, it will be assigned to the current working
            directory.
    
    """
    # Sets 'folder' to current working directory, if not passed.
    folder = folder or pathlib.Path.cwd()
    covid_data = bar_exam_covid.loader.get_covid_data()
    bar_exam_data = bar_exam_covid.loader.get_bar_exam_data() 
    bar_exam_data.dropna(axis = 0, inplace = True)
    bar_exam_data = bar_exam_data.apply(
        bar_exam_covid.munger.add_covid_data,
        covid_data = covid_data,
        axis = 1)
    visualizations = bar_exam_covid.visualizer.visualize(data = bar_exam_data)
    export_visuals(visualizations = visualizations)
    return

def export_visuals(visualizations: Sequence[object]) -> None:
    for visual in visualizations:
        pass
    return

if __name__ == '__main__':
    # Removes various python warnings from console output.
    warnings.filterwarnings('ignore')
    # Gets command line arguments and converts them to dict.
    arguments = _args_to_dict()
    # Calls Project with passed command-line arguments.
    main(arguments.get('-folder'))
