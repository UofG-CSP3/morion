import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CSP3_project",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'pydantic>=1.9',
        'pymongo>=4'
    ],
    python_requires=">=3.7",
)