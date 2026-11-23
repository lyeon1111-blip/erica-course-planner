#!/usr/bin/env python3
"""present.html(아티팩트용 조각)을 깃허브 페이지에서 그대로 열리는 index.html로 감싼다.
아티팩트는 발행할 때 스켈레톤을 붙여 주지만, 깃허브 페이지는 파일을 날것으로 주기 때문에
여기서 doctype·head·기본 리셋을 직접 넣어야 똑같이 보인다."""
import re, pathlib, sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/haksa/present.html')
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'index.html')
frag = SRC.read_text(encoding='utf-8')

title = (re.search(r'<title>(.*?)</title>', frag, re.S) or [None, '수강신청 전 한 화면'])[1].strip()
desc  = '수강신청 전 에타와 헤이영을 번갈아 보는 구간을 한 화면으로 — 한양대 ERICA 학사 정보 서비스'

# 조각에서 head로 올려야 하는 것들을 뽑아낸다
head_bits = []
for pat in (r'<title>.*?</title>', r'<meta[^>]*>', r'<link[^>]*>'):
    for m in re.findall(pat, frag, re.S):
        head_bits.append(m)
        frag = frag.replace(m, '', 1)
frag = frag.lstrip('\n')

RESET = """<style>
/* 아티팩트 런타임이 넣어 주던 기본값을 그대로 재현 */
:root{color-scheme:light;
  padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font-size:14px;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>"""

html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{chr(10).join(head_bits)}
{RESET}
</head>
<body>
{frag}
</body>
</html>
"""
OUT.write_text(html, encoding='utf-8')
print(f'{OUT}  {len(html):,} bytes  (title: {title})')
