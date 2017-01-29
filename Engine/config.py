FEEDBACK_SERVER = {
    "server_url": "http://localhost:8080",
    "reports_path": "/reports",
    "status_path": "/dashboard"
}

CLIENT = {
    "hostname": "KentChen"
}


class VariablesPool(object):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
