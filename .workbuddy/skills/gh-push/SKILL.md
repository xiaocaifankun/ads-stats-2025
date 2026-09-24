---
name: gh-push
description: 把当前仓库的本地内容推送到 GitHub 远程仓库（add → commit → push 全链路）。当用户说"推送到 GitHub""提交并推送""push 一下""同步到远程""把改动传到仓库"时使用。含两条通道：默认 HTTPS + gh CLI 凭据（静默、不弹 GCM 窗口），以及 SSH + ssh-agent（含校园网封禁时的 CONNECT 隧道方案）。内置网络重试、无 .git 副本接远端历史的接法、推送前"别把旧版推上去"的方向性核对、冲突与非快进推送的安全处理。只处理已存在的 GitHub 仓库；若是全新仓库需要先创建远程，改用 git-init。
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
effort: low
---

# gh-push — 本地内容推送到 GitHub

把当前仓库的工作区改动，一路送到 GitHub 远程分支上。全程无弹窗、无模态。

## 核心原则

1. **先看清，再动手**：推送前必须知道"要推什么、推到哪、有没有冲突"。
2. **方向性核对**：`M` 不代表"本地更新"。**逐个文件确认方向**，别把旧版覆盖新版（踩过两次，见第六节）。
3. **不弹窗**：认证走 gh CLI 凭据，绕开 Git Credential Manager。
4. **破坏性操作先停手**：强推必须先确认。
5. **推完必验证**：比对远程 HEAD 与本地 HEAD，不靠 push 的退出码自证。
6. **网络失败要重试**：本机会话代理间歇性 502，一次失败不代表断网（见第二节事实二）。

---

## 一、两条通道：先选，再执行

| 通道 | 认证方式 | 本机可用性 | 何时用 |
|---|---|---|---|
| **A. HTTPS + gh 凭据** | `!gh auth git-credential` | ✅ 可用（2026-09-24 实测） | **默认**，直接走 |
| **B. SSH + ssh-agent** | ed25519 key（`~/.ssh/id_ed25519_github`） | ❌ 当前网络不可用（见第七节） | 换网 / 代理出口在境外时 |

**选择规则**：默认走 A。用户明确点名 "SSH" 时，**先花 15 秒做第七节的连通性预检**——通了走 B，不通就如实报告并回落 A，**不要反复重试、不要自造隧道变通**。

---

## 二、本机环境的硬事实（2026-09-24 复核，逐条带实测）

### 事实一：传输层只有「会话代理」一条路

| 路径 | 实测结果 |
|---|---|
| `github.com:443` 直连 | **CLOSED**（`/dev/tcp` 探测，TCP 层就不通） |
| 会话代理 `$https_proxy`（形如 `http://127.0.0.1:<随机端口>`） | CONNECT 200，可用 |
| 静态代理 `127.0.0.1:10808` | 未运行（用户自己的 v2rayN 类客户端，不保证在跑） |

→ **必须走会话代理**。旧版 skill 写的"清代理直连"降级分支**已失效**，不要再当兜底用。

### 事实二：会话代理会间歇性 502，必须重试

`CONNECT tunnel failed, response 502` 会突然出现，几秒后又恢复。同一条命令里 `gh api user` 成功、`git fetch` 报 502 是常态。

→ 见第四节的**重试循环**写法。单次失败不要下"网络不可用"的结论。

### 事实三：`refs/remotes/origin/*` 现在会落盘

2026-09-24 在一个全新初始化并 fetch 的仓库中实测：

```
git for-each-ref refs/remotes   → refs/remotes/origin/HEAD / origin/main 均在
git rev-parse origin/main       → 6667d6f... 可解析
```

→ 与 09-17 记录（不落盘、需用 `ls-remote` / `FETCH_HEAD` 替代）**不一致**，如实并列记录，不做取舍。
→ 写法上仍推荐 `git ls-remote origin refs/heads/<b>`（查远程真值，跨环境稳定），但 `origin/<b>` 现在也可以用。

### 事实四：`@{upstream}` 无上游时实测**报 fatal**，不是返回字面量

```
git rev-parse --abbrev-ref '@{upstream}'
→ fatal: no upstream configured for branch 'main'
```

