# Obsidian + GitHub 联动使用指南

## 目录
1. [为什么联动](#为什么联动)
2. [基础配置](#基础配置)
3. [Obsidian Git插件使用](#obsidian-git插件使用)
4. [工作流程](#工作流程)
5. [进阶技巧](#进阶技巧)
6. [常见问题](#常见问题)

---

## 为什么联动

**Obsidian** 是强大的本地知识库工具
**GitHub** 是可靠的云端备份和协作平台

**联动的优势：**
- ☁️ 云端备份，不怕本地数据丢失
- 📱 多设备同步（电脑、手机、平板）
- 🤝 团队协作，共享知识库
- 📝 版本历史，随时回滚
- 🌐 免费发布为网站（GitHub Pages）

---

## 基础配置

### 第一步：创建GitHub仓库

1. 登录GitHub → 点击右上角 **+** → **New repository**
2. 填写信息：
   - **Repository name**: `obsidian-vault`（或你喜欢的名字）
   - **Description**: 我的Obsidian知识库
   - 选择 **Public**（公开）或 **Private**（私有）
   - ✅ 勾选 **Add a README file**
3. 点击 **Create repository**

### 第二步：本地克隆仓库

```bash
# 克隆仓库到本地
git clone https://github.com/你的用户名/obsidian-vault.git

# 进入文件夹
cd obsidian-vault
```

### 第三步：创建Obsidian仓库

1. 打开Obsidian
2. 点击 **打开本地仓库**
3. 选择刚才克隆的文件夹 `obsidian-vault`
4. 完成！

**文件夹结构：**
```
obsidian-vault/
├── .git/                 # Git版本控制
├── .obsidian/            # Obsidian配置
│   ├── app.json
│   ├── appearance.json
│   └── ...
├── README.md             # 仓库说明
├── 00-Inbox/             # 收件箱（临时笔记）
├── 01-Daily/             # 日记
├── 02-Projects/          # 项目笔记
├── 03-Areas/             # 领域知识
├── 04-Resources/         # 参考资料
├── 05-Archive/           # 归档
└── Attachments/          # 附件（图片、PDF等）
```

---

## Obsidian Git插件使用

### 安装插件

1. 打开Obsidian → **设置** → **第三方插件**
2. 关闭 **安全模式**
3. 点击 **浏览** → 搜索 **"Git"**
4. 安装 **Obsidian Git** 插件
5. 启用插件

### 配置插件

1. 打开 **Obsidian Git** 设置
2. 基础配置：
   - ✅ **自动提交**: 开启
   - ✅ **自动推送**: 开启
   - **提交间隔**: 5-10分钟
   - **提交信息模板**: `vault backup: {{date}}`

3. 高级配置：
   - **自定义Git路径**: 留空（使用系统Git）
   - **排除文件夹**: `.obsidian/workspace.json`（避免冲突）

### 插件界面

安装后左下角会出现Git图标：
- 🔄 显示当前状态
- 点击可手动提交/推送/拉取

---

## 工作流程

### 日常使用流程

```
1. 打开Obsidian
   ↓
2. 自动拉取最新内容（如果有）
   ↓
3. 正常编辑笔记
   ↓
4. 自动提交（每5-10分钟）
   ↓
5. 自动推送到GitHub
   ↓
6. 关闭Obsidian
```

### 多设备同步

**电脑A（工作）**
```
编辑笔记 → 自动提交推送
```

**电脑B（家里）**
```
打开Obsidian → 自动拉取更新 → 继续编辑
```

**手机（移动端）**
```
使用GitHub App查看
或使用Working Copy（iOS）编辑
```

### 手动同步命令

**Obsidian Git插件快捷键：**
- `Ctrl/Cmd + P` → 输入 "Git"
- 选择：
  - **Commit all changes** - 提交所有更改
  - **Push** - 推送到GitHub
  - **Pull** - 拉取最新内容
  - **Commit and push** - 提交并推送

**命令行方式：**
```bash
# 进入仓库目录
cd obsidian-vault

# 查看状态
git status

# 添加所有更改
git add .

# 提交
git commit -m "更新笔记"

# 推送到GitHub
git push origin main

# 拉取更新
git pull origin main
```

---

## 进阶技巧

### 1. 使用.gitignore忽略不需要同步的文件

创建 `.gitignore` 文件：
```gitignore
# Obsidian工作区文件（会冲突）
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# 缓存文件
.obsidian/cache

# 插件数据（可选）
.obsidian/plugins/*/data.json

# 大型附件（如果不用Git管理）
*.mp4
*.mov
*.zip
```

### 2. 分支管理（团队协作）

```bash
# 创建个人分支
git checkout -b my-notes

# 编辑后提交
git add .
git commit -m "添加新笔记"

# 推送到GitHub
git push origin my-notes

# 在GitHub上发起Pull Request合并到主分支
```

### 3. 发布为网站（GitHub Pages）

**使用Obsidian Publish替代方案：**

1. 安装 **Obsidian Digital Garden** 插件
2. 配置GitHub Pages
3. 免费发布为网站

**或使用MkDocs：**
```bash
# 安装MkDocs
pip install mkdocs-material

# 初始化
cd obsidian-vault
mkdocs new .

# 配置后部署
git add .
git commit -m "添加网站配置"
git push
```

### 4. 自动备份脚本

创建 `backup.sh`：
```bash
#!/bin/bash
cd /path/to/obsidian-vault

# 添加所有更改
git add .

# 提交（带时间戳）
git commit -m "自动备份: $(date '+%Y-%m-%d %H:%M:%S')"

# 推送
git push origin main

echo "备份完成!"
```

设置定时任务（Mac/Linux）：
```bash
# 每小时备份一次
crontab -e

# 添加：
0 * * * * /path/to/backup.sh
```

### 5. 手机端同步（iOS）

**使用 Working Copy App：**
1. App Store下载 Working Copy
2. 克隆GitHub仓库
3. 用Obsidian Mobile打开Working Copy的文件夹
4. 编辑后Working Commit和Push

---

## 常见问题

### Q1: 冲突怎么办？

**A:** 当多设备同时修改时可能出现冲突。

**解决：**
```bash
# 1. 先拉取最新内容
git pull origin main

# 2. 如果有冲突，手动解决
# Obsidian会显示冲突文件，选择保留哪个版本

# 3. 解决后提交
git add .
git commit -m "解决冲突"
git push
```

**建议：** 避免同时在多个设备编辑同一文件。

### Q2: 大文件（图片/PDF）怎么管理？

**A:** 几种方案：

**方案1：** 使用Git LFS（大文件存储）
```bash
git lfs track "*.png"
git lfs track "*.pdf"
```

**方案2：** 使用图床（推荐）
- 图片上传到图床（如SM.MS、GitHub图床）
- Obsidian只存链接

**方案3：** 分开存储
- 笔记用Git管理
- 附件用云盘（iCloud、OneDrive）

### Q3: 私有笔记不想公开？

**A:** 
- GitHub仓库设为 **Private**
- 或使用GitLab、Gitee等私有仓库

### Q4: 如何查看历史版本？

**A:**
```bash
# 查看提交历史
git log --oneline

# 查看某个文件的历史
git log -p 文件名

# 回滚到某个版本
git checkout 提交ID -- 文件名
```

### Q5: Obsidian Git插件不工作？

**A:** 检查以下几点：
1. 是否安装了Git？`git --version`
2. 仓库是否正确克隆？
3. 是否有写入权限？
4. 检查插件设置中的Git路径

---

## 推荐工作流总结

### 个人使用
```
Obsidian编辑
    ↓
自动提交（每5分钟）
    ↓
自动推送（每30分钟或关闭时）
    ↓
GitHub备份
```

### 团队协作
```
主分支（main）- 稳定版本
    ↓
个人分支（name-notes）- 各自编辑
    ↓
Pull Request - 审核合并
    ↓
主分支更新
```

---

## 学习资源

- [Obsidian官方文档](https://help.obsidian.md/)
- [Obsidian Git插件文档](https://github.com/denolehov/obsidian-git)
- [GitHub Docs](https://docs.github.com/cn)
- [廖雪峰Git教程](https://www.liaoxuefeng.com/wiki/896043488029600)

---

## 快速开始清单

- [ ] 创建GitHub仓库
- [ ] 克隆到本地
- [ ] 用Obsidian打开
- [ ] 安装Obsidian Git插件
- [ ] 配置自动提交/推送
- [ ] 编辑一篇笔记测试
- [ ] 检查GitHub是否同步成功
- [ ] （可选）配置手机端

---

完成以上步骤，你就拥有了一个安全、同步、可协作的云端知识库！

