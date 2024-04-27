
default:
	uvicorn main:app --reload --reload-dir gitstore --host 0.0.0.0 --port 8111

worker:
	celery -A main.celery worker --loglevel=info -Q high_priority,default -E

beat:
	celery -A main.celery beat -l info

flower:
	flower \
    --app=main.celery \
    --broker="${CELERY_BROKER_URL}"

ping:
	celery -A main.celery inspect ping

init:
	pip3 install -r requirements.txt
