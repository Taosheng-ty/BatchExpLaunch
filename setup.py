import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BatchExpLaunch",
    version="0.0.3",
    author="Tao Yang",
    author_email="taoyang@cs.utah.edu",
    description="A project for batch scripts submission",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Taosheng-ty/BEL.git",
    project_urls={
        "Bug Tracker": "https://github.com/Taosheng-ty/BEL/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
    scripts=['bin/slurm_python','bin/Extract_result'],
)
