from distutils.core import setup
import py2exe
setup(console=['auto.py'], options={"py2exe": {"includes": ["sip"]}})
