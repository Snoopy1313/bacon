from setuptools import find_packages, setup

setup(
    name="bacon_package",
    version="1.0",
    description="A bacon_package",
    author="Marik",
    packages=find_packages(),
    install_requires=["flask"],
)
