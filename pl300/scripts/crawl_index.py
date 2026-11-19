"""Step 1: walk ExamTopics' public Microsoft discussion listing and collect PL-300 discussion URLs.

Usage: python3 crawl_index.py OUT_DIR [START_PAGE] [END_PAGE]
Resumable: progress is stored in OUT_DIR/index_progress.json, links in OUT_DIR/pl300_links.tsv
"""
import json, os, re, sys, time, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
BASE = "https://www.examtopics.com/discussions/microsoft/{}/"
LINK = re.compile(r'href="(https://www\.examtopics\.com/discussions/microsoft/view/(\d+)-exam-pl-300-topic-(\d+)-question-(\d+)-discussion/)"')


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            wait = 5 * (i + 1)
            print(f"  retry {url}: {e} (sleep {wait}s)", flush=True)
            time.sleep(wait)
    raise RuntimeError(url)


def main():
    out = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else None
    os.makedirs(out, exist_ok=True)
    prog_f = os.path.join(out, "index_progress.json")
    links_f = os.path.join(out, "pl300_links.tsv")
    done = set(json.load(open(prog_f))) if os.path.exists(prog_f) else set()
    seen = set()
    if os.path.exists(links_f):
        seen = {l.split("\t")[0] for l in open(links_f)}
    if end is None:
        h = get(BASE.format(1))
        end = max(int(x) for x in re.findall(r'<option value="(\d+)"', h))
        print("last page", end, flush=True)
    for p in range(start, end + 1):
        if p in done:
            continue
        h = get(BASE.format(p))
        new = 0
        with open(links_f, "a") as f:
            for url, did, topic, q in LINK.findall(h):
                if url not in seen:
                    seen.add(url)
                    f.write(f"{url}\t{did}\t{topic}\t{q}\n")
                    new += 1
        done.add(p)
        if p % 10 == 0 or new:
            json.dump(sorted(done), open(prog_f, "w"))
            print(f"page {p}/{end}: +{new} (total {len(seen)})", flush=True)
        time.sleep(1.0)
    json.dump(sorted(done), open(prog_f, "w"))
    print("DONE", len(seen), flush=True)


if __name__ == "__main__":
    main()
