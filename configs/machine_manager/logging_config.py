# Big Thanks to Yash Nag's and JPG's answers from
# https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api.

log_config = {
    "version": 1,
    "formatters": {
        "main": {
            "format": "%(levelname)s::%(asctime)s:    %(module)s  ---  %(message)s"
        },
    },
    "handlers": {
        "machine_manager": {
            "class": "logging.FileHandler",
            "formatter": "main",
            "filename": "logs/machine_manager.log",
        },
        "local_linter_deployer": {
            "class": "logging.FileHandler",
            "formatter": "main",
            "filename": "logs/local_linter_deployer.log",
        },
    },
    "loggers": {
        "machine_manager_logger": {
            "level": "DEBUG",
            "handlers": ["machine_manager"],
        },
        "local_linter_deployer_logger": {
            "level": "DEBUG",
            "handlers": ["local_linter_deployer"],
        },
    },
    "disable_existing_loggers": False,
}
