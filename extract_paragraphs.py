import glob
import os
import sqlite3
import pandas as pd

from lxml import etree


parser = etree.HTMLParser()

paragraphs_lst = []

for file_name in glob.glob("./annuals/*.txt",recursive=False):
    parts = os.path.basename(file_name).split("_")
    company_name = parts[1]
    company_name_2 = parts[2]
    company_name += " " + company_name_2 if company_name_2[:2]!='en' else ""
    year = parts[0]
    print(company_name)
    f = etree.parse(file_name,parser)
    pages = f.xpath("//div[@style='page-break-before:always; page-break-after:always']")

    paragraph_nr = 0

    for nr,page in enumerate(pages):
        paragraphs = page.xpath('.//p//text()')
        for paragraph in paragraphs:
            paragraph = str(paragraph).strip()
            if paragraph != "":
                paragraphs_lst.append([company_name, year, nr+1,paragraph_nr,paragraph])
                paragraph_nr += 1


conn = sqlite3.connect('paragraphs.db')
df = pd.DataFrame(paragraphs_lst, columns=["company","year","page","paragraph_nr","paragraph"])

df.to_sql("paragraph",conn,if_exists='replace',index=False)
