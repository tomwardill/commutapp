from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name = 'leedshackthing',
    version = version,
    description = "",
    long_description = "",
    author = "",
    author_email = "",
    url = "",
    license = "",
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    
    install_requires = [
        'lxml',
        'south',
        'python-dateutil==1.5',
        'tweepy'
        ]
    )