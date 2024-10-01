# Fear & Greed Index for Crypto Markets

## Introduction

The **Fear & Greed Index** is designed to measure the sentiment of the crypto market, focusing on **Bitcoin (BTC)** and **Ethereum (ETH)**. This project aims to create an index that reflects the overall market sentiment by analyzing data from perpetual swaps, futures, and options.

## Project Structure

```bash
fear_greed_index_project/
│
├── data/                     # Folder for raw data, preprocessed data, etc.
│   ├── raw/                  # Raw data collected from APIs
│   └── processed/            # Cleaned and preprocessed data
│
├── notebooks/                # Jupyter notebooks for exploratory data analysis (EDA)
│   └── eda_fear_greed.ipynb  # Example notebook for EDA
│
├── src/                      # Main source code for the project
│   ├── __init__.py           # Marks the src directory as a Python module
│   ├── market_data/          # Folder for data fetching and handling classes
│   │   ├── __init__.py
│   │   ├── crypto_market_data.py       # Base class for market data
│   │   ├── perpetual_swaps_data.py     # Handles perpetual swaps data
│   │   ├── futures_data.py             # Handles futures data and annualized basis
│   │   └── options_data.py             # Handles options data (IV and skew)
│   │
│   ├── calculators/          # Folder for classes that perform index calculations
│   │   ├── __init__.py
│   │   └── fear_greed_calculator.py    # Main class for calculating Fear & Greed Index
│   │
│   ├── validation/           # Folder for backtesting and validation classes
│   │   ├── __init__.py
│   │   └── backtesting.py             # Class for backtesting the index
│   │
│   └── utils/                # Utility functions (data normalization, scaling, etc.)
│       ├── __init__.py
│       └── normalization.py          # Functions to normalize data (e.g., z-score, min-max)
│
├── tests/                    # Unit tests for the project
│   ├── test_perpetual_swaps.py        # Tests for perpetual swaps data handling
│   ├── test_futures_data.py           # Tests for futures data handling
│   ├── test_options_data.py           # Tests for options data handling
│   ├── test_fear_greed_calculator.py   # Tests for Fear & Greed index calculation
│   └── test_backtesting.py            # Tests for backtesting logic
│
├── config/                   # Configuration files for APIs, environment variables, etc.
│   ├── config.yml            # Configuration file for API keys and other settings
│   └── secrets.yml           # Separate file for sensitive information (e.g., API keys)
│
├── logs/                     # Log files for the system (for debugging or audit purposes)
│   └── app.log               # Example log file
│
├── .gitignore                # Git ignore file to avoid committing unnecessary files (e.g., data, logs)
├── README.md                 # Project documentation (overview, instructions, etc.)
├── requirements.txt          # Python dependencies required for the project
└── setup.py                  # Script to install the project as a package (if needed)

```
