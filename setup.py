from setuptools import find_packages, setup

setup(
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    entry_points={
        'console_scripts': [
            'airflow-check = airflow_hook.check_local_test_items:main',
        ],
    },
)
