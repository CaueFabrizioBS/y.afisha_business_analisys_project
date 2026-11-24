import pandas as pd
from scipy import stats as st


def cac_by_source(costs: pd.DataFrame, buyers: pd.DataFrame) -> pd.DataFrame:
    cac = pd.DataFrame({
        'costs': costs.groupby('source_id')['costs'].sum(),
        'customers': buyers.groupby('source_id').size(),
    })
    cac['cac'] = cac['costs'] / cac['customers']
    return cac.sort_values('cac').round(2)


def romi_by_cohort(cohorts: pd.DataFrame, costs: pd.DataFrame) -> pd.DataFrame:
    cohorts = cohorts.copy()
    costs_by_month = costs.groupby(costs['dt'].dt.to_period('M').astype(str))['costs'].sum()

    # CAC of a cohort = costs of the month / new customers of the month
    new_customers = cohorts.groupby('first_order_month')['n_buyers'].first()
    cohort_cac = costs_by_month / new_customers

    cohorts['romi'] = cohorts['revenue'] / cohorts['n_buyers'] / cohorts['first_order_month'].map(cohort_cac)
    return cohorts.pivot_table(index='first_order_month', columns='age', values='romi').cumsum(axis=1).round(2)


def romi_by_source(costs: pd.DataFrame, buyers: pd.DataFrame) -> pd.DataFrame:
    romi = pd.DataFrame({
        'revenue': buyers.groupby('source_id')['revenue'].sum(),
        'costs': costs.groupby('source_id')['costs'].sum(),
    })
    romi['romi'] = romi['revenue'] / romi['costs']
    return romi.sort_values('romi').round(2)


def device_revenue_test(buyers: pd.DataFrame, alpha: float) -> pd.DataFrame:
    desktop_revenue = buyers[buyers['device'] == 'desktop']['revenue']
    touch_revenue = buyers[buyers['device'] == 'touch']['revenue']

    # Levene passes, but the variances are about 13 times apart (big orders on desktop),
    # so Welch's t-test (equal_var=False) is the safer choice
    levene_pvalue = st.levene(desktop_revenue, touch_revenue).pvalue
    ttest_pvalue = st.ttest_ind(desktop_revenue, touch_revenue, equal_var=False).pvalue

    return pd.DataFrame({
        'desktop_mean': [desktop_revenue.mean()],
        'touch_mean': [touch_revenue.mean()],
        'levene_pvalue': [levene_pvalue],
        'ttest_pvalue': [ttest_pvalue],
        'result': ['We reject the null hypothesis' if ttest_pvalue < alpha else 'We cannot reject the null hypothesis'],
    }).round(4)