→ 与 09-17 记录（"返回字面量 `@{upstream}` 而非报错，`||` 兜底失效"）不一致，如实并列。
→ 无论哪种，用 `git config --get branch.<b>.merge` 判定上游都是最稳的，继续沿用。

---

## 三、第一步：环境预检（每次都要做）

```bash
export PATH="/usr/bin:/bin:/c/Windows/System32:/c/Windows:$PATH"
cd <repo>

# 1. 是否在 git 仓库、远程指向
git rev-parse --is-inside-work-tree && git remote -v

# 2. 当前分支
BRANCH=$(git rev-parse --abbrev-ref HEAD); echo "branch=$BRANCH"

# 3. 是否配了上游（用 config 判定）
git config --get "branch.$BRANCH.merge" || echo "NO_UPSTREAM"

# 4. gh 认证（不弹窗的前提）
gh auth status 2>&1 | head -5
```

| 情况 | 处置 |
|---|---|
| 无 `origin` 远程 | 停下，告知缺远程；新仓库改用 `git-init` |
| 无上游分支 | push 时加 `-u origin <branch>`，或推完用 `git branch --set-upstream-to=origin/<b> <b>` 补（见下） |
| gh 未登录 | 停下，让用户跑 `gh auth login`；**不要**回退 GCM |
| 不在 git 仓库 | 见第六节（无 `.git` 且远端已存在时的接法） |

---

## 四、第二步：看清要推的内容

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

**分叉检测：**

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

### 重试循环（代理 502 时用它）

```bash
for i in 1 2 3 4 5 6; do
  echo "--- 尝试 $i ---"
  timeout 90 git -c credential.helper= -c credential.helper='!gh auth git-credential' \
    fetch origin main 2>&1 | tail -2
  if git rev-parse --verify -q FETCH_HEAD >/dev/null 2>&1; then
    echo "FETCH_HEAD 就绪: $(git rev-parse FETCH_HEAD)"; break
  fi
  sleep 3
done
```

`push` 同理加重试。注意：`ls-remote`（小请求）常常能过而 `fetch`（带 packfile）被断，所以**不能用 ls-remote 成功来推断 fetch 会成功**。

---

## 五、第三步：提交

只暂存该提交的内容，不要无脑 `git add -A`：

```bash
git add <具体路径>        # 优先
```

**必须先通过第六节的方向性核对**，再 add。

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

## 六、方向性核对：别把旧版推上去

**`git status` 的 `M` 只表示"与 HEAD 不同"，不表示"本地更新"。** 从别处拷来的目录常常是**旧快照**，直接提交等于回退远端的更新。

对每个非 `??` 文件，跑 `git diff -- <file>` 看方向，然后按下表判定：

| 状态 | 含义 | 处置 |
|---|---|---|
| `??` | 远端没有 | **真正的增量**，提交 |
| ` M` 且本地是新版 | 正常修改 | 提交 |
| ` M` 但本地是**旧版**（远端更早提交过更新） | **会回退远端** | `git checkout -- <file>` 丢弃本地，**不要提交** |
| ` D` | 远端有、本地没有 | **误删**，`git checkout -- <file>` 恢复，**不要提交删除** |

### 实战案例（2026-09-24，一个无 `.git` 的副本）

对比后发现的四个方向性问题：

| 文件 | 表面状态 | 真相 | 处置 |
|---|---|---|---|
| `scripts/01.ipynb` | ` M` | 本地把远端已改好的中文说明回退成 `print('hi ff')` | 丢弃本地 |
| `.workbuddy/memory/2026-09-17.md` | ` M` | 本地是旧版，比远端少一整节（含 gh-push 建 skill 记录） | 丢弃本地 |
| `.workbuddy/skills/gh-push/SKILL.md` | ` D` | 副本缺该文件 | `checkout` 恢复 |
| `README.md` / `MEMORY.md` | ` M` | 本地确实是新版（09-24 新增内容） | 提交 |

**只看 `git status` 会误判两个文件、丢掉一整节记录。**

### 无 `.git` 的目录，但远端已有仓库时

不要 `clone`（会覆盖本地增量），也不要强推（会覆盖远端历史）。接法：

