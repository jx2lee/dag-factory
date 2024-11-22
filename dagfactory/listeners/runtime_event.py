from airflow.listeners import hookimpl
from airflow.models import DagRun
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.state import State

from dagfactory import telemetry

log = LoggingMixin().log


def _get_tis_metric(dag_run):
    # Fetch all task instances for the given DagRun
    tis = []  # TODO: Fix dag_run.get_task_instances()

    ti_metric = {
        "ti": len(tis),
        "ti_success": 0,
        "ti_failed": 0,
        "ti_skipped": 0,
        "ti_upstream_failed": 0,
    }

    # Count the different states of task instances
    for ti in tis:
        if ti.state == State.SUCCESS:
            ti_metric["ti_success"] += 1
        elif ti.state == State.FAILED:
            ti_metric["ti_failed"] += 1
        elif ti.state == State.SKIPPED:
            ti_metric["ti_skipped"] += 1
        elif ti.state == State.UPSTREAM_FAILED:
            ti_metric["ti_upstream_failed"] += 1

    return ti_metric


@hookimpl
def on_dag_run_success(dag_run: DagRun, msg: str):
    # Collect additional telemetry metrics for the DagRun
    additional_telemetry_metrics = {
        "dag_hash": dag_run.dag_hash,
        "dr_success": 1,
        **_get_tis_metric(dag_run),  # Add task instance metrics
    }

    log.info("========================================")
    log.info("%s", additional_telemetry_metrics)
    log.info("========================================")

    # Emit usage metrics if telemetry is enabled
    telemetry.emit_usage_metrics_if_enabled("dagrun", additional_telemetry_metrics)
