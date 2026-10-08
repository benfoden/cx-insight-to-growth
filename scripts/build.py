"""Rebuild everything in downloads/ from skills/voc-report/. Run: python3 scripts/build.py

  downloads/voc-report-skill.zip     Claude.ai skill upload
  downloads/voc-report-prompt.md     one self-contained prompt for any AI (paste or upload)
  downloads/chatgpt-gemini-files.zip prompt + metrics.py + sample data, for a ChatGPT GPT or a Gemini Gem
"""
import os, re, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "voc-report")
OUT = os.path.join(ROOT, "downloads")
DEMO = "https://github.com/benfoden/cx-insight-to-growth/tree/main/skills/voc-report/sample-data"


def swap(text, old, new):
    if old not in text:
        raise SystemExit(f"build: SKILL.md changed, update scripts/build.py (missing: {old[:60]!r})")
    return text.replace(old, new)


def prompt():
    s = open(os.path.join(SKILL, "SKILL.md")).read()
    s = re.sub(r"\A---.*?---\n", "", s, flags=re.S)
    s = swap(s, "Files in this skill: `template.html` (the page), `metrics.py` (optional exact calculator),\n`sample-data/` (demo data only).",
             "The page template is at the end of this prompt.")
    s = swap(s, "If the user asks for a demo, use `sample-data/` (a fictional outdoor-gear store).",
             f"If the user asks for a demo, use the sample files if you have them. If not, ask the user to download and upload them from {DEMO}")
    s = swap(s, "If you can run Python, run `python3 metrics.py <files or folder>` and use its JSON output.",
             "If you have the file `metrics.py` and can run Python, run `python3 metrics.py <files or folder>` and use its JSON output.\nIf not, calculate with your code tool, or by hand.")
    s = swap(s, "Fill in `template.html`.", "Fill in the page template at the end of this prompt.")
    s = swap(s, "with the same `<style>`\nfrom `template.html`.", "with the same `<style>`\nfrom the page template.")
    tpl = open(os.path.join(SKILL, "template.html")).read()
    return ("<!-- voc-report prompt. Paste all of this into any AI chat (or upload it as a file), then add your data. -->\n"
            + s.rstrip() + "\n\n## Page template\n\nCopy this HTML for each page and replace every {{...}}.\n\n```html\n" + tpl.rstrip() + "\n```\n")


def zipdir(path, files, arc):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f, a in zip(files, arc):
            z.write(f, a)


def main():
    os.makedirs(OUT, exist_ok=True)
    md = prompt()
    if "\u2014" in md:
        raise SystemExit("build: em dash found")
    p = os.path.join(OUT, "voc-report-prompt.md")
    open(p, "w").write(md)
    skill_files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(SKILL) for f in fs if "__pycache__" not in dp and f != ".DS_Store")
    zipdir(os.path.join(OUT, "voc-report-skill.zip"), skill_files, [os.path.join("voc-report", os.path.relpath(f, SKILL)) for f in skill_files])
    demo = sorted(os.path.join(SKILL, "sample-data", f) for f in os.listdir(os.path.join(SKILL, "sample-data")))
    files = [p, os.path.join(SKILL, "metrics.py")] + demo
    zipdir(os.path.join(OUT, "chatgpt-gemini-files.zip"), files, ["voc-report-prompt.md", "metrics.py"] + [os.path.join("sample-data", os.path.basename(f)) for f in demo])
    for f in sorted(os.listdir(OUT)):
        print(f"downloads/{f}  {os.path.getsize(os.path.join(OUT, f)) // 1024 or 1} KB")


if __name__ == "__main__":
    main()
