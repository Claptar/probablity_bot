from setuptools import setup, find_packages

setup(
    name="probability-trial-bot",
    version="0.1",
    packages=find_packages(where="."),
    install_requires=[
        "sqlalchemy",
        "python-telegram-bot",
        "pyyaml",
        "dogpile.cache",
    ],
)
