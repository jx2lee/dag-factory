from airflow.plugins_manager import AirflowPlugin
from airflow.www.views import Airflow
from flask import redirect, url_for
from flask_appbuilder import expose

# from airflow.www.decorators import auth
# from airflow.www.security import DagAccessEntity
# from airflow.www.utils import sanitize_args


class CustomCodeView(Airflow):
    default_view = "custom_code"

    @expose("/dags/<string:dag_id>/custom_code")
    # @auth.has_access_dag("GET", DagAccessEntity.CODE)
    def custom_code(self, dag_id):
        """Dag Code."""
        kwargs = {
            # **sanitize_args(request.args),
            "dag_id": dag_id,
            "tab": "custom_code",
        }
        return redirect(url_for("Airflow.grid", **kwargs))


v_appbuilder_view = {
    "name": "Custom Code",
    "category": "Airflow.grid",
    "view": CustomCodeView(),
    "href": "/dags/<string:dag_id>/custom_code",
}


class CustomTabPlugin(AirflowPlugin):
    name = "custom_tab_plugin"
    appbuilder_views = [v_appbuilder_view]
