import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-alkiz",
    version="0.0.1",
    author="Andrew Woodward (xarses)r",
    author_email="xarses@gmail.com",
    description="Unofficial Library to interact with Alkiz Command Center",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xarses/python-alkiz",
    project_urls={
        "Bug Tracker": "https://github.com/xarses/python-alkiz/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
   install_requires=[
        "requests",
        "bs4",
    ],)
