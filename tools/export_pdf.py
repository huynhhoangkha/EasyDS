"""Export DSBoard2026_specs.md to a print-styled PDF via Chrome."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "docs" / "DSBoard2026_specs.md"
PDF_DIR = ROOT / "docs" / "generated"
PDF_PATH = PDF_DIR / "DSBoard2026_specs.pdf"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
MERMAID_JS = Path(tempfile.gettempdir()) / "mermaid-11.min.js"

CSS = r"""
@page { size: A4; margin: 16mm 14mm; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Segoe UI", Calibri, Helvetica, Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.45;
  color: #1f2328;
  background: #fff;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
h1 { font-size: 20pt; font-weight: 650; margin: 0 0 12pt; letter-spacing: -0.02em; page-break-after: avoid; }
h2 { font-size: 14pt; font-weight: 650; margin: 18pt 0 8pt; padding-bottom: 3pt; border-bottom: 1px solid #d0d7de; page-break-after: avoid; }
h3 { font-size: 12pt; font-weight: 650; margin: 14pt 0 6pt; page-break-after: avoid; }
p { margin: 0 0 8pt; }
a { color: #0969da; text-decoration: none; }
ul, ol { margin: 0 0 8pt; padding-left: 1.3em; }
li { margin: 0 0 2pt; }
hr { border: 0; border-top: 1px solid #d0d7de; margin: 14pt 0; }
blockquote {
  margin: 8pt 0 10pt;
  padding: 6pt 12pt;
  border-left: 4px solid #0969da;
  background: #f6f8fa;
}
blockquote p { margin: 0; }
code {
  font-family: Consolas, "Cascadia Mono", "Courier New", monospace;
  font-size: 9pt;
  background: #f6f8fa;
  padding: 0.1em 0.35em;
  border-radius: 4px;
}
pre {
  background: #f6f8fa;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  padding: 8pt 10pt;
  overflow: hidden;
  font-size: 8.5pt;
  line-height: 1.35;
  page-break-inside: avoid;
  white-space: pre-wrap;
}
pre code { background: none; padding: 0; font-size: inherit; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0 0 12pt;
  font-size: 9.5pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #d0d7de;
  padding: 5pt 7pt;
  vertical-align: top;
  text-align: left;
}
th { background: #f6f8fa; font-weight: 650; }
tr:nth-child(even) td { background: #fbfcfd; }
.mermaid {
  margin: 10pt 0 14pt;
  page-break-inside: avoid;
  text-align: center;
}
.mermaid svg { max-width: 100% !important; height: auto !important; }
"""

HTML_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Minimal Digital Logic Board — Product Specification</title>
  <style>{css}</style>
  <script>{mermaid_js}</script>
</head>
<body>
  <article class="doc">{body}</article>
  <script>
    mermaid.initialize({{
      startOnLoad: false,
      theme: "neutral",
      securityLevel: "loose",
      flowchart: {{ useMaxWidth: true, htmlLabels: true, padding: 12, nodeSpacing: 30, rankSpacing: 40 }},
      themeVariables: {{
        fontFamily: "Segoe UI, Calibri, Helvetica, Arial, sans-serif",
        fontSize: "15px",
        lineColor: "#24292f",
        primaryColor: "#ffffff",
        primaryTextColor: "#1f2328",
        primaryBorderColor: "#24292f",
        secondaryColor: "#f6f8fa",
        tertiaryColor: "#ffffff"
      }}
    }});
    mermaid.run().then(function () {{
      document.documentElement.setAttribute("data-ready", "1");
    }});
  </script>
</body>
</html>
"""


def md_to_html(text: str) -> str:
    placeholders: list[str] = []

    def stash(match: re.Match[str]) -> str:
        placeholders.append(match.group(1).strip("\n"))
        return f"\n\nMERMAID_PLACEHOLDER_{len(placeholders) - 1}\n\n"

    text = re.sub(r"```mermaid\n(.*?)```", stash, text, flags=re.S)
    body = markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False}},
    )
    for i, src in enumerate(placeholders):
        body = body.replace(
            f"<p>MERMAID_PLACEHOLDER_{i}</p>",
            f'<pre class="mermaid">{src.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</pre>',
        )
    return body


def main() -> None:
    if not MERMAID_JS.exists():
        raise SystemExit(f"Missing {MERMAID_JS}; download mermaid.min.js first")
    body = md_to_html(MD_PATH.read_text(encoding="utf-8"))
    html = HTML_TMPL.format(
        css=CSS,
        body=body,
        mermaid_js=MERMAID_JS.read_text(encoding="utf-8"),
    )
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    html_path = PDF_DIR / "_pdf_preview.html"
    html_path.write_text(html, encoding="utf-8")
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=20000",
            f"--print-to-pdf={PDF_PATH}",
            html_path.resolve().as_uri(),
        ],
        check=True,
    )
    html_path.unlink(missing_ok=True)
    print(f"Wrote {PDF_PATH} ({PDF_PATH.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
