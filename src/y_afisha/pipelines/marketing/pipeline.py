from kedro.pipeline import Pipeline, node, pipeline

from .nodes import cac_by_source, device_revenue_test, romi_by_cohort, romi_by_source


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(cac_by_source, ['costs_raw', 'buyers'], 'cac_by_source', name='cac_by_source'),
        node(romi_by_cohort, ['order_cohorts', 'costs_raw'], 'romi_by_cohort', name='romi_by_cohort'),
        node(romi_by_source, ['costs_raw', 'buyers'], 'romi_by_source', name='romi_by_source'),
        node(device_revenue_test, ['buyers', 'params:alpha'], 'device_revenue_test', name='device_revenue_test'),
    ])
