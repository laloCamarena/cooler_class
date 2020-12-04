from setuptools import setup

try:
    with open('requirements.txt') as f:
        install_reqs = f.read().splitlines()
except Exception:
    install_reqs = []

setup(name='cooler-class',
    version='0.0.1',
    description='Live online classes',
    author='Eduardo Camarena Santamaria',
    author_email='lalo.a.camarena@gmail.com',
    package_dir={'': 'src'},
    packages=['cooler_class'],
    install_requires=install_reqs
)