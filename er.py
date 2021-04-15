import sys
from transformations import *


def match(er, word):
    return afdToAFDmin(afnToAFD(afneToAFN(erToAFNe(er)))).accepted(word)

if len(sys.argv )> 1:
  arguments = sys.argv[1:]
  final = "Not OK"
 
  if arguments[0] == "-f":
    
    arq = arguments[1]
    word = arguments[2]
    
    
    
    try:
      arq = open(arq, 'r')
      regular_expressions = arq.readlines()
      
      for regular_expression in regular_expressions:
        
        regular_expression = regular_expression.rstrip('\n')
        response = match(regular_expression, word)
        
        if response:
          final = "OK"
        else:
          final = "Not OK"    
        print("match("+regular_expression+","+word+") == "+final+"\n")
        
            
      arq.close()
    except FileNotFoundError as e:
      sys.exit("ERROR: O arquivo não existe!")

  else:
    regular_expression = arguments[0] 
    word = arguments[1]
    response = match(regular_expression, word)
    
    if response:
      final = "OK"
    print("match("+regular_expression+","+word+") == "+final+"\n")


