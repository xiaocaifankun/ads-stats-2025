"""HTML -> Markdown converter for the learning-guide handbooks.

Why this exists: `tools/file_to_md.py` delegates to markitdown, which is not
installed here and cannot be fetched reliably. These handbooks are structured
(section / h2 / h3 / p / div-based "rule" lists / tables / inline <svg>
diagrams / script-held quiz data). Three details decide fidelity:

  * Text lives in <div class="rule"> blocks, not <li> — so the converter keeps a
    single "current line" buffer that block boundaries flush, instead of
    emitting every fragment as its own paragraph.
  * <svg> diagrams carry most of the explanatory text in <text> elements. They
    are reconstructed (rows grouped by y, cells ordered by x) into fenced
    blocks instead of being dropped.
  * The quiz lives in a JS array whose field names differ per file
    (`o`/`opts`, `a`/`ans`, `e`/`why`, `lt`/`lv`). It is evaluated with node and
    rendered as a markdown section with normalised field access.

Usage:
    python tools/html_to_md.py <input.html> [<input2.html> ...]

Writes `<stem>.md` next to each input.
"""

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

NODE_BIN = r"C:\Users\yangjh\.workbuddy\binaries\node\versions\22.22.2-3\node.exe"

VOID_TAGS = {"br", "hr", "img", "input", "meta", "link"}
SKIP_TAGS = {"style", "head", "title"}
INLINE_WRAP = {"strong": "**", "b": "**", "em": "_", "i": "_", "code": "`", "kbd": "`"}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")


def needs_space(left: str, right: str) -> bool:
    """Whether two fragments need a separating space when joined."""
    if not left or not right:
        return False
    if left[-1] in " \n\t([`/|-":
        return False
    if right[0] in " \n\t),.;:!?%\u3001\u3002\uff0c\uff09]":
        return False
    if CJK.match(left[-1]) or CJK.match(right[0]):
        return False
    return True


