#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Leonhardt Hu",
    author_email='huwkigane@gmail.com',
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
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='a pyqt6 node editor',
    name='node-editor-hu',
    packages=find_packages(include=['node_editor_hu*'], exclude=['examples*', 'tests*']),
    package_data={'': ['qss/*']},
    setup_requirements=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/1e0nhardt/PyQtNodeEditor.git',
    version='0.1.0',
    zip_safe=False,
)
