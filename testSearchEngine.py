import unittest
import shelve
import os
from indexer import Indexator, Position, Position_with_lines, SearchEngine


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        index = indexer.Indexer('database')        
        file1 = open('test1.txt', 'w')
        file1.write('this is\ntest')
        file1.close()
        file2 = open('test2.txt', 'w')
        file2.write('test')
        file2.close()        
        index.indextie_with_lines('test1.txt')
        index.indexitie_with_lines('test2.txt')
        del index
        self.s = SearchEngine('database')

    def test_empty(self):
        result = self.s.search('')
        self.assertEqual(result, {})

    def test_search(self):
        result = self.s.search('test')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(0, 4, 1)],
                                  'test2.txt': [Position_with_lines(0, 4, 0)]})

    def test_search_many(self):
        result = self.s.search_many('test')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(0, 4, 1)],
                                  'test2.txt': [Position_with_lines(0, 4, 0)]})

    def tearDown(self):
        del self.s
        for filename in os.listdir(os.getcwd()):            
            if filename == 'database' or filename.startswith('database.'):
                os.remove(filename)        
        if 'test1.txt' in os.listdir(os.getcwd()):
            os.remove('test.txt')
        if 'test2.txt' in os.listdir(os.getcwd()):
            os.remove('tst.txt')
        

if __name__ == '__main__':
    unittest.main()







        




