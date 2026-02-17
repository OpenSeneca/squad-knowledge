from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-code-analyzer",
    version="1.0.0",
    author="OpenSeneca",
    description="Analyze Claude Code session logs and identify inefficiencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenSeneca/claude-code-analyzer",
    py_modules=["claude-analyzer"],
    entry_points={
        "console_scripts": [
            "claude-analyzer=claude-analyzer:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    keywords="claude code ai session analyzer productivity",
    project_urls={
        "Bug Reports": "https://github.com/OpenSeneca/claude-code-analyzer/issues",
        "Source": "https://github.com/OpenSeneca/claude-code-analyzer",
    },
)
