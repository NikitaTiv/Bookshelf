style:
	flake8 .

types:
	mypy webapp

test:
	python -m pytest
	
check:
	make style types test
