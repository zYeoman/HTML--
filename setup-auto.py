from distutils.core import setup
import py2exe
setup(
    version="7",
    zipfile=None,
    console=['auto.py'],
    options={"py2exe": {"includes": ["sip"]}}
)
