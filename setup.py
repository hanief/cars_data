import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="cars-data",
  version="0.0.1",
  author="Hanief Utama",
  author_email="hanief@gmail.com",
  description="A package to get cars data",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.6",
  install_requires=[
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
  ]
)
