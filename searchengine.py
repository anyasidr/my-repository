import shelve
import os
import indexer
from moytokenizer import Tokenizer


class SearchEngine(object):
    
    def __init__(self, dbname):
        self.database = shelve.open(dbname, writeback=True)

    def search_one(self, query):
        if not isinstance(query, str):
            raise TypeError
        return self.database.get(query, {})

    def search_many(self, query):
        if not isinstance(query, str):
            raise TypeError
        if query == '':
            return {}
        
        tokenizer = Tokenizer()
        words = list(tokenizer.for_index_tokenize(query))
        results = []
        for word in words:
            results.append(self.database[word.text])        
        files = set(results[0])
        for result in results:
            files &= set(result)
        positions = {}
        for file in files:
            for result in results:
                  positions.setdefault(file, []).extend(result[file])
        return positions

    def close(self):
        self.database.close()

def main():    
    index = indexer.Indexator('db')    
    t = open('tst.txt', 'w')
    t.write(' this is testing\nthis is testing\nthis is testing')
    t.close()
    d = open('tgt.txt', 'w')
    d.write(' is\n testing  ')
    d.close()
    index.indextie_with_lines('tst.txt')
    index.indextie_with_lines('tgt.txt')
    del index
    engine = SearchEngine('db')
    result = engine.search_many('this testing ')
    print(result)
    del engine
    if 'tgt.txt' in os.listdir(os.getcwd()):
        os.remove('tgt.txt')
    if 'tst.txt' in os.listdir(os.getcwd()):
        os.remove('tst.txt')
    for filename in os.listdir(os.getcwd()):            
        if filename == 'db' or filename.startswith('db.'):
            os.remove(filename) 

if __name__=='__main__':
    main()
