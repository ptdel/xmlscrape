import os
from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))

requires = [
    "argparse",
    "progress",
    "lxml",
    "bs4",
    "xlsxwriter",
    ]

setup(
    name="xmlscrape",
    description="Extracts URLs from XML sitemaps located in the CWD.",
    classifiers=[
        "Development Status :: Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: SEO",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation :: Sphinx",
    ],
    author="@tcaldron",
    url="https://github.com/tcaldron/xmlscrape",
    keywords="xml sitemap scrape parse seo",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="xmlscrape",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=requires,
)