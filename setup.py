# Copyright Utah State University Research Foundation.
# All rights reserved except as specified below.
# This information is protected by a Non-Disclosure/Government Purpose
# License Agreement and is authorized only for United States Federal
# Government use.
# This information may be subject to export control.

"""Project configuration for setuptools."""

import setuptools

with open("readme.md", "r") as file_:
   LONG_DESCRIPTION = file_.read()

setuptools.setup(
    name="tracking_analysis",
    version="0.0.dev1",
    author="brobeson",
    author_email="brobeson@users.noreply.github.com",
    description="Analyse the results of object tracking experiments.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/brobeson/data-analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
    install_requires=["matplotlib"],
    python_requires=">=3",
    entry_points={
        # pylint: disable=line-too-long
        "console_scripts": ["data-analysis = tracking_analysis.data_analysis:main"]
    },
)
