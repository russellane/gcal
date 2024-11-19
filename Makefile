include Python.mk
PROJECT	= gcal
COV_FAIL_UNDER = 92
lint :: mypy
doc :: README.md