```bash
git init -b main
git remote add origin https://github.com/<owner>/<repo>.git
git fetch origin main
git reset --mixed FETCH_HEAD      # HEAD 接上远端历史，工作区不动
git status --short                # 现在看到的才是"真实差异"
git checkout -- <本地是旧版的> <被误删的>   # 按第六节核对表处理
```

`reset --mixed` 之后，HEAD 与远端一致、工作区没被动过，因此 `status` 展示的就是真差异。之后提交增量，推送是**快进**，不需要强推。

---

## 七、通道 B：SSH + ssh-agent（当前网络不可用，配置已就位）

### 先做连通性预检（15 秒，别跳过）

```bash
timeout 12 ssh -o StrictHostKeyChecking=accept-new -T git@github.com 2>&1 | head -3
```

- 返回 `Hi <user>! You've successfully authenticated` → 通，继续。
- 返回 `Permission denied (publickey)` → 隧道通、key 没注册，去做"注册公钥"。
- 返回 `Connection timed out` / `Connection reset` / `Connection closed` → **网络封禁，直接停止**，回落通道 A，如实报告。

### 已就位的部分（2026-09-24 建成）

| 组件 | 位置 / 状态 |
|---|---|
| 隧道脚本 | `~/.ssh/gh-connect.py` — 纯 stdlib，替代本机缺失的 `nc` / `connect.exe` / `socat` |
| SSH 配置 | `~/.ssh/config` — `Host github.com` → `HostName ssh.github.com` / `Port 443` / `ProxyCommand <python> gh-connect.py %h %p` |
| 密钥 | `~/.ssh/id_ed25519_github`（ed25519，无口令），指纹 `SHA256:n7zoMram3tjON8KGIeshEnMOFHxo3DPNzIcCn6f2878` |
| ssh-agent | 已托管该 key。**会话级**：`ssh-agent -s > ~/.ssh/agent.env`，之后每条命令先 `. ~/.ssh/agent.env` |

### 为什么需要隧道

校园网对 GitHub 的 SSH 入口做了**整体封禁**，且是 IP 级而非主机名级：

| 探测 | 结果 |
|---|---|
| `github.com:22` | 直连超时 |
| `ssh.github.com:443` 直连 | TCP 通，SSH 握手被 RST（`kex_exchange_identification: Connection reset`） |
| 经会话代理 CONNECT 到 `ssh.github.com:443` | 隧道 200 建立，**远端立刻关闭（零字节）** |
| 经会话代理 CONNECT 到解析出的 IP `20.205.243.160:443` | 同样零字节 → **排除主机名过滤** |
| 11 个 GitHub 备用 IP × {22, 443} | 22 全超时、443 全 RST |

**结论**：本机当前无论直连还是经代理，都到不了 GitHub 的 SSH 入口。隧道方案在网络放开（境外出口）后即可用，脚本无需改动。

### 注册公钥

本机 gh token 的 scopes 是 `gist, read:org, repo, workflow`，**没有 `admin:public_key`**，因此：

| 方式 | 是否可自动 | 说明 |
|---|---|---|
| **Deploy Key**（仓库级） | ✅ 可以 | `gh api -X POST repos/<owner>/<repo>/keys -f title=... -f key="$(cat ~/.ssh/id_ed25519_github.pub)" -F read_only=false`。只需 `repo` scope。**仅对该仓库有效** |
| **账号 SSH Key** | ❌ 需一次授权 | 先 `gh auth refresh -h github.com -s admin:public_key`（会弹浏览器/设备码），再 `gh ssh-key add ~/.ssh/id_ed25519_github.pub --title "<machine>"`。所有仓库通用 |

### 切到 SSH 推送

```bash
git remote set-url origin git@github.com:<owner>/<repo>.git
git push origin "$BRANCH"        # 认证走 ssh-agent，不需要 credential.helper
```

---

## 八、通道 A：HTTPS 推送（默认）

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

新分支首次推送加 `-u`。

### 持久化（可选）

`gh auth setup-git` 可让以后直接 `git push` 就走 gh。**它改全局配置，执行前须征得用户同意。**

---

## 九、推完必须验证

