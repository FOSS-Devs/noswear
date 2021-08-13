import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noswear",
    version="0.1",
    author="FOSS-Devs",
    description="A library for detecting swear words.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FOSS-Devs/noswear",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    data_files=[('noswear', ['noswear/data/wordlist.txt']), ('noswear', ['noswear/data/clean.json']) ],
    package_data={
        'badwords': ['noswear/wordlist.txt'],
        'cleanword': ['noswear/clean.json']
    },
)
