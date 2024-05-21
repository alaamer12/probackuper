from setuptools import setup

setup(
    name='probackuper',
    version='0.0.1',
    packages=['tests', 'utils', 'utils.helpers', 'future', 'commands', 'commands.handler', 'commands.strategies',
              'commands.strategies.vendors'],
    url='https://github.com/alaamer12/probackuper',
    license='MIT',
    author='Alaamer',
    author_email='alaamerthefirst@gmail.com',
    description='A small file based-backup system to make backups for important files only.',
    long_description=open('README.md').read(),  # noqa: SIM115
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt').read().splitlines(),  # noqa: SIM115
    entry_points={'probackup': ['probackuper=main']}
    # entry_points={'console_scripts': ['probackuper=main:main']}

)
