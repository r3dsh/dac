import uvicorn

original_callback = uvicorn.main.callback


def callback(**kwargs):
    from celery.contrib.testing.worker import start_worker
    from dac import tasks

    print("CELERY TASK RESULT:", tasks.add.delay(2, 2))
    # print("CELERY TASK RESULT:", tasks.ping())

    with start_worker(tasks.app, perform_ping_check=False, loglevel="info"):
        original_callback(**kwargs)


uvicorn.main.callback = callback

if __name__ == "__main__":
    uvicorn.main()
