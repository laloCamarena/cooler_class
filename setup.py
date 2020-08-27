from setuptools import setup

setup(name='cooler-class',
    version='0.0.1',
    description='Live online classes',
    author='Eduardo Camarena Santamaria',
    author_email='lalo.a.camarena@gmail.com',
    package_dir={'': 'src'},
    packages=['cooler_class'],
    install_requires=[
        'numpy', 'sqlalchemy', 'pandas', 'seaborn',
        'mysqlclient', 'opencv-python', 'flask',
        'flask-sqlalchemy', 'flask-restful', 'flask-cors',
        'PyQt5==5.13.0', 'pyqt5-tools', 'pytest'
    ]
)