import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='comapsmarthome-public-api',
    version='<VERSION_NUMBER>',
    packages=setuptools.find_packages(),
    url='https://gitlab.com/melec/comapsmarthome_public_api_python',
    license='MIT',
    author='Melec Petit-Pierre',
    author_email='melec.petit-pierre@comap.eu',
    description='Comap Smart Home public API python module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'boto3',
        'python-dateutil'
    ],
    python_requires='>=3.6',
)
