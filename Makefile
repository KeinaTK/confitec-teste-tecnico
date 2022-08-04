lock:
	docker-compose exec api bash -c "pip freeze > requirements.txt"

install_part:
	docker-compose exec api bash -c "pip install ${PACKAGE}"

install: install_part lock

lint:
	python3 -m pre_commit run -a -v