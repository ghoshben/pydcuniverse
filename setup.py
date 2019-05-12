import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydcuniverse",
    version="1.1.0",
    author="espydy",
    author_email="espydy@secmail.pro",
    description="Python library for interacting with DC Universe API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/espydy/pydcuniverse",
    packages=["pydcuniverse"],
    install_requires=['PyJWT', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
