import nltk
import glob
import os
import sqlite3
import pandas as pd

from lxml import etree


parser = etree.HTMLParser()

paragraphs_lst = []

for file_name in glob.glob("./annuals/*.txt",recursive=False):
    company_name = os.path.basename(file_name).split("_")[1]
    year = os.path.basename(file_name).split("_")[0]
    print(company_name)
    f = etree.parse(file_name,parser)
    pages = f.xpath("//div[@style='page-break-before:always; page-break-after:always']")



    for nr,page in enumerate(pages):
        paragraphs = page.xpath('.//p//text()')
        for paragraph in paragraphs:
            paragraph = str(paragraph).strip()
            if paragraph != "":
                paragraphs_lst.append([company_name, year, nr, paragraph])


conn = sqlite3.connect('paragraphs.db')
df = pd.DataFrame(paragraphs_lst, columns=["company","year","page_nr","paragraph"])

df.to_sql("paragraph",conn)

df = pd.read_sql("Select * from paragraph",conn)
df.head()