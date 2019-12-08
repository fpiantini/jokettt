import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jokettt",
    version="0.0.1",
    author="Francesco Piantini",
    author_email="francesco.piantini@gmail.com",
    description="A Tic Tac Toe game developed by joke",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fpiantini/jokettt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)

