"""Step 3: parse downloaded discussion pages into JSON / CSV / XLSX / SQLite.

Usage: python3 build_db.py HTML_DIR OUT_DIR [VIEW_PAGE_HTML ...]
VIEW_PAGE_HTML: optional saved /exams/microsoft/pl-300/view/N/ pages; their "Correct Answer"
                (site-suggested answer) is merged in when present.
"""
import csv, html, json, os, re, sqlite3, sys
from collections import Counter
from bs4 import BeautifulSoup

TITLE = re.compile(r"Exam PL-300 topic (\d+) question (\d+) discussion", re.I)


def clean(t):
    t = html.unescape(html.unescape(t or ""))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def body_to_text(node):
    """Question HTML -> text, images replaced by [IMG:url]."""
    for img in node.find_all("img"):
        img.replace_with(f"\n[IMG:{img.get('src')}]\n")
    for br in node.find_all("br"):
        br.replace_with("\n")
    return clean(node.get_text())


def upvotes(c):
    u = c.select_one(".upvote-count")
    if not u:
        return 0
    m = re.search(r"(\d+)", u.get_text())
    return int(m.group(1)) if m else 0


def qtype(text):
    t = text[:400].upper()
    if "HOTSPOT" in t or "HOT SPOT" in t:
        return "HOTSPOT"
    if "DRAG DROP" in t or "DRAG AND DROP" in t:
        return "DRAG DROP"
    if "THIS QUESTION IS PART OF A SERIES" in t or "NOTE: THIS QUESTION IS PART OF A SERIES" in t:
        return "SERIES (Yes/No)"
    if "CASE STUDY" in t or "CASE STUDY" in text.upper()[:2000]:
        return "CASE STUDY"
    return "MULTIPLE CHOICE"


def canonical(s, did):
    for a in s.find_all("form", action=True):
        if "/discussions/microsoft/view/" in a["action"]:
            return a["action"].split("#")[0]
    return f"https://www.examtopics.com/discussions/microsoft/view/{did}/"


def parse_discussion(path):
    s = BeautifulSoup(open(path, encoding="utf-8", errors="replace").read(), "lxml")
    h1 = s.select_one(".discussion-list-header h1")
    m = TITLE.search(h1.get_text() if h1 else "")
    if not m:
        return None
    topic, qno = int(m.group(1)), int(m.group(2))
    did = int(re.search(r"(\d+)\.html$", path).group(1))
    qb = s.select_one(".discussion-header-container .question-body")
    qid = qb.get("data-id") if qb else None
    p = qb.select_one("p.card-text") if qb else None
    raw = body_to_text(p) if p else ""
    # split options "A. ..." that ExamTopics appends at the end of the body
    options = {}
    parts = re.split(r"\n([A-H])\.\s*\n?", "\n" + raw)
    stem = parts[0].strip()
    if len(parts) > 1:
        for i in range(1, len(parts) - 1, 2):
            options[parts[i]] = parts[i + 1].strip()
    images = re.findall(r"\[IMG:([^\]]+)\]", raw)
    by = s.select_one(".discussion-header-container .fa-user-o")
    posted = None
    if by:
        it = by.find_parent("div").find("i", string=True)
        posted = it.get_text(strip=True) if it else None

    comments = []
    for c in s.select(".comment-container"):
        ml = re.search(r"margin-left:(\d+)px", c.get("style") or "")
        sel = c.select_one(".comment-body > .badge-warning, .badge-warning")
        sel_ans = None
        if sel and "Selected Answer" in sel.get_text():
            sel_ans = sel.get_text().split(":", 1)[1].strip()
        content = c.select_one(".comment-content")
        user = c.select_one(".comment-username")
        date = c.select_one(".comment-date")
        badges = [b.get_text(" ", strip=True) for b in c.select(".comment-username ~ .badge")]
        comments.append({
            "comment_id": int(c.get("data-comment-id")),
            "level": int(ml.group(1)) // 20 if ml else 0,
            "user": user.get_text(strip=True) if user else "",
            "date": date.get("title") if date else "",
            "selected_answer": sel_ans,
            "upvotes": upvotes(c),
            "highly_voted": any("Highly Voted" in b for b in badges),
            "content": clean(content.get_text("\n") if content else ""),
        })
    # community vote: each voting comment = 1 + its upvotes (ExamTopics' own rule)
    tally = Counter()
    for c in comments:
        if c["selected_answer"]:
            tally[c["selected_answer"]] += 1 + c["upvotes"]
    total = sum(tally.values())
    dist = ", ".join(f"{k} {round(v * 100 / total)}%" for k, v in tally.most_common()) if total else ""
    top = sorted([c for c in comments if c["content"]], key=lambda c: -c["upvotes"])[:3]
    return {
        "key": f"T{topic}-Q{qno:03d}",
        "topic": topic,
        "question_no": qno,
        "discussion_id": did,
        "question_id": qid,
        "url": canonical(s, did),
        "question_type": qtype(stem),
        "question": stem,
        "options": options,
        "images": images,
        "suggested_answer": None,
        "community_answer": tally.most_common(1)[0][0] if tally else None,
        "vote_distribution": dist,
        "vote_total": total,
        "num_comments": len(comments),
        "top_comments": [{"user": c["user"], "upvotes": c["upvotes"], "selected": c["selected_answer"],
                          "text": c["content"]} for c in top],
        "posted": posted,
        "_comments": comments,
    }


