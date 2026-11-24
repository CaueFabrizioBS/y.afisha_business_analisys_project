import pandas as pd


def build_buyers(visits: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # Device and source of the first visit: how the customer arrived at the site
    first_visits = (
        visits.sort_values('start_ts')
        .groupby('uid')
        .first()[['start_ts', 'device', 'source_id']]
        .rename(columns={'start_ts': 'first_visit'})
    )
    customers = orders.groupby('uid').agg(first_order=('buy_ts', 'min'), revenue=('revenue', 'sum'))

    buyers = first_visits.join(customers, how='inner')
    # Calendar days: an order on the day after the first visit counts as 1 day, even if less than 24 hours passed
    buyers['days_to_buy'] = (buyers['first_order'].dt.normalize() - buyers['first_visit'].dt.normalize()).dt.days
    return buyers.reset_index()


def conversion_share(buyers: pd.DataFrame) -> pd.DataFrame:
    groups = pd.cut(
        buyers['days_to_buy'],
        bins=[-1, 0, 1, 7, 30, 365],
        labels=['0d', '1d', '2-7d', '8-30d', 'more than 30d'],
    )
    return groups.value_counts(normalize=True).sort_index().round(4).rename('share').reset_index()


def build_order_cohorts(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    orders['order_month'] = orders['buy_ts'].dt.to_period('M')
    orders['first_order_month'] = orders.groupby('uid')['order_month'].transform('min')
    orders['age'] = (
        (orders['order_month'].dt.year - orders['first_order_month'].dt.year) * 12
        + (orders['order_month'].dt.month - orders['first_order_month'].dt.month)
    )

    cohorts = (
        orders.groupby(['first_order_month', 'age'])
        .agg(n_orders=('uid', 'count'), revenue=('revenue', 'sum'))
        .reset_index()
    )
    cohorts['n_buyers'] = cohorts['first_order_month'].map(orders.groupby('first_order_month')['uid'].nunique())
    cohorts['first_order_month'] = cohorts['first_order_month'].astype(str)
    return cohorts


def ltv_by_cohort(cohorts: pd.DataFrame) -> pd.DataFrame:
    # The revenue is taken as Y.Afisha's own money, so the margin is 100%
    cohorts = cohorts.copy()
    cohorts['ltv'] = cohorts['revenue'] / cohorts['n_buyers']
    return cohorts.pivot_table(index='first_order_month', columns='age', values='ltv').cumsum(axis=1).round(2)
