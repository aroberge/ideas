# pylint: skip-file
from setuptools import setup, find_packages
from ideas import __version__

with open("README.md", encoding="utf8") as f:
    README = f.read()

setup(
    name="ideas",
    version=__version__,
    description="Easy creation of import hooks to test ideas.",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    url="https://github.com/aroberge/ideas",
    author="André Roberge",
    author_email="Andre.Roberge@gmail.com",
    install_requires=["token-utils"],
    packages=find_packages(
        exclude=["dist", "build", "tools", "tests", "examples", "docs"]
    ),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["ideas = ideas.__main__:main"],
    },
)
