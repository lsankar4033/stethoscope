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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
