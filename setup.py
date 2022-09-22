from setuptools import setup

setup(
    name='pycle',
    version='0.0.1',
    description='Pycle is a light-weight kernel with support for persistence for executing Python.',
    author='Anand Chitipothu',
    author_email='anandology@gmail.com',
    url='https://github.com/anandology/pycle',
    packages=['pycle'],
    license="MIT",
    platforms=["any"],
    entry_points = {
        'console_scripts': [
            'pycle = pycle.pycle:main',
        ]
    }
)
