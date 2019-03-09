from moytokenizer import Tokenizer
import shelve
import os


class Position(object):
    
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, obj):
        return self.start == obj.start and self.end == obj.end

    def __repr__(self):
        return '(' + str(self.start) + ';' + ' ' + str(self.end) + ')'
    
    
class Position_with_lines(object):

    def __init__(self, start, end, line):
        self.start = start
        self.end = end
        self.line = line

    def __eq__(self, obj):
        return (self.start == obj.start and self.end == obj.end and
                self.line == obj.line)

    def __repr__(self):
        return '(' + str(self.start) + ',' + ' ' + str(self.end) + ',' + str(self.line) + ')'

     
class Indexator(object):

    def __init__(self, db_name):
        self.database = shelve.open(db_name, writeback=True)

    def indextie(self, filename):
        if not isinstance(filename, str):
            raise TypeError('Inappropriate type')
        text = open(filename)
        tokenizer = Tokenizer()
        for word in tokenizer.for_index_tokenize(text.read()):
            self.database.setdefault(word.text, {}).setdefault(filename, []).append(Position(word.position,
            (word.position + len(word.text))))
        text.close()
        self.database.sync()
        
    def indextie_with_lines(self, filename):
        if not isinstance(filename, str):
            raise TypeError('Inappropriate type')
        text = open(filename)
        tokenizer = Tokenizer()
        for number, line in enumerate(text):
            for word in tokenizer.for_index_tokenize(line):
                self.database.setdefault(word.text, {}).setdefault(filename, []).append(Position_with_lines
                (word.position, (word.position + len(word.text)), number))
        text.close()
        self.database.sync()
        
    def __del__(self):
        self.database.close()

def main():
    indexator = Indexator('database')
    file = open('text.txt', 'w')
    file.write('well well well')
    file.close()
    indexator.indextie_with_lines('text.txt')
    del indexator
    os.remove('text.txt')
    print(dict(shelve.open('database')))
    for filename in os.listdir(os.getcwd()):
        if filename == 'database' or filename.startswith('database.'):
            os.remove(filename)


if __name__=='__main__':
    main()


