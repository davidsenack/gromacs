from setuptools import setup, find_packages

setup(
    name='gromacs',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gromacs=gromacs.gromacs:main',  # Adjust this if your main function is located differently
        ],
    },
    author='David Senack',
    author_email='david.senack@gmail.com',
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourgithub/gromacs',
    install_requires=[
        # List your project's dependencies here, e.g.,
        # 'numpy',
        # 'pandas',
    ],
    classifiers=[
        # Choose your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)