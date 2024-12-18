include Python.mk
PROJECT	= gcal
ifdef SLOW
	COV_FAIL_UNDER = 100
else
	COV_FAIL_UNDER = 98
endif
lint :: mypy
doc :: README.md
