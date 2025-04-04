from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="twikit_happens",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A framework for building Twitter/X bots and automation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/twikit_happens",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "twikit>=0.1.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "black>=21.5b2",
            "flake8>=3.9.2",
        ],
    },
)