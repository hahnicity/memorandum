from setuptools import find_packages, setup


__version__ = "0.1.0"


setup(
    name="memorandum",
    author="Greg Rehm",
    version=__version__,
    description=(
        "Aggregator of page view statistics for select groups of wiki pages"
    ),
    packages=find_packages(),
    install_requires=[
        "numpy==1.7.1",
        "requests==1.2.0", 
        "ujson==1.30"
    ],
    entry_points={
        "console_scripts": [
            "memorandum=memorandum.main:main"    
        ]
    },
)
