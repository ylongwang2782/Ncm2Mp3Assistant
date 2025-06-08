import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'ncm_converter.py',
    '--onefile',
    '--clean',
    '--name=ncm_converter',
    '--distpath=./dist_python',
    '--workpath=./build_python',
    '--specpath=./build_python',
    '--hidden-import=ncmdump',
]) 