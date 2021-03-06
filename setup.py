#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["pandas", "geopandas", "wget", "openpyxl"]

test_requirements = []

setup(
    author="Marc Wiedermann",
    author_email='marcwiedermann@posteo.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Easy access to NUTS and LAU codes for a given location",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='pynuts',
    name='pynuts',
    packages=find_packages(include=['pynuts', 'pynuts.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcwie/pynuts',
    version='0.1.0',
    zip_safe=False,
)
