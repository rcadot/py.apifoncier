from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="apifoncier",
    version="0.0.27",
    description="Mobiliser les données foncières de l'api du Cerema directement avec python",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rcadot/py.apifoncier",
    author="Romain Cadot",
    author_email="romain.cadot@cerema.fr",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["api", "foncier", "cerema", "dv3f", "friches", "artificialisation"],
    install_requires=["pandas", "requests", "geopandas", "tqdm"],
    extras_require={"dev": ["pytest"]},
    python_requires=">=3.9",
)
