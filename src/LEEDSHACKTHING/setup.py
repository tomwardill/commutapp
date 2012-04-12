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
        'Django==1.4',
        'lxml==2.3',
        'south>=0.7.3',
        'python-dateutil==1.5',
        'tweepy>=1.7.1',
        'celery>=2.2.7',
        'django-celery==2.5.1',
        'pytz>=2012b',
        ]
    )