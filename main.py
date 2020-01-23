import requests as r
from lxml import html

SITEMAP_URL = "https://www.toy.ru/sitemap_files.xml"
#SITEMAP_URL = "https://www.krasotkapro.ru/sitemap_files.xml"
#SITEMAP_URL = "https://www.drive2.ru/assets/sitemaps/content_27095.xml"

#anti-waf headers
reqHeaders={
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Connection': 'close',
}

resp = r.get(SITEMAP_URL,  headers=reqHeaders).content
tree = html.fromstring(resp)
urls_from_sitemap = tree.xpath('//url/loc/text()')

pages_with_non_200_code = []
pages_with_canonical = []
pages_with_diff_canonical = []

for url in urls_from_sitemap:
    resp_for_url = r.get(url, allow_redirects=False, headers=reqHeaders)
    if resp_for_url.status_code != 200:
        pages_with_non_200_code.append(f"For {url} response code is {resp_for_url.status_code}")
    if resp_for_url.text:
        urls_canonical = html.fromstring(resp_for_url.text).xpath('//link[@rel="canonical"]/@href')
    if urls_canonical:
        for i in urls_canonical:
            pages_with_canonical.append(i)
            if url != i:
                pages_with_diff_canonical.append(f"Canonical link {i} diffs from requested url {url} ")

if not pages_with_diff_canonical:
    print("There are no diffrients or cannonical links.")
else:
    with open('pages_with_diff_canonical.txt', 'w') as file:
        for page in pages_with_diff_canonical:
            file.write("%s\n" % page)

if not pages_with_non_200_code:
    print("There are no pages with non 200 code.")
else:
    with open('pages_with_non_200_code.txt', 'w') as file:
        for page in pages_with_non_200_code:
            file.write("%s\n" % page)
