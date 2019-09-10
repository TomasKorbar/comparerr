import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
    name="comparerr",
    version="0.2.0",
    author="Tomas Korbar",
    author_email="tomas.korb@seznam.cz",
    license="GPL3",
    description="Comparerr is a tool which which analyzes two versions of python software "
    "versioned by git with pylint and shows you errors which you added and fixed.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/TomasKorbar/comparerr",
    scripts=["bin/comparerr"],
    packages=["comparerr", "comparerr.utils"],
    install_requires=["GitPython>=3", "pylint>=2.3.1"],
    python_requires=">=3.7",
    classifiers=["Development Status :: 4 - Beta",
                 "Topic :: Software Development :: Debuggers",
                 "Topic :: Software Development :: Quality Assurance",
                 "Topic :: Software Development :: Testing",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
                ],
    keywords=["lint", "testing", "CI"]
)
