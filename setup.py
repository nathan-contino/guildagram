import io

from setuptools import find_packages
from setuptools import setup

setup(
    name="guildagram",
    version="1.0.0",
    url="nathan-contino.github.io",
    license="BSD",
    maintainer="Nathan Contino",
    maintainer_email="ncontino [at] u.rochester.edu",
    description="A basic messenger API built with Flask.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)