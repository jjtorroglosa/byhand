from setuptools import setup, find_packages
setup(
        name="byhand",
        version="1.0",
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        py_modules=["__main__"],
        python_requires='>3.5',
        install_requires=['Jinja2', 'configobj', 'pyyaml', 'clipboard'],
        package_dir={'byhand': 'byhand'},
        entry_points={
            'console_scripts': [
                'byhand = byhand.__main__:main'
            ]
        }
)
