
.PHONY: test pep8 clean check-venv check-reqs check-venv

# clean out potentially stale pyc files
clean:
	@find . -name "*.pyc" -exec rm {} \;

# check that virtualenv is enabled
check-venv:
ifndef VIRTUAL_ENV
	$(error VIRTUAL_ENV is undefined, try "workon" command)
endif

# Install pip requirements.txt file
reqs: check-venv
	pip install -r requirements.txt

# Show all occurence of same error
# Exclude the static directory, since it's auto-generated
PEP8_OPTS=--repeat --exclude=static,migrations,south_migrations,js --show-source

pep8: check-venv
	python setup.py pep8 $(PEP8_OPTS)

test: check-venv clean
	python -Wall manage.py test --keepdb -v 2

travis-tests: check-venv
	@echo "travis_fold:start:flake8"
	make flake8
	@echo "travis_fold:end:flake8"

	coverage erase
	@echo "travis_fold:start:test"
	coverage run $(COVERAGE_ARGS) ./manage.py test --keepdb -v 2
	@echo "travis_fold:end:test"

	@echo "travis_fold:start:coverage"
	coverage report
	coverage html
	@echo "travis_fold:end:coverage"


# flake8
#

FLAKE8_OPTS = --max-complexity 10 --exclude='dist,build,htmlcov,migrations,south_migrations'
flake8: check-venv
	flake8 $(FLAKE8_OPTS) . 

#
# code coverage
#

COVERAGE_ARGS=--source=guac_auth

coverage: check-venv
	coverage erase
	-coverage run $(COVERAGE_ARGS) ./manage.py test --keepdb -v 2
	coverage report
	coverage html
	@echo "See ./htmlcov/index.html for coverage report"
