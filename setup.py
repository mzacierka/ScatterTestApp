from setuptools import setup

setup(
    name='FlaskAPP',
    packages=['FlaskAPP'],
    install_requires=[
        'flask',
        'flask-login',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'flask-sqlalchemy',
        'flask-security',
        'PyMySQL',
        'wtforms',
        'requests',
        'XlsxWriter'
    ]
)
