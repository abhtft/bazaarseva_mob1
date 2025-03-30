from setuptools import setup, find_packages

setup(
    name="dep-sustomer-suvidha",
    version="1.0.0",
    description="A shopping list management system for Kirana shops",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.0.2",
        "pymongo>=4.6.1",
        "reportlab>=4.1.0",
        "python-dotenv>=1.0.1",
        "Werkzeug>=3.0.1",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 