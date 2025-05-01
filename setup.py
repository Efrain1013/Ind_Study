from setuptools import setup, find_packages

setup(
    name="bandtool",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        # add any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "bandtool=bandtool.main:main",  # or whatever the entry point is
        ],
    },
    author="Efrain Martinez",
    author_email="efrain1013@gmail.com",
    description="A tool for analyzing electronic band structure data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Efrain1013/bandtool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
