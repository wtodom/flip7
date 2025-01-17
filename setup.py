from setuptools import setup, find_packages

setup(
    name="flip7",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.0",
        "pandas>=2.1.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "pytest>=7.4.0",
        "loguru>=0.7.0",
        "tqdm>=4.66.0",
    ],
) 