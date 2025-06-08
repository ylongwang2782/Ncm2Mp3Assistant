import subprocess
import sys
import os
import time
from tkinter import messagebox, Tk

def show_message(title, message):
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo(title, message)
    root.destroy()

def install_dependencies():
    try:
        # 配置pip使用国内镜像
        print("正在配置pip镜像源...")
        subprocess.run([sys.executable, "-m", "pip", "config", "set", "global.index-url", "https://pypi.tuna.tsinghua.edu.cn/simple"], check=True)
        
        print("正在安装依赖...")
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, "requirements.txt")
        
        # 安装依赖
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            show_message("安装成功", "Python依赖安装成功！\n现在可以运行NCM to MP3 Assistant了。")
        else:
            error_msg = f"安装失败：\n{result.stderr}"
            show_message("安装失败", error_msg)
            
    except Exception as e:
        show_message("错误", f"安装过程中出现错误：\n{str(e)}")

if __name__ == "__main__":
    print("开始安装Python依赖...")
    install_dependencies()
    # 等待用户查看消息框
    time.sleep(1) 