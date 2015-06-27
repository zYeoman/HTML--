from distutils.core import setup
import py2exe
setup(console=['html.py'], options={"py2exe": {"includes": ["sip"]}})
