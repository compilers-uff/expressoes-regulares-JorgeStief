import pytest
import er

def test0():
    assert er.match("a", "a") == True

def test1():
    assert er.match("+(a, b)", "a") == True

def test2():
    assert er.match(".(a, b)", "a") == False

def test3():
    assert er.match(".(a, b)", "ab") == True
    
def test4():    
    assert er.match("*(+(a, b))", "a") == True
    
def test5():    
    assert er.match("*(+(a, b))", "aaa") == True
    
def test6():    
    assert er.match("*(+(a, b))", "ab") == True
    
def test7():    
    assert er.match("*(+(a, b))", "aba") == True
    
def test8():    
    assert er.match("*(+(a, b))", "abababa") == True

def test9():
  assert er.match('.(*(+(a,b)), *(+(+(a,b),c)))', 'ababababbabacababacbacb') == True
  
def test10():
    assert er.match(".(.(*(+(a,b)), .(a,.(b,.(b,a)))), *(+(a,b)))", "baabbaba") == True

def test11():
    assert er.match(".(.(*(+(a,b)), .(a,.(b,.(b,a)))), *(+(a,b)))", "ababa") == False

def test12():
    assert er.match(".(.(0,*(+(0,1))),1)", "0001010") == False

def test13():
    assert er.match(".(.(0,*(+(0,1))),1)", "00010101") == True

def test14():
    assert er.match(".(*(1), *(.(.(0,*(1)), .(0,*(1)))))", "1100") == True

def test15():
    assert er.match(".(*(1), *(.(.(0,*(1)), .(0,*(1)))))", "110010") == False

def test16():
    assert er.match(".(*(+(1, .(0,1))), +(e,0))", "11101010110") == True

def test17():
    assert er.match(".(*(+(1, .(0,1))), +(e,0))", "111010100110") == False

def test18():
    assert er.match(".(+(a, e), *(+(b, .(b,a))))", "abbababababb") == True

def test19():
    assert er.match(".(+(a, e), *(+(b, .(b,a))))", "abbaababababb") == False

def test20():
    assert er.match('*(.(.(a,b),c))', 'abc') == True
    
def test21():
    assert er.match('+(+(+(+(a,b),c),d),e)', '') == False  

def test22():
    assert er.match('.(.(+(a,b),+(c,d)), .(+(a,b),+(c,d)))', 'abcbd')    == False   