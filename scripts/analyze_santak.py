import requests, re
from bs4 import BeautifulSoup

r = requests.get('https://www.santak.com.cn', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
r.encoding = r.apparent_encoding
soup = BeautifulSoup(r.text, 'lxml')
imgs = []
for img in soup.find_all('img'):
    for a in ['src','data-src','data-original']:
        if img.get(a):
            imgs.append((a, img.get(a), len(img.get(a,''))))
print('img tags:', len(imgs))
for x in imgs[:15]:
    print(x)
urls = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp|gif)', r.text, re.I)
print('regex urls:', len(urls))
for u in urls[:15]:
    print(u)
