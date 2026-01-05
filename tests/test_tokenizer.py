from pysearch.tokenizer import tokenize

def test_basic_tokenizer():
  word = "Hello + World"
  assert tokenize(word) == ["hello", "world"]
  word = "What's Up /39,Joe?"
  assert tokenize(word) == ["what", "s", "up", "39", "joe"]


if __name__ == "__main__":
    test_basic_tokenizer()
