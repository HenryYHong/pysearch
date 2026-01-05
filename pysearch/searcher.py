from pysearch.tokenizer import tokenize
from pysearch.indexer import build_index
from collections import defaultdict

def doc_searcher(index, docstore, query_text, k=10):
  scores = defaultdict(int)
  query_tokens = tokenize(query_text)
  for token in query_tokens:
    if token in index:
      for doc, appearances in index[token].items():
          scores[doc] += appearances
  scores = [key for key, value in sorted(scores.items(), key = lambda item : item[1], reverse = True)]
  if k < len(scores):
    return scores[:k]
  return scores