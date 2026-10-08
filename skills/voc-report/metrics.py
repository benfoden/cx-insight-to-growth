"""Exact metrics for the voc-report skill. Optional: if you cannot run Python, use the formulas in SKILL.md.

Usage:  python3 metrics.py <file or folder> [more files...]   ->  prints JSON

Reads CSV, TSV, JSON, JSONL, MD and TXT. Finds the kind of each file from its columns, so exports
from GA4, Looker Studio, Zendesk, Intercom, Gorgias, Freshdesk or pasted tables all work:
  behavior  sessions + purchases (or conversions / transactions), with any of: date/week, channel, device
  funnel    step + users
  search    search term + searches (exits optional)
  tickets   message / body / description / text / comment
  notes     .md or .txt files
Standard library only. Every number in the report must come from this output (or the SKILL.md formulas).
"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict

ALIAS = {
    "sessions": ["sessions", "visits"], "purchases": ["purchases", "conversions", "transactions", "orders", "ecommerce_purchases"],
    "revenue": ["revenue", "purchase_revenue", "total_revenue"], "date": ["week", "week_start", "date", "day", "created_at", "created", "timestamp"],
    "channel": ["channel", "session_default_channel_group", "default_channel_group", "source_medium", "source"],
    "device": ["device", "device_category"], "step": ["step", "funnel_step", "event_name", "stage_name"], "users": ["users", "active_users", "count"],
    "term": ["search_term", "term", "query", "keyword"], "searches": ["searches", "search_count", "count"], "exits": ["exits", "search_exits"],
    "message": ["message", "body", "description", "text", "comment", "content"], "subject": ["subject", "title"],
    "tags": ["tags", "tag", "category", "topic", "type"], "csat": ["csat", "satisfaction", "satisfaction_rating", "rating", "score"],
    "stage": ["stage", "order_stage", "customer_stage"], "id": ["id", "ticket_id", "number"],
}
STEPS = ["view_item", "add_to_cart", "begin_checkout", "add_shipping_info", "add_payment_info", "purchase"]
POS = {"love": 3, "amazing": 3, "excellent": 3, "best": 2, "great": 2, "perfect": 2, "helpful": 2, "happy": 2, "thanks": 1, "thank": 1, "recommend": 2, "recommending": 2, "easy": 1, "fast": 1}
NEG = {"frustrating": 3, "annoying": 2, "invalid": 1, "failing": 2, "fails": 2, "error": 2, "late": 1, "stuck": 2, "never": 1, "unhappy": 2, "broken": 3,
       "worst": 3, "disappointed": 3, "expensive": 2, "abandoned": 2, "won't": 1, "hasn't": 1, "can't": 1, "slow": 2, "delay": 2, "competitor": 2, "amazon": 1, "missing": 1}
STOP = set("a an and are as at be but by for from i i'm in is it it's its me my of on or so that the this to was we were with you your".split())
REPEAT = {"buy_again": r"\b(buy|order|shop) (here |from you )?again\b|\bnext (purchase|order)\b",
          "recommend": r"\brecommend(ing|ed|s)?\b|\btold (my|a) (friends?|group)\b"}


def col(row, key):
    keys = {k.lower().strip().replace(" ", "_"): k for k in row}
    for a in ALIAS[key]:
        if a in keys:
            return keys[a]


def is_num(v):
    return bool(re.fullmatch(r"\s*-?[\d,.]+\s*%?\s*", str(v)))


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("%", ""))
    except ValueError:
        return 0.0


def read(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".txt"):
        return "notes", open(path, encoding="utf-8", errors="replace").read()
    if ext == ".jsonl":
        rows = [json.loads(l) for l in open(path) if l.strip()]
    elif ext == ".json":
        rows = json.load(open(path))
        rows = rows if isinstance(rows, list) else next((v for v in rows.values() if isinstance(v, list)), [])
    else:
        sample = open(path, encoding="utf-8", errors="replace").read(4096)
        rows = list(csv.DictReader(open(path, encoding="utf-8", errors="replace"), dialect=csv.Sniffer().sniff(sample, ",\t;")))
    if not rows:
        return None, None
    r = rows[0]
    if col(r, "message"):
        return "tickets", rows
    if col(r, "step") and col(r, "users"):
        return "funnel", rows
    if col(r, "term") and col(r, "searches"):
        return "search", rows
    if col(r, "sessions") and col(r, "purchases"):
        return "behavior", rows
    return None, None


def halves(rows, dkey):
    dates = sorted({str(r[dkey])[:10] for r in rows})
    return dates[len(dates) // 2] if len(dates) > 1 else None, (dates[0], dates[-1]) if dates else None


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def behavior(rows):
    r0 = rows[0]
    s, p, rv, d, ch, dev = (col(r0, k) for k in ("sessions", "purchases", "revenue", "date", "channel", "device"))
    out = {"sessions": int(sum(num(r[s]) for r in rows)), "purchases": int(sum(num(r[p]) for r in rows))}
    out["conversion_rate_pct"] = pct(out["purchases"], out["sessions"])
    if rv:
        out["revenue"] = round(sum(num(r[rv]) for r in rows))
    for name, key in (("by_channel", ch), ("by_device", dev)):
        if key:
            g = defaultdict(lambda: [0.0, 0.0])
            for r in rows:
                g[r[key]][0] += num(r[s]); g[r[key]][1] += num(r[p])
            out[name] = sorted(({"name": k, "sessions": int(v[0]), "share_pct": pct(v[0], out["sessions"]), "conversion_rate_pct": pct(v[1], v[0])}
                                for k, v in g.items()), key=lambda x: -x["sessions"])
    if d:
        mid, period = halves(rows, d)
        out["period"] = period
        if mid:
            a = [r for r in rows if str(r[d])[:10] < mid]; b = [r for r in rows if str(r[d])[:10] >= mid]
            ca, cb = pct(sum(num(r[p]) for r in a), sum(num(r[s]) for r in a)), pct(sum(num(r[p]) for r in b), sum(num(r[s]) for r in b))
            out["conversion_first_half_pct"], out["conversion_second_half_pct"], out["split_date"] = ca, cb, mid
    return out


def funnel(rows):
    r0 = rows[0]
    st, u, d, dev = (col(r0, k) for k in ("step", "users", "date", "device"))
    mid = halves(rows, d)[0] if d else None
    tot = defaultdict(lambda: defaultdict(float))
    for r in rows:
        for seg in ("all", r[dev] if dev else None, ("first_half" if str(r[d])[:10] < mid else "second_half") if mid else None):
            if seg:
                tot[seg][r[st]] += num(r[u])
    order = [x for x in STEPS if x in tot["all"]] + [x for x in tot["all"] if x not in STEPS]
    rates = {seg: {b: pct(v[b], v[a]) for a, b in zip(order, order[1:])} for seg, v in tot.items()}
    out = {"steps": order, "users_all": {k: int(v) for k, v in tot["all"].items()}, "step_through_pct": rates,
           "note": "step_through_pct[segment][step] = % of users at the previous step who reach this step"}
    if "first_half" in rates:
        ch = {k: round(rates["second_half"][k] - rates["first_half"][k], 1) for k in rates["all"] if rates["first_half"].get(k) is not None}
        out["biggest_drop_vs_first_half"] = min(ch.items(), key=lambda x: x[1]) if ch else None
        out["split_date"] = mid
    if "mobile" in rates and "desktop" in rates:
        gap = {k: round(rates["desktop"][k] - rates["mobile"][k], 1) for k in rates["all"]}
        out["biggest_mobile_gap"] = max(gap.items(), key=lambda x: x[1])
    return out


def search(rows):
    r0 = rows[0]
    t, n, x = (col(r0, k) for k in ("term", "searches", "exits"))
    res = [{"term": r[t], "searches": int(num(r[n])), "exit_rate_pct": pct(num(r[x]), num(r[n])) if x else None} for r in rows]
    return sorted(res, key=lambda r: -r["searches"])[:10]


def sentiment(text):
    w = re.findall(r"[a-z']+", text.lower())
    score = sum(POS.get(t, 0) - NEG.get(t, 0) for t in w)
    if re.search(r"\bnot (great|good|happy|helpful|paying)\b|more than i expected|would have been nice|gave up", text.lower()):
        score -= 3
    return "positive" if score >= 2 else "negative" if score <= -2 else "neutral"


def phrases(texts, ids, top=12):
    """Word groups (2 to 6 words, inside one sentence) in 2 or more tickets, longest form kept.
    Also returns capitalized names (products, places) in 2 or more tickets, kept out of the phrases."""
    seen, named = defaultdict(set), defaultdict(set)
    for t, tid in zip(texts, ids):
        for m in re.findall(r"\b[A-Z][a-z0-9]+(?: (?:[A-Z][a-z0-9]+|\d+))+", t):
            w = m.lower().split()
            while w and w[0] in STOP:
                w.pop(0)
            if len(w) > 1:
                named[" ".join(w)].add(tid)
        for part in re.split(r"[.!?;:,()]+", t):
            w = re.findall(r"[a-z0-9']+", part.lower())
            for n in range(2, 7):
                for k in range(len(w) - n + 1):
                    g = w[k:k + n]
                    if g[0] not in STOP and g[-1] not in STOP:
                        seen[" ".join(g)].add(tid)
    names = [n for n in named if len(named[n]) >= 2]
    hits = {g: ids for g, ids in seen.items() if len(ids) >= 2 and not any(g in n for n in names)}
    keep = [g for g, i in hits.items() if not any(g != h and f" {g} " in f" {h} " and hits[h] == i for h in hits)]
    keep.sort(key=lambda g: (-len(hits[g]), -len(g)))
    return ([{"phrase": g, "tickets": len(hits[g]), "ticket_ids": sorted(hits[g])} for g in keep[:top]],
            sorted(({"name": n, "tickets": len(named[n])} for n in names), key=lambda x: -x["tickets"]))


def praise(rows, m, sb, tg, cs, d):
    """Positive tickets: praise tags, or positive wording with no question in it."""
    pos = [r for r in rows if r["_tag"] in ("praise", "compliment", "positive", "feedback-positive")
           or (r["_sent"] == "positive" and "?" not in str(r[m]))]
    if not pos:
        return None
    text = [str(r[m]) for r in pos]
    ph, named = phrases(text, [r["_id"] for r in pos])
    out = {"count": len(pos), "share_pct": pct(len(pos), len(rows)), "phrases": ph, "named_most": named,
           "repeat_signals": {k: {"tickets": len(i), "ticket_ids": i} for k, rx in REPEAT.items()
                              for i in [[r["_id"] for r, t in zip(pos, text) if re.search(rx, t.lower())]]},
           "quotes": [{"id": r["_id"], "text": str(r[m]), "date": str(r[d])[:10] if d else None}
                      for r in sorted(pos, key=lambda r: -len(str(r[m])))[:8]],
           "note": "phrases = exact word groups from positive tickets; ticket_ids let you check each one. named_most = products or names praised most"}
    c = [num(r[cs]) for r in pos if cs and is_num(r.get(cs))]
    out["csat_avg"] = round(sum(c) / len(c), 2) if c else None
    return out


def tickets(rows):
    r0 = rows[0]
    m, sb, tg, cs, d, stg, i = (col(r0, k) for k in ("message", "subject", "tags", "csat", "date", "stage", "id"))
    mid, period = halves(rows, d) if d else (None, None)
    g = defaultdict(list)
    for n, r in enumerate(rows):
        raw = r.get(tg) if tg else None
        tags = [str(x).strip() for x in raw] if isinstance(raw, list) else [x.strip() for x in re.split(r"[;,|]", str(raw or "")) if x.strip()]
        r["_tag"] = tags[0].lower() if tags else "(untagged)"
        r["_sent"] = sentiment(f"{r.get(sb, '') if sb else ''} {r[m]}")
        r["_id"] = str(r[i]) if i else f"row{n + 1}"
        g[r["_tag"]].append(r)
    for r in rows:  # nested ratings, e.g. Zendesk {"score": "good"}
        if cs and isinstance(r.get(cs), dict):
            r[cs] = r[cs].get("score", "")
        if cs and str(r.get(cs)).lower() in ("good", "bad"):
            r[cs] = 5 if str(r[cs]).lower() == "good" else 1
    csat = [num(r[cs]) for r in rows if cs and is_num(r.get(cs))]
    out = {"count": len(rows), "period": period, "csat_avg": round(sum(csat) / len(csat), 2) if csat else None,
           "sentiment_pct": {k: pct(v, len(rows)) for k, v in Counter(r["_sent"] for r in rows).items()}}
    if stg:
        pre = sum(str(r.get(stg)).lower() in ("pre_purchase", "checkout", "presale", "pre-sale", "prospect") for r in rows)
        out["pre_purchase_pct"] = pct(pre, len(rows))
    out["by_tag"] = []
    for tag, rs in sorted(g.items(), key=lambda x: -len(x[1])):
        c = [num(r[cs]) for r in rs if cs and is_num(r.get(cs))]
        a = sum(str(r[d])[:10] < mid for r in rs) if mid else None
        out["by_tag"].append({"tag": tag, "count": len(rs), "share_pct": pct(len(rs), len(rows)),
                              "negative_pct": pct(sum(r["_sent"] == "negative" for r in rs), len(rs)),
                              "csat_avg": round(sum(c) / len(c), 2) if c else None,
                              "first_half": a, "second_half": len(rs) - a if a is not None else None,
                              "positive_pct": pct(sum(r["_sent"] == "positive" for r in rs), len(rs)),
                              "ticket_ids": [r["_id"] for r in rs][:40]})
    out["praise"] = praise(rows, m, sb, tg, cs, d)
    return out


def main(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(os.path.join(p, "*"))) if os.path.isdir(p) else [p]
    out = {"files": {}}
    for f in files:
        try:
            kind, data = read(f)
        except Exception as e:  # unreadable file: report it, keep going
            out["files"][os.path.basename(f)] = f"skipped: {e}"
            continue
        if not kind:
            out["files"][os.path.basename(f)] = "skipped: unknown columns"
            continue
        out["files"][os.path.basename(f)] = kind
        out[kind] = data if kind == "notes" else {"behavior": behavior, "funnel": funnel, "search": search, "tickets": tickets}[kind](data)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:] or ["sample-data"])
