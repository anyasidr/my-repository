"""This module is used for tokenizing strings.
The string must be divided into alphabetic characters.""" 

import re
"""
importing the module of regular expressions
"""


class Token(object):
    """
    this class represents tokens aka alphabetic sequences
    """
    def __init__(self, position, text):
        """
        position is a position of each first character of a token
        text is a representation of tokens
        """
        self.position = position
        self.text = text

    
class Tokenizer(object):
    """
    this class uses method tokenize to tokenize a string
    """
    def __init__(self):
        """
        this method makes groups of letters
        """
        # searching for alphabetic sequences only
        self.pattern = re.compile("[^\W\d]+")
         
            
    def tokenize(self, text):
        """
        this method divides a string into tokens consisting of alphabetic symbols
        @param text: string that'll be divided into tokens
        @return: list of tokens
        """
        if not type(text) is str:
            raise ValueError
        tokens = []
        # searching for pattern in a string
        for match in self.pattern.finditer(text):
            # extracting tokens with their positions
            token = Token(match.start(), match.group())
            tokens.append(token)
        return tokens
    
    def gen_tokenize(self, text):
        """
        this method divides a string into tokens
        consisting of alphabetic symbols
        @param text: string that'll be divided into tokens
        @return: generator
        """
        if not type(text) is str:
            raise ValueError
        # searching for pattern in a string
        for match in self.pattern.finditer(text):
            # extracting tokens with their positions
            token = Token(match.start(), match.group())
            yield token


if __name__ == '__main__':
    text = "доброе утро44 !!! - ++ 6&13 **(   спокойной темно-синий  441 ночи привет. Стол - это предмет мебели"
    words = Tokenizer().tokenize(text)
    for token in words:
        print(token.text, token.position)
    gen_words = Tokenizer().gen_tokenize(text)
    for token in gen_words:
        print(token.text, token.position)
    
    





        



