import shelve
import os
import indexer
from moytokenizer import Tokenizer


class SearchEngine(object):
    """
    This class is used for searching of
    positions of tokens in a given database.
    """
    
    def __init__(self, dbname):
        """
        This method creates an example of 
        class SearchEngine.
        """
        self.database = shelve.open(dbname, writeback=True)

    def search_one(query, str):
        """
        This method searches in a database. The method uses
        a key that is a tokens, returns all the positions
        of the token.
        """
        if not isinstance(query, str):
            raise TypeError
        return self.database.get(query, {})

    def search_many(self, query):
        """
        This method uses tokenization. The method searches in a database, 
        finds tokens in a tokenized string. Returns a dictionary where
        the tokens are keys with their positions in all given files.
        """
        if not isinstance(query, str):
            raise TypeError
        if query == '':
            return {}
        
        tokenizer = Tokenizer() # using tokenizer for extracting tokens
        words = list(tokenizer.for_index_tokenize(query))
        results = [] # creating a tuple
        for word in words:
            results.append(self.database[word.text])   
        files = set(results[0]) # converting tuple into set
        for result in results:
            files &= set(result) # intersecting sets of documents
        positions = {} # creating a dictionary with positions
        for file in files:
            for result in results:
                  positions.setdefault(file, []).extend(result[file])
        return positions

    def close(self):
        """
        methos closes database.
        """
        self.database.close()

def main():    
    index = indexer.Indexator('db')    
    t = open('test.txt', 'w')
    t.write(' this is testing\nthis is testing\nthis is testing')
    t.close()
    d = open('tst.txt', 'w')
    d.write(' is\n testing  ')
    d.close()
    index.indextie_with_lines('test.txt')
    index = indexer.Indexator('db')
    index.indextie_with_lines('tst.txt')
    del index
    engine = SearchEngine('db')
    result = engine.search_many('this testing ')
    print(result)
    del engine
    if 'tst.txt' in os.listdir(os.getcwd()):
        os.remove('tst.txt')
    if 'test.txt' in os.listdir(os.getcwd()):
        os.remove('test.txt')
    for filename in os.listdir(os.getcwd()):            
        if filename == 'db' or filename.startswith('db.'):
            os.remove(filename) 

if __name__=='__main__':
    main()
