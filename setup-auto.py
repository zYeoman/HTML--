from distutils.core import setup
import py2exe
setup(console=['auto.py'], zipfile=None,
      options={"py2exe": {"includes": ["sip"]}})
