from setuptools import setup, find_packages

setup(
    name="Pyalchemist",
    version="0.1.0",
    author="Mihail Voicu",
	author_email="ucakmav@ucl.ac.uk",
    license = "CreativeCommons",
    packages=find_packages(exclude=['*tests']),
    install_requires=['argparse', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'abracadabra = alchemist.command:process'
        ]})