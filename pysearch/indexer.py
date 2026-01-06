from pysearch.tokenizer import tokenize

def build_index(docs):
  """
  docs: iterable of (doc_id: int, text: str)
  returns: (index, docstore)
  """
  index = {}
  docstore = {}
  for doc in docs:
    doc_id, text = doc
    tokens = tokenize(text)
    token_count = {}
    for token in tokens:
      if token not in token_count:
        token_count[token] = 1
      else:
        token_count[token] += 1
    docstore[doc_id] = {"length" : len(tokens), "unique_length" : len(token_count), "text" : text}
    for token in token_count:
      if token not in index:
        index[token] = {doc_id : token_count[token]}
      else:
        index[token][doc_id] = token_count[token]
  return (index, docstore)

