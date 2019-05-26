import shelve
import os
import indexer
import re
from moytokenizer import Tokenizer
from indexer import Position_with_lines

class ContextWindow(object):
    """
    This class is used to store context windows data

    position: list of positions of words for context window
    line: string that contains the word for context
    start: position of the first character of the context window
    end: position after the last character of the context window
    """
    def __init__(self, line, position, start, end):
        self.line = line
        self.position = position
        self.start = start
        self.end = end 

    @classmethod
    def load_from_file(cls, filename, position, size):
        """
        Creates an instance of class ContextWindow from file.

        @param filename: path to the file with the word
        @param position: position of the searching word in context window
        @param size: size of the context window
        """
        tok = Tokenizer()
        if not (isinstance(filename, str)
                and isinstance(position, Position_with_lines)
                and isinstance(size, int)):
            raise ValueError (filename, position, size)

        with open(filename) as f:
            for i, line in enumerate(f):
                if i == position.line:
                    break
        if i != position.line:
            raise ValueError('Wrong line number')
        line = line.strip("\n")
        positions = [position]        
        right = line[position.start:]
        left = line[:position.end][::-1]
        
        for i, token in enumerate(tok.for_index_tokenize(left)):
            if i == size:
                break
        start = position.end - token.position - len(token.text)
        for i, token in enumerate(tok.for_index_tokenize(right)):
            if i == size:
                break
        end = position.start + token.position + len(token.text)
        return cls(line, positions, start, end)

    def is_cross(self, wnd):
        """
        Check cross of two context windows

        @param wnd: context window to check
        """
        return (self.start <= wnd.end and
                self.end >= wnd.start and
                wnd.line == self.line)

    def join_context(self, wnd):
        """
        Join context windows and set it to self

        @param wnd: context window to join
        """
        for position in wnd.position:
            if position not in self.position:
                self.position.append(position)
        self.start = min(self.start, wnd.start)
        self.end = max(self.end, wnd.end)

    def expand_context(self):
        """
        Expand context window to sentence
        """

        first = re.compile(r'[.!?]\s[A-ZА-Яa-zа-я]')
        last = re.compile(r'[A-ZА-Яa-zа-я]\s[.!?]')

        right = self.line[self.end:]
        left = self.line[:self.start+1][::-1]    
        if left:
            try:
                self.start = self.start - last.search(left).start()
            except:
                pass
        if right:
            try:
                self.end += first.search(right).start() + 1
            except:
                pass

    def highlight(self):
        """
        Creates a string with highlighted words in search query
        """
        highlighted = self.line[self.start:self.end]
        for pos in self.position[::-1]:
            end = pos.end - self.start
            start = pos.start - self.start
            highlighted = highlighted[:end] + '</strong>' + highlighted[end:]
            highlighted = highlighted[:start] + '<strong>' + highlighted[start:]
        return highlighted
        
    def __eq__(self, wnd):
        """
        Check if two context windows are equal

        @param wnd: context window to check
        """
        return ((self.position == wnd.position) and
                (self.line == wnd.line) and
                (self.start == wnd.start) and
                (self.end == wnd.end))

    def __repr__(self):
        """
        Represents ContextWindow instance to string
        """
        return str(self.position)+ ', ' + str(self.start)+ ', ' \
               + str(self.end)+ ', ' + self.line

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

    def get_context_windows(self, in_dict, size=3):
        """
        Сreate dictionary of files and context windows
        """
        if not (isinstance(in_dict, dict) and
                isinstance(size, int)):
            raise ValueError
        
        contexts_dict = {}
        for f, positions in in_dict.items():
            
            for position in positions:
                context = ContextWindow.load_from_file(f, position, size)
                contexts_dict.setdefault(f, []).append(context)

        joined_contexts_dict = self.join_context_windows(contexts_dict)
        return joined_contexts_dict

    def join_context_windows(self, in_dict):
        """
        Join cross windows in a dictionary of files

        @param in_dict: dict to join
        """
        contexts_dict = {}
        null = ContextWindow([], "", 0, 0)
        for f, contexts in in_dict.items():
            previous_context = null
            for context in contexts:
                if previous_context.is_cross(context):
                    previous_context.join_context(context)
                else:
                    if previous_context is not null:
                        contexts_dict.setdefault(f, []).append(previous_context)
                    previous_context = context
            contexts_dict.setdefault(f, []).append(previous_context)

        return contexts_dict

    def search_to_context_window(self, query, size=3):
        """
        Search query words in database
        """
        positions_dict = self.search_many(query)
        context_dict = self.get_context_windows(positions_dict, size)
        return context_dict

    def search_to_sentence(self, query, size=3):
        """
        Search multiword query in database
        """
        context_dict = self.search_to_context_window(query, size)
        for contexts in context_dict.values():
            for context in contexts:
                context.expand_context()
        sentence_dict = self.join_context_windows(context_dict)
        return sentence_dict

    def search_to_highlight(self, query, size=3):
        """
        Search multiword query in database and highlighting them with 
        <strong> tag
        """
        sentence_dict = self.search_to_sentence(query, size)
        quote_dict = {}
        for f, contexts in sentence_dict.items():
            for context in contexts:
                quote_dict.setdefault(f, []).append(context.highlight())
        return quote_dict

    def close(self):
        """
        methos closes database.
        """
        self.database.close()

def main():    
    '''i = indexer.Indexator('db_name')    
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

    i = indexer.Indexator('warandpeace')
    i.indextie_with_lines('warandpeace.txt')
    del i'''
    search_engine = SearchEngine('warandpeace')
    r = search_engine.search_to_highlight('подошла', 4)
    for key in r.keys():
        for val in r[key]:
            print (val)


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
