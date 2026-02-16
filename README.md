# Claude Code Statusline

一个功能丰富的 Claude Code 状态栏脚本，支持 Token 统计、费用追踪、Git 状态等功能。

## 功能特性

| 功能 | 说明 |
|------|------|
| 🤖 **模型显示** | 当前使用的 AI 模型名称 |
| 📊 **Token 统计** | 总 Token 数和输出 Token 数 |
| 💰 **费用追踪** | 实时显示会话费用 |
| 📈 **上下文使用** | 上下文使用百分比，颜色随使用率变化 |
| 🌿 **Git 状态** | 分支名、变更统计、远程同步状态 |
| 📁 **完整路径** | 当前工作目录的完整路径 |

## 效果预览

```
[glm-5[1m]] │ [Tok:25.7K] │ [Out:2.4K] │ [$0.268] │ [Ctx:6%] │ [main] │ [C:/Users/user/projects/myapp]
```

### 颜色说明

- **模型**: 青色加粗
- **Token**: 蓝色
- **Out**: 灰色
- **费用**: 紫色
- **Ctx**: 绿色 (<50%) / 黄色 (50-75%) / 红色 (>75%)
- **Git 分支**: 绿色
- **目录**: 亮青色

## 快速安装

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/leonlaw-god/claude-statusline/main/install.ps1 | iex
```

### Linux / macOS

```bash
curl -sL https://raw.githubusercontent.com/leonlaw-god/claude-statusline/main/install.sh | bash
```

## 手动安装

1. 下载 `statusline-enhanced.py` 到 `~/.claude/` 目录

2. 编辑 `~/.claude/settings.json`，添加以下配置：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python ~/.claude/statusline-enhanced.py"
  }
}
```

3. 重启 Claude Code

## 依赖

- Python 3.x
- Git（可选，用于 Git 状态功能）

## 自定义

你可以编辑 `statusline-enhanced.py` 来调整：

- 颜色方案（修改 ANSI 颜色代码）
- 显示字段（添加或删除区块）
- 分隔符样式

## 许可证

MIT License
