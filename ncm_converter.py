import sys
import os

def check_module(module_name):
    try:
        __import__(module_name)
        print(f"成功导入模块: {module_name}")
        return True
    except ImportError as e:
        print(f"导入模块失败 {module_name}: {str(e)}")
        return False

# 检查必要的模块
required_modules = ['ncmdump', 'ncmdump.dump', 'ncmdump.core']
for module in required_modules:
    if not check_module(module):
        print(f"error:缺少必要的模块 {module}")
        sys.exit(1)

from ncmdump import dump

def convert_file(input_file, output_file):
    try:
        print(f"开始转换: {input_file} -> {output_file}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"Python 路径: {sys.path}")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        dump(input_file, output_file)
        print("success")
    except Exception as e:
        print(f"error:{str(e)}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    print("Python 脚本开始执行")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"命令行参数: {sys.argv}")
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.path}")
    
    if len(sys.argv) != 3:
        print("error:Invalid arguments")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"error:Input file does not exist: {input_file}")
        sys.exit(1)
    
    print(f"输入文件存在: {input_file}")
    convert_file(input_file, output_file) 