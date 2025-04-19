import spacy
import textstat


nlp = spacy.load("en_core_web_lg")

COMMON_WORDS_SUBTLEX = set()
with open('common_words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        word = line.strip().lower()
        COMMON_WORDS_SUBTLEX.add(word)
#print(f"Loaded {len(COMMON_WORDS_SUBTLEX)} common words")

def has_rare_words(sentence, common_words=COMMON_WORDS_SUBTLEX):
  doc = nlp(sentence)
  for token in doc:
    lemma = token.lemma_.lower()
    if lemma not in common_words and not token.is_punct and not token.is_space:
      return True
  return False

def is_difficult_readability(sentence, threshold=50):
  try:
    reading_ease = textstat.flesch_reading_ease(sentence)
    return reading_ease < threshold
  except ValueError:
    return False

def get_syntactic_complexity(sentence):
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
  subordinate_marker_deps = ["mark"]

  for token in doc:
    if token.dep_ in subordinate_clause_deps or (token.dep_ == "mark" and token.head.dep_ == "advcl"):
      subordinate_clause_count += 1

  return {"tree_depth": tree_depth, "subordinate_clause_count": subordinate_clause_count}

def is_syntactically_complex(complexity_metrics, depth_threshold=5, clause_threshold=2):
  return complexity_metrics["tree_depth"] > depth_threshold or complexity_metrics["subordinate_clause_count"] > clause_threshold

def keep(piece, sentence):
  if has_rare_words(sentence):
    if is_difficult_readability(sentence) or is_syntactically_complex(get_syntactic_complexity(sentence)):
      return True
    else:
      return has_rare_words(piece)

  else:
    if is_difficult_readability(sentence) or is_syntactically_complex(get_syntactic_complexity(sentence)):
      return len(piece.split()) > 4
    else:
      return False


"""
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
"""