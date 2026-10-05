"""put the comparison table and a status line into log.html (between the CMP markers)."""
import re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
table = subprocess.run([sys.executable, str(ROOT / "scripts/compare.py"), str(ROOT / "workdir/runs/capella")], capture_output=True, text=True, check=True).stdout
n = int(re.search(r"runs found: (\d+)", table).group(1))
status = sys.argv[1] if len(sys.argv) > 1 else ""
log = ROOT / "log.html"
s = log.read_text()
a, b = s.index("<!--CMP-START-->"), s.index("<!--CMP-END-->")
s = s[: a + len("<!--CMP-START-->")] + "\n" + table + s[b:]
s = re.sub(r"<li>status: .*?</li>", f"<li>status: {n} of 54 runs finished (21 dfs-lightgbm, 21 tabpfn-rel, 12 rdb-pfn). {status}</li>", s, count=1)
log.write_text(s)
print(n)
