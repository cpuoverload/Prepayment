## Installation

```bash
conda create -n prepayment python=3.10 -y
conda activate prepayment

poetry install
```

## Run

```bash
PYTHONPATH=src python src/main.py
```

You will be prompted to input the month:

```bash
Please input the month (e.g. Apr 2024):
```

The output will be saved to `data/Accounting Entries.csv`.

## Tests

```bash
pytest
```
