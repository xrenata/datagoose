from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='datagoose',
  version='1.0.0',
  description='Easy to use database for python.',
  long_description_content_type="text/markdown",
  long_description=open('README.md').read(),
  url='https://github.com/5elenay/datagoose/', 
  author='5elenay',
  author_email='',
  license='GNU General Public License v3 (GPLv3)', 
  classifiers=classifiers,
  keywords='database', 
  packages=find_packages(),
  install_requires=[''] 
)