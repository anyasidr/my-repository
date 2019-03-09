import unittest
import shelve
import os
from indexer import Indexator, Position, Position_with_lines

class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.indexer = Indexator('database')

    def tearDown(self):
        del self.indexer
        for filename in os.listdir(os.getcwd()):
            if filename == 'database' or filename.startswith('database'):
                os.remove(filename)
        if 'text.txt' in os.listdir(os.getcwd()):
            os.remove('text.txt')
        if 'text1.txt' in os.listdir(os.getcwd()):
            os.remove('text1.txt')


    def test_two_words(self):
        test = open("text.txt", 'w' )
        test.write("my my")
        test.close()
        self.indexer.indextie("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "my":{"text.txt": [Position(0, 2),
                               Position(3, 5)]
        }}
        self.assertEqual(words1, words2)
                  
    def test_two_files(self):
        test = open("text.txt", 'w' )
        test.write("test")
        test.close()
        test = open("text1.txt", 'w' )
        test.write("my my")
        test.close()
        self.indexer.indextie("text.txt")
        self.indexer = Indexator('database')
        self.indexer.indextie("text1.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "my":{"text1.txt": [Position(0, 2),
                               Position(3, 5)]},
            "test":{"text.txt": [Position(0, 4)]
        }}
        self.assertEqual(words1, words2)

    def test_lines(self):
        test = open("text.txt", 'w' )
        test.write("testing\ntest")
        test.close()
        self.indexer.indextie_with_lines("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "testing":{"text.txt": [Position_with_lines(0, 7, 0)]},
            "test":{"text.txt": [Position_with_lines(0, 4, 1)]
        }}
        self.assertEqual(words1, words2)
        

if __name__ == '__main__':
    unittest.main()







        




