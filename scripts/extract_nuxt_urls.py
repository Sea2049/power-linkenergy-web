# -*- coding: utf-8 -*-
import re, requests
r = requests.get('https://www.santak.com.cn/product/list', headers={'User-Agent':'Mozilla/5.0'}, timeout=30)
print('len', len(r.text))
for pat in [r'window\.__NUXT__', r'__NUXT__', r'osscn\.santak']:
    print(pat, 'count', len(re.findall(pat, r.text)))
# show context around __NUXT__
idx = r.text.find('__NUXT__')
print('idx', idx)
if idx >= 0:
    print(r.text[idx:idx+200])
