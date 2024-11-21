from airflow.listeners import hookimpl
from airflow.models import DagRun
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log


@hookimpl
def on_dag_run_running(dag_run: DagRun, msg: str):
    log.info("=========DAG run pankaj!===========")
    log.info(dag_run.dag.__dict__)
    log.info(f"====={msg}============")
