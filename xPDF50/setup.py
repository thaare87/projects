from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='xPDF50',
    version='0.0.1',
    description='Get clean PDFs of CS50 course materials from thier URLs',
    long_description = long_description, long_description_content_type=("text/markdown"),
    py_modules=["xPDF50", "prepare"],
    package_dir={'':'src'},
    classifiers = [
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require = {
            "dev": [
                "pytest>=3.7",
            ],
    },
    url="https://github.com/thaare87/projects/tree/master/xPDF50",
    author="Thaare87",
    author_email="thaare87@gmail.com",
)

