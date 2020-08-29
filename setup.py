"""
steel-toes uses distutils to create a python package.

To Build steel-toes as a Python package

    $ python setup.py sdist bdist_wheel --bdist-dir ~/temp/bdistwheel

To setup local Development

    $ pip install -e .
"""
from pathlib import Path

from setuptools import find_packages, setup

NAME = "steel-toes"

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

with open("requirements_dev.txt", "r", encoding="utf-8") as f:
    dev_requires = [x.strip() for x in f if x.strip()]

setup(
    name=NAME,
    version="0.2.0",
    url="https://github.com/WaylonWalker/find-kedro.git",
    author="Waylon Walker",
    author_email="waylon@waylonwalker.com",
    description="protection against stepping on teammates toes in a kedro project",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    platforms="any",
    license="MIT",
    install_requires=requires,
    extras_require={"dev": dev_requires},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "kedro.global_commands": ["steel-toes = steel_toes:cli"],
        "console_scripts": ["steel-toes = steel_toes:cli"],
    },
)
