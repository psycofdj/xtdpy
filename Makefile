SOURCES=$(shell find . -name '*.py' | grep -v test_)
SOURCEDIRS=$(shell find . -name '*.py' | grep -v test | xargs dirname | sort -u)
TESTS=$(shell find . -name 'test_*.py')

.doc-built: $(SOURCES) $(TESTS) Makefile
	@make -C docs html
	@touch $@

check: $(SOURCES)
	@./scripts/unittests.py

.covdoc-built: $(SOURCES) $(TESTS) Makefile
	@make -C docs coverage
	@touch $@

.cov-built: $(SOURCES) $(TESTS) Makefile
	@./scripts/coverage.sh
	@touch $@

.lint-built: $(SOURCES) $(TESTS) Makefile
	@./scripts/lint.sh html
	@touch $@

.cov-report-built: .cov-built
	@coverage3 html -d build/coverage
	@touch $@

cov: .cov-built .cov-report-built
covdoc: .covdoc-built
doc: .doc-built
lint: .lint-built

show-cov: .cov-report-built
	@sensible-browser build/coverage/index.html
show-doc: .doc-built
	@sensible-browser build/docs/html/index.html
show-covdoc: .covdoc-built
	@sensible-browser build/docs/coverage/python.txt
show-lint: .lint-built
	@sensible-browser build/lint/index.html

show: show-doc show-cov show-covdoc show-lint

clean:
	@rm -rf .cov-buit .cov-report-built .coverage build/coverage .doc-built .covdoc-built
