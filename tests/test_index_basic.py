from pysearch.indexer import build_index

def test_basic_indexer():
  docs = ((0, "He ate an apple"), (1, "She was amazed by the apple!"))
  index, docstore = build_index(docs)
  assert index == {"he" : {0: 1}, "ate" : {0: 1}, "an" : {0: 1}, "apple" : {0: 1, 1: 1}, \
    "she" : {1: 1}, "was" : {1: 1}, "amazed" : {1: 1}, "by" : {1: 1}, "the" : {1: 1}}
  assert index["apple"] == {0: 1, 1: 1}
  assert docstore[0]["length"] == 4
  
if __name__ == "__main__":
  test_basic_indexer()