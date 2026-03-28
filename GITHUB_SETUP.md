# 🚀 推送到GitHub指南

本指南将帮助你将Video Organizer Tool项目推送到GitHub。

## 📋 前提条件

1. 已安装Git
2. 已创建GitHub账户
3. 已配置Git全局用户名和邮箱

## 🔧 配置Git（如果尚未配置）

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

## 🎯 推送到GitHub的步骤

### 步骤1：在GitHub上创建新仓库
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `Video-Organizer-Tool`
   - Description: `一个强大的视频文件整理工具，能够递归遍历目录，将所有视频文件移动到一级目录，并智能删除空文件夹。`
   - Public (公开) 或 Private (私有)
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 步骤2：添加远程仓库URL
在本地项目目录执行：

```bash
cd "F:\github\Video-Organizer-Tool"

# 使用HTTPS方式（推荐新手）
git remote add origin https://github.com/你的用户名/Video-Organizer-Tool.git

# 或者使用SSH方式（需要配置SSH密钥）
# git remote add origin git@github.com:你的用户名/Video-Organizer-Tool.git
```

### 步骤3：推送到GitHub

```bash
# 第一次推送
git push -u origin master

# 或者如果你使用main分支
git branch -M main
git push -u origin main
```

### 步骤4：验证推送成功
1. 访问你的GitHub仓库页面
2. 刷新页面查看文件
3. 确认所有文件已成功上传

## 🔐 认证方式

### 方式A：HTTPS + Personal Access Token（推荐）
1. 在GitHub设置中生成Token：
   - Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 生成新token，勾选 `repo` 权限
2. 推送时会提示输入用户名和密码：
   - 用户名：你的GitHub用户名
   - 密码：刚才生成的token

### 方式B：SSH密钥
1. 生成SSH密钥：`ssh-keygen -t ed25519 -C "your_email@example.com"`
2. 将公钥添加到GitHub：Settings → SSH and GPG keys
3. 使用SSH URL添加远程仓库

## 🌐 访问你的GitHub仓库

仓库创建后，可以通过以下URL访问：
```
https://github.com/你的用户名/Video-Organizer-Tool
```

## 📊 仓库状态检查

### 检查本地仓库状态
```bash
git status
git log --oneline
```

### 检查远程仓库配置
```bash
git remote -v
```

### 强制推送（如果遇到问题）
```bash
git push -f origin master
```

## 🎨 添加GitHub特性

推送成功后，你可以：

### 1. 添加徽章
在README.md中添加状态徽章：

```markdown
![GitHub stars](https://img.shields.io/github/stars/你的用户名/Video-Organizer-Tool)
![GitHub forks](https://img.shields.io/github/forks/你的用户名/Video-Organizer-Tool)
![GitHub issues](https://img.shields.io/github/issues/你的用户名/Video-Organizer-Tool)
```

### 2. 启用GitHub Pages
为项目创建文档网站：
1. Settings → Pages
2. Source: `master` branch
3. Folder: `/docs` (或root)

### 3. 添加议题模板
在 `.github/ISSUE_TEMPLATE/` 目录下创建模板文件

### 4. 添加Pull Request模板
在 `.github/PULL_REQUEST_TEMPLATE.md` 创建模板

## 🛠️ 常见问题解决

### 问题1：认证失败
```
remote: Support for password authentication was removed...
```
**解决方案**：使用Personal Access Token代替密码

### 问题2：权限拒绝
```
Permission denied (publickey)
```
**解决方案**：配置SSH密钥或使用HTTPS方式

### 问题3：分支不匹配
```
error: failed to push some refs
```
**解决方案**：
```bash
git pull origin master --rebase
git push -u origin master
```

### 问题4：文件名编码问题
**解决方案**：使用UTF-8编码，Git已正确处理中文文件名

## 📞 获取帮助

- GitHub官方文档：https://docs.github.com
- Git官方文档：https://git-scm.com/doc
- 社区支持：Stack Overflow

## ✅ 完成检查清单

- [ ] 已在GitHub创建 `Video-Organizer-Tool` 仓库
- [ ] 已配置本地Git用户名和邮箱
- [ ] 已添加远程仓库URL
- [ ] 已成功推送代码
- [ ] 已验证GitHub页面显示正常
- [ ] 已添加项目描述和标签

---

🎉 **恭喜！你的Video Organizer Tool项目现已成功托管在GitHub上！**