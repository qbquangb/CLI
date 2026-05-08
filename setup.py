import io
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='thuongcli',
    version='1.1.4',
    author='Trần Đình Thương',
    author_email='qbquangbinh@gmail.com',
    # url='https://github.com/qbquangb/thuongcli',
    url='https://github.com/qbquangb/cli',
    description='Công cụ dòng lệnh (CLI) điều khiển máy tính và xử lý tệp',
    long_description=long_description,
    long_description_content_type='text/markdown',  
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "thuongcli": [
            "*.bat",
            "*.pyw",
            "*.py",
            "*.txt",
            "*.yaml",
        ],
    },
    python_requires='>=3.10.6',
    install_requires=[
        'thuonglib',
        'pycryptodome',
        'numpy',
        'pillow',
    ],
    entry_points={
        'console_scripts': [
            'cli=thuongcli.thuongcli:main',
        ],
    },
)

'''
1. python setup.py sdist bdist_wheel
2. python -m twine upload --repository testpypi dist/*
   python -m twine upload dist/*
   python -m twine upload --skip-existing dist/*
3. pip install --index-url https://test.pypi.org/simple/ my-package
   pip install thuongcli
   pip install --no-cache-dir thuongcli
'''
