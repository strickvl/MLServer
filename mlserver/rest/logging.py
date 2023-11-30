import logging


class HealthEndpointFilter(logging.Filter):
    """
    Filter to avoid logging health endpoints.
    From:
        https://github.com/encode/starlette/issues/864#issuecomment-653076434
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if not isinstance(record.args, tuple):
            return True

        if len(record.args) < 3:
            return True

        request_method = record.args[1]
        if request_method != "GET":
            return True

        query_string = record.args[2]
        return query_string not in ["/v2/health/live", "/v2/health/ready"]


def disable_health_access_logs() -> None:
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.addFilter(HealthEndpointFilter())


loggerName = "mlserver.rest"
logger = logging.getLogger(loggerName)
