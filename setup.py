from setuptools import setup, find_packages

setup(
    name='sensorviz',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7,<8',
            'flake8>=5,<6',
            ],
        },
    entry_points={
        'console_scripts': [
            'sensorviz = sensorviz.sensorviz:main',
        ],
    },
    author='Hagen Paul Pfeifer',
    author_email='hagen@jauu.net',
    description='Visualize Sensor Push CSV daata',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='sensor-push',
    url='https://github.com/hgn/sensorviz',
)
