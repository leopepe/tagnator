clean:
	rm -rf venv/*

virtualenv:
	virtualenv -p python3.5 venv
	./venv/bin/python -m pip install -r requirements

