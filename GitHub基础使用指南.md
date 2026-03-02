# GitHub 基础使用指南

## 目录
1. [什么是GitHub](#什么是github)
2. [注册账号](#注册账号)
3. [基础概念](#基础概念)
4. [创建第一个仓库](#创建第一个仓库)
5. [常用操作](#常用操作)
6. [协作流程](#协作流程)
7. [常用工具](#常用工具)

---

## 什么是GitHub

**GitHub** 是全球最大的代码托管平台，基于 **Git** 版本控制系统。

**主要功能：**
- 🗂️ 代码托管和版本管理
- 🤝 团队协作开发
- 🐛 Bug追踪（Issues）
- 📋 项目管理（Projects）
- 🚀 自动化部署（Actions）
- 🌐 免费静态网站托管（Pages）

---

## 注册账号

### 步骤：
1. 访问 https://github.com
2. 点击 **"Sign up"**
3. 填写信息：
   - 邮箱地址
   - 密码
   - 用户名（唯一，会成为你的主页地址）
4. 验证邮箱
5. 选择免费计划（Free）

### 设置个人资料：
- 上传头像
- 填写Bio（简介）
- 添加个人网站链接

---

## 基础概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Repository (仓库)** | 存放项目代码的地方 | 项目文件夹 |
| **Commit (提交)** | 保存代码的变更记录 | 保存游戏存档 |
| **Branch (分支)** | 代码的平行版本 | 游戏的不同存档槽 |
| **Pull Request (PR)** | 请求合并代码 | 申请审核修改 |
| **Fork** | 复制别人的仓库到自己的账号 | 复制别人的文档 |
| **Clone** | 下载仓库到本地 | 下载文件 |
| **Push** | 上传本地代码到GitHub | 上传文件 |
| **Pull** | 下载GitHub最新代码到本地 | 同步文件 |

---

## 创建第一个仓库

### 网页端创建：
1. 点击右上角 **"+"** → **"New repository"**
2. 填写信息：
   - **Repository name**: 仓库名称（如 `my-first-project`）
   - **Description**: 项目描述（可选）
   - **Public/Private**: 公开或私有
   - **Initialize with README**: 勾选（创建说明文件）
3. 点击 **"Create repository"**

### 仓库页面说明：
```
📁 仓库名/
├── 📄 README.md      # 项目说明文档
├── 📁 src/           # 源代码文件夹
├── 📄 .gitignore     # 忽略文件配置
└── 📄 LICENSE        # 开源协议
```

---

## 常用操作

### 1. 上传文件（网页端）
1. 进入仓库
2. 点击 **"Add file"** → **"Upload files"**
3. 拖拽文件或点击选择
4. 填写提交信息（Commit message）
5. 点击 **"Commit changes"**

### 2. 编辑文件（网页端）
1. 点击文件名
2. 点击 ✏️ 编辑图标
3. 修改内容
4. 填写提交信息
5. 点击 **"Commit changes"**

### 3. 删除文件
1. 点击文件名
2. 点击 🗑️ 删除图标
3. 确认删除

### 4. 查看历史版本
- 点击 **"Commits"** 查看所有提交记录
- 点击任意提交查看当时的代码状态

---

## 命令行操作（推荐）

### 安装Git
- **Windows**: https://git-scm.com/download/win
- **Mac**: `brew install git`
- **Linux**: `sudo apt install git`

### 配置Git
```bash
# 设置用户名和邮箱
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 查看配置
git config --list
```

### 基础命令速查

```bash
# 1. 克隆仓库到本地
git clone https://github.com/用户名/仓库名.git

# 2. 进入仓库文件夹
cd 仓库名

# 3. 查看当前状态
git status

# 4. 添加文件到暂存区
git add 文件名          # 添加单个文件
git add .               # 添加所有修改

# 5. 提交更改
git commit -m "提交说明"

# 6. 推送到GitHub
git push origin main

# 7. 拉取最新代码
git pull origin main
```

### 完整工作流程
```bash
# 第一次使用
 git clone https://github.com/你的用户名/仓库名.git
cd 仓库名

# 日常开发循环
# 1. 拉取最新代码
git pull origin main

# 2. 修改代码...

# 3. 查看修改
git status

# 4. 添加修改
git add .

# 5. 提交
git commit -m "修复了登录bug"

# 6. 推送
git push origin main
```

---

## 协作流程

### 参与开源项目：
1. **Fork** 项目到自己的账号
2. **Clone** 到本地：`git clone https://github.com/你的用户名/项目名.git`
3. 创建分支：`git checkout -b 新功能名`
4. 修改代码并提交
5. **Push** 到你的仓库
6. 在GitHub上发起 **Pull Request**
7. 等待项目维护者审核合并

### 团队协作文档：
```
主分支 (main)
    │
    ├── 开发分支 (develop)
    │       │
    │       ├── 功能A分支 (feature/login)
    │       └── 功能B分支 (feature/payment)
    │
    └── 修复分支 (hotfix/bug-123)
```

---

## 常用工具

### 桌面客户端
| 工具 | 平台 | 特点 |
|------|------|------|
| **GitHub Desktop** | Win/Mac | 官方出品，简单易用 |
| **SourceTree** | Win/Mac | 功能强大，可视化好 |
| **GitKraken** | 全平台 | 界面美观，功能丰富 |

### VS Code集成
- 内置Git支持
- 安装 **GitLens** 插件增强功能
- 可视化diff对比

### 命令行增强
- **Oh My Zsh** (Mac/Linux): 美化终端
- **Git Bash** (Windows): Linux风格命令行

---

## 学习资源

### 官方资源
- [GitHub Docs](https://docs.github.com/cn)
- [GitHub Skills](https://skills.github.com/) - 互动教程
- [Git官方文档](https://git-scm.com/doc)

### 推荐教程
- [廖雪峰Git教程](https://www.liaoxuefeng.com/wiki/896043488029600)
- [GitHub入门视频](https://www.youtube.com/githubguides)

---

## 常见问题

**Q: 忘记密码怎么办？**
A: 登录页面点击 "Forgot password?" 重置

**Q: 如何删除仓库？**
A: 仓库 → Settings → 最下面 Danger Zone → Delete this repository

**Q: 代码提交了能撤回吗？**
A: 可以，`git reset` 或 `git revert`，具体看情况

**Q: 免费版有什么限制？**
A: 免费版可以创建无限公开仓库和有限私有仓库，足够个人使用

---

## 下一步

1. ✅ 注册GitHub账号
2. ✅ 创建第一个仓库
3. ✅ 上传一个文件试试
4. ✅ 安装Git并配置
5. ✅ 克隆仓库到本地
6. ✅ 修改、提交、推送

**完成以上步骤，你就掌握了GitHub基础！**

---

*文档生成时间: 2026-03-02*
*作者: Kimi Claw*
