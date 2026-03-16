from setuptools import find_packages, setup

setup(
    name="updater_package",
    version="1.0",
    description="A updater_package",
    author="Marik",
    packages=find_packages(),
    install_requires=["pika"],
)
