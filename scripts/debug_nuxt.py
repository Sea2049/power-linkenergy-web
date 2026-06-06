import re, requests
r = requests.get('https://www.santak.com.cn/product/list', headers={'User-Agent':'Mozilla/5.0'}, timeout=30)
samples = re.findall(r'.{0,30}osscn\.santak.{0,80}', r.text)
print('samples', len(samples))
for s in samples[:5]:
    print(repr(s))
