import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noswear",
    version="0.1",
    author="FOSS-Devs",
    description="A library for detection swear words.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FOSS-Devs/noswear",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["requests", "re"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
