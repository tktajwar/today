from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='today_cli',
        version='1.1.0',
        description='Command Line Day Planner',
        long_description = long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/TajwarHjkl/today/archive/refs/tags/v1.1.0.tar.gz',
        author='Takey Tajwar',
        author_email='tajwar.earth@proton.me',
        license='GPLv3',
        packages=['today'],
        scripts=['bin/today'],
        package_data={'today': ['themes/*.json']},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
    ],
        )
