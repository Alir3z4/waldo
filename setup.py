import subprocess
import sys
import unittest

from setuptools import setup, Command, find_packages


class CommandBase(Command):
    """Setup.py base command."""
    user_options: list = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class RunTests(CommandBase):
    """New setup.py command to run all tests for the package."""
    description: str = "run all tests for the package"

    @staticmethod
    def run() -> None:
        tests = unittest.TestLoader().discover('.')
        runner = unittest.TextTestRunner()
        results = runner.run(tests)
        sys.exit(not results.wasSuccessful())


class RunCoverage(CommandBase):
    """Command to Run Coverage."""
    @staticmethod
    def run() -> None:  # pragma: no cover
        subprocess.run("coverage run setup.py test")
        subprocess.run('coverage report --skip-covered')
        subprocess.run('coverage html')


setup(
    name="subimage",
    version="2018.7.27",
    description="Find the cropped image in the original one.",
    author="Alireza Savand",
    author_email="alireza.savand@gmail.com",
    maintainer='Alireza Savand',
    maintainer_email='alireza.savand@gmail.com',
    url='https://github.com/Alir3z4/waldo/',
    cmdclass={
        'test': RunTests,
        'coverage': RunCoverage,
    },
    platforms='OS Independent',
    entry_points="""
        [console_scripts]
        subimage=subimage:main
    """,
    license='GNU GPL 3',
    install_requires=(
        'numpy==1.15.0',
        'opencv-python==3.4.2.17',
    ),
    packages=find_packages(exclude=['tests']),
    py_modules=['subimage'],
    include_package_data=True,
    zip_safe=False,
)
