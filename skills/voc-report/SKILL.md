---
name: voc-report
description: Make simple one-page customer insight briefs (HTML) for sales, marketing and product teams from voice-of-customer data (support tickets, CSAT, sentiment, support team notes) and website behavior data (Google Analytics). Use when asked for a VoC report, customer insights, support ticket insights, or what sales, marketing or product should do based on customer data.
---

# VoC one-page briefs

You make one HTML page per team (sales, marketing, product) that turns customer data into three
findings and three next steps. Numbers come from calculation. Meaning and wording come from you.
Files in this skill: `template.html` (the page), `metrics.py` (optional exact calculator),
`sample-data/` (demo data only).

## 1. Get the data

Use the first option that works. Do not use sample data unless the user asks for a demo.

1. **Connected sources.** Check your tools and connectors for analytics (Google Analytics, BigQuery,
   Looker), help desk (Zendesk, Intercom, Gorgias, Freshdesk, HubSpot, Salesforce), and team notes
   (Slack, Google Drive, Notion). Pull the last 8 weeks.
2. **Files the user already gave you** in this chat or project.
3. **Ask.** Name the sources you need and the easiest way to give them:
   - Behavior: a GA4 export (CSV) by week, channel and device with sessions and purchases. A funnel
     export (step, users, by device) and a site search export (term, searches, exits) help too.
   - Voice of customer: a help desk ticket export (CSV), or 30 to 100 recent tickets pasted as text.
   - Team notes: paste support team observations as plain text.

One source is enough to start. Say which sources are missing and what they would add.
If the user asks for a demo, use `sample-data/` (a fictional outdoor-gear store).

## 2. Calculate

If you can run Python, run `python3 metrics.py <files or folder>` and use its JSON output.
Pasted text: save it as a .csv or .txt file first. If you cannot run code, calculate by hand:

| Metric | Formula |
|---|---|
| Conversion rate | purchases / sessions (total, per channel, per device) |
| Channel share | channel sessions / all sessions |
| Step-through | users at a funnel step / users at the step before it |
| Trend | split the period at its middle date; compare first half to second half |
| Search exit rate | exits / searches, per term |
| Ticket share | tickets on a topic / all tickets |
| Negative share | tickets that complain or show frustration / tickets on that topic |
| CSAT | mean of the scores that exist |

Every number in a report must come from this step. Round to whole numbers unless the value is under 10.

## 3. Interpret

1. Group tickets into 5 to 8 topics. Start from tags. Read the untagged and catch-all tickets
   ("general", "other"): they often hold a new topic that no tag covers. Name it if 3 or more tickets share it.
2. Join sources. The strongest findings show one cause in two places, for example a topic that rises
   in tickets while a funnel step drops, or a search term with a high exit rate that matches a ticket topic.
3. Pick the 3 findings that matter most for each team:
   - **Sales:** questions and doubts that stop a first purchase, the answer to each, and proof customers give.
   - **Marketing:** channels that convert or waste spend, promises that create friction, the words customers use.
   - **Product:** where the funnel leaks, gaps between devices, defects, and missing information.
4. Each finding gets one next step: a concrete action that team owns this month.

## 4. Write each page

Fill in `template.html`. Keep the page to these blocks only, so it stays easy to scan:

- **Action title:** the main message as a full sentence, max 15 words. Not a topic name.
- **Meta line:** team, company, period, sources with counts.
- **3 numbers:** the three numbers this team needs most, each with a short plain label.
- **3 key findings:** headline (max 12 words), one evidence sentence with the numbers, one next step.
- **Exhibit 1:** one bar chart with max 6 rows. Its title states the conclusion. Highlight only the bar
  the finding is about. Add the source line.
- **One customer quote** that makes finding 1 real. Remove names, order numbers, emails, phone numbers.
- **Follow-up offer** and footnote: keep as in the template.

Delete a block if there is no data for it. Do not add blocks. Keep generous white space.
Design rules: no border wider than 1px, no small label above a heading, no extra colors.

Writing: short sentences, active voice, plain words, no jargon. Each sentence says one thing.
Do not use em dashes.

## 5. Check before you deliver

- Each number on the page exists in the step 2 output.
- Each page fits on one printed Letter page.
- The three pages do not repeat the same three findings. Shared causes are fine; the angle and next step differ.

## 6. Deliver

Make each page a separate HTML artifact:
- **Claude:** an HTML artifact per team (in Claude Code: an .html file per team).
- **ChatGPT:** a canvas per team, or save `.html` files with your code tool and give download links.
- **Gemini:** a Canvas per team. Otherwise, give each page as one complete HTML code block.

Then reply in chat with one line per team (its action title) and this offer:
"Want more detail? Ask for a detailed report on any finding or topic." Do not make detailed reports
until the user asks.

## Detailed report (only on request)

When the user asks for detail on a finding or topic, make one new HTML file with the same `<style>`
from `template.html`. Use `.page` blocks for pages and `.section`, `table` and the bar rows inside them:

1. Action title and meta line.
2. Summary: 3 short bullets.
3. What we see: 2 or 3 exhibits, each with a conclusion title and a source line.
4. Why it happens: root causes, with ticket quotes and counts.
5. Options: a table with option, impact, effort and risk.
6. Recommended next steps: a table with step, owner and timing.
7. Data notes: sources, period, gaps and caveats.

Keep the same rules: real numbers only, 1px rules, white space, no em dashes.
