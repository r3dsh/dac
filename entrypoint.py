import asyncio
import time

import uvicorn

from dac import logging, bootstrap
from fastapi_events.typing import Event
from fastapi import Request
from starlette.responses import JSONResponse

from dac.manifest.parser import ManifestParser

# let's highlight our logs in yellow
logger = logging.getLogger(__name__, f"%(levelname)s: %(asctime)s {logging.yellow}%(name)s{logging.reset} %(message)s")
logger.setLevel(logging.DEBUG)


class BaseApp:

    def __init__(self, app_id, dispatch, api_app):
        self.id = app_id
        self.version = "development"
        self.dispatch = dispatch

    def send_event(self, request: Request):
        logger.info(f"send_event: {request}")
        self.dispatch("my_app:event", payload={"send_event": 1, "time": time.time()})
        return JSONResponse({"detail": {"msg": "hello world"}})

    def event(self, event: Event):
        logger.info(f"[{self.id}] REC Event: {event}")


class MyApp(BaseApp):
    def __init__(self, app_id, dispatch, api_app):
        super().__init__(app_id, dispatch, api_app)

        api_app.add_api_route("/event", self.send_event, methods=["GET"])

        logger.info(f"MyApp STARTED! {self.version}")

        self.manifest_parser = ManifestParser(["../manifests", "../manifests2"])
        self.manifests = self.manifest_parser.load_all()

        # updates graph.html file - can be served by api endpoint
        # self.visualize_graph()


# bootstrap.register always returns main API app (API app extends FastAPI)
# alternatively, use: app = bootstrap.app
app = bootstrap.register("my_app", MyApp)

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = logging.logFormat
    log_config["formatters"]["default"]["fmt"] = logging.logFormat

    uvicorn.run(app, log_config=log_config, host="127.0.0.1", port=7300)
