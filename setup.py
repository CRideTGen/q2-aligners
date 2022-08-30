from setuptools import setup, find_packages
import versioneer
setup(
    name='q2-readmappers',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    url='github.com/CRideTGen/q2-readmappers',
    license='Academic and Research License',
    author='Chase Ridenour',
    author_email='cridenour@tgen.org',
    description='',
    entry_points={
        'qiime2.plugins': ['q2-readmappers=q2_readmappers.plugin_setup:plugin']
    },
    zip_safe=False,
)
