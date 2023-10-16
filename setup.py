import re
import pathlib 
import setuptools


_here = pathlib.Path()

name = "ua-datasets"
author = "FIdo AI"
description = "A collection of ukrainian language datasets"
python_requires = ">=3.7.0"
url = "https://github.com/fido-ai/" + name


with open(_here / name.replace('-', '_') / "__init__.py") as f:
    meta_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if meta_match:
        version = meta_match.group(1)
    else:
        raise RuntimeError("Unable to find __version__ string")

with open(_here / "README.md" , "r") as f:
    readme = f.read()


setuptools.setup(
    name=name,
    version=version,
    author=author,
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=python_requires,
    url=url,
    install_requires=[],
    include_package_data=True,
    license="MIT",  # Don't forget to change classifiers if you change the license
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: Ukrainian",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
)
