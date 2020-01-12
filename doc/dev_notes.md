# Notes for developers

## How to publish the package to PyPi

Short answer:

```sh
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

Refer to the following pages for further details:

- [Packaging Python Projects]
- [How to upload your python package to PyPi]

## Conda

General useful information about managing environments:

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html


### How to update an enviroment

```sh
conda env update --file environment.yml  --prune
```

[Packaging Python Projects]: https://packaging.python.org/tutorials/packaging-projects/
[How to upload your python package to PyPi]: https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
