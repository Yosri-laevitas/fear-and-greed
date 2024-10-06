from setuptools import setup, find_packages

setup(
    name='fear-and-greed',
    version='1.0.0',
    description='A Python package for analyzing fear and greed index data.',
    author='Your Name',
    author_email='yosri@laevitas.ch',
    url='https://github.com/your_username/fear-and-greed',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)