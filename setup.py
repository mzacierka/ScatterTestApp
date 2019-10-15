from setuptools import setup

setup(
    name='FlaskAPP',
    packages=['FlaskAPP'],
    install_requires=[
        'flask',
        'flask-login',
        'flask-sqlalchemy'
    ]
)