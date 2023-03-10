# Allow to run multiple lines in a recipe in the same shell.
.ONESHELL:

SRCDIR=microservices_example
TESTDIR=tests

TARGETDIRS=$(SRCDIR)/ $(TESTDIR)/

PROTOC=poetry run python -m grpc_tools.protoc

types-protobuf:
	$(PROTOC) --proto_path=./protos --python_out=$(SRCDIR) --pyi_out=$(SRCDIR) protos/types.proto

users-protobuf: types-protobuf
	$(PROTOC) --proto_path=./protos --python_out=$(SRCDIR)/users/ --pyi_out=$(SRCDIR)/users/ --grpc_python_out=$(SRCDIR)/users/ protos/users.proto

compile-protobuf: users-protobuf

autoflake:
	poetry run autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports $(TARGETDIRS)

black:
	poetry run black $(TARGETDIRS)

isort:
	poetry run isort $(TARGETDIRS)

mypy:
	poetry run mypy $(TARGETDIRS)

# line-too-long is disabled because black already takes care of that.
pylint:
	poetry run pylint --disable=fixme --disable=too-few-public-methods --disable=line-too-long $(TARGETDIRS)

consistent-format: autoflake black isort

correct-format: consistent-format mypy pylint

tests: compile-protobuf
	poetry run pytest -x --cov=$(SRCDIR) $(TESTDIR)

coverage-report:
	poetry run coverage report -m --sort=Cover > coverage-report.txt
	cat coverage-report.txt

# .PHONY indicates which targets are not connected to the generation of one or more files.
.PHONY: autoflake black isort mypy pylint consistent-format correct-format tests coverage
