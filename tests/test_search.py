from pysearch.searcher import doc_searcher
from pysearch.indexer import build_index


def test_search():
  docs = ((0, "He ate an apple"), (1, "She was amazed by the apple apple!"))
  index, docstore = build_index(docs)
  ranking = doc_searcher(index, docstore, "apple")
  assert ranking == [1, 0], f"got {ranking}"
  ranking = doc_searcher(index, docstore, "he")
  assert ranking == [0], f"got {ranking}"
  ranking = doc_searcher(index, docstore, "banana")
  assert ranking == [], f"got {ranking}"


if __name__ == "__main__":
  test_search()