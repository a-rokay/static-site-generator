# Contributing
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Please be sure to format and lint before submitting a pull request!

## Formatting

##### This project uses [Python Black](https://pypi.org/project/black/).
#### Installation

`pip install black`

#### Usage

To format the **whole** project, run`black.sh`. This script will run Python Black against `ssg/`.

To format **single files**, run `python -m black {source_file_or_directory}`.

## Linting
##### This project uses [Flake8](https://flake8.pycqa.org/en/latest/index.html).

#### Installation

`pip install flake8`

#### Usage

To lint the **whole** project, run`flake8.sh`. This script will run flake8 against `ssg/`.

To lint **single files**, run `python -m flake8 {source_file_or_directory}`.

## Visual Studio Code
The project contains the necessary settings for both Python Black and Flake8 to automatically run. All you have to do is save a file. Keep an eye on the `Problems` tab for any issues.

## Testing
Please ensure all tests pass before submitting a PR.

#### Installation
`pip install pytest`

#### Usage
`python -m pytest`

When writing a new function, writing a test in `tests/` would be appreciated. You can follow the existing tests as a guideline.
