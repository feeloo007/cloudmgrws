VERSION = '0.0.1'

from setuptools import setup, find_packages

setup(
      name = 'cloudmgrws',
      version = VERSION,
      author = '',
      author_email = '',
      description = '',
      license = '',
      keywords = '',
      url = '',
      packages = find_packages(),
      include_package_data = True,
      package_data = {'' : ['*.cfg']},
      zip_safe = False,
      install_requires = (
          'nagare==0.4.1',
          'ssh==1.7.13',
          'Fabric==1.4.1',
          'jinja2==2.6',
          'pyinotify==0.9.4',
      ),
      message_extractors = { 'cloudmgrws' : [('**.py', 'python', None)] },
      entry_points = """
      [nagare.applications]
      cloudmgrws = cloudmgrws.app:app
      """
     )

