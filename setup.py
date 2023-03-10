from setuptools import setup, find_packages
from hiddenpng import __version__


with open('README.md') as readme:
    long_description = readme.read().strip()


setup(
    name='hiddenpng',
    version=__version__,
    description='Hide data inside Image files.',
    author='Gaurav Raj',
    url='https://github.com/thehackersbrain/hiddenpngpy',
    author_email='techw803@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['hiddenpng', 'steganography', 'python', 'thehackersbrain', 'gauravraj'],
    packages=find_packages(),
    install_requires=['rich', 'pillow', 'cryptography'],
    entry_points={'console_scripts': ['hiddenpng=hiddenpng.__main__:main']},
    zip_safe=False,
)
