#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


requirements = []

test_requirements = ["pytest>=3"]

setup(
    author="Pedro Martins",
    author_email="pedromartins.cwb@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Datazeit MLE ",
    install_requires=requirements,
    include_package_data=True,
    keywords="datazeit",
    name="datazeit",
    packages=find_packages(include=["datazeit", "datazeit.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    version="0.1.0",
    zip_safe=False,
)
