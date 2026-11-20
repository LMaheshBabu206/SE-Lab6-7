# Fuel Station — Lab 6 and Lab 7 completion

This package follows the two uploaded lab handouts and keeps Lab 6 and Lab 7 in separate folders because they are separate exercises.

## Lab 6 — Code and branch coverage

Files: `Lab 6/fuel_station.py`, `Lab 6/test_fuel_station.py`.

From the `Lab 6` folder, run:

```bash
python -m pip install pytest coverage
coverage erase
coverage run -m pytest -v
coverage report -m
coverage erase
coverage run --branch -m pytest -v
coverage report -m
```

Save terminal screenshots after the coverage report reaches at least 90%. The handout requests separate application/test artifacts for code and branch coverage; the same comprehensive test suite is used for both runs here.

## Lab 7 — Hypothesis fuzz testing

Files: `Lab 7/fuel_station_buggy.py` (the original buggy implementation for the before-fix demonstration), `Lab 7/fuel_station.py` (hardened implementation), and `Lab 7/test_fuel_station.py`.

From the `Lab 7` folder, run:

```bash
python -m pip install pytest hypothesis
python fuel_station_buggy.py
python -m pytest -q
python fuel_station.py
python -m pytest -q
```

The buggy version is a library module without an interactive demo; use Python calls or the tests to demonstrate its failures. The hardened `fuel_station.py` has a safe interactive `main()` that reports invalid inputs rather than terminating with uncaught validation errors.

## Git commits required by the Lab 6 handout

The handout explicitly asks for at least two commits: one for the code-coverage tests and another for the branch-coverage tests. After capturing the reports, create the commits in your own writable clone. Do not claim screenshots or commits until they have actually been produced.
