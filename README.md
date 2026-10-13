# Mobile Money Agent Network Data Clean-Up

## Project Summary

This project cleans and validates a mobile money agent transaction dataset. The workflow removes duplicate transaction IDs, standardises transaction types, fixes invalid and missing amounts, converts transaction dates into ISO format, flags outliers using the IQR method, merges agent county information, and produces summary tables for analysis.

## How to Regenerate the Data

Run:

python generate_data.py

This creates the raw transaction and agent reference CSV files using random seed 44.

## How to Run the Cleaning Pipeline

Open `agent_cleanup.ipynb` in Google Colab or Jupyter Notebook and run all cells from top to bottom.

The notebook imports and calls `clean_agent_data()` from `cleaning_pipeline.py`.

## Before and After Row Count

The generated raw transaction dataset contains 302 rows.

After removing duplicate transaction IDs, the cleaned dataset contains 300 rows.

## Output

The cleaned dataset is saved to:

`outputs/agent_transactions_clean.csv`

The final output contains no duplicate transaction IDs, standardised transaction types, numeric amounts, ISO-formatted transaction dates, the `amount_imputed` and `is_outlier` flag columns, and agent county information.

## Data Quality Checks

The notebook includes:

- A data-quality audit table
- Post-merge row-count validation
- Unknown-agent checks
- A county summary table
- A weekly pivot table
- A Data Quality Report organised by the six dimensions of data quality
