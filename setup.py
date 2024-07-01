import setuptools

setuptools.setup(
    include_package_data=True,
    name='jotdown',
    version='0.1',
    description='journaling tool for coders',
    url='https://github.com/rurangiza/jotdown',
    author='Arsene Rurangiza',
    author_email='a.rurangiza@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'pytest',
    ],
    long_description='',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)