**不要相信 push 的退出码**，用远程实际值确认：

```bash
echo -n "本地: "; git rev-parse HEAD
echo -n "远程: "; timeout 60 git ls-remote origin "refs/heads/$BRANCH" | cut -f1
echo -n "上游: "; git config --get "branch.$BRANCH.merge" || echo "未设置"
git status --short && echo "(空=工作区干净)"
```

哈希一致 = 成功。

> **实测（2026-09-24）**：全局 `push.autosetupremote=true` **并未**在 `git push origin main` 后建立上游——推送成功但 `branch.main.merge` 仍为空。
> 后果：之后 `git pull` / 不带参数的 `git push` 会报 `no upstream configured`。
> **处理**：推完顺手查一次，缺了就 `git branch --set-upstream-to=origin/<branch> <branch>`。
>
> 注意 `ls-remote` 可能被代理 502 打断，此时**不要**据此判定推送失败——以 `git push` 自身的输出（`<old>..<new>  main -> main`）和 `gh repo view --json pushedAt` 交叉确认。

---

## 十、冲突与报错处置

| 报错 | 原因 | 处置 |
|---|---|---|
| `CONNECT tunnel failed, response 502` | 会话代理间歇失效 | 走第四节的**重试循环**；别断言断网 |
| `Failed to connect ... after 21104 ms` | 清代理直连（已不可用） | 去掉 `env -u *_proxy`，让 git 走会话代理 |
| `non-fast-forward` | 远程有新 commit | `git pull --rebase origin <branch>` 后重推 |
| `fetch first` | 本地落后 | 同上 |
| `stale info` | `--force-with-lease` 期望值过期 | 用 `git ls-remote` 取真实远程值作 lease |
| `could not read Username` | helper 链被清空 | 回到第八节两段式写法 |
| `GH013 ... push protection` | 提交含疑似密钥 | 停止，移除敏感内容后重来 |
| SSH: `Connection reset` / `timed out` | 校园网封 GitHub SSH | 停止，回落通道 A（第七节） |
| `ambiguous argument 'origin/main'` | remote-tracking ref 缺失（旧环境） | 用 `ls-remote` / `FETCH_HEAD` 替代 |

### 强推（危险）

**仅在用户明确要求时执行**，优先 `--force-with-lease`：

```bash
REMOTE=$(git ls-remote origin "refs/heads/$BRANCH" | cut -f1)
git ... push --force-with-lease="$BRANCH:$REMOTE" origin "$BRANCH"
```

lease 期望值必须是**真实远程哈希**（用 `ls-remote` 取，不要用本地记的值）。

> **强推会覆盖远程历史，可能造成他人工作丢失。执行前必须向用户确认，并说明目标哈希。**

---

## 快速参考：一键流程（无冲突、通道 A）

```bash
export PATH="/usr/bin:/bin:/c/Windows/System32:/c/Windows:$PATH"
cd <repo>
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git fetch origin "$BRANCH"                    # 502 就重试
git status --short                            # 逐文件做方向性核对（第六节）
git add <paths> && git commit -m "<type>: <desc>"
timeout 90 git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin "$BRANCH"
git rev-parse HEAD && timeout 60 git ls-remote origin "refs/heads/$BRANCH" | cut -f1
```

---

## 边界

- **只管推送**，不做仓库初始化、不建 PR（PR 用 `gh pr create`）。
- 仓库**无 GitHub 远程** → 本 skill 无能为力，改用 `git-init`。
- **不做** `git reset --hard`、`git clean -fd` 这类丢弃本地改动的事。
- 第六节的 `git checkout -- <file>` 是**丢弃本地旧版**，属于必要动作，但每次都要在报告里写清丢了什么。
- 用户说"不要提交 X"时，**绝不**用 `git add -A` 兜底。
- SSH 不通时**不要**自造更多隧道变通（换协议、装第三方工具、改 hosts）——报告根因即可。

## 报告格式

一句话：(通道 A/B) (分支) 从 `<旧哈希>` 推到 `<新哈希>`，N 个 commit、M 个文件变更。**方向性核对丢弃了哪些文件也要写出来**。失败则直说卡在哪步、什么报错、下一步建议。
