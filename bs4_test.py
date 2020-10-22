# -*- encoding: utf-8 -*-
# author: RenAilin
# time: 2020/10/21 21:35

from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

#print(soup.prettify())

print(soup.title)
print(soup.title.name)
print(soup.title.string)
print(soup.title.parent.name)
print(soup.a)
# get a list of string
print(soup.find_all('a'))

print(soup.find(id='link3'))

for link in soup.find_all('a'):
    print(link.get('href'))
    print(link.string)

print(soup.find('p'))
print(soup.select("p > b")[0].string)