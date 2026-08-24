import json
import re
import shutil

PAGE = "GeoMiner.html"

html = open(PAGE, encoding="utf-8").read()
records = json.load(open("coltan_polys.json"))

match = re.search(r"const POLYS_RAW = (\[.*?\]);\n", html, re.S)
polys = json.loads(match.group(1))

# guard: the records carry the mine indices they belong to, so if any of
# those already appear in POLYS_RAW this page has been spliced before.
incoming = {rec[0] for rec in records}
existing = [rec for rec in polys if rec[0] in incoming]
if existing:
    print(f"Already spliced — {len(existing)} records for these mines are present.")
    print("Restore GeoMiner.html.backup first if you want to redo it.")
    raise SystemExit

shutil.copy(PAGE, PAGE + ".backup")
print(f"before: {len(polys)}")
polys.extend(records)
print(f"after:  {len(polys)}")

blob = json.dumps(polys, separators=(",", ":"))
html = html[: match.start(1)] + blob + html[match.end(1) :]
open(PAGE, "w", encoding="utf-8").write(html)
print("written")