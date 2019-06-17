import shelve
import os
import indexer
import re
import windows
from moytokenizer import Tokenizer
from indexer import Position_with_lines


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
        # print(dict(self.database))
        self.tokenizer = Tokenizer()

    def search_one(self, query):
        """
        This method searches in a database. The method uses
        a key that is a tokens, returns all the positions
        of the token.
        """
        if not isinstance(query, str):
            raise ValueError
        return self.database.get(query, {})

    def search_many(self, query):
        """
        This method uses tokenization. The method searches in a database, 
        finds tokens in a tokenized string. Returns a dictionary where
        the tokens are keys with their positions in all given files.
        """
        if not isinstance(query, str):
            raise ValueError
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

    def get_window(self, in_dict, size=3):
        """
        Сreate dictionary of files and context windows
        """
        if not (isinstance(in_dict, dict) and
                isinstance(size, int)):
            raise ValueError
        
        conts_dict = {}
        for f, positions in in_dict.items():
            for position in positions:
                cont = windows.ContextWindow.find_window(f, position, size)
                conts_dict.setdefault(f, []).append(cont)
        joined_conts_dict = self.join_windows(conts_dict)
        return joined_conts_dict

    def join_windows(self, in_dict):
        """
        Join cross windows in a dictionary of files

        @param in_dict: dict to join
        """
        conts_dict = {}
        empty = windows.ContextWindow([], "", 0, 0)
        for f, conts in in_dict.items():
            previous_cont = empty
            for cont in conts:
                if previous_cont.is_cross(cont):
                    previous_cont.join_cont(cont)
                else:
                    if previous_cont is not empty:
                        conts_dict.setdefault(f, []).append(previous_cont)
                    previous_cont = cont
            conts_dict.setdefault(f, []).append(previous_cont)
        return conts_dict

    def search_to_window(self, query, size=3):
        """
        Search query words in database
        """
        positions_dict = self.search_many(query)
        cont_dict = self.get_window(positions_dict, size)
        return cont_dict

    def search_to_sentence(self, query, size=3):
        """
        Search multiword query in database
        """
        context_dict = self.search_to_window(query, size)
        for contexts in context_dict.values():
            for context in contexts:
                context.expand_context()
        sentence_dict = self.join_windows(context_dict)
        return sentence_dict

    def search_to_highlight(self, query, size=3):
        """
        Search multiword query in database and highlighting them with 
        <strong> tag
        """
        sentence_dict = self.search_to_sentence(query, size)
        quote_dict = {}
        for f, conts in sentence_dict.items():
            for cont in conts:
                quote_dict.setdefault(f, []).append(cont.highlight())
        return quote_dict

    def close(self):
        """
        methos closes database.
        """
        self.database.close()

def main():    
    i = indexer.Indexator('db_name')    
    file1 = open('test1.txt', 'w')
    file1.write('Да, это пустые слова, здесь нет ничего полезного. привет как твои дела ? у меня все хорошо, я хочу домой приди ко мне! но ты же не свободна?')
    file1.close()
    file2 = open('test2.txt', 'w')
    file2.write('да я хочу сказать тебе . привет и все, но зачем все привет эти слова? я хочу быть счастливым! И точка')
    file2.close()
    i.indextie_with_lines('test1.txt')
    i.indextie_with_lines('test2.txt')
    del i
    search_engine = SearchEngine('db_name')
    #result = search_engine.search_many('my test')
    #print(result)

    r = search_engine.search_to_highlight('привет', 4)
    print(r)

    """i = indexer.Indexator('tolstoy')
    i.indextie_with_lines('tolstoy1.txt')
    del i
    search_engine = SearchEngine('tolstoy')
    r = search_engine.search_to_highlight('Анна', 4)
    for key in r.keys():
        for val in r[key]:
            print (val)"""


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
