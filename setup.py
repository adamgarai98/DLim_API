import pathlib

import pkg_resources
import setuptools

import versioneer

install_requires = []
with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]


setuptools.setup(
    name="dlim_api",
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requires,
    packages=setuptools.find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "dlim_api=dlim_api.__main__:main",
        ],
    },
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    extras_require={
        "dev": ["check-manifest", "versioneer"],
        # 'test': ['coverage'],
    },
    author="Adam Garai",
    author_email="a.garai98@gmail.com",
)
