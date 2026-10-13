
import pandas as pd
import numpy as np


def clean_agent_data(txns, agents):
    """
    Clean mobile money transaction data and merge agent details.

    Parameters
    ----------
    txns : pandas.DataFrame
        Raw transaction data.
    agents : pandas.DataFrame
        Agent reference data.

    Returns
    -------
    clean_df : pandas.DataFrame
        Cleaned transaction data with agent county information.
    log : list
        Cleaning log describing each change made.
    """

    log = []
    df = txns.copy()

    # 1. Remove duplicate transaction IDs
    before = len(df)
    df = df.drop_duplicates(subset=["txn_id"]).copy()
    removed_duplicates = before - len(df)
    log.append(f"Removed {removed_duplicates} duplicate transaction rows")

    # 2. Standardise transaction type
    df["txn_type"] = (
        df["txn_type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    valid_types = ["Deposit", "Withdrawal"]
    invalid_types = (~df["txn_type"].isin(valid_types)).sum()

    df.loc[
        ~df["txn_type"].isin(valid_types),
        "txn_type"
    ] = np.nan

    log.append(
        f"Found {invalid_types} invalid transaction type values"
    )

    # 3. Clean amount column
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Flag missing or invalid amounts before filling
    df["amount_imputed"] = df["amount"].isna()

    missing_amounts = int(df["amount_imputed"].sum())

    median_amount = df["amount"].median()

    df["amount"] = df["amount"].fillna(
        median_amount
    )

    log.append(
        f"Imputed {missing_amounts} missing or invalid amounts with the median"
    )

    # 4. Clean transaction dates
    original_dates = df["txn_date"].copy()

    df["txn_date"] = pd.to_datetime(
        df["txn_date"],
        errors="coerce",
        dayfirst=False
    )

    # Retry unresolved dates using day-first parsing
    unresolved = df["txn_date"].isna()

    if unresolved.any():
        df.loc[unresolved, "txn_date"] = pd.to_datetime(
            original_dates[unresolved],
            errors="coerce",
            dayfirst=True
        )

    invalid_dates = int(df["txn_date"].isna().sum())

    log.append(
        f"Found {invalid_dates} transaction dates that could not be parsed"
    )

    # 5. Flag amount outliers using IQR
    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1

    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    df["is_outlier"] = (
        (df["amount"] < lower_fence)
        | (df["amount"] > upper_fence)
    )

    outlier_count = int(df["is_outlier"].sum())

    log.append(
        f"Flagged {outlier_count} amount outliers using the IQR method"
    )

    # 6. Merge agent information
    before_merge = len(df)

    clean_df = df.merge(
        agents,
        on="agent_id",
        how="left",
        validate="many_to_one"
    )

    after_merge = len(clean_df)

    unknown_agents = int(
        clean_df["county"].isna().sum()
    )

    log.append(
        f"Merged agent data: {before_merge} rows before merge and "
        f"{after_merge} rows after merge"
    )

    log.append(
        f"Found {unknown_agents} transactions with unknown agents"
    )

    # 7. Format dates as ISO YYYY-MM-DD
    clean_df["txn_date"] = clean_df["txn_date"].dt.strftime(
        "%Y-%m-%d"
    )

    return clean_df, log
