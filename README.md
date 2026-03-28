# 🎬 Video Organizer Tool

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)

一个强大的视频文件整理工具，能够递归遍历目录，将所有视频文件移动到一级目录，并智能删除空文件夹。

## ✨ 特性

- **递归搜索**：深度查找所有子文件夹中的视频文件
- **智能整理**：将视频文件移动到一级目录，自动处理文件名冲突
- **安全清理**：仅删除完全空的文件夹，保护您的数据
- **双版本支持**：提供命令行和GUI图形界面两种版本
- **格式广泛**：支持20+种常见视频格式
- **详细日志**：完整的操作记录，方便追踪和排查

## 📁 支持的文件格式

| 格式 | 扩展名 |
|------|--------|
| MP4 | `.mp4` |
| AVI | `.avi` |
| MKV | `.mkv` |
| MOV | `.mov` |
| WMV | `.wmv` |
| FLV | `.flv` |
| WebM | `.webm` |
| MPEG | `.mpg`, `.mpeg` |
| 3GP | `.3gp` |
| TS | `.ts`, `.mts`, `.m2ts` |
| 其他 | `.rm`, `.rmvb`, `.asf`, `.divx`, `.vob`, `.dat`, `.f4v`, `.swf` |

## 🚀 快速开始

### 系统要求
- Windows 7/8/10/11
- Python 3.6+

### 安装Python
如果尚未安装Python：
1. 访问 [python.org](https://www.python.org/downloads/)
2. 下载最新版本
3. 安装时勾选 "Add Python to PATH"

### 使用方法

#### 方案A：GUI图形界面版本（推荐）
1. 双击运行 `视频整理器_GUI.bat`
2. 点击"浏览..."按钮选择目录
3. 点击"开始整理"
4. 实时查看处理进度和日志

#### 方案B：命令行版本
1. 双击运行 `视频整理器.bat`
2. 按提示输入或拖拽目录路径
3. 确认后开始整理

## 📋 文件结构

```
Video-Organizer-Tool/
├── video_organizer.py      # 命令行版本核心脚本
├── video_organizer_gui.py  # GUI图形界面版本核心脚本
├── 视频整理器.bat          # 命令行版本启动文件
├── 视频整理器_GUI.bat      # GUI版本启动文件
├── README.md              # 项目说明文档
├── .gitignore            # Git忽略文件配置
└── 使用说明.txt          # 详细中文使用说明
```

## 🔧 技术细节

### 主要功能模块
1. **文件搜索模块**：递归遍历目录树，识别视频文件
2. **文件移动模块**：安全移动文件，自动重命名处理冲突
3. **文件夹清理模块**：智能检查并删除空文件夹
4. **日志记录模块**：详细记录所有操作步骤

### 安全特性
- ✅ 不会删除原始目录
- ✅ 不会删除非空文件夹  
- ✅ 操作前有确认提示
- ✅ 支持操作撤销（手动）

## 📝 使用示例

### 命令行版本示例
```bash
视频文件整理器 v1.0
==========================================
请选择要整理的目录：D:\Downloads\Videos

正在搜索视频文件...
找到 47 个视频文件

正在移动视频文件...
处理: movie1.mp4 ✓ 已移动到: movie1.mp4
处理: video2.avi ✓ 已移动到: video2_1.avi (重命名)

正在删除空文件夹...
✓ 删除空文件夹: subfolder1
✓ 删除空文件夹: subfolder2

处理完成！
视频文件总数: 47
成功移动: 47
移动失败: 0
删除空文件夹: 8
```

### GUI版本截图
![GUI界面](https://via.placeholder.com/600x400/3498db/ffffff?text=Video+Organizer+GUI)

## ⚠️ 重要注意事项

1. **使用前请备份重要数据**
2. 程序只能删除完全空的文件夹
3. 处理大量文件时请耐心等待
4. 建议先在测试目录试用

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 作者

**尼克 (Nick)**
- 项目创建者和维护者
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 致谢

感谢所有为本项目做出贡献的用户和开发者！

---

⭐ 如果这个项目对你有帮助，请给个星星支持！