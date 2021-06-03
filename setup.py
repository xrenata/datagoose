from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
]

setup(
    name='datagoose',
    version='1.6.1',
    description='Easy to use 👋 fast & lightweight ☄️ secure 🔐 JSON based database for python! 🐍.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/5elenay/datagoose/',
    author='5elenay',
    author_email='',
    license='GNU General Public License v3 (GPLv3)',
    project_urls={
        "Bug Tracker": "https://github.com/5elenay/datagoose/issues",
    },
    classifiers=classifiers,
    keywords=["database", "lightweight", "json", "python-database", "json-database", "fast", "secure"],
    packages=find_packages(),
    install_requires=['orjson']
)
