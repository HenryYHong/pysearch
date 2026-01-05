""" Tokenizer v1
- Splits on nonalphanumeric Strings
- Currently keeps single letter chars
"""
def tokenize(tokens): 
  output = "" 
  for char in tokens:  
    if char.isalnum(): 
      output += char.lower()
    else: output += " "
  result = output.split()
  return result
  