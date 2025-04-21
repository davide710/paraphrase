import pandas as pd
import spacy
import textstat
import random

"""
nlp = spacy.load("en_core_web_lg")

COMMON_WORDS_SUBTLEX = set()
with open('common_words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        word = line.strip().lower()
        COMMON_WORDS_SUBTLEX.add(word)

def has_rare_words(sentence, common_words=COMMON_WORDS_SUBTLEX):
  doc = nlp(sentence)
  for token in doc:
    lemma = token.lemma_.lower()
    if lemma not in common_words and not token.is_punct and not token.is_space:
      return True
  return False

d = pd.read_csv('dataset_newapproach.txt', sep='\t')

i = 0
def f(row):
    global i
    i += 1
    if i % 500 == 0:
        print(f"Processed {i} rows")
    if has_rare_words(row['sub_sentence']):
            return True
    else:
        return len(row['sub_sentence'].split()) > 4

d = d[d.apply(f, axis=1)]
print(f"Filtered dataset to {len(d)} rows")
d.to_csv('filtered.txt', sep='\t', index=False)
"""

d = pd.read_csv('filtered.txt', sep='\t')
print(f"Loaded dataset with {len(d)} rows")

filtered_rows = d[d['target_sentence'].apply(lambda x: len(x.split()) < 35)]
sampled_rows = filtered_rows.sample(n=500, random_state=42)
new_rows = sampled_rows.copy()
new_rows['sub_sentence'] = new_rows['target_sentence']

d = pd.concat([d, new_rows], ignore_index=True)

d.drop(columns=['target_sentence'], inplace=True)
d.to_csv('orig.txt', sep='\t', index=False)
print(f"Filtered dataset to {len(d)} rows")