class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []          # finished lines
        self.cur: str = ""                # line currently being built
        self.buf: list[str] = []          # raw inline text, not yet drained
        self.suppress = 0
        self.in_script = False
        self.script_buf: list[str] = []
        self.in_pre = False
        # lists
        self.lists: list[str] = []
        self.li_buf: list[str] | None = None
        self.li_depth = 0
        # tables
        self.row: list[str] | None = None
        self.rows: list[list[str]] = []
        # links
        self.href: str | None = None
        self.a_mark = 0
        self.a_buf_mark = 0
        self.in_a = False
        # svg
        self.in_svg = 0
        self.in_text = False
        self.text_buf: list[str] = []
        self.svg_x = 0.0
        self.svg_y: float | None = None
        self.svg_line: list[tuple[float, str]] = []
        self.svg_rows: list[list[tuple[float, str]]] = []

    # ------------------------------------------------------------- line model
    def drain(self) -> None:
        text = re.sub(r"[ \t\u00a0\r\n]+", " ", "".join(self.buf)).strip()
        self.buf = []
        if not text:
            return
        if self.li_buf is not None:
            self.li_buf.append(text)
            return
        if self.row is not None:
            self.row.append(text)
            return
        if not self.cur:
            self.cur = text
        elif needs_space(self.cur, text):
            self.cur += " " + text
        else:
            self.cur += text

    def push(self) -> None:
        """Finish the current line and start a new one."""
        self.drain()
        if self.cur:
            self.out.append(self.cur.strip())
            self.cur = ""

    def start_line(self, prefix: str) -> None:
        self.push()
        self.cur = prefix

    # ----------------------------------------------------------------- svg
    def flush_svg_line(self) -> None:
        if self.svg_line:
            self.svg_rows.append(self.svg_line)
            self.svg_line = []
        self.svg_y = None

    def render_svg(self) -> None:
        self.flush_svg_line()
        if not self.svg_rows:
            self.svg_y = None
            return
        self.out.append("")
        self.out.append("```text")
        for row in self.svg_rows:
            row.sort(key=lambda t: t[0])
            self.out.append("   ".join(t for _, t in row))
        self.out.append("```")
        self.out.append("")
        self.svg_rows = []

    # ----------------------------------------------------------------- tags
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VOID_TAGS:
            return
        if tag in SKIP_TAGS:
            self.suppress += 1
            return
        if self.suppress:
            return

        if tag == "script":
            self.in_script = True
            self.script_buf = []
            return
        if tag == "svg":
            self.push()
            self.in_svg += 1
            self.svg_rows = []
            self.out.append("")
            self.out.append("<!-- 图 -->")
            return
        if self.in_svg:
            if tag == "text":
                self.in_text = True
                self.text_buf = []
                try:
                    y = float(a.get("y", "0").split()[0])
                except ValueError:
                    y = self.svg_y or 0.0
                if self.svg_y is not None and abs(y - self.svg_y) > 6:
                    self.flush_svg_line()
                self.svg_y = y
                try:
                    self.svg_x = float(a.get("x", "0").split()[0])
                except ValueError:
                    self.svg_x = 0.0
            return

        if tag in HEADINGS:
            self.start_line("#" * HEADINGS[tag] + " ")
        elif tag == "p":
            self.push()
        elif tag == "div":
            self.push()
        elif tag == "br":
            self.push()
        elif tag == "figcaption":
            self.start_line("> ")
        elif tag == "blockquote":
            self.start_line("> ")
        elif tag == "pre":
            self.push()
            self.in_pre = True
            self.out.append("```")
        elif tag in ("ul", "ol"):
            self.end_li()
            self.push()
            self.lists.append(tag)
        elif tag == "li":
            self.push()
            self.li_buf = []
            self.li_depth = len(self.lists)
        elif tag == "table":
            self.push()
            self.rows = []
        elif tag == "tr":
            self.row = []
        elif tag == "hr":
            self.push()
            self.out.append("---")
        elif tag == "a":
            self.a_mark = len(self.out)
            self.a_buf_mark = len(self.buf)
            self.href = a.get("href")
            self.in_a = True
        elif tag in INLINE_WRAP:
            self.buf.append(INLINE_WRAP[tag])

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if tag in SKIP_TAGS:
            self.suppress = max(0, self.suppress - 1)
            return
        if self.suppress:
            return

        if tag == "script":
            self.in_script = False
            self.capture_quiz()
            return
        if tag == "svg":
            self.in_svg = max(0, self.in_svg - 1)
            if self.in_svg == 0:
                self.render_svg()
            return
        if self.in_svg:
            if tag == "text":
                self.in_text = False
                txt = re.sub(r"\s+", " ", "".join(self.text_buf)).strip()
                if txt:
                    self.svg_line.append((self.svg_x, txt))
                self.text_buf = []
            return

        if tag in HEADINGS or tag in ("p", "div", "figcaption", "blockquote"):
            self.push()
        elif tag == "pre":
            self.drain()
            self.out.append("```")
            self.in_pre = False
        elif tag in ("ul", "ol"):
            self.end_li()
            if self.lists:
                self.lists.pop()
            self.push()
        elif tag == "li":
            self.end_li()
        elif tag in ("td", "th"):
            self.drain()
        elif tag == "tr":
            self.drain()
            if self.row:
                self.rows.append(self.row)
            self.row = None
        elif tag == "table":
            self.push()
            self.render_table()
        elif tag == "a":
            self.end_a()
        elif tag in INLINE_WRAP:
            self.buf.append(INLINE_WRAP[tag])

    def handle_data(self, data):
        if self.in_script:
            self.script_buf.append(data)
            return
        if self.suppress:
            return
        if self.in_svg:
            if self.in_text:
                self.text_buf.append(data)
            return
        self.buf.append(data)

    # ------------------------------------------------------------------ li
    def end_li(self) -> None:
        if self.li_buf is None:
            return
        self.drain()
        body = " ".join(x for x in self.li_buf if x).strip()
        self.li_buf = None
        if body:
            self.cur = "  " * max(0, self.li_depth - 1) + "- " + body
            self.push()

    # ------------------------------------------------------------------- a
    def end_a(self) -> None:
        if not self.in_a:
            return
        url = self.href or ""
        self.in_a = False
        self.href = None
        if len(self.out) > self.a_mark:
            # block-level content was flushed inside the anchor: re-join it
            self.push()
            block = self.out[self.a_mark:]
            del self.out[self.a_mark:]
            label = re.sub(r"\s+", " ", " ".join(x for x in block if x)).strip()
            if label:
                self.cur = f"[{label}]({url})"
                self.push()
        else:
            # purely inline: bracket the text in place
            self.buf.insert(min(self.a_buf_mark, len(self.buf)), "[")
            self.buf.append(f"]({url})" if url else "]")

    # ---------------------------------------------------------------- table
    def render_table(self) -> None:
        if not self.rows:
            return
        width = max(len(r) for r in self.rows)
        rows = [r + [""] * (width - len(r)) for r in self.rows]
        self.out.append("")
        for i, r in enumerate(rows):
            cells = [c.replace("|", "\\|") for c in r]
            self.out.append("| " + " | ".join(cells) + " |")
            if i == 0:
                self.out.append("|" + "---|" * width)
        self.out.append("")
        self.rows = []

    # ----------------------------------------------------------------- quiz
    def capture_quiz(self) -> None:
        src = "".join(self.script_buf)
        m = re.search(
            r"\b(?:var|const|let)\s+(QUIZ|QS|QUESTIONS)\s*=\s*(\[.*?\])\s*;", src, re.S
        )
        if not m:
            return
        try:
            res = subprocess.run(
                [NODE_BIN, "-e", f"console.log(JSON.stringify({m.group(2)}))"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            items = json.loads(res.stdout)
        except Exception as exc:  # noqa: BLE001
            self.out.append(f"<!-- quiz extraction failed: {exc} -->")
            return

        self.out.append("")
        self.out.append("## 自测题")
        self.out.append("")
        self.out.append(f"> 提取自页面交互脚本，共 {len(items)} 题。")
        for i, q in enumerate(items, 1):
            lv_label = q.get("lt") or {
                1: "基础 · 识别",
                2: "进阶 · 理解",
                3: "挑战 · 应用",
            }.get(q.get("lv"), str(q.get("lv") or ""))
            meta = " · ".join(x for x in (lv_label, q.get("tag", "")) if x)
            self.out.append("")
            self.out.append(f"### 第 {i} 题{'（' + meta + '）' if meta else ''}")
            self.out.append("")
            self.out.append(re.sub(r"<[^>]+>", "", q.get("q", "")).strip())
            opts = q.get("opts") or q.get("o") or []
            ans = q.get("ans", q.get("a"))
            for j, opt in enumerate(opts):
                body = re.sub(r"<[^>]+>", "", opt).strip()
                self.out.append(f"- {'ABCD'[j]}. {body}{' ✅' if j == ans else ''}")
            exp = q.get("why") or q.get("e") or q.get("exp")
            if exp:
                self.out.append("")
                self.out.append("**解析**：" + re.sub(r"<[^>]+>", "", exp).strip())
            if q.get("back"):
                self.out.append("")
                self.out.append(f"*对应章节：`{q['back']}`*")

    # ---------------------------------------------------------------- output
    def result(self) -> str:
        self.end_li()
        self.push()
        text = "\n".join(self.out)
        text = re.sub(r"\[\s*\n\s*", "[", text)
        text = re.sub(r"\s*\n\s*\]\(", "](", text)
        # keep a blank line after every ATX heading
        text = re.sub(r"^(#{1,6} .+)$", r"\1\n", text, flags=re.M)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def convert(path: Path) -> Path:
    raw = path.read_text(encoding="utf-8", errors="replace")
    guide = GuideParser()
    guide.feed(raw)

    title = "Untitled"
    for pat in (r"<h1[^>]*>(.*?)</h1>", r"<h2[^>]*>(.*?)</h2>", r"<title>(.*?)</title>"):
        m = re.search(pat, raw, re.S | re.I)
        if m:
            title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
            break

    out_path = path.with_suffix(".md")
    header = (
        f"# {title}\n\n"
        f"> 转换自 `{path.name}`（`tools/html_to_md.py`）· 原 HTML 保留在同目录，作为不可变源。\n\n"
    )
    out_path.write_text(header + guide.result(), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)
    for arg in sys.argv[1:]:
        p = Path(arg)
        written = convert(p)
        print(f"{p.name} -> {written.name} ({written.stat().st_size} B)")
