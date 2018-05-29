"""
Setup.py for Kaznet
"""
from setuptools import setup, find_packages

setup(
    name='kaznet',
    version='0.0.1',
    description='Django Project For ILRI Kaznet',
    license='Apache 2.0',
    author='Ona Kenya',
    author_email='tech@ona.io',
    url='https://github.com/onaio/kaznet-web',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'Django >= 2',
        'djangorestframework',
        'psycopg2-binary',
        'django-prices',
        'django-phonenumber-field',
        'babel',
        'phonenumbers',
        'django-allauth',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2',
    ],
)
