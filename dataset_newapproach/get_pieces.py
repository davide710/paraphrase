import spacy
import pandas as pd
import random


def get_meaningful_subcomponents(sentence):
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(sentence)
  subcomponents = set()

  for chunk in doc.noun_chunks:
    cleaned_chunk = chunk.text.strip('“"\'”')
    if len(cleaned_chunk.split()) == 1:
      continue
    if len(chunk) == 2 and chunk[0].dep_ == "det" and chunk[1].pos_ == "NOUN":
      continue
    if len(chunk) == 2 and chunk[0].dep_ == "poss" and chunk[1].pos_ == "NOUN":
      continue

    if all(token.pos_ == "PROPN" for token in chunk):
      continue

    if len(chunk) == 2 and chunk[1].pos_ == "PROPN" and chunk[0].dep_ in ["det", "poss"]:
      continue

    subcomponents.add(chunk.text)

  phrase_pieces = set()
  for token in doc:
    if token.dep_ in ["appos", "advcl", "acl", "relcl"] or token.dep_.startswith("prep"):
      phrase_pieces.add(doc[token.head.i:].text)
    elif token.dep_ == "mark" and token.head.dep_ == "advcl":
      phrase_pieces.add(doc[token.head.i:].text)
    elif token.text == "such" and len(list(token.rights)) > 0 and list(token.rights)[0].dep_ == "amod":
      phrase_pieces.add(doc[token.i:].text)

  if phrase_pieces:
    subcomponents.add(random.choice(list(phrase_pieces)))

  return list(subcomponents)

def create_simplified_translation_dataset(text):
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(text)
  sentences = [sent.text for sent in doc.sents]
  dataset = []

  for i, target_sentence in enumerate(sentences):
    sub_sentences = get_meaningful_subcomponents(target_sentence)
    for sub_sentence in sub_sentences:
      dataset.append({
          "sub_sentence": sub_sentence,
          "context": None,
          "target_sentence": target_sentence
      })

    previous_sentence = sentences[i - 1] if i > 0 else ""
    next_sentence = sentences[i + 1] if i < len(sentences) - 1 else ""
    context = f"{previous_sentence} {target_sentence} {next_sentence}".strip()

    for item in dataset:
      if item["target_sentence"] == target_sentence:
        item["context"] = context

  return pd.DataFrame(dataset)

"""
with open("This-side-of-paradise.txt", "r") as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    test_book = " ".join(lines)[:6000]
df = create_simplified_translation_dataset(test_book)
df.to_csv("dataset_newapproach.csv", index=False, sep='\t')
"""