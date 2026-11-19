"""Step 2: download every PL-300 discussion page found by crawl_index.py.

Usage: python3 fetch_discussions.py HTML_OUT_DIR LINKS_TSV [LINKS_TSV ...]
Files already downloaded are skipped (resumable).
"""
import os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch(job):
    url, path = job
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return "skip"
    for i in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
            time.sleep(0.5)
            return "ok"
        except Exception as e:  # noqa: BLE001
            print("retry", url, e, flush=True)
            time.sleep(5 * (i + 1))
    return "fail"


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    jobs = {}
    for tsv in sys.argv[2:]:
        for line in open(tsv):
            url, did, topic, q = line.rstrip("\n").split("\t")
            jobs[did] = (url, os.path.join(out, f"{did}.html"))
    print("discussions:", len(jobs), flush=True)
    n = 0
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(fetch, jobs.values()):
            n += 1
            if n % 25 == 0:
                print(n, res, flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
