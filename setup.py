import setuptools
from distutils.core import setup
from pathlib import Path

with (Path(__file__).parent / "readme.md").open("r") as f:
    long_description = f.read()

setup(
    name="tool-myopy",
    version="0.0.1",
    description="analyze EMG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ethan rich",
    author_email="ethanmrich@gmail.com",
    url="https://github.com/ethanrich/tool-myopy.git",
    download_url="https://github.com/ethanrich/tool-myopy.git",
    license="MIT",
    packages=["myopy"],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries",
    ],
)
