build:
	rm -rf dist
	poetry install
	poetry build
	
pip-install:
	pip uninstall goforge
	pip install dist/goforge-0.1.1-py3-none-any.whl

upload:
	python3 -m twine upload dist/*

install: build pip-install

deploy: build upload
