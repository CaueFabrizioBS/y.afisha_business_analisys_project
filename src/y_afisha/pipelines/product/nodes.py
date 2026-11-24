import pandas as pd


def audience_metrics(visits: pd.DataFrame) -> pd.DataFrame:
    visits = visits.copy()
    visits['session_date'] = visits['start_ts'].dt.date
    visits['session_year'] = visits['start_ts'].dt.isocalendar().year
    visits['session_week'] = visits['start_ts'].dt.isocalendar().week
    visits['session_month'] = visits['start_ts'].dt.to_period('M')

    dau = visits.groupby('session_date')['uid'].nunique().mean()
    wau = visits.groupby(['session_year', 'session_week'])['uid'].nunique().mean()
    mau = visits.groupby('session_month')['uid'].nunique().mean()

    sessions_per_day = visits.groupby('session_date').agg(n_sessions=('uid', 'count'), n_users=('uid', 'nunique'))

    # Zero-second sessions are left out of the session length
    durations = visits.loc[visits['session_duration_sec'] > 0, 'session_duration_sec']

    return pd.DataFrame({
        'metric': [
            'dau', 'wau', 'mau', 'sticky_factor_week', 'sticky_factor_month',
            'sessions_per_user_per_day', 'session_mean_sec', 'session_median_sec', 'session_mode_sec',
        ],
        'value': [
            dau, wau, mau, dau / wau, dau / mau,
            (sessions_per_day['n_sessions'] / sessions_per_day['n_users']).mean(),
            durations.mean(), durations.median(), durations.mode()[0],
        ],
    }).round(3)


def retention_by_cohort(visits: pd.DataFrame) -> pd.DataFrame:
    visits = visits.copy()
    visits['session_month'] = visits['start_ts'].dt.to_period('M')
    visits['first_month'] = visits.groupby('uid')['session_month'].transform('min')
    visits['lifetime'] = (
        (visits['session_month'].dt.year - visits['first_month'].dt.year) * 12
        + (visits['session_month'].dt.month - visits['first_month'].dt.month)
    )

    cohorts = visits.groupby(['first_month', 'lifetime'])['uid'].nunique().reset_index()
    cohorts['cohort_users'] = cohorts.groupby('first_month')['uid'].transform('first')
    cohorts['retention'] = cohorts['uid'] / cohorts['cohort_users']

    return cohorts.pivot_table(index='first_month', columns='lifetime', values='retention').round(4)
