SOURCES=$(shell find . -name '*.py' | grep -v test_)
SOURCEDIRS=$(shell find . -name '*.py' | grep -v test | xargs dirname | sort -u)
TESTS=$(shell find . -name 'test_*.py')

check: $(SOURCES)
	@./scripts/unittests.py

.cov-buit: $(SOURCES) $(TESTS) Makefile
	@./scripts/coverage.sh
	@touch $@

.cov-report-built: .cov-buit
	@coverage3 html -d build/coverage
	@touch $@

cov: .cov-buit .cov-report-built

show-cov: .cov-report-built
	@sensible-browser build/coverage/index.html

clean:
	@rm -rf .cov-buit .cov-report-built .coverage build/coverage
