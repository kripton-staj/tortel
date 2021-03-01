import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tortel",
    version="",
    author="",
    author_email="",
    description="Product similarity detection with NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kripton-staj/tortel",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
)
