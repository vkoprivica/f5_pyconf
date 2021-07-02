import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="f5_pyconf",
    version="1.0.0",
    description="""Containes Build Functions to Utilize F5 SDK API for 
    device configuration.""",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vkoprivica/f5_pyconf",
    author="Vukasin Koprivica",
    author_email="vkoprivica.git@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    # packages=["bigip", "api", "ltm", "data", "logs"],
    packages=find_packages(exclude=("bigip/tests",)),
    include_package_data=True,
    # entry_points={
    #     "console_scripts": [
    #         "f5_pyconf=pyconf/bigip.__init__:main",
    #     ]
    # },
)