from setuptools import setup


setup(
    name='pymidi',
    version='0.0.1',
    description='MIDI I/O for humans',
    author='Matt Hosack',
    author_email='hosack.matt@gmail.com',
    url='https://github.com/hosackm/PyMidi',
    packages=('pymidi', ),
    package_data={},
    package_dir={'pymidi': 'pymidi'},
    install_requires=('cffi', ),
    license='MIT',
    zip_safe=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
    extras_require={},
)
