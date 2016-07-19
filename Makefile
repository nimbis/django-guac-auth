
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

#
# Release process
#

VERSION := $(shell python ./setup.py --version 2>&1)
RELEASE_TAG := v$(VERSION)
PREV_VERSION := $(shell git describe --match='v*' 2>&1 | sed -e s'/\(v[0-9.]*\).*/\1/')

.PHONY: release
release:
	@echo ""

	@echo "Performing pre-release checks for version $(VERSION)"

	@echo -n "Looking for an existing tag $(RELEASE_TAG)... "
	@if git tag -l $(RELEASE_TAG) | grep $(RELEASE_TAG); then \
	    echo ""; \
	    echo "Error: A release tag $(RELEASE_TAG) already exists."; \
	    echo "  To make a new release, please increment the version"; \
	    echo "  number in setup.py, (use semantic versioning).";\
	    echo ""; \
	    false; \
	fi
	@echo "None found. Good"

	@echo -n "Looking for release notes for $(VERSION)... "
	@if ! grep -q '^$(VERSION) ' CHANGES; then \
	    echo "None found. Bad"; \
	    echo ""; \
	    echo "Error: No release notes found for version $(VERSION)"; \
	    echo ""; \
	    echo "  Please look through completed Trello cards and recent"; \
	    echo "  commits, then summarize changes in the file"; \
	    echo "  CHANGES"; \
	    echo ""; \
	    echo "  The following output may prove useful:"; \
	    echo ""; \
	    echo "  $$ git log $(PREV_VERSION).."; \
	    echo ""; \
	    git --no-pager log $(PREV_VERSION)..; \
	    false; \
	fi
	@echo "Found them. Good"

	@echo -n "Checking for locally-modified files... "
	@mods=$$(git ls-files -m); if [ "$${mods}" != "" ]; then \
	    echo "Found some. Bad"; \
	    echo ""; \
	    echo "Error: The following files have modifications."; \
	    echo "  Please commit the desired changes to git before"; \
	    echo "  attempting a release."; \
	    echo ""; \
	    echo "$$mods"; \
	    echo ""; \
	    false; \
	fi
	@echo "None found. Good"

	@echo ""
	@echo "Preparing to package and release version $(VERSION)"
	@echo "to the Nimbis private repository. You have 10 seconds to abort."
	@echo ""
	@for cnt in $$(seq 10 -1 1); do echo -n "$$cnt... "; sleep 1; done
	@echo "0"

	@echo "python setup.py sdist upload -r nimbis"
	@if ! python setup.py sdist upload -r nimbis; then \
	    echo ""; \
	    echo "Error: Failed to upload new release."; \
	    echo "  Please resolve any error messages above, and then"; \
	    echo "  try again."; \
	    false; \
	fi

	@echo ""
	@echo "Successfully released a package with version $(VERSION)"

	@if ! git tag -s -m "Release $(VERSION)" $(RELEASE_TAG); then \
	    echo ""; \
	    echo "Error: Packaged release has been uploaded, but failed to"; \
	    echo "  create a tag. Please create and push a $(RELEASE_TAG)"; \
	    echo "  tag manually now"; \
	    false; \
        fi

	@if ! git push origin $(RELEASE_TAG); then \
	    echo ""; \
	    echo "Error: Packaged release has been uploaded and tagged."; \
	    echo "  But an error occurred while pushing the tag. Please"; \
	    echo "  manually push the $(RELEASE_TAG) tag now"; \
	    false; \
	fi
