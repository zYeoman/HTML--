from distutils.core import setup
import py2exe
setup(console=['html.py'], version='7',
      zipfile=None,
      options={"py2exe": {"includes": ["sip"]}})
