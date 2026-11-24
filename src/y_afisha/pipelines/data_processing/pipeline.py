from kedro.pipeline import Pipeline, node, pipeline

from .nodes import clean_orders, clean_visits


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(clean_visits, 'visits_raw', 'visits_clean', name='clean_visits'),
        node(clean_orders, ['orders_raw', 'params:cutoff_date'], 'orders_clean', name='clean_orders'),
    ])
