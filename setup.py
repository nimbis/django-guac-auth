#!/usr/bin/env python

from setuptools import setup, find_packages

# setup the project
setup(
    name="django-guac-auth",
    version="1.0.0",
    author="Nimbis Services, Inc.",
    author_email="devops@nimbisservices.com",
    description="Django app to enable Guacamole authentication",
    license="BSD",
    packages=find_packages(exclude=["tests", ]),
    install_requires=[
        'django>=1.8,<1.9',
        'sqlparse'
    ],
    zip_safe=False,
    include_package_data=True,
)
