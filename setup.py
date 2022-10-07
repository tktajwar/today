from setuptools import setup

setup(
        name='today_cli',
        version='1.0',
        description='Plan and execute your day in an organised way.',
        url='https://github.com/TajwarHjkl/today',
        author='Takey Tajwar',
        author_email='tajwar.earth@proton.me',
        license='GPLv3',
        packages=['today'],
        scripts=['bin/today'],
        package_data={'today': ['themes/*.json']},
        zip_safe=False,
        )
