import spacy
import pandas as pd
import random


def get_meaningful_subcomponents_v4(sentence):
  """
  Estrae sottocomponenti significativi da una frase in inglese (versione 4).
  Esclude singole parole, combinazioni articolo/possessivo + nome comune,
  e ora anche nomi propri singoli o preceduti da articolo/possessivo.
  """
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(sentence)
  subcomponents = set()

  for chunk in doc.noun_chunks:
    cleaned_chunk = chunk.text.strip('“"\'”')
    # Escludi i chunk di una sola parola
    if len(cleaned_chunk.split()) == 1:
      continue
    # Escludi i chunk che sono solo articolo + nome comune
    if len(chunk) == 2 and chunk[0].dep_ == "det" and chunk[1].pos_ == "NOUN":
      continue
    # Escludi i chunk di due parole con un possessivo + nome comune
    if len(chunk) == 2 and chunk[0].dep_ == "poss" and chunk[1].pos_ == "NOUN":
      continue

    # Escludi i chunk che sono solo nomi propri (uno o più)
    if all(token.pos_ == "PROPN" for token in chunk):
      continue

    # Escludi i chunk di due parole con articolo/possessivo + nome proprio
    if len(chunk) == 2 and chunk[1].pos_ == "PROPN" and chunk[0].dep_ in ["det", "poss"]:
      continue

    subcomponents.add(chunk.text)

  # Estrazione di "pezzi di frase" (gestione delle similarità mantenuta)
  phrase_pieces = set()
  for token in doc:
    if token.dep_ in ["appos", "advcl", "acl", "relcl"] or token.dep_.startswith("prep"):
      phrase_pieces.add(doc[token.head.i:].text)
    elif token.dep_ == "mark" and token.head.dep_ == "advcl":
      phrase_pieces.add(doc[token.head.i:].text)
    elif token.text == "such" and len(list(token.rights)) > 0 and list(token.rights)[0].dep_ == "amod":
      phrase_pieces.add(doc[token.i:].text)

  # Aggiungi un campione casuale dei "pezzi di frase"
  if phrase_pieces:
    subcomponents.add(random.choice(list(phrase_pieces)))

  return list(subcomponents)

def create_simplified_translation_dataset_v4(text):
  """
  Crea un dataset raffinato di "sotto-frasi significative" (versione 4) e coppie (contesto, frase target).
  """
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(text)
  sentences = [sent.text for sent in doc.sents]
  dataset = []

  for i, target_sentence in enumerate(sentences):
    sub_sentences = get_meaningful_subcomponents_v4(target_sentence)
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


with open("This-side-of-paradise.txt", "r") as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    test_book = " ".join(lines)[:6000]
df = create_simplified_translation_dataset_v4(test_book)
df.to_csv("dataset_newapproach.csv", index=False, sep='\t')