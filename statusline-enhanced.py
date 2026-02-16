#!/usr/bin/env python3
"""
Enhanced Claude Code Status Line for Windows
Features: Git status, model info, context usage, token count, cost
Style: Border blocks with separators, always show all fields
"""
import sys
import json
import os
import subprocess

# ANSI Color codes
RESET = '\033[0m'
CYAN = '\033[36m'
GRAY = '\033[90m'
MAGENTA = '\033[35m'
YELLOW = '\033[33m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BRIGHT_CYAN = '\033[96m'
BOLD = '\033[1m'

def run_git(*args):
    """Run git command and return output"""
    try:
        result = subprocess.run(
            ['git'] + list(args),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except:
        return ''

def get_git_status():
    """Get git status counts"""
    result = {'M': 0, 'D': 0, 'S': 0, 'U': 0, 'ahead': 0, 'behind': 0, 'stash': 0, 'conflicts': 0, 'branch': ''}

    if not run_git('rev-parse', '--is-inside-work-tree'):
        return result

    result['branch'] = run_git('branch', '--show-current') or 'no-branch'

    modified = run_git('diff', '--name-only', '--diff-filter=M')
    result['M'] = len(modified.split('\n')) if modified else 0

    deleted = run_git('diff', '--name-only', '--diff-filter=D')
    result['D'] = len(deleted.split('\n')) if deleted else 0

    staged = run_git('diff', '--cached', '--name-only')
    result['S'] = len(staged.split('\n')) if staged else 0

    untracked = run_git('ls-files', '--others', '--exclude-standard')
    result['U'] = len(untracked.split('\n')) if untracked else 0

    ahead_behind = run_git('rev-list', '--left-right', '--count', '@{u}...HEAD')
    if ahead_behind:
        parts = ahead_behind.split()
        if len(parts) == 2:
            result['behind'] = int(parts[0]) if parts[0].isdigit() else 0
            result['ahead'] = int(parts[1]) if parts[1].isdigit() else 0

    stash = run_git('stash', 'list')
    result['stash'] = len(stash.split('\n')) if stash else 0

    conflicts = run_git('diff', '--name-only', '--diff-filter=U')
    result['conflicts'] = len(conflicts.split('\n')) if conflicts else 0

    return result

def format_tokens(num):
    """Format token count with K/M suffix"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    elif num > 0:
        return str(num)
    return "--"

def format_cost(cost):
    """Format cost with $ prefix"""
    if cost is None or cost == 0:
        return "$--"
    try:
        cost_float = float(cost)
        if cost_float >= 1:
            return f"${cost_float:.2f}"
        elif cost_float >= 0.01:
            return f"${cost_float:.3f}"
        else:
            return f"${cost_float:.4f}"
    except:
        return "$--"

def format_ctx(pct):
    """Format context percentage"""
    if pct is None or pct == '':
        return "--%"
    try:
        return f"{int(float(pct))}%"
    except:
        return "--%"

def block(text, color=RESET):
    """Create a bordered block with color"""
    return f"{GRAY}[{RESET}{color}{text}{RESET}{GRAY}]{RESET}"

def main():
    try:
        data = json.load(sys.stdin)
    except:
        print('Claude Code Ready', end='')
        return

    # Debug log
    try:
        with open(os.path.expanduser('~/.claude/statusline-debug.log'), 'a') as f:
            from datetime import datetime
            f.write(f"\n{'='*50}\n{datetime.now()}\n")
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        pass

    parts = []
    sep = f"{GRAY} │ {RESET}"

    # === 模型区块 ===
    model = data.get('model', {}).get('display_name', '') or data.get('model', {}).get('id', '') or 'Unknown'
    model = model.replace('Claude ', '').replace(' 4.5', '4.5')
    parts.append(block(model, BOLD + CYAN))

    # === Token 区块（始终显示）===
    ctx_window = data.get('context_window', {})
    total_input = ctx_window.get('total_input_tokens', 0) or 0
    total_output = ctx_window.get('total_output_tokens', 0) or 0
    total_tok = total_input + total_output

    tok_str = format_tokens(total_tok)
    out_str = format_tokens(total_output)

    parts.append(block(f"Tok:{tok_str}", BLUE))
    parts.append(block(f"Out:{out_str}", GRAY))

    # === 费用区块（始终显示）===
    cost = data.get('cost', {})
    total_cost = cost.get('total_cost_usd', None) if isinstance(cost, dict) else None
    if total_cost is None:
        total_cost = data.get('total_cost_usd', None)

    cost_str = format_cost(total_cost)
    parts.append(block(cost_str, MAGENTA))

    # === 上下文区块（始终显示）===
    used = ctx_window.get('used_percentage', None)
    ctx_str = format_ctx(used)

    # 根据使用率选择颜色
    try:
        pct = float(used) if used else 0
        if pct < 50:
            ctx_color = GREEN
        elif pct < 75:
            ctx_color = YELLOW
        else:
            ctx_color = RED
    except:
        ctx_color = GRAY

    parts.append(block(f"Ctx:{ctx_str}", ctx_color))

    # === Git 区块 ===
    git = get_git_status()
    if git['branch']:
        # 分支名
        parts.append(block(git['branch'], GREEN))

        # 变更统计（有变更时才显示）
        changes = []
        if git['M'] > 0: changes.append(f"M:{git['M']}")
        if git['D'] > 0: changes.append(f"D:{git['D']}")
        if git['S'] > 0: changes.append(f"S:{git['S']}")
        if git['U'] > 0: changes.append(f"U:{git['U']}")

        if changes:
            parts.append(block(' '.join(changes), YELLOW))

        # 远程状态
        remote = []
        if git['ahead'] > 0: remote.append(f"↑{git['ahead']}")
        if git['behind'] > 0: remote.append(f"↓{git['behind']}")
        if remote:
            parts.append(block(' '.join(remote), CYAN))

        # Stash 和冲突
        if git['stash'] > 0:
            parts.append(block(f"≡{git['stash']}", GRAY))
        if git['conflicts'] > 0:
            parts.append(block(f"⚠{git['conflicts']}", RED))

    # === 目录区块（完整路径）===
    cwd = data.get('workspace', {}).get('current_dir', '') or data.get('cwd', '')
    if cwd:
        # 统一使用正斜杠显示完整路径
        cwd_display = cwd.replace('\\', '/')
        parts.append(block(cwd_display, BRIGHT_CYAN))

    if parts:
        print(sep.join(parts), end='')
    else:
        print('Claude Code Ready', end='')

if __name__ == '__main__':
    main()
