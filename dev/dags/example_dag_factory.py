import os
from pathlib import Path

# The following import is here so Airflow parses this file
# from airflow import DAG
import dagfactory

DEFAULT_CONFIG_ROOT_DIR = "/usr/local/airflow/dags/"
CONFIG_ROOT_DIR = Path(os.getenv("CONFIG_ROOT_DIR", DEFAULT_CONFIG_ROOT_DIR))

config_file = str(CONFIG_ROOT_DIR / "example_dag_factory.yml")

example_dag_factory = dagfactory.DagFactory(config_file)

# Creating task dependencies
example_dag_factory.clean_dags(globals())
example_dag_factory.generate_dags(globals())

"""
{'owner_links': {}, 'user_defined_macros': None, 'user_defined_filters': None, 'default_args': {'owner': 'custom_owner', 'start_date': DateTime(2024, 11, 11, 0, 0, 0, tzinfo=Timezone('UTC')), 'retries': 1, 'on_success_callback_name': 'print_hello_from_callback', 'on_success_callback_file': '/usr/local/airflow/dags//print_hello.py', 'retry_delay': datetime.timedelta(seconds=300), 'on_success_callback': 'def print_hello_from_callback(context):\n    print("hello from callback")\n'}, 'params': {}, '_dag_id': 'example_dag', '_dag_display_property_value': None, '_max_active_tasks': 16, '_pickle_id': None, '_description': 'this is an example dag', 'fileloc': '/usr/local/airflow/dags/example_dag_factory.py', 'task_dict': {'task_1': <Task(BashOperator): task_1>, 'task_2': <Task(BashOperator): task_2>, 'task_3': <Task(PythonOperator): task_3>}, 'timezone': Timezone('UTC'), 'start_date': None, 'end_date': None, 'timetable': <airflow.timetables.interval.CronDataIntervalTimetable object at 0xffff6b7d39b0>, 'schedule_interval': '0 3 * * *', 'template_searchpath': None, 'template_undefined': <class 'jinja2.runtime.StrictUndefined'>, 'last_loaded': datetime.datetime(2024, 11, 20, 14, 4, 44, 379589, tzinfo=Timezone('UTC')), 'safe_dag_id': 'example_dag', 'max_active_runs': 1, 'max_consecutive_failed_dag_runs': 0, 'dagrun_timeout': datetime.timedelta(seconds=600), 'sla_miss_callback': None, '_default_view': 'grid', 'orientation': 'LR', 'catchup': True, 'partial': False, 'on_success_callback': None, 'on_failure_callback': None, 'edge_info': {}, 'has_on_success_callback': False, 'has_on_failure_callback': True, '_access_control': None, 'is_paused_upon_creation': None, 'auto_register': True, 'fail_stop': False, 'jinja_environment_kwargs': None, 'render_template_as_native_obj': True, 'doc_md': None, 'tags': [], '_task_group': <airflow.utils.task_group.TaskGroup object at 0xffff5e578770>, '_processor_dags_folder': '/usr/local/airflow/dags', 'dag_dependencies': []}"""
