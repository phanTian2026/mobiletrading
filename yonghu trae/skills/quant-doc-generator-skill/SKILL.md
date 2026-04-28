---
name: quant-doc-generator-skill
description: "Use when you need to understand, document, or visualize a quantitative trading framework's architecture, data flow, or core modules."
---

# Quant Doc Generator Skill

这是一个专门用于生成量化框架技术文档的 Skill。

## 功能 (Capabilities)

### 1. 📐 结构与功能全景分析
*功能*: 分析框架目录结构，梳理数据流向和模块耦合关系
*指令*: `/struct` 或 `/结构分析`
*输出*: 结构与功能全景分析.md

### 2. 🔍 核心模块深度解析
*功能*: 针对核心模块生成详细的开发者文档
*指令*: `/core` 或 `/核心解析`
*输出*: 核心模块深度解析与文档化.md

### 3. 🎨 架构可视化
*功能*: 生成 Mermaid 流程图和架构图
*指令*: `/viz` 或 `/可视化`
*输出*: Mermaid 代码和架构图提示词

### 4. 🚀 一键完整分析
*功能*: 执行上述所有步骤，生成完整文档
*指令*: `/all` 或 `/完整分析`
*输出*: 所有文档 + 可视化

## 使用流程

### 第一步：上传框架代码
用户需要提供：
- 目录结构说明
- 核心文件内容（`core/`、`回测主程序.py` 等）

### 第二步：选择分析模式
```
用户: /struct
AI: [分析目录结构，输出数据流向和耦合关系]

用户: /core
AI: [深度解析核心模块，生成技术文档]

用户: /viz
AI: [生成 Mermaid 流程图代码]

用户: /all
AI: [执行完整的 3 阶段分析]
```

## 路由逻辑 (Routing Logic)

1. **结构分析**: `/struct` → `prompts/stage1_structure.md`
2. **核心解析**: `/core` → `prompts/stage2_core.md`
3. **架构可视化**: `/viz` → `prompts/stage3_visualization.md`
4. **完整分析**: `/all` → 依次执行上述 3 个阶段

## 适用场景

- ✅ Python 量化回测框架
- ✅ 策略库、因子库、信号库的文档化
- ✅ 代码架构梳理和优化建议
- ✅ 新成员快速了解框架结构

## 输出示例

### 结构分析输出
- 数据流向图
- 模块耦合关系分析
- 目录职责说明

### 核心解析输出
- 功能描述
- 核心函数/类清单（Markdown 表格）
- 异常处理机制
- 优化建议

### 可视化输出
- Mermaid.js 流程图代码
- 架构图 AI 绘图提示词