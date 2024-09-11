from setuptools import setup, find_packages

setup(
    name="stonks",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'pytest',
        'pandas',
        'yfinance',
        'matplotlib',
        'mplfinance',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'run_stonks_analysis=stonks.stonks:run_stonks_analysis',
        ],
    },
    author="Daniel Lasota",
    author_email="grossmann.root@gmail.com",
    description="stonks stonks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DanielLasota/Stonks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.8, <3.9',
)