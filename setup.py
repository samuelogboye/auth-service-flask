from setuptools import setup, find_packages

setup(
    name='authentication_service',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-Bcrypt',
        'Flask-JWT-Extended',
        'Flask-Script',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'run=manage:manager.run'
        ]
    },
)
