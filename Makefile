build:
	rm -rf dist build
	poetry install
	poetry build
	
pip-install:
	pip uninstall goforge
	pip install dist/goforge-0.0.7-py3-none-any.whl

upload:
	python3 -m twine upload dist/*

install: build pip-install

deploy: build upload
