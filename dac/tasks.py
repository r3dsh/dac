from celery.schedules import crontab
from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)

from celery import Celery

app = Celery("tasks", broker='redis://localhost:6379/0', backend='redis://localhost')


# app.conf.beat_schedule = {
#     'print-ping-every-5-seconds': {
#         'task': 'ping',
#         'schedule': 5.0,
#     },
# }

@app.task
def add(x, y):
    logger.info("CELERY TASK TRIGGERED")
    return x + y


@shared_task(name="ping")
def ping():
    return "pong"


app.add_periodic_task(5.0, ping, name='ping every 5')


# from celery import Celery as celery, shared_task
#
#
def register_tasks(app):
    logger.warn("Registering celery tasks")

    @app.task(queue='default', max_retries=5, retry_backoff=True, retry_backoff_max=1)
    def sample_task():
        import time
        for i in range(4):
            time.sleep(5)
        print("Task Completed")
        logger.info("Task Completed")
        return "Foo"

    # Schedule the task to run every 10 seconds
    app.conf.beat_schedule = {
        'print-ping-every-5-seconds': {
            'task': 'dac.tasks.noop',
            'schedule': 5.0,
        },
    }

    # @app.on_after_configure.connect
    # def setup_periodic_tasks(app, **kwargs):
    logger.info("CONFIGURING SCHEDULED TASKS")
    logger.info("CONFIGURING SCHEDULED TASKS")
    logger.info("CONFIGURING SCHEDULED TASKS")
    logger.info("CONFIGURING SCHEDULED TASKS")

    # Calls test('hello') every 10 seconds.
    # app.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    # app.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    # app.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # app.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

    @app.task
    def test(arg):
        print(arg)

    @app.task
    def add(x, y):
        z = x + y
        print(z)

    @app.task
    def noop():
        logger.info("NOOP Task")
        return "BAZINGA"
