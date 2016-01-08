from setuptools import setup


setup(name='stim',
      version='0.1.0',
      description='stim -- an optimizing brainfuck-to-C compiler',
      url='http://github.com/dasmithii/stim',
      author='Douglas Adam Smith II',
      author_email='douglassmith@umass.edu',
      license='MIT',
      packages=['stim'],
      install_requires=[
          'docopt',
      ],
      zip_safe=False,
      long_description=open('README.txt').read(),
      scripts=['bin/stim'],)