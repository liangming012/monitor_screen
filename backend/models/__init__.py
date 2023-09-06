from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
#  列出.py当前文件夹下的所有python()文件，并将它们作为__all__变量放入__init__.py
#  其他目录的文件要使用时，直接 from models import *



