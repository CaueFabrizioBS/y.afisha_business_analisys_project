from kedro.pipeline import Pipeline, node, pipeline

from .nodes import audience_metrics, retention_by_cohort


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(audience_metrics, 'visits_clean', 'product_metrics', name='audience_metrics'),
        node(retention_by_cohort, 'visits_clean', 'retention', name='retention_by_cohort'),
    ])
