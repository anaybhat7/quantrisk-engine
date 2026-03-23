import os
from setuptools import setup, find_packages

setup(
    name="quantrisk_engine",
    version="0.1.0",
    author="Your Name",
    description="A multi-asset risk estimation and stress-testing engine.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantrisk-engine",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "yfinance",
        "fredapi",
        "pandas-datareader",
        "pyarrow",
        "python-dotenv",
        "scipy",
        "statsmodels",
        "matplotlib",
        "seaborn",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",  # Essential for hitting that >80% coverage goal
            "flake8",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)