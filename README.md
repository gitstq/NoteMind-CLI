<div align="center">

# 🧠 NoteMind-CLI

### Lightweight Terminal AI Smart Note Engine
### 轻量级终端AI智能笔记引擎

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)](https://github.com/gitstq/NoteMind-CLI)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange)](https://github.com/gitstq/NoteMind-CLI)

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

</div>

---

<a name="english"></a>
## US English

### 🎉 Introduction

**NoteMind-CLI** is a lightweight, zero-dependency terminal-based intelligent note management engine. Inspired by modern knowledge management needs, it goes beyond traditional note-taking tools by offering **AI-powered features** including semantic search, auto-tagging, knowledge graph visualization, and smart summaries — all from your terminal.

**Why NoteMind-CLI?**
- 🚀 **Zero Dependencies**: Pure Python 3.8+ standard library, no pip install hassles
- 🧠 **AI-Ready**: Built-in hooks for LLM integration (OpenAI, Claude, GLM-5.1 compatible)
- 🔍 **Semantic Search**: Full-text search across titles, content, and tags
- 🕸️ **Knowledge Graph**: Visualize connections between your notes
- 🏷️ **Auto-Tagging**: Extract tags automatically from markdown content
- 📊 **Smart Analytics**: Track your note-taking habits and insights

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📝 **Smart Notes** | Markdown-native note creation with YAML frontmatter | ✅ |
| 🔍 **Full-Text Search** | Search in titles, content, or tags | ✅ |
| 🏷️ **Auto-Tagging** | Extract `#tags` from content automatically | ✅ |
| 🕸️ **Knowledge Graph** | Build and visualize note relationships | ✅ |
| 📊 **Statistics** | Note count, word count, tag analytics | ✅ |
| 🔗 **Related Notes** | Find notes by shared tags | ✅ |
| 📤 **Export/Import** | JSON and Markdown formats | ✅ |
| 🎨 **Colorful TUI** | Beautiful terminal output with ANSI colors | ✅ |
| 🖊️ **External Editor** | Edit notes with your favorite editor (vim, nano, etc.) | ✅ |

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- Any terminal with ANSI color support

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/NoteMind-CLI.git
cd NoteMind-CLI

# Install (optional)
pip install -e .

# Or run directly
python3 notemind.py
```

#### First Steps

```bash
# Initialize NoteMind
notemind init

# Create your first note
notemind new -t "My First Note" -c "# Hello World\n\nThis is my first #note!"

# List all notes
notemind list

# Search notes
notemind search "hello"

# Show statistics
notemind stats

# View knowledge graph
notemind graph
```

### 📖 Usage Guide

#### Creating Notes

```bash
# Quick note with inline content
notemind new -t "Meeting Notes" -c "# Team Meeting\n\nDiscussed Q3 goals." --tags "work,meeting"

# Open external editor (vim, nano, etc.)
notemind new -t "Deep Thought" -e
```

#### Managing Notes

```bash
# Show a note
notemind show <note-id>

# Edit a note
notemind edit <note-id> -e

# Delete a note
notemind delete <note-id>
```

#### Search & Discovery

```bash
# Search all fields
notemind search "python"

# Search specific field
notemind search "python" --in title

# List by tag
notemind list --tag python

# Find related notes
notemind related <note-id>
```

#### Configuration

```bash
# View current config
notemind config --show

# Set custom editor
notemind config --editor vim

# Set notes directory
notemind config --notes-dir ~/my-notes
```

### 💡 Design Philosophy

NoteMind-CLI follows the **Unix Philosophy**: do one thing well. It focuses on:
- **Privacy-first**: All data stored locally
- **Markdown-native**: Plain text, future-proof format
- **Terminal-native**: Fast, keyboard-driven workflow
- **Extensible**: Easy to integrate with AI APIs

### 📦 Deployment

```bash
# Export notes
notemind export -f json -o backup.json
notemind export -f markdown -o notes.md

# Import notes
notemind import backup.json
```

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

### 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<a name="simplified-chinese"></a>
## CN 简体中文

### 🎉 项目介绍

**NoteMind-CLI** 是一款轻量级、零依赖的终端AI智能笔记引擎。受现代知识管理需求启发，它在传统笔记工具基础上增加了 **AI驱动功能**，包括语义搜索、自动标签、知识图谱可视化、智能摘要等 —— 全部在终端中完成。

**为什么选择 NoteMind-CLI？**
- 🚀 **零依赖**：纯 Python 3.8+ 标准库，无需 pip 安装烦恼
- 🧠 **AI就绪**：内置 LLM 集成钩子（兼容 OpenAI、Claude、GLM-5.1）
- 🔍 **语义搜索**：支持标题、内容、标签的全文搜索
- 🕸️ **知识图谱**：可视化笔记之间的关联关系
- 🏷️ **自动标签**：从 Markdown 内容中自动提取 `#标签`
- 📊 **智能分析**：追踪笔记习惯和数据洞察

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📝 **智能笔记** | 支持 YAML 前置元数据的 Markdown 原生笔记 | ✅ |
| 🔍 **全文搜索** | 在标题、内容或标签中搜索 | ✅ |
| 🏷️ **自动标签** | 自动从内容中提取 `#标签` | ✅ |
| 🕸️ **知识图谱** | 构建和可视化笔记关联 | ✅ |
| 📊 **统计分析** | 笔记数量、字数、标签分析 | ✅ |
| 🔗 **关联笔记** | 通过共享标签发现相关笔记 | ✅ |
| 📤 **导入导出** | 支持 JSON 和 Markdown 格式 | ✅ |
| 🎨 **彩色终端** | 支持 ANSI 颜色的精美终端输出 | ✅ |
| 🖊️ **外部编辑器** | 使用喜爱的编辑器编辑笔记（vim、nano 等） | ✅ |

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- 支持 ANSI 颜色的终端

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/NoteMind-CLI.git
cd NoteMind-CLI

# 安装（可选）
pip install -e .

# 或直接运行
python3 notemind.py
```

#### 初次使用

```bash
# 初始化 NoteMind
notemind init

# 创建第一条笔记
notemind new -t "我的第一条笔记" -c "# 你好世界\n\n这是我的第一条 #笔记！"

# 列出所有笔记
notemind list

# 搜索笔记
notemind search "你好"

# 查看统计
notemind stats

# 查看知识图谱
notemind graph
```

### 📖 详细使用指南

#### 创建笔记

```bash
# 快速创建带内容的笔记
notemind new -t "会议记录" -c "# 团队会议\n\n讨论了Q3目标。" --tags "工作,会议"

# 打开外部编辑器（vim、nano 等）
notemind new -t "深度思考" -e
```

#### 管理笔记

```bash
# 查看笔记
notemind show <笔记ID>

# 编辑笔记
notemind edit <笔记ID> -e

# 删除笔记
notemind delete <笔记ID>
```

#### 搜索与发现

```bash
# 搜索所有字段
notemind search "python"

# 搜索特定字段
notemind search "python" --in title

# 按标签列出
notemind list --tag python

# 查找关联笔记
notemind related <笔记ID>
```

#### 配置

```bash
# 查看当前配置
notemind config --show

# 设置编辑器
notemind config --editor vim

# 设置笔记目录
notemind config --notes-dir ~/my-notes
```

### 💡 设计思路

NoteMind-CLI 遵循 **Unix 哲学**：把一件事做好。它专注于：
- **隐私优先**：所有数据本地存储
- **Markdown 原生**：纯文本，面向未来的格式
- **终端原生**：快速、键盘驱动的工作流
- **可扩展**：易于集成 AI API

### 📦 打包与部署

```bash
# 导出笔记
notemind export -f json -o backup.json
notemind export -f markdown -o notes.md

# 导入笔记
notemind import backup.json
```

### 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feat/amazing-feature`
5. 发起 Pull Request

### 📄 开源协议

MIT 协议 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="traditional-chinese"></a>
## TW 繁體中文

### 🎉 專案介紹

**NoteMind-CLI** 是一款輕量級、零依賴的終端AI智能筆記引擎。受現代知識管理需求啟發，它在傳統筆記工具基礎上增加了 **AI驅動功能**，包括語義搜索、自動標籤、知識圖譜可視化、智能摘要等 —— 全部在終端中完成。

**為什麼選擇 NoteMind-CLI？**
- 🚀 **零依賴**：純 Python 3.8+ 標準庫，無需 pip 安裝煩惱
- 🧠 **AI就緒**：內建 LLM 整合鉤子（相容 OpenAI、Claude、GLM-5.1）
- 🔍 **語義搜索**：支援標題、內容、標籤的全文搜索
- 🕸️ **知識圖譜**：可視化筆記之間的關聯關係
- 🏷️ **自動標籤**：從 Markdown 內容中自動提取 `#標籤`
- 📊 **智能分析**：追蹤筆記習慣和數據洞察

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📝 **智能筆記** | 支援 YAML 前置元資料的 Markdown 原生筆記 | ✅ |
| 🔍 **全文搜索** | 在標題、內容或標籤中搜索 | ✅ |
| 🏷️ **自動標籤** | 自動從內容中提取 `#標籤` | ✅ |
| 🕸️ **知識圖譜** | 構建和可視化筆記關聯 | ✅ |
| 📊 **統計分析** | 筆記數量、字數、標籤分析 | ✅ |
| 🔗 **關聯筆記** | 通過共享標籤發現相關筆記 | ✅ |
| 📤 **匯入匯出** | 支援 JSON 和 Markdown 格式 | ✅ |
| 🎨 **彩色終端** | 支援 ANSI 顏色的精美終端輸出 | ✅ |
| 🖊️ **外部編輯器** | 使用喜愛的編輯器編輯筆記（vim、nano 等） | ✅ |

### 🚀 快速開始

#### 環境要求
- Python 3.8 或更高版本
- 支援 ANSI 顏色的終端

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/NoteMind-CLI.git
cd NoteMind-CLI

# 安裝（可選）
pip install -e .

# 或直接執行
python3 notemind.py
```

#### 初次使用

```bash
# 初始化 NoteMind
notemind init

# 建立第一條筆記
notemind new -t "我的第一條筆記" -c "# 你好世界\n\n這是我的第一條 #筆記！"

# 列出所有筆記
notemind list

# 搜索筆記
notemind search "你好"

# 查看統計
notemind stats

# 查看知識圖譜
notemind graph
```

### 📖 詳細使用指南

#### 建立筆記

```bash
# 快速建立帶內容的筆記
notemind new -t "會議記錄" -c "# 團隊會議\n\n討論了Q3目標。" --tags "工作,會議"

# 開啟外部編輯器（vim、nano 等）
notemind new -t "深度思考" -e
```

#### 管理筆記

```bash
# 查看筆記
notemind show <筆記ID>

# 編輯筆記
notemind edit <筆記ID> -e

# 刪除筆記
notemind delete <筆記ID>
```

#### 搜索與發現

```bash
# 搜索所有欄位
notemind search "python"

# 搜索特定欄位
notemind search "python" --in title

# 按標籤列出
notemind list --tag python

# 查找關聯筆記
notemind related <筆記ID>
```

#### 配置

```bash
# 查看目前配置
notemind config --show

# 設定編輯器
notemind config --editor vim

# 設定筆記目錄
notemind config --notes-dir ~/my-notes
```

### 💡 設計思路

NoteMind-CLI 遵循 **Unix 哲學**：把一件事做好。它專注於：
- **隱私優先**：所有資料本地儲存
- **Markdown 原生**：純文字，面向未來的格式
- **終端原生**：快速、鍵盤驅動的工作流
- **可擴展**：易於整合 AI API

### 📦 打包與部署

```bash
# 匯出筆記
notemind export -f json -o backup.json
notemind export -f markdown -o notes.md

# 匯入筆記
notemind import backup.json
```

### 🤝 貢獻指南

1. Fork 本倉庫
2. 建立功能分支：`git checkout -b feat/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feat/amazing-feature`
5. 發起 Pull Request

### 📄 開源協議

MIT 協議 - 詳見 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ by NoteMind Team**

[⬆ Back to Top](#english)

</div>
