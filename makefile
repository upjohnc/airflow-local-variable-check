test:
	PYTHONPATH=. pytest -v

isort:
	isort -rc . .isort.cfg
