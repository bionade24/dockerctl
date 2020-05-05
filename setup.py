from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "dockerctl",
    version = "0.4",
    description = "Python Script to steer (multiple) docker-compose-yaml's from everywhere.",
    long_description= long_description,
    url = "https://github.com/bionade24/dockerctl",
    author = "Oskar Roesler (bionade24)",
    author_email = "o.roesler@oscloud.info",
    license = "GPLv3",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        "Operating System :: POSIX :: Linux",
    ],
    py_modules = ["dockerctl"],
    install_requires = ["argparse", "docker-compose"],
    packages = ["dockerctl"],
    scripts = ["bin/dockerctl"]
)
