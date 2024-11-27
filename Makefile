include Python.mk
PROJECT	= gcal
ifdef SLOW
	COV_FAIL_UNDER = 96
else
	COV_FAIL_UNDER = 94
endif
lint :: mypy
doc :: README.md
