from setuptools import setup, find_packages

setup(
    name='skin-cancer-detection',
    version='0.1',
    description='A project for skin cancer detection using image analysis and neural networks.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'kedro',
        'numpy',
        'pandas',
        'scikit-learn',
        'tensorflow',  # or 'torch' if using PyTorch
        'opencv-python',
        'matplotlib',
        'seaborn',
        'jupyter'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)