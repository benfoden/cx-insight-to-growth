<!-- voc-report prompt. Paste all of this into any AI chat (or upload it as a file), then add your data. -->

# VoC one-page briefs

You make one HTML page per team (sales, marketing, product) that turns customer data into three
findings and three next steps. Numbers come from calculation. Meaning and wording come from you.
The page template is at the end of this prompt.

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
If the user asks for a demo, use the sample files if you have them. If not, ask the user to download and upload them from https://github.com/benfoden/cx-insight-to-growth/tree/HEAD/skills/voc-report/sample-data

## 2. Calculate

If you have the file `metrics.py` and can run Python, run `python3 metrics.py <files or folder>` and use its JSON output.
If not, calculate with your code tool, or by hand.
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
| Praise | tickets that praise a product or the team (praise tag, or positive words and no question) |
| Phrase count | praise tickets that contain the exact word group |

Every number in a report must come from this step. Round to whole numbers unless the value is under 10.

## 3. Interpret

1. Group tickets into 5 to 8 topics. Start from tags. Read the untagged and catch-all tickets
   ("general", "other"): they often hold a new topic that no tag covers. Name it if 3 or more tickets share it.
2. Read the praise. In the `praise` output (or by hand), find what customers like most: the products
   they name most (`named_most`), the word groups they repeat (`phrases`), and how many say they will
   buy again or recommend you (`repeat_signals`).
3. Join sources. The strongest findings show one cause in two places, for example a topic that rises
   in tickets while a funnel step drops, or a search term with a high exit rate that matches a ticket topic.
4. Pick the 3 findings that matter most for each team:
   - **Sales:** questions and doubts that stop a first purchase, the answer to each, and proof customers give.
   - **Marketing:** channels that convert or waste spend, promises that create friction, the words customers use.
   - **Product:** where the funnel leaks, gaps between devices, defects, and missing information.

   For sales and marketing, at least 1 of the 3 findings is a strength to use, not a problem to fix.
   Base it on the praise. Skip this rule only if there is no praise in the data.
5. Each finding gets one next step: a concrete action that team owns this month.
6. Match doubts to proof (sales). For each top pre-purchase doubt, find praise that answers it. For
   example: "Is it waterproof?" matches "stayed completely dry". If no praise answers a doubt, say so.
7. Find the words gap (marketing). Look for words that customers use often (in praise, tickets or site
   search) but that the site or ads do not use, or a promise the site does not prove.
8. Match the strength to a channel (marketing). Name the best-converting channel for the product or
   message that customers praise most.

## 4. Write each page

Fill in the page template at the end of this prompt. Keep the page to these blocks only, so it stays easy to scan:

- **Action title:** the main message as a full sentence, max 15 words. Not a topic name.
- **Meta line:** team, company, period, sources with counts.
- **3 numbers:** the three numbers this team needs most, each with a short plain label.
- **3 key findings:** headline (max 12 words), one evidence sentence with the numbers, one next step.
- **Exhibit 1:** one bar chart with max 6 rows. Its title states the conclusion. Highlight only the bar
  the finding is about. Add the source line.
- **One customer quote** that makes finding 1 real. Remove names, order numbers, emails, phone numbers.
- **Sales page only: Doubts and proof.** A table with max 3 rows: the shopper doubt (with ticket
  count), the answer to give, and the proof (an exact customer phrase with its ticket count).
- **Marketing page only: In their words.** Max 4 exact phrases from praise, each with its ticket count,
  and one line that names the words gap. These blocks use space: keep each next step to one line.
- **Follow-up offer** and footnote: keep as in the template.

Delete a block if there is no data for it. Do not add blocks. Keep generous white space.
Design rules: no border wider than 1px, no small label above a heading, no extra colors.

Writing: short sentences, active voice, plain words, no jargon. Each sentence says one thing.
Do not use em dashes.

## 5. Check before you deliver

- Each number on the page exists in the step 2 output.
- Each phrase in quotation marks occurs word for word in the data. Each talking point has a count.
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
from the page template. Use `.page` blocks for pages and `.section`, `table` and the bar rows inside them:

1. Action title and meta line.
2. Summary: 3 short bullets.
3. What we see: 2 or 3 exhibits, each with a conclusion title and a source line.
4. Why it happens: root causes, with ticket quotes and counts.
5. Options: a table with option, impact, effort and risk.
6. Recommended next steps: a table with step, owner and timing.
7. Data notes: sources, period, gaps and caveats.

Keep the same rules: real numbers only, 1px rules, white space, no em dashes.

## Page template

Copy this HTML for each page and replace every {{...}}.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{Team}} brief: {{Company}}</title>
<!--
  voc-report template. Replace every {{...}}. Delete any block you have no data for.
  Rules: no border wider than 1px. No label above a heading. Do not add blocks to the one-pager.
  Bar widths: style="width:NN%" where NN = value / largest value in the exhibit x 100.
  Highlight the one bar the exhibit is about with class "bar hl"; leave the rest as "bar".
-->
<style>
  :root {
    --navy: #051c2c; --blue: #2251ff; --ink: #1a1a1a; --mid: #4d4d4d; --soft: #808080;
    --rule: #d9d9d9; --bar: #c7cdd4; --tint: #f5f6f7; --paper: #ffffff;
  }
  @page { size: letter; margin: 0; }
  * { box-sizing: border-box; }
  body { margin: 0; background: #eceef0; color: var(--ink);
         font: 11px/1.55 "Helvetica Neue", Helvetica, Arial, sans-serif;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { width: 8.5in; min-height: 11in; margin: 24px auto; background: var(--paper);
          padding: 0.8in 0.85in 0.7in; display: flex; flex-direction: column; }
  h1 { font: 400 26px/1.25 Georgia, "Times New Roman", serif; color: var(--navy);
       margin: 0 0 10px; max-width: 6in; letter-spacing: -0.01em; }
  .meta { color: var(--soft); font-size: 10px; margin: 0 0 22px; }
  hr { border: 0; border-top: 1px solid var(--rule); margin: 0; }
  .kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; padding: 22px 0 24px; }
  .kpi b { display: block; font: 400 30px/1.1 Georgia, serif; color: var(--navy); }
  .kpi span { display: block; color: var(--mid); margin-top: 6px; max-width: 1.9in; }
  .body { display: grid; grid-template-columns: 1.15fr 1fr; gap: 0.45in; padding-top: 26px; }
  h2 { font-size: 12px; font-weight: 700; color: var(--navy); margin: 0 0 14px; }
  .finding { display: grid; grid-template-columns: 22px 1fr; padding: 0 0 18px; }
  .finding .n { color: var(--blue); font-weight: 700; font-size: 12px; }
  .finding h3 { font-size: 12px; line-height: 1.4; margin: 0 0 4px; color: var(--ink); }
  .finding p { margin: 0 0 4px; color: var(--mid); }
  .finding .next { color: var(--ink); }
  .finding .next b { color: var(--blue); font-weight: 600; }
  .exhibit h2 { font-weight: 400; font-size: 12px; line-height: 1.4; color: var(--ink); }
  .exhibit h2 b { color: var(--navy); }
  .row { display: grid; grid-template-columns: 1.05in 1fr 0.45in; align-items: center; gap: 8px; margin: 0 0 9px; }
  .row .lab { color: var(--mid); text-align: right; font-size: 10px; }
  .row .val { color: var(--ink); font-size: 10px; font-variant-numeric: tabular-nums; }
  .track { height: 10px; }
  .bar { display: block; height: 10px; background: var(--bar); }
  .bar.hl { background: var(--blue); }
  .bar.b2 { background: var(--navy); }
  .pair { grid-template-columns: 1.05in 1fr 0.75in; } .pair .track { height: auto; } .pair .bar { height: 7px; margin: 1px 0; }
  .legend { display: flex; gap: 14px; color: var(--soft); font-size: 9.5px; margin: -6px 0 12px; }
  .legend i { display: inline-block; width: 8px; height: 8px; margin-right: 5px; vertical-align: -1px; }
  .source { color: var(--soft); font-size: 9px; margin: 6px 0 0; }
  blockquote { margin: 28px 0 0; padding: 2px 0 2px 14px; border-left: 1px solid var(--blue);
               font: italic 12px/1.5 Georgia, serif; color: var(--ink); }
  blockquote cite { display: block; font: normal 9.5px/1.4 "Helvetica Neue", Arial, sans-serif; color: var(--soft); margin-top: 6px; }
  .extra { border-top: 1px solid var(--rule); padding-top: 18px; margin-bottom: 14px; }
  .extra td:first-child { width: 30%; } .extra td:nth-child(2) { width: 33%; }
  .proof { font-family: Georgia, serif; font-style: italic; color: var(--ink); }
  .count { color: var(--soft); font-size: 9.5px; white-space: nowrap; }
  .words .count { display: block; margin-top: 2px; }
  .words { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 4px 0 12px; }
  .words b { display: block; font: italic 400 15px/1.3 Georgia, serif; color: var(--navy); }
  .gap { margin: 0; color: var(--mid); }
  .gap b { color: var(--ink); font-weight: 600; }
  .more { margin-top: auto; background: var(--tint); padding: 14px 16px; color: var(--mid); }
  .more b { color: var(--navy); }
  .foot { color: var(--soft); font-size: 9px; padding-top: 10px; }
  /* Detailed follow-up report only (made on request). Same look, more pages, more exhibits. */
  .section { padding: 22px 0 6px; } .section p { max-width: 6.2in; color: var(--mid); }
  table { width: 100%; border-collapse: collapse; font-size: 10.5px; margin: 6px 0 4px; }
  th { text-align: left; font-weight: 700; color: var(--navy); padding: 6px 10px 6px 0; border-bottom: 1px solid var(--navy); }
  td { padding: 8px 10px 8px 0; border-bottom: 1px solid var(--rule); vertical-align: top; }
  @media print { body { background: none; } .page { margin: 0; min-height: 0; height: 11in; overflow: hidden; } .page + .page { break-before: page; } }
  @media screen and (max-width: 820px) { .page { width: auto; min-height: 0; margin: 0; padding: 32px 18px; }
                             .kpis, .body { grid-template-columns: 1fr; } .words { grid-template-columns: 1fr 1fr; } }
