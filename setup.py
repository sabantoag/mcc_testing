#!/usr/bin/env python

""" The setup script """

from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = ['pytest>=3']

setup(
    author='Cody Kapka',
    author_email='cody.kapka@sabantoag.com',
    python_requires='>3.4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ],
    description="Test software to test Sabanto electronics",
    # entry_points={
    #     'console_scripts': [
    #         'sabanto-test=sabanto_test.scripts.test:run_example',
    #     ],
    # }
    install_requires=requirements,
    license="Proprietary",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='9999-DD-2004',
    name='9999-DD-2004',
    packages=find_packages(include=['9999-DD-2004', '9999-DD-2004.*' 'utils', 'utils.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sabantoag/mcc_testing.git',
    version='0.1.0',
    zip_safe=False,
)
