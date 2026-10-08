# CX insight to growth

Turn customer data into reportsfor **sales**, **marketing** and **product** team leaders, in their own language.
step for each one.

**Examples:** [Sales brief](examples/sales.pdf) · [Marketing brief](examples/marketing.pdf) · [Product brief](examples/product.pdf)

---

## How to use this

1. [What you need](#what-you-need)
2. [Set it up](#set-it-up)
3. [Use it](#use-it)
4. [Before you share a report](#before-you-share-a-report)
5. [For maintainers](#for-maintainers)

---

## What you need

| | |
|---|---|
| **An AI account** | Claude, ChatGPT or Gemini. Any other AI chat also works with the copy-paste prompt. |
| **Customer data** | One source is enough to start. More sources give better findings. |

**Data you can use:**

| Source | What to give the AI |
|---|---|
| Support tickets | An export from your help desk (Zendesk, Intercom, Gorgias, Freshdesk and others), or 30 to 100 tickets copied into the chat |
| Website data | A Google Analytics export: sessions and purchases by week, channel and device |
| Support team notes | Plain text observations from your support team |

> If your AI is already connected to these tools, it can get the data itself.

---

## Set it up

Pick the AI you use. Each setup takes about 5 minutes and you do it only once.

| Your AI | What you download |
|---|---|
| [Claude (claude.ai)](#claude-claudeai) | [voc-report-skill.zip](downloads/voc-report-skill.zip) |
| [Claude Code](#claude-code) | Nothing: type two commands |
| [ChatGPT](#chatgpt) | [chatgpt-gemini-files.zip](downloads/chatgpt-gemini-files.zip) |
| [Gemini](#gemini) | [chatgpt-gemini-files.zip](downloads/chatgpt-gemini-files.zip) |
| [Any other AI](#any-other-ai) | [voc-report-prompt.md](downloads/voc-report-prompt.md) |

To download a file: click its link, then click **Download raw file** (the arrow icon at the top right).

### Claude (claude.ai)

1. Download [voc-report-skill.zip](downloads/voc-report-skill.zip). Do not unzip it.
2. In Claude, open **Settings**, then **Capabilities**. Make sure **code execution** is on.
3. Under **Skills**, click **Upload skill** and choose the zip file.

### Claude Code

Type these two commands in Claude Code:

```
/plugin marketplace add benfoden/cx-insight-to-growth
/plugin install cx-insight-to-growth@cx-insight-to-growth
```

### ChatGPT

You need a paid ChatGPT plan to make a GPT.

1. Download [chatgpt-gemini-files.zip](downloads/chatgpt-gemini-files.zip) and unzip it.
2. In ChatGPT, open **GPTs**, click **Create**, then open the **Configure** tab.
3. Give it a name, for example "Customer insight briefs".
4. Copy the [instructions text](#instructions-text-for-chatgpt-and-gemini) into **Instructions**.
5. Under **Knowledge**, upload all the files from the unzipped folder, including the files in `sample-data`.
6. Under **Capabilities**, turn on **Code Interpreter & Data Analysis** and **Canvas**.
7. Click **Create** and choose who can use it.

### Gemini

1. Download [chatgpt-gemini-files.zip](downloads/chatgpt-gemini-files.zip) and unzip it.
2. In Gemini, open **Gems**, then click **New Gem**.
3. Give it a name, and copy the [instructions text](#instructions-text-for-chatgpt-and-gemini) into **Instructions**.
4. Under **Knowledge**, add all the files from the unzipped folder.
   If Gemini refuses a file, add `.txt` to the end of its name and try again.
5. Click **Save**.

### Instructions text for ChatGPT and Gemini

```text
You make one-page customer insight briefs for sales, marketing and product teams.
Follow voc-report-prompt.md in your knowledge files exactly, step by step.
If you can run Python, run metrics.py on the data.
Use the sample-data files only when the user asks for a demo.
```

### Any other AI

No setup needed.

1. Open [voc-report-prompt.md](downloads/voc-report-prompt.md) and click **Copy raw file**.
2. Paste it into a new chat.
3. Add your data in the same message, or in the next one.

---

## Use it

**Step 1.** Ask:

> Make the customer insight briefs for the last 8 weeks.

**Step 2.** Give your data when the AI asks for it. Upload files or paste text.

**Step 3.** You get three pages: sales, marketing and product.
To save a page as a PDF, open it in your browser, click **Print**, then **Save as PDF**.

**Step 4.** Want more? Ask for detail on any part:

> Make a detailed report on finding 2 of the product brief.

> Deep dive on shipping costs.

**Try a demo first.** Ask "Show me a demo with the sample data." The demo uses a made-up outdoor-gear store.

---

## Before you share a report

- **Check each page.** The numbers come from your data, but the AI writes the findings.
- **Remove personal data** (names, emails, phone numbers, order numbers) before you give data to an AI.
- **Follow your company's rules** for customer data.

---

## For maintainers

| Path | What it is |
|---|---|
| `skills/voc-report/` | The skill: `SKILL.md` (instructions), `template.html` (page design), `metrics.py` (optional calculator), `sample-data/` |
| `.claude-plugin/` | Claude Code plugin and marketplace files |
| `downloads/` | Built files for Claude.ai, ChatGPT, Gemini and the copy-paste prompt |
| `examples/` | Example briefs made from the sample data (HTML and PDF) |
| `scripts/build.py` | Rebuilds `downloads/` after you change the skill |

After you edit anything in `skills/voc-report/`, run `python3 scripts/build.py` and commit the new `downloads/`.
