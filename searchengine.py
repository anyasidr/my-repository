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
            results.append(self.search_one[word.text])        
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
