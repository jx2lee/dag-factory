from airflow.plugins_manager import AirflowPlugin

from dagfactory import _listeners


class ListenersPlugin(AirflowPlugin):
    name = "Listener Plugin"
    listeners = [_listeners]


my_plugin = ListenersPlugin()
