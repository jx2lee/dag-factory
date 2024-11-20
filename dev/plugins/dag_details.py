import os
from typing import Any, Dict

from airflow.models import DagBag
from airflow.plugins_manager import AirflowPlugin
from airflow.www.app import csrf
from flask import Blueprint, redirect, request, url_for
from flask_appbuilder import BaseView as AppBuilderBaseView, expose

current_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(current_dir, "templates")

bp = Blueprint(
    "dagdetailsplugin",
    __name__,
    template_folder=template_folder,
    static_folder="static",
    static_url_path="/static/dagdetailsplugin",
)


def get_tag_name(tag: Any) -> str:
    """Safely get tag name whether it's a string or an object."""
    try:
        return tag.name if hasattr(tag, "name") else str(tag)
    except Exception:
        return str(tag)


def get_dag_details(dag_id: str = None) -> Dict[str, Any]:
    """Fetch DAG details from DagBag."""
    try:
        dag_bag = DagBag(read_dags_from_db=True)
        dag_bag.collect_dags_from_db()

        if dag_id:
            dag = dag_bag.get_dag(dag_id)
            if not dag:
                return None

            return {
                "dag": dag,  # Original DAG object for permissions
                "display_data": {  # Formatted data for display
                    "dag_id": dag.dag_id,
                    "description": dag.description or "No description available",
                    "file_location": dag.fileloc,
                    "owner": dag.owner,
                    "start_date": dag.start_date,
                    "schedule_interval": dag.schedule_interval,
                    "tags": [get_tag_name(tag) for tag in (dag.tags or [])],
                    "default_args": dag.default_args if hasattr(dag, "default_args") else {},
                    "catchup": dag.catchup,
                    "max_active_runs": dag.max_active_runs,
                    "concurrency": dag.concurrency,
                    "tasks": [
                        {
                            "task_id": task.task_id,
                            "task_type": task.task_type,
                            "downstream_task_ids": list(task.downstream_task_ids),
                            "upstream_task_ids": list(task.upstream_task_ids),
                            "retries": task.retries,
                            "retry_delay": str(task.retry_delay) if task.retry_delay else None,
                        }
                        for task in dag.tasks
                    ],
                },
            }

        # Return list of all DAGs
        dags_list = {}
        for dag_id, dag in dag_bag.dags.items():
            dags_list[dag_id] = {
                "dag": dag,  # Original DAG object for permissions
                "display_data": {  # Formatted data for display
                    "dag_id": dag.dag_id,
                    "description": dag.description or "No description available",
                    "owner": dag.owner,
                    "schedule_interval": dag.schedule_interval,
                    "tags": [get_tag_name(tag) for tag in (dag.tags or [])],
                    "file_location": dag.fileloc,
                },
            }
        return dags_list

    except Exception as e:
        return {"error": f"Error fetching DAG details: {str(e)}"}


class DagDetailsView(AppBuilderBaseView):
    default_view = "list"
    template_folder = template_folder

    @expose("/")
    @csrf.exempt
    def list(self):
        """Show list of all DAGs with basic details."""
        # Handle navigation from DAG pages
        referrer = request.referrer
        if referrer and "/dags/" in referrer:
            try:
                # Extract DAG ID from referrer URL
                dag_id = referrer.split("/dags/")[1].split("/")[0]
                return redirect(url_for("DagDetailsView.details", dag_id=dag_id))
            except Exception:
                pass

        # Show list view
        dags = get_dag_details()
        if "error" in dags:
            return self.render_template("error.html", error=dags["error"])
        return self.render_template("dag_details_list.html", dags=dags, title="DAG Details")

    @expose("/<string:dag_id>")
    @csrf.exempt
    def details(self, dag_id):
        """Show detailed view of a specific DAG."""
        result = get_dag_details(dag_id)
        if not result:
            return self.render_template("error.html", error=f"DAG '{dag_id}' not found")
        if "error" in result:
            return self.render_template("error.html", error=result["error"])

        return self.render_template(
            "dag_details.html",
            dag=result["dag"],  # Original DAG object for permissions
            dag_details=result["display_data"],  # Formatted data for display
            title=f"DAG Details - {dag_id}",
        )


# Create AppBuilder View
v_appbuilder_view = DagDetailsView()
v_appbuilder_package = {"name": "DAG Details", "category": "Custom Plugins", "view": v_appbuilder_view}


# Create Plugin
class DagDetailsPlugin(AirflowPlugin):
    name = "dagdetailsplugin"
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package]
