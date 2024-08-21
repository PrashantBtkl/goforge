build:
	poetry install
	poetry build
	
pip-install:
	pip uninstall goforge
	pip install dist/goforge-0.0.5-py3-none-any.whl

install: build pip-install
