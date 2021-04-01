from setuptools import setup

# with open("../README.md", "r") as fh:
#    long_description = fh.read()

setup(name='pulzar-pkg',
      version='21.4.1',
      author='Mauricio Cleveland',
      author_email='mauricio.cleveland@gmail.com',
      description='Distributed database and jobs',
      #    long_description=long_description,
      #     long_description_content_type="text/markdown",
      # data_files=[('/var/lib/pulzar/data', [])],
      url='http://github.com/cleve/pulzar',
      packages=['pulzarcore', 'pulzarutils'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux"
      ],
      python_requires='>=3.6',
      )
