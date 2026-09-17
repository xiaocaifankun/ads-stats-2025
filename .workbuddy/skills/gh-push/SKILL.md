---
name: gh-push
description: 把当前仓库的本地内容推送到 GitHub 远程仓库（add → commit → push 全链路）。当用户说"推送到 GitHub""提交并推送""push 一下""同步到远程""把改动传到仓库"时使用。内置静默认证（gh CLI 凭据，不弹 GCM 窗口）、代理降级链、本机 remote-tracking ref 缺失的规避写法、冲突与非快进推送的安全处理、以及推送前预检。只处理已存在的 GitHub 仓库；若是全新仓库需要先创建远程，改用 git-init。
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
effort: low
---

# gh-push — 本地内容推送到 GitHub

把当前仓库的工作区改动，一路送到 GitHub 远程分支上。全程无弹窗、无模态。

## 核心原则

1. **先看清，再动手**：推送前必须知道"要推什么、推到哪、有没有冲突"。
2. **不弹窗**：认证走 gh CLI 凭据，绕开 Git Credential Manager。
3. **不依赖 `origin/<branch>` 引用**（本机该引用不落盘，见下）。
4. **破坏性操作先停手**：强推必须先确认。
5. **推完必验证**：比对远程 HEAD 与本地 HEAD，不靠 push 的退出码自证。

---

## 本机环境的两条硬事实（实测，2026-09-17）

### 事实一：`refs/remotes/origin/*` 不会落盘

fetch 会报告 `* [new branch] main -> origin/main`，**看似成功，但 `.git/refs/remotes/` 是空的**，`packed-refs` 也不生成。后果：

- `git rev-list HEAD...origin/main` → `fatal: ambiguous argument`
- `git for-each-ref refs/remotes` → 空
- 每次 fetch 都重复报 "new branch"

**规避**：用 `git ls-remote`（查远程真实值）或 `FETCH_HEAD`（fetch 后立即读）代替所有 `origin/<branch>` 引用。下文命令均已按此改写。

> 不要试图"修复"它（重配 refspec / 重建仓库）——`remote.origin.fetch` 配置本身是正确 的 `+refs/heads/*:refs/remotes/origin/*`，问题在沙箱的 ref 写入，改配置无效。

### 事实二：会话注入的代理会中途失效

`http_proxy=http://127.0.0.1:<随机端口>` 会突然报 `CONNECT tunnel failed, response 502`。降级链见第五节。

### 事实三：`@{upstream}` 判定会假阳性

`git rev-parse --abbrev-ref '@{upstream}'` 在无上游时**返回字面量 `@{upstream}` 而非报错**，导致 `||` 兜底失效。用 `git config --get branch.$(git rev-parse --abbrev-ref HEAD).merge` 判定更可靠。

---

## 第一步：环境预检（每次都要做）

```bash
export PATH="/usr/bin:/bin:/c/Windows/System32:/c/Windows:$PATH"
cd <repo>

# 1. 是否在 git 仓库、远程指向
git rev-parse --is-inside-work-tree && git remote -v

# 2. 当前分支
BRANCH=$(git rev-parse --abbrev-ref HEAD); echo "branch=$BRANCH"

# 3. 是否配了上游（用 config 判定，不用 @{upstream}）
git config --get "branch.$BRANCH.merge" || echo "NO_UPSTREAM"

# 4. gh 认证（不弹窗的前提）
gh auth status 2>&1 | head -5
```

| 情况 | 处置 |
|---|---|
| 无 `origin` 远程 | 停下，告知缺远程；新仓库改用 `git-init` |
| 无上游分支 | push 时加 `-u origin <branch>` |
| gh 未登录 | 停下，让用户跑 `gh auth login`；**不要**回退 GCM |
| 不在 git 仓库 | 停下，提示先 `git init` |

---

## 第二步：看清要推的内容

```bash
git status --short
git diff --stat
git diff --cached --stat
```

**必须检查的坑：**

- **大文件**：>5MB 先提醒（GitHub 单文件限 100MB）。用户惯例是大文件放坚果云。
- **敏感文件**：`.env`、`*token*`、`*credential*`、`*.key`、`*.pem`。发现就停下问。
- **构建产物**：`node_modules/`、`__pycache__/`、`.DS_Store`、`*.pyc`、`.ipynb_checkpoints/`。
- **空改动**：无改动且无未推送 commit → 告知"没有需要推送的内容"，结束。

**分叉检测（不依赖 `origin/<branch>`）：**

```bash
git fetch origin "$BRANCH" >/dev/null 2>&1
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse FETCH_HEAD)

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "=> 已同步，无需推送"
else
  BASE=$(git merge-base HEAD FETCH_HEAD 2>/dev/null)
  echo "本地领先: $(git rev-list --count "$REMOTE"..HEAD)"
  echo "远程领先: $(git rev-list --count "$BASE".."$REMOTE" 2>/dev/null)"
fi
```

| 结果 | 处置 |
|---|---|
| 本地领先 N、远程领先 0 | 正常推送 |
| 远程领先、本地领先 0 | `git pull --rebase origin <branch>` 后重推 |
| 双方都领先（分叉） | 停下，说明情况由用户定 |
| 都 0 | 已同步，结束 |

---

## 第三步：提交

只暂存该提交的内容，不要无脑 `git add -A`：

