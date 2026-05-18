from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="padiem_ai",
    version="0.1.0",
    description="AI ERP for Korean SMEs",
    author="Padiem",
    author_email="noreply@padiem.co.kr",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
