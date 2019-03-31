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
    i = indexer.Indexator('db_name')    
    file1 = open('test1.txt', 'w')
    file1.write('this is my test')
    file1.close()
    file2 = open('test2.txt', 'w')
    file2.write('my test')
    file2.close()
    i.indextie_with_lines('test1.txt')
    i.indextie_with_lines('test2.txt')
    del i
    search_engine = SearchEngine('db_name')
    result = search_engine.search_many('my test')
    print(result)
    del search_engine
    if 'test1.txt' in os.listdir(os.getcwd()):
        os.remove('test1.txt')
    if 'test2.txt' in os.listdir(os.getcwd()):
        os.remove('test2.txt')
    for filename in os.listdir(os.getcwd()):            
        if filename == 'db_name' or filename.startswith('db_name.'):
            os.remove(filename) 

            
if __name__=='__main__':
    main()
