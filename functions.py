from models.AFNE import *
import string 
from functions import *

ALPHABET = list(string.ascii_lowercase)

def match(er, word):
  return erToAFNe(er)

def erToAFNe(er):
  return True