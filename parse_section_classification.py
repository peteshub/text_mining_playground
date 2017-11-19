import pandas as pd
import numpy as np
import sqlite3

df = pd.read_excel('./Notes_Checklist_Sites.xlsx')

df['year'] = df.iloc[:,0].str.extract("(\d{4})",expand=False)

parts = df.iloc[:,0].str.split('_')

df['company'] = parts.str[2]
df.loc[parts.str[3].str[:2]!='en','company'] += " " + parts.str[3]
df.drop(df.columns[0], axis=1, inplace=True)


df = df.melt(id_vars=['company','year'],var_name='section',value_name='pages')

df['start_end'] = np.where(df.loc[:,'section'].str.lower().str.startswith('beg_'),0,1)
df['section'] = df.loc[:,'section'].str.lower().str.replace('end_|beg_','')

df[['pages']] = df[['pages']].applymap(lambda x:  [[int(i) for i in str(x).split('&')]] if type(x)==str else [[x]] if np.isnan(x) else [[int(x)]] ) #if np.isnan(x) else [int(x)]

df.sort_values(by=['company','year','section','start_end'],inplace=True)

df_grouped = (df.groupby(['company','year','section'])['pages']
              .apply(sum)
              .apply(lambda x: zip(*x))
              .apply(list))



df_list = df_grouped.map(lambda x: list(np.arange(i[0],i[1]+1) for i in x)).map(lambda x: [i for sublist in x for i in sublist])

df_pages = pd.DataFrame(df_list.values.tolist())

pd_concat = pd.concat([df_list.reset_index(),df_pages],axis=1)

page_classes = pd_concat.drop(columns=['pages']).melt(['company','year','section'],value_name='page').drop(columns=['variable']).dropna()

page_classes[['page']] = page_classes[['page']].astype(int)


# Write into database

conn = sqlite3.connect('paragraphs.db')

page_classes.to_sql("page_classes",conn,if_exists='replace',index=False)