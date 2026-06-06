#!/usr/bin/env python3
"""
NoteMind-CLI Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="notemind-cli",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="🧠 NoteMind-CLI - Lightweight Terminal AI Smart Note Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/NoteMind-CLI",
    py_modules=["notemind"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "notemind=notemind:main",
        ],
    },
    keywords="notes markdown cli terminal productivity ai knowledge-management",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/NoteMind-CLI/issues",
        "Source": "https://github.com/gitstq/NoteMind-CLI",
    },
)