def parse_view_pages(paths):
    """Site-suggested answers from /view/N/ pages (question_id -> answer text or image)."""
    ans = {}
    for p in paths:
        s = BeautifulSoup(open(p, encoding="utf-8").read(), "lxml")
        for card in s.select(".exam-question-card"):
            qb = card.select_one(".question-body")
            box = card.select_one(".question-answer")
            if not qb or not box:
                continue
            strong = box.select("strong")
            a = None
            for st in strong:
                if "ml-1" in (st.get("class") or []):
                    img = st.find("img")
                    a = f"[IMG:{img['src']}]" if img else st.get_text(strip=True)
            desc = box.select_one(".answer-description")
            lab = card.select_one("span[id^=qLabel]")
            m = TITLE.search(lab.get_text() if lab else "")
            if not m:
                continue
            ans[f"T{int(m.group(1))}-Q{int(m.group(2)):03d}"] = (a, body_to_text(desc) if desc else "")
    return ans


def main():
    src, out = sys.argv[1], sys.argv[2]
    views = parse_view_pages(sys.argv[3:])
    os.makedirs(out, exist_ok=True)
    recs = {}
    for f in sorted(os.listdir(src)):
        if not f.endswith(".html"):
            continue
        r = parse_discussion(os.path.join(src, f))
        if not r:
            continue
        if r["key"] in views:
            r["suggested_answer"], r["suggested_explanation"] = views[r["key"]]
        # duplicates: keep the thread with the most votes/comments
        old = recs.get(r["key"])
        if not old or (r["vote_total"], r["num_comments"]) > (old["vote_total"], old["num_comments"]):
            if old:
                r.setdefault("duplicate_discussions", []).append(old["discussion_id"])
            recs[r["key"]] = r
        else:
            old.setdefault("duplicate_discussions", []).append(r["discussion_id"])
    rows = sorted(recs.values(), key=lambda r: (r["topic"], r["question_no"]))
    print("questions:", len(rows))

    # JSON (without the full comment list)
    json.dump([{k: v for k, v in r.items() if k != "_comments"} for r in rows],
              open(os.path.join(out, "pl300_questions.json"), "w"), ensure_ascii=False, indent=1)

    cols = ["key", "topic", "question_no", "question_type", "question", "A", "B", "C", "D", "E", "F",
            "suggested_answer", "community_answer", "vote_distribution", "vote_total", "num_comments",
            "top_comment_1", "top_comment_2", "top_comment_3", "images", "url"]

    def flat(r):
        d = {k: r.get(k) for k in cols}
        for L in "ABCDEF":
            d[L] = r["options"].get(L, "")
        for i in range(3):
            tc = r["top_comments"][i] if i < len(r["top_comments"]) else None
            d[f"top_comment_{i+1}"] = (f"[{tc['upvotes']} upvotes | {tc['user']} | selected {tc['selected']}] {tc['text']}"
                                       if tc else "")
        d["images"] = "\n".join(r["images"])
        return d

    flats = [flat(r) for r in rows]
    with open(os.path.join(out, "pl300_questions.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        w.writerows(flats)

    db = os.path.join(out, "pl300.db")
    if os.path.exists(db):
        os.remove(db)
    con = sqlite3.connect(db)
    con.execute("""CREATE TABLE questions(key TEXT PRIMARY KEY, topic INT, question_no INT, question_type TEXT,
        question TEXT, options_json TEXT, images TEXT, suggested_answer TEXT, community_answer TEXT,
        vote_distribution TEXT, vote_total INT, num_comments INT, url TEXT, discussion_id INT,
        domain TEXT, subtopic TEXT, notes_ja TEXT)""")
    con.execute("""CREATE TABLE comments(comment_id INT PRIMARY KEY, question_key TEXT, level INT, user TEXT,
        date TEXT, selected_answer TEXT, upvotes INT, highly_voted INT, content TEXT)""")
    for r in rows:
        con.execute("INSERT INTO questions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL,NULL,NULL)",
                    (r["key"], r["topic"], r["question_no"], r["question_type"], r["question"],
                     json.dumps(r["options"], ensure_ascii=False), "\n".join(r["images"]),
                     r["suggested_answer"], r["community_answer"], r["vote_distribution"], r["vote_total"],
                     r["num_comments"], r["url"], r["discussion_id"]))
        for c in r["_comments"]:
            con.execute("INSERT OR IGNORE INTO comments VALUES(?,?,?,?,?,?,?,?,?)",
                        (c["comment_id"], r["key"], c["level"], c["user"], c["date"], c["selected_answer"],
                         c["upvotes"], int(c["highly_voted"]), c["content"]))
    con.commit()
    con.close()
    print("wrote", out)


if __name__ == "__main__":
    main()
