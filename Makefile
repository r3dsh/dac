
default:
	uvicorn entrypoint:app --reload --reload-dir dac --host 0.0.0.0 --port 8111 --lifespan on

init:
	pip3 install -r requirements.txt

