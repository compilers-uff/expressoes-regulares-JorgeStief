import sys
from functions import *

arguments = sys.argv[1:]

if arguments[0] == "-f":
  
  arq = arguments[1]
  word = arguments[2]
  
  final = "Not OK"
  
  try:
    arq = open(arq, 'r')
    regulars_expressions = arq.readlines()
    users_list = []
    
    for regular_expression in regulars_expressions:
      regular_expression = regular_expression.rstrip('\n')
      response = match(regular_expression, word)
      if response:
        final = "OK"
          
      print("match("+regular_expression+","+word+") == \n")
      print(response)
          
    arq.close()
  except FileNotFoundError as e:
    sys.exit("ERROR: O arquivo não existe!")

else:
  regular_expression = arguments[0] 
  word = arguments[1] 
  response = match(regular_expression, word)
  
  print("match("+regular_expression+","+word+") == "+response)
