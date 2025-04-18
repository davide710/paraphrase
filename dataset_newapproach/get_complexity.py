import spacy
import textstat


COMMON_WORDS_SUBTLEX = set()
with open('common_words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        word = line.strip().lower()
        COMMON_WORDS_SUBTLEX.add(word)
print(f"Loaded {len(COMMON_WORDS_SUBTLEX)} common words")

def has_rare_words_v3(sentence, common_words=COMMON_WORDS_SUBTLEX):
  """
  Verifica se una frase contiene almeno una parola (nella sua forma base/lemma)
  non presente nella lista di parole comuni fornita e che non sia punteggiatura o spazio.
  """
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(sentence)
  for token in doc:
    lemma = token.lemma_.lower()
    if lemma not in common_words and not token.is_punct and not token.is_space:
      return True
  return False

def is_difficult_readability(sentence, threshold=50):
  """
  Verifica se una frase è considerata difficile in base al punteggio
  Flesch Reading Ease.
  """
  try:
    reading_ease = textstat.flesch_reading_ease(sentence)
    return reading_ease < threshold
  except ValueError:
    return False

def get_syntactic_complexity(sentence):
  """
  Calcola alcune metriche di complessità sintattica per una frase.

  Args:
    sentence (str): La frase da analizzare.

  Returns:
    dict: Un dizionario contenente la profondità dell'albero delle dipendenze
          e il numero di clausole subordinate.
  """
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(sentence)

  def get_tree_depth(token, depth=1):
    max_depth = depth
    for child in token.children:
      child_depth = get_tree_depth(child, depth + 1)
      if child_depth > max_depth:
        max_depth = child_depth
    return max_depth

  root = [token for token in doc if token.head == token][0]
  tree_depth = get_tree_depth(root)

  subordinate_clause_count = 0
  subordinate_clause_deps = ["advcl", "sbar", "relcl"]
  subordinate_marker_deps = ["mark"] # per le congiunzioni subordinanti

  for token in doc:
    if token.dep_ in subordinate_clause_deps or (token.dep_ == "mark" and token.head.dep_ == "advcl"):
      subordinate_clause_count += 1

  return {"tree_depth": tree_depth, "subordinate_clause_count": subordinate_clause_count}

def is_syntactically_complex(complexity_metrics, depth_threshold=5, clause_threshold=2):
  """
  Verifica se una frase è sintatticamente complessa in base alle metriche calcolate.

  Args:
    complexity_metrics (dict): Il dizionario restituito da get_syntactic_complexity.
    depth_threshold (int): Soglia per la profondità dell'albero.
    clause_threshold (int): Soglia per il numero di clausole subordinate.

  Returns:
    bool: True se la frase è considerata sintatticamente complessa, False altrimenti.
  """
  return complexity_metrics["tree_depth"] > depth_threshold or complexity_metrics["subordinate_clause_count"] > clause_threshold


easy_sentence = "This is a simple sentence."
complex_sentence = "Although the weather was terrible, the team played very well and scored many goals because they were highly motivated."

complexity_easy = get_syntactic_complexity(easy_sentence)
complexity_complex = get_syntactic_complexity(complex_sentence)

print(f"Complessità sintattica per '{easy_sentence}': {complexity_easy}")
print(f"Complessità sintattica per '{complex_sentence}': {complexity_complex}")

difficult_syntax_easy = is_syntactically_complex(complexity_easy)
difficult_syntax_complex = is_syntactically_complex(complexity_complex)

print(f"'{easy_sentence}' is syntactically complex: {difficult_syntax_easy}")
print(f"'{complex_sentence}' is syntactically complex: {difficult_syntax_complex}")