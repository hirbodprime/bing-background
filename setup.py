import setuptools


with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bing-background',
    version='0.0.1',
    author='hirbod aflaki',
    author_email='hirbodprime@gmail.com',
    description='downloads bing background with some other modules',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://git.pe42.ir/hirbod/bing-background-python',
    # project_urls = {
        # "Bug Tracker": "https://git.pe42.ir/hirbod/bing-background-python/issues"
    # },
    keywords=['python', 'bing','daily bing picture' 'beautifulsoup'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license='MIT',
    packages=['bing-background'],
    install_requires=['beautifulsoup4' , 'requests'],
)