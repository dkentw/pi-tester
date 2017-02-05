#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pitester",
    version="1.0.0",
    # package_dir={'': 'src'},
    packages=['Engine'],
    # py_module=['pi_tester'],
    # scripts = [''],
    install_requires=['docutils>=0.3', 'junit-xml>=1.7'],
    package_data={},
    entry_points={
        'console_scripts': [
            'pitester=pitester:main'
        ]
    },
    py_modules=['pitester'],

    author="Dken",
    author_email="dken.tw@gmail.com",
    description="Automation test framework",
    license="MIT",
    keywords="automation test",
    url="https://github.com/dkentw/pi-tester",
)

if __name__ == '__main__':
    print find_packages()
