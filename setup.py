from distutils.core import setup

setup(
    name="comparerr",
    version="0.1",
    author="Tomas Korbar",
    author_email="tomas.korb@seznam.cz",
    license="GPL3",
    description="Comparerr is a set of scripts allowing you to compare outputs"
    "of pylint and find errors which have been fixed or created.",
    url="https://github.com/TomasKorbar/comparerr",
    scripts=["bin/comparerr", "bin/pylint2comparerr"],
)
