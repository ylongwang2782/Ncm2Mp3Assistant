# NCM to MP3 Assistant

一个使用 Electron + Vue 开发的 NCM 格式转 MP3 格式的桌面应用程序。

## 系统要求

- Windows 操作系统
- Node.js 16.0 或更高版本
- Python 3.6 或更高版本

## 安装步骤

### 1. 安装 Python 环境

1. 访问 [Python 官网](https://www.python.org/downloads/) 下载并安装 Python 3.6 或更高版本
2. 安装时请勾选 "Add Python to PATH" 选项
3. 安装完成后，打开命令提示符（CMD）或 PowerShell，输入以下命令验证安装：
   ```bash
   python --version
   ```

### 2. 安装 Python 依赖

1. 打开命令提示符（CMD）或 PowerShell
2. 进入项目目录
3. 运行以下命令安装必要的 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 3. 安装 Node.js 依赖

1. 确保已安装 Node.js
2. 在项目目录中运行：
   ```bash
   npm install
   ```

## 运行应用

### 开发模式

1. 启动开发服务器：
   ```bash
   npm run dev
   ```
2. 在另一个终端窗口启动 Electron：
   ```bash
   npm run electron:dev
   ```

### 生产模式

1. 构建应用：
   ```bash
   npm run build
   npm run electron:build
   ```
2. 在 `dist_electron` 目录下找到安装程序
3. 运行安装程序安装应用

## 使用说明

### 单个文件转换

1. 点击"单个转换"标签页
2. 点击"浏览"按钮选择要转换的 NCM 文件
3. 如果需要自定义输出位置：
   - 勾选"自定义输出位置"
   - 点击"浏览"按钮选择输出文件夹
4. 点击"开始转换"按钮
5. 等待转换完成

### 批量转换

1. 点击"批量转换"标签页
2. 点击"浏览"按钮选择包含 NCM 文件的文件夹
3. 如果需要自定义输出位置：
   - 勾选"自定义输出位置"
   - 点击"浏览"按钮选择输出文件夹
4. 点击"开始转换"按钮
5. 等待所有文件转换完成

## 注意事项

- 确保系统已安装 Python 并已添加到系统环境变量
- 确保已安装所有必要的 Python 依赖
- 转换过程中请勿关闭应用程序
- 如果遇到问题，请检查 Python 和依赖是否正确安装

## 常见问题

1. 提示"请先安装 Python 依赖"
   - 运行 `pip install -r requirements.txt` 安装依赖

2. 转换失败
   - 检查输入文件是否存在
   - 检查输出路径是否有写入权限
   - 确保 Python 环境正确安装

3. 程序无法启动
   - 检查 Node.js 是否正确安装
   - 检查是否已安装所有依赖
   - 尝试重新安装应用 