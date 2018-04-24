from setuptools import setup

setup(name='smartcrop',
      version='0.1',
      description='OpenCV smart crop with python',
      url='https://github.com/fizzday/imageCropSmart',
      author='Fizzday',
      author_email='fizzday@yeah.net',
      include_package_data=True,
      license='MIT',
      packages=['smartcrop'],
      scripts=['bin/smartcrop'],
      zip_safe=False)
