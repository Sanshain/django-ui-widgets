python setup.py sdist
twine upload dist/*
:: twine upload --skip-existing dist/*