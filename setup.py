from setuptools import setup, find_packages
import versioneer
setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
