# NCM to MP3 Converter

一个使用 Electron + Vue 开发的 NCM 格式转 MP3 格式的桌面应用程序。

## 系统要求

- Windows 操作系统
- Node.js 16.0 或更高版本
- Python 3.6 或更高版本

## 安装步骤

1. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

2. 安装 Node.js 依赖：
```bash
npm install
```

## 开发模式运行

1. 启动开发服务器：
```bash
npm run dev
```

2. 在另一个终端窗口启动 Electron：
```bash
npm run electron:dev
```

## 构建应用

1. 构建 Vue 应用：
```bash
npm run build
```

2. 构建 Electron 应用：
```bash
npm run electron:build
```

构建完成后，可以在 `dist_electron` 目录下找到打包好的应用程序。

## 功能特点

1. 单个文件转换
   - 选择单个 NCM 文件进行转换
   - 可选择自定义输出位置
   - 默认输出到原文件所在目录

2. 批量转换
   - 选择包含多个 NCM 文件的文件夹
   - 可选择自定义输出文件夹
   - 默认输出到原文件夹
   - 显示转换进度

## 注意事项

- 确保系统已安装 Python 并已添加到系统环境变量
- 确保已安装所有必要的 Python 依赖
- 转换过程中请勿关闭应用程序 