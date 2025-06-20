# NCM to MP3 Assistant

一个简单易用的 NCM 音乐文件转换工具，可以将网易云音乐的 NCM 格式转换为通用的 MP3 格式。

## 功能特点

- 支持单个或多个 NCM 文件拖放转换
- 支持整个文件夹批量转换
- 可选择是否保留原文件
- 支持自定义输出位置
- 实时显示转换进度
- 保存转换历史记录

## 系统要求

- Windows 操作系统
- Python 3.6 或更高版本
- Node.js 14 或更高版本

## 安装步骤

### 1. 安装 Python

1. 访问 [Python 官网](https://www.python.org/downloads/) 下载 Python
2. 运行下载的安装程序
3. **重要：** 在安装界面勾选 "Add Python to PATH" 选项
4. 点击 "Install Now" 开始安装

### 2. 安装依赖

1. 双击运行 `install_dependencies.py` 文件
2. 等待安装完成
3. 如果看到"安装成功"的提示，说明依赖已经安装完成

### 3. 安装 Node.js

1. 访问 [Node.js 官网](https://nodejs.org/) 下载 Node.js
2. 运行下载的安装程序
3. 点击 "Next" 继续安装
4. 点击 "I accept the terms in the License Agreement" 并点击 "Next"
5. 选择安装路径并点击 "Next"
6. 点击 "Install" 开始安装

### 4. 运行程序

开发模式：
```bash
npm run dev
```

构建可执行文件：
```bash
npm run build
```

构建完成后，可执行文件将在 `dist` 目录中生成。

## Windows 安全提示

由于程序未签名，在 Windows 系统上下载或运行程序时可能会遇到安全警告。这是正常现象，您可以按照以下步骤解决：

这个是因为没有购买证书的原因（穷），免费软件就不购买证书了
需要忽略这个警告强制保留文件
可能的解决方法：
点击右边三个-保留-查看更多-保留

这些警告是 Windows 的安全机制，用于保护用户免受潜在的安全威胁。本程序是开源的，您可以在 GitHub 上查看源代码，确认其安全性。

## 使用说明

### 拖放转换

1. 将 NCM 文件拖入虚线框内，或点击选择文件
2. 可以添加多个文件到转换列表
3. 选择是否自定义输出位置
4. 选择是否删除原文件
5. 点击"开始转换"按钮

### 文件夹转换

1. 选择包含 NCM 文件的输入文件夹
2. 选择是否自定义输出位置
3. 选择是否删除原文件
4. 点击"开始转换"按钮

## 注意事项

- 确保有足够的磁盘空间
- 转换过程中请勿关闭程序
- 建议定期备份重要文件

## 常见问题

### 1. 提示"请先安装 Python 依赖"
- 双击运行 `install_dependencies.py` 文件安装依赖

### 2. 转换失败
- 确保选择的文件是 NCM 格式
- 确保有足够的磁盘空间
- 确保输出位置有写入权限

### 3. 程序无法启动
- 确保已安装 Python
- 确保已运行 `install_dependencies.py` 安装依赖

### 4. 如果遇到 Node.js 相关错误
- 确保已正确安装 Node.js 和所需依赖

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 