import os
import sys

from setuptools import setup, find_packages, Extension


REPO_DIR = os.path.dirname(os.path.realpath(__file__))


def findRequirements():
  """
  Read the requirements.txt file and parse into requirements for setup's
  install_requirements option.
  """
  return [
    line.strip()
    for line in open("requirements.txt").readlines()
    if not line.startswith("#")
  ]


description = """Auditory tools and experiments using HTM/CLA (for NuPIC).

This repository is structured as follows:
- stand-alone experiments in separate folders
- `Theory/` with collection of interesting papers
- `nupic/audio/` with reusable components (pip-installable), mainly Encoders
"""

if __name__ == "__main__":
 setup(
    name="nupic.audio",
    description=description,
    package_data = {"nupic.examples.data": ["*.wav"]},
    namespace_packages=["nupic"],
    packages=find_packages(),
    requires=findRequirements(),
    version="0.1.0",
    author="NuPIC-community",
    author_email="markotahal@gmail.com",
    url="https://github.com/nupic-community/nupic.audio",
#    zip_safe=False,
    classifiers=[
      "Programming Language :: Python",
      "Programming Language :: Python :: 2",
      "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
      "Operating System :: MacOS :: MacOS X",
      "Operating System :: POSIX :: Linux",
      "Operating System :: Microsoft :: Windows",
      # It has to be "5 - Production/Stable" or else pypi rejects it!
      "Development Status :: 5 - Production/Stable",
      "Environment :: Console",
      "Intended Audience :: Science/Research",
      "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    license="AGPL",
    keywords="HTM NuPIC audio AI encoders music",
 )
