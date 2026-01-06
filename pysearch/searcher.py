from pysearch.tokenizer import tokenize
from pysearch.indexer import build_index
from collections import defaultdict
import math

def doc_searcher(index, docstore, query_text, k=10, method="tf"):
  N = len(docstore)
  scores = defaultdict(float)
  query_tokens = set(tokenize(query_text))
  for token in query_tokens:
    if token in index:
      df = len(index[token]) # document frequency
      if method == "tfidf":
        idf = math.log((N + 1) / (df + 1)) + 1
      for doc, tf in index[token].items():
        if method == "tf":
          scores[doc] += tf
        elif method == "tfidf":
          doc_len = docstore[doc]["length"]
          scores[doc] += (tf / doc_len) * idf
        else:
          raise ValueError("Not a known method")
  scores = [key for key, value in sorted(scores.items(), key = lambda item : (item[1], -item[0]), reverse = True)]
  if k < len(scores):
    return scores[:k]
  return scores

def make_snippet(text, query_tokens, window=30):
  lower_text = text.lower()
  min_index = math.inf
  for token in query_tokens:
    index = lower_text.find(token.lower())
    if index != -1:
      min_index = min(index, min_index)
      # min_token = token
  if min_index != math.inf:
    if min_index - window <= 0:
      left = text[: min_index]
    else:
      left = "..." + text[min_index - window: min_index]
    if min_index + window >= len(text) - 1:
      right = text[min_index: ]
    else:
      right = text[min_index: min_index + window] + "..."
    return left + right
  if 2*window >= len(text):
    return text
  else:
    return text[: 2 * window] + "..."
      
def search_with_snippets(index, docstore, query_text, k=10, method="tf", window=30):
  doc_ids = doc_searcher(index, docstore, query_text, k, method=method)
  query_tokens = tokenize(query_text)

  results = []
  for doc_id in doc_ids:
    text = docstore[doc_id]["text"]
    snippet = make_snippet(text, query_tokens)
    results.append({"doc_id" : doc_id, "snippet" : snippet})
  return results