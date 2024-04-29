import time
from typing import Any

import uvicorn, asyncio
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse, JSONResponse
from contextlib import suppress
from contextlib import asynccontextmanager

from fastapi_events.dispatcher import dispatch
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from dac import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

registered_apps = {}


class API(FastAPI):

    def __init__(self, **extra: Any):
        super().__init__(**extra)
        self.event_handler_id = id(self)
        self.add_middleware(
            EventHandlerASGIMiddleware,
            handlers=[local_handler],
            middleware_id=self.event_handler_id
        )

        self.add_api_route("/", self.get_root, methods=["GET"], include_in_schema=False)
        self.add_api_route("/version", self.get_version, methods=["GET"])

        local_handler.register(event_name="*", _func=self.handle_all_events)

    def dispatch(self, event, payload):
        dispatch(event, payload=payload, middleware_id=self.event_handler_id)

    async def dispatch_task(self) -> None:
        for lapp in registered_apps:
            # print(f"starting local application {lapp}")

            # registered_apps[lapp]()
            loaded_app = registered_apps[lapp](lapp, self.dispatch, self)
            if hasattr(loaded_app, 'version'):
                logger.info(f"Starting local application {lapp} {loaded_app.version}")
            else:
                logger.info(f"Starting local application {lapp}")

            local_handler.register(event_name=f"{lapp}:*", _func=loaded_app.event)

        """Background task to dispatch autonomous events"""
        logger.info("Dispatching tasks")
        i = 0
        while True:
            dispatch("my_app:date", payload={"idx": i, "time": time.time()}, middleware_id=self.event_handler_id)
            await asyncio.sleep(10)
            i += 1

    @staticmethod
    async def tasks_cleanup(self):
        # Let's also finish all running tasks:
        pending = asyncio.Task.all_tasks()
        # loop.run_until_complete(asyncio.gather(*pending))
        print(asyncio.gather(*pending))

    @staticmethod
    async def tasks_kill(self):
        # Let's also cancel all running tasks:
        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress:
            with suppress(asyncio.CancelledError):
                # loop.run_until_complete(task)
                print(task)

    async def handle_all_events(self, event: Event):
        logger.debug(f"Got Event: {event}")

    @staticmethod
    async def get_root() -> HTMLResponse:
        return HTMLResponse('<meta http-equiv="Refresh" content="0; url=\'/docs\'" />')

    async def get_version(self) -> JSONResponse:
        return JSONResponse({"FastAPI version": self.version})

    @staticmethod
    async def hello(request: Request):
        dispatch("hello", payload={"id": 1})
        return JSONResponse({"detail": {"msg": "hello world"}})


@asynccontextmanager
async def lifespan(api_app: API):
    logger.info("Starting task dispatcher...")
    # This is lifespan, it CANNOT be awaited!!!!
    asyncio.create_task(api_app.dispatch_task())  # noqa
    yield
    logger.warning('Shutting down...')


url = "https://core.r3d.sh/x/dac"
app = API(
    lifespan=lifespan,
    title="API app",
    description=f"Source: <a href='{url}'>r3d</a>",
)


def register(name, new_app):
    if name in registered_apps:
        print(f"app {name} already exists!")
        return

    registered_apps[name] = new_app
    return app