</style>
</head>
<body>
<div class="page">

  <!-- Action title: the single most important message for this team, as a full sentence (max 15 words). -->
  <h1>{{Action title}}</h1>
  <p class="meta">{{Team}} brief · {{Company}} · {{Period}} · Sources: {{sources, with counts}}</p>
  <hr>

  <!-- Exactly 3 numbers. Each label says what the number means for this team. -->
  <div class="kpis">
    <div class="kpi"><b>{{value}}</b><span>{{what it means, max 8 words}}</span></div>
    <div class="kpi"><b>{{value}}</b><span>{{what it means}}</span></div>
    <div class="kpi"><b>{{value}}</b><span>{{what it means}}</span></div>
  </div>
  <hr>

  <div class="body">
    <div>
      <h2>Key findings</h2>
      <!-- Exactly 3. Headline max 12 words. Evidence: one sentence with the numbers. Next step: one action this team owns. -->
      <div class="finding"><div class="n">1</div><div>
        <h3>{{Finding headline}}</h3>
        <p>{{Evidence sentence}}</p>
        <p class="next"><b>Next step:</b> {{action}}</p></div></div>
      <div class="finding"><div class="n">2</div><div>
        <h3>{{Finding headline}}</h3>
        <p>{{Evidence sentence}}</p>
        <p class="next"><b>Next step:</b> {{action}}</p></div></div>
      <div class="finding"><div class="n">3</div><div>
        <h3>{{Finding headline}}</h3>
        <p>{{Evidence sentence}}</p>
        <p class="next"><b>Next step:</b> {{action}}</p></div></div>
    </div>

    <div class="exhibit">
      <!-- One exhibit. Its title states the conclusion, not the topic. Max 6 rows. -->
      <h2><b>Exhibit 1:</b> {{Conclusion the chart proves}}</h2>
      <!-- Single series: -->
      <div class="row"><span class="lab">{{label}}</span><span class="track"><span class="bar hl" style="width:100%"></span></span><span class="val">{{value}}</span></div>
      <div class="row"><span class="lab">{{label}}</span><span class="track"><span class="bar" style="width:60%"></span></span><span class="val">{{value}}</span></div>
      <!-- Two series instead (e.g. desktop vs mobile): series A gray "bar", series B navy "bar b2",
           and the one bar the finding is about blue "bar hl". Add the legend, then one pair per row:
      <div class="legend"><span><i style="background:#c7cdd4"></i>{{series A}}</span><span><i style="background:#051c2c"></i>{{series B}}</span></div>
      <div class="row pair"><span class="lab">{{label}}</span><span class="track"><span class="bar" style="width:78%"></span><span class="bar b2" style="width:51%"></span></span><span class="val">{{A}} / {{B}}</span></div>
      -->
      <p class="source">Source: {{data source, period}}</p>

      <!-- One short customer quote that makes finding 1 real. Remove order numbers, names, emails, phone numbers. -->
      <blockquote>{{Quote}}<cite>{{Customer type or topic}}, {{month}}</cite></blockquote>
    </div>
  </div>

  <!-- SALES PAGE ONLY. Doubts and proof: max 3 rows, one short line per cell. Proof is an exact customer phrase with its ticket count.
       If no praise answers a doubt, write "No proof yet" and what to get. Delete this block on other pages. -->
  <div class="extra">
    <h2>Doubts and proof</h2>
    <table>
      <tr><th>Shopper doubt</th><th>Answer to give</th><th>Proof from customers</th></tr>
      <tr><td>{{Doubt in the shopper's words}} <span class="count">{{n}} tickets</span></td><td>{{Answer}}</td><td><span class="proof">“{{exact phrase}}”</span> <span class="count">{{n}} tickets</span></td></tr>
    </table>
  </div>

  <!-- MARKETING PAGE ONLY. In their words: max 4 exact phrases from praise, each with its ticket count,
       then one line that names the words gap. Delete this block on other pages. -->
  <div class="extra">
    <h2>In their words</h2>
    <div class="words">
      <div><b>“{{exact phrase}}”</b><span class="count">{{n}} tickets</span></div>
      <div><b>“{{exact phrase}}”</b><span class="count">{{n}} tickets</span></div>
    </div>
    <p class="gap"><b>Words gap:</b> {{a word customers use that the site or ads do not, with a number}}</p>
  </div>

  <div class="more"><b>Want more detail?</b> Ask for a detailed report on any finding or topic, for example
    "Detailed report on finding 2" or "Deep dive: {{topic}}".</div>
  <p class="foot">Numbers are calculated from the source data. Findings and wording are written by AI: check them before external use.</p>
</div>
</body>
</html>
```
