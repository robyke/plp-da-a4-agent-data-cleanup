
import numpy as np
import pandas as pd

rng = np.random.default_rng(44)

agents = pd.DataFrame({
    "agent_id": [
        "A001", "A002", "A003", "A004", "A005",
        "A006", "A007", "A008", "A009", "A010"
    ],
    "agent_name": [
        "Kamau Agency",
        "Achieng Services",
        "Wanjiku Mobile",
        "Otieno Cash Point",
        "Mwangi Agency",
        "Njeri Services",
        "Omondi Mobile",
        "Chebet Cash Point",
        "Mutiso Agency",
        "Ali Services"
    ],
    "county": [
        "Nairobi",
        "Kisumu",
        "Nakuru",
        "Mombasa",
        "Nairobi",
        "Nakuru",
        "Kisumu",
        "Nairobi",
        "Machakos",
        "Mombasa"
    ]
})

n = 300

dates = pd.to_datetime("2026-01-01") + pd.to_timedelta(
    rng.integers(0, 180, n),
    unit="D"
)

txns = pd.DataFrame({
    "txn_id": [f"T{i:04d}" for i in range(1, n + 1)],
    "agent_id": rng.choice(
        [
            "A001", "A002", "A003", "A004", "A005",
            "A006", "A007", "A008", "A009", "A010",
            "A999"
        ],
        n
    ),
    "txn_type": rng.choice(
        ["Deposit", "Withdrawal"],
        n
    ),
    "amount": rng.integers(
        100,
        30000,
        n
    ).astype(object),
    "txn_date": dates.strftime("%Y-%m-%d")
})

txns.loc[5, "txn_type"] = "deposit"
txns.loc[15, "txn_type"] = "WITHDRAWAL"
txns.loc[25, "txn_type"] = " Deposit "

txns.loc[10, "amount"] = "abc"
txns.loc[20, "amount"] = None
txns.loc[30, "amount"] = "12,500"

txns.loc[40, "amount"] = 250000

txns.loc[12, "txn_date"] = "2026/02/15"
txns.loc[22, "txn_date"] = "15-03-2026"

txns = pd.concat(
    [txns, txns.iloc[[50, 100]]],
    ignore_index=True
)

agents.to_csv("agents.csv", index=False)
txns.to_csv("agent_transactions.csv", index=False)

print("Generated agent_transactions.csv")
print("Generated agents.csv")
print("Transaction rows:", len(txns))
print("Agent rows:", len(agents))
