import PyInstaller.__main__
import os
import sys
import site

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取 Python 包安装路径
site_packages = site.getsitepackages()[0]

# 构建 ncmdump 模块的路径
ncmdump_path = os.path.join(site_packages, 'ncmdump')

print(f"Building with ncmdump path: {ncmdump_path}")

PyInstaller.__main__.run([
    'ncm_converter.py',
    '--onefile',
    '--clean',
    '--name=ncm_converter',
    '--distpath=./dist_python',
    '--workpath=./build_python',
    '--specpath=./build_python',
    '--hidden-import=ncmdump',
    '--hidden-import=ncmdump.dump',
    '--hidden-import=ncmdump.core',
    '--collect-all=ncmdump',
    '--log-level=DEBUG',
]) 