import pandas as pd


def clean_visits(visits: pd.DataFrame) -> pd.DataFrame:
    visits = visits.copy()
    visits.columns = visits.columns.str.lower().str.replace(' ', '_')
    visits['session_duration_sec'] = (visits['end_ts'] - visits['start_ts']).dt.total_seconds()

    # Sessions that end before they start are errors in the record
    return visits[visits['session_duration_sec'] >= 0]


def clean_orders(orders: pd.DataFrame, cutoff_date: str) -> pd.DataFrame:
    orders = orders.copy()
    orders.columns = orders.columns.str.lower().str.replace(' ', '_')

    # Orders after the period of the visits and costs are left out
    return orders[orders['buy_ts'] < cutoff_date]
