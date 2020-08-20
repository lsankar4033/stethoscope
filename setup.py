import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stethoscope",
    version="0.0.1",
    author="Lakshman Sankar",
    author_email="me@lsankar.com",
    description="Network testing for Eth2 clients",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lsankar4033/stethoscope",
    packages=setuptools.find_packages(),
    install_requires=[
        # NOTE: to be consistent with pyrum's versions
        "trio==0.13.0",
        "pyrum>=0.3.0,<0.4.0",
        "stethoscope-clients==0.1.5",
        "PyYAML==5.3.1",
        "ansicolors==1.1.8",
        "eth-utils==1.8.4",
        "eth2spec==0.12.2",
        "eth2fastspec==0.0.5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
