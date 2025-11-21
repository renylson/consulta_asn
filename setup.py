"""
Setup configuration for ASN Lookup Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="asn-lookup-tool",
    version="1.1.0",
    author="Renylson Marques",
    author_email="renylsonm@gmail.com",
    description="Uma aplicação web Flask para consulta de informações ASN através de IPs ou domínios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renylson/consulta_asn",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "isort>=5.12",
        ],
    },
    entry_points={
        "console_scripts": [
            "asn-lookup=app:main",
        ],
    },
    include_package_data=True,
    keywords="asn, ip lookup, network tools, flask, ipinfo",
    project_urls={
        "Bug Reports": "https://github.com/renylson/consulta_asn/issues",
        "Source": "https://github.com/renylson/consulta_asn",
        "Documentation": "https://github.com/renylson/consulta_asn#readme",
    },
)