```bash
git add <具体路径>        # 优先
```

**commit message**：无特殊约定时用 Conventional Commits，描述用**英文**（用户偏好）：

```
<type>: <简短描述>
type ∈ feat | fix | docs | chore | refactor | test | style | perf
```

```bash
git commit -m "docs: add wiki source pages for agent memory"
```

用户已明确说明提交范围与 message 时，直接执行，不再追问。

---

## 第四步：推送（静默认证的关键）

```bash
git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin "$BRANCH"
```

**逐段解释，改动前必读：**

| 片段 | 作用 |
|---|---|
| `-c credential.helper=` | **先清空**已有 helper 链（否则 GCM 仍在链上） |
| `-c credential.helper='!gh auth git-credential'` | 追加 gh 作为唯一 helper |
| `!` 前缀 | 告诉 git 这是 shell 命令而非 helper 名 |

> **踩坑记录（实测）**：两段缺一不可。
> - 只写 `-c credential.helper='!gh ...'`（不加置空）→ git 叠加，GCM 仍可能被调用；
> - 写成 `-c credential.helper=''`（空串）→ 整条链被清空，报 `could not read Username for 'https://github.com': terminal prompts disabled`。
>
> **必须是「先置空，再 append」的两段式。**

新分支首次推送加 `-u`：

```bash
git -c credential.helper= -c credential.helper='!gh auth git-credential' push -u origin "$BRANCH"
```

### 持久化（可选）

`gh auth setup-git` 可让以后直接 `git push` 就走 gh。**它改全局配置，执行前须征得用户同意。**

---

## 第五步：网络失败降级链

```bash
# ① 默认（用会话注入的代理）
timeout 90 git ... push origin "$BRANCH"

# ② 清代理直连
timeout 90 env -u https_proxy -u http_proxy -u HTTPS_PROXY -u HTTP_PROXY \
  git -c http.proxy= -c https.proxy= ... push origin "$BRANCH"

# ③ 走本机静态代理 10808（不保证在跑）
timeout 90 git -c http.proxy=http://127.0.0.1:10808 \
  -c https.proxy=http://127.0.0.1:10808 ... push origin "$BRANCH"
```

每步都加 `timeout`（直连失败可能卡 20 秒以上）。三步皆败 → 停下报告"网络不可达"，**不要**反复重试。

---

## 第六步：推完必须验证

**不要相信 push 的退出码**，用远程实际值确认：

```bash
echo -n "本地: "; git rev-parse HEAD
echo -n "远程: "; timeout 60 git ls-remote origin "refs/heads/$BRANCH" | cut -f1
git status --short && echo "(空=工作区干净)"
```

哈希一致 = 成功。

---

## 冲突与报错处置

| 报错 | 原因 | 处置 |
|---|---|---|
| `non-fast-forward` | 远程有新 commit | `git pull --rebase origin <branch>` 后重推 |
| `fetch first` | 本地落后 | 同上 |
| `stale info` | `--force-with-lease` 期望值过期 | 用 `git ls-remote` 取真实远程值作 lease |
| `could not read Username` | helper 链被清空 | 回到第四步两段式写法 |
| `CONNECT tunnel failed` | 会话代理失效 | 走第五步降级链 |
| `GH013 ... push protection` | 提交含疑似密钥 | 停止，移除敏感内容后重来 |
| `ambiguous argument 'origin/main'` | remote-tracking ref 缺失 | 用 `ls-remote` / `FETCH_HEAD` 替代 |

### 强推（危险）

**仅在用户明确要求时执行**，优先 `--force-with-lease`：

```bash
# 1. 取远程真实哈希
REMOTE=$(git ls-remote origin "refs/heads/$BRANCH" | cut -f1)
# 2. 带 lease 强推
git ... push --force-with-lease="$BRANCH:$REMOTE" origin "$BRANCH"
```

lease 期望值必须是**真实远程哈希**。本机 `origin/<branch>` 引用不存在，写 `--force-with-lease=main:<本地记的值>` 会报 `stale info`。

> **强推会覆盖远程历史，可能造成他人工作丢失。执行前必须向用户确认，并说明目标哈希。**

---

## 快速参考：一键流程（无冲突时）

```bash
export PATH="/usr/bin:/bin:/c/Windows/System32:/c/Windows:$PATH"
cd <repo>
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git fetch origin "$BRANCH" >/dev/null 2>&1
# 比 FETCH_HEAD 判断分叉；查 status 看改动
git add <paths> && git commit -m "<type>: <desc>"
timeout 90 git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin "$BRANCH"
# 验证
git rev-parse HEAD && timeout 60 git ls-remote origin "refs/heads/$BRANCH" | cut -f1
```

---

## 边界

- **只管推送**，不做仓库初始化、不建 PR（PR 用 `gh pr create`）。
- 仓库**无 GitHub 远程** → 本 skill 无能为力，改用 `git-init`。
- **不做** `git reset --hard`、`git clean -fd` 这类丢弃本地改动的事。
- 用户说"不要提交 X"时，**绝不**用 `git add -A` 兜底。
- 不要为绕过沙箱的 ref 写入限制而重建仓库或改 refspec——那是过度设计。

## 报告格式

一句话：(分支) 从 `<旧哈希>` 推到 `<新哈希>`，N 个 commit、M 个文件变更。失败则直说卡在哪步、什么报错、下一步建议。
