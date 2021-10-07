#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note:
# To use the "upload" functionality of this file, you must:
#   $ pipenv install twine --dev
# To publish the package:
#   $ setup.py

import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

NAME = "ua-datasets"
DESCRIPTION = "A collection of ukrainian language datasets"
URL = "https://github.com/fido-ai/ua-datasets"
# EMAIL = "me@example.com"
AUTHOR = "FIdo AI"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.0.1"
REQUIRED = [
]
EXTRAS = {
    # Optional packages
}

here = os.path.abspath(os.path.dirname(__file__))
print(here)

# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload"""

    description = "Build and publish the package"
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag v{0}".format(VERSION))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    # author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
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
    cmdclass={
        "upload": UploadCommand,
    },
)
