"""Compile src/index.src.html (JSX inline) -> index.html (plain JS, no Babel at runtime).
Usage:  python tools/build.py        (needs Node + `npm i -g typescript`, or npx)
"""
import re, shutil, subprocess, sys, tempfile, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "src" / "index.src.html").read_text(encoding="utf-8")
m = re.search(r'<script type="text/babel">(.*?)</script>', src, re.S)
if not m:
    sys.exit("No <script type=\"text/babel\"> block found")
tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / "app.tsx").write_text(m.group(1), encoding="utf-8")
tsc = [shutil.which("tsc")] if shutil.which("tsc") else ["npx", "--yes", "-p", "typescript", "tsc"]
# type errors are expected (untyped JSX); we only need the emitted JS
subprocess.run(tsc + ["--jsx", "react", "--target", "es2020", "--noResolve", "--skipLibCheck",
                      "--outDir", str(tmp / "out"), str(tmp / "app.tsx")], capture_output=True)
js = (tmp / "out" / "app.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
out = src[:m.start()] + "<script>\n" + js + "\n</script>" + src[m.end():]
out = re.sub(r'<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>\n?', "", out)
(root / "index.html").write_text(out, encoding="utf-8")
print("Built index.html", len(out), "bytes")
