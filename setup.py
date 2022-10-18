import setuptools
import os


def load_requirements():
    folder = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(folder, 'requirements.txt')
    with open(filename) as f:
        lines = f.read().splitlines()
    install_requires = []
    for line in lines:
        if not line.startswith("#"):
            install_requires.append(line)
    return install_requires


setuptools.setup(
    name="dsa-pywnprpc",
    version="1.0.1",
    packages=setuptools.find_namespace_packages(include=["dsa.*", ]),
    install_requires=load_requirements(),
)
