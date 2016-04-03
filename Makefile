SOURCES=$(shell find . -name '*.py' | grep -v test_)
SOURCEDIRS=$(shell find . -name '*.py' | grep -v test | xargs dirname | sort -u)
TESTS=$(shell find . -name 'test_*.py')

.doc-built: $(SOURCES) $(TESTS) Makefile
	@make -s -C docs html
	@touch $@

check: $(SOURCES)
	@./devtools/unittests.py

.covdoc-built: $(SOURCES) $(TESTS) Makefile
	@make -s -C docs coverage
	@touch $@

.cov-built: $(SOURCES) $(TESTS) Makefile
	@./devtools/coverage.sh
	@touch $@

.pylint-built: $(SOURCES) Makefile
	@mkdir -p build/pylint/
	@./devtools/xtdlint.py --rcfile=.pylintrc -j4 xtd -f html > build/pylint/index.html || true
	@touch $@

.cov-report-built: .cov-built
	@coverage3 html -d build/coverage
	@touch $@

all: cov covdoc cov pylint

cov: .cov-built .cov-report-built
covdoc: .covdoc-built
doc: .doc-built
pylint: .pylint-built

show-cov: .cov-report-built
	@sensible-browser build/coverage/index.html
show-doc: .doc-built
	@sensible-browser build/docs/html/index.html
show-covdoc: .covdoc-built
	@sensible-browser build/docs/coverage/python.txt
show-pylint: .pylint-built
	@sensible-browser build/pylint/index.html

show: all show-doc show-cov show-covdoc show-pylint

clean:
	@rm -rf build .cov-buit .cov-report-built .coverage  .doc-built .covdoc-built
