# -*- coding: utf-8 -*-
"""Копия блокнота ml_users 2чекпоинт.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Niw7_v-jJIkp-gqKLBYZX9DortT21bu9
"""

!pip install fuzzywuzzy
!pip install rapidfuzz
import pandas as pd
from rapidfuzz import fuzz, process

pd.set_option('display.max_columns', 30)

# df = pd.read_csv('main1.csv',skipinitialspace=True, nrows = 1_000)
# df2 = pd.read_csv('main2.csv',skipinitialspace=True, nrows = 1_000)
# df3 = pd.read_csv('main3.csv',skipinitialspace=True, nrows = 1_000)

df1 = pd.read_csv('main1.csv',skipinitialspace=True)

df2 = pd.read_csv('main2.csv',skipinitialspace=True)

df3 = pd.read_csv('main3.csv',skipinitialspace=True)

df1 = df1.applymap(lambda s: s.lower() if type(s) == str else s)
df2 = df2.applymap(lambda s: s.lower() if type(s) == str else s)
df3 = df3.applymap(lambda s: s.lower() if type(s) == str else s)

df3

# count = 80
# go = -1
# end = 0
# for i in df2['first_name'] + ' ' + df2['middle_name'] + ' ' + df2['last_name'] :
#   go+=1
#   for j in df['full_name']:
#      name_similarity = fuzz.WRatio(i , j)
#      name_similarity2 = fuzz.token_sort_ratio(i , j)
#      name_similarity_all = (name_similarity2 + name_similarity) / 2
#      if name_similarity_all >= count:
#         df_full_concat = pd.concat([
#             df.iloc[end],
#             df2.iloc[go]
#         ],axis = 1)
#         #  print(df_full_concat)
#         end+=1

count = 70
results = []

df2_full_names = df2['first_name'] + ' ' + df2['middle_name'] + ' ' + df2['last_name']
df3_full_names = df3['name']

for go, i in enumerate(df2_full_names):

    matches_df = process.extract(i, df1['full_name'], scorer=fuzz.WRatio, limit=2)


    for match_df in matches_df:
        j = match_df[0]
        name_similarity = match_df[1]
        name_similarity2 = fuzz.token_sort_ratio(i, j)
        name_similarity_all = (name_similarity2 + name_similarity) / 2


        if name_similarity_all >= count:

            matches_df3 = process.extract(i, df3_full_names, scorer=fuzz.WRatio, limit=2)


            for match_df3 in matches_df3:
                k = match_df3[0]
                name_similarity3 = match_df3[1]
                name_similarity4 = fuzz.token_sort_ratio(i, k)
                name_similarity_all3 = (name_similarity3 + name_similarity4) / 2

                if name_similarity_all3 >= count:
                    results.append(pd.concat([
                        df1.loc[df['full_name'] == j],
                        df2.iloc[[go]],
                        df3.loc[df3['name'] == k]
                    ], axis=1))


if results:
    df_full_concat = pd.concat(results, ignore_index=True)

df_full_concat

count = 75
result_fuzzy = []


full_names = df_full_concat['full_name']

for i, name_i in enumerate(full_names):
    matches = process.extract(name_i, full_names, scorer=fuzz.WRatio, limit=5)
    for match in matches:
        name_j = match[0]
        name_similarity = match[1]

        if name_similarity >= count and name_i != name_j:
            result_fuzzy.append({
                'name_1': name_i,
                'name_2': name_j,
                'similarity': name_similarity
            })

if result_fuzzy:
    result_fuzzy_df = pd.DataFrame(result_fuzzy)
else:
    result_fuzzy_df = pd.DataFrame(columns=['name_1', 'name_2', 'similarity'])

result_fuzzy_df.to_csv('result_fuzzy.csv', index=False)

result_fuzzy_df

# df_full_concat['index'] = 1
# df_full_concat = df_full_concat.drop(columns = 'index')
# df_full_concat
