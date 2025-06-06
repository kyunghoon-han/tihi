from setuptools import setup, find_packages

setup(
    name='tihi',
    version='0.9.0',
    description='A GUI tool that can detrend the signal, identify its peaks and fit the signal with distributions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kyunghoon HAN',
    author_email='kyunghoon.h@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5==5.15.10',
        'pyqtgraph==0.13.3',
        'numpy',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'tihi=tihi.app:main',  # Correctly specify the path to main function
        ],
    },
)
