# Lab 7 – Bike Share Rental Fuzz Testing

## Objective
To identify and fix input validation bugs in a Python application using Hypothesis fuzz testing.

## Files
| File | Description |
|---|---|
| `bike_share_rental_parser.py` | Fixed bike-share parser application |
| `test_bike_share_rental_parser.py` | Hypothesis fuzz tests |
| `PES1UG24CS365_Rakshan_R_LAB7.pdf` | Screenshots and lab observations |

## Installation
```bash
pip install hypothesis pytest
```

## Run the Application
```bash
python bike_share_rental_parser.py
```

## Run Tests
```bash
python -m pytest test_bike_share_rental_parser.py -v
```

## Changes Made
- Added input validation to all three parser functions.
- Handled invalid and unexpected inputs without crashing.
- Used Hypothesis to generate random inputs and identify bugs.
- Verified the fixes using automated tests.

## Result
All three parser functions were fuzz-tested and updated to handle invalid inputs safely.
