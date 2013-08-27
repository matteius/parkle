from datetime import datetime
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = []

version = '%s' % datetime.now().strftime("%Y-%m-%d-%H_%M_%S_%f")
setup(
    name="parkle",
    version=version,
    author="Parkle Players",
    author_email="matteius@gmail.com",
    description=("Modified Parkle engine to meet the needs of Django-farkle"),
    license="BSD",
    keywords="Parkle and Farkle",
    include_package_data=True,
    packages=['parkle'],
    package_dir={'': 'parkle'},
    install_requires=install_requires,
    long_description=read('README'),
    zip_safe=False,
)
