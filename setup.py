from setuptools import setup, find_packages

setup(
    name="quantrisk_engine",
    version="0.1.0",
    author="Anay Bhat",
    description="A multi-asset stress-testing and risk attribution engine for ORIE 5270.",
    long_description=open("README.md").read() if hasattr(open("README.md"), "read") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantrisk-engine",  # Update once you have your repo
    packages=find_packages(include=["engine", "engine.*", "data", "data.*", "utils", "utils.*"]),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "yfinance>=0.2.0",
        "fredapi>=0.5.0",
        "python-dotenv>=1.0.0",
        "pyarrow>=12.0.0",  # Critical for the Parquet caching we built
        "matplotlib>=3.7.0", # You'll likely want this for the reporting module later
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=5.0.0",
        ],
    },
    python_requires=">=3.11", # Safe floor for Python 3.13 stability
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    entry_points={
        'console_scripts': [
            'run-backtest=scripts.backtest:main',
        ],
    },
)