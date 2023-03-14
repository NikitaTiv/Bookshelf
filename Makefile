style:
	flake8 .

types:
	mypy webapp

tests:
	pytest .
	
check:
	make style types tests
