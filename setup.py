from setuptools import setup, find_packages

setup(
    name='myproj',
    description='',
    author='Adrian van den Houten',
    author_email='adrianvdh@gmail.com',
    use_scm_version=True,  # Version from git
    setup_requires=['setuptools_scm'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
)
