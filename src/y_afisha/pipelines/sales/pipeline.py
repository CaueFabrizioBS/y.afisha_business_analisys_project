from kedro.pipeline import Pipeline, node, pipeline

from .nodes import build_buyers, build_order_cohorts, conversion_share, ltv_by_cohort


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(build_buyers, ['visits_clean', 'orders_clean'], 'buyers', name='build_buyers'),
        node(conversion_share, 'buyers', 'conversion', name='conversion_share'),
        node(build_order_cohorts, 'orders_clean', 'order_cohorts', name='build_order_cohorts'),
        node(ltv_by_cohort, 'order_cohorts', 'ltv', name='ltv_by_cohort'),
    ])
