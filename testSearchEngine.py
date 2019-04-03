import unittest
import shelve
import os
from indexer import Indexator, Position, Position_with_lines
from searchengine import SearchEngine


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        i = indexer.Indexator('db_name')        
        test1 = open('test1.txt', 'w')
        test1.write('this is my test')
        test1.close()
        test2 = open('test2.txt', 'w')
        test2.write('my test')
        test2.close()        
        i.indextie_with_lines('test1.txt')
        i.indextie_with_lines('test2.txt')
        del i
        self.engine = SearchEngine('db_name')

    def test_empty(self):
        result = self.engine.search('')
        self.assertEqual(result, {})

    def test_search_one(self):
        result = self.engine.search('test')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(11, 15, 0)],
                                  'test2.txt': [Position_with_lines(3, 7, 0)]})

    def test_search_two(self):
        result = self.engine.search('this is')
        self.assertEqual(result, {'test1.txt': [Position_with_lines((0, 4, 0), (5, 7, 0))]})

    def test_search_many_one(self):
        result = self.engine.search_many('test')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(11, 15, 0)],
                                  'test2.txt': [Position_with_lines(3, 7, 0)]})

    def test_search_many_two(self):
        result = self.engine.search_many('my test')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(8, 10, 0),
                                               Position_with_lines(11, 15, 0)],
                                  'test2.txt': [Position_with_lines(0, 2, 0),
                                               Position_with_lines(3, 7, 0)]})

    def tearDown(self):
        del self.engine
        for filename in os.listdir(os.getcwd()):
            if filename == 'db_name' or filename.startswith('db_name'):
                os.remove(filename)
        if 'test1.txt' in os.listdir(os.getcwd()):
            os.remove('test1.txt')
        if 'test2.txt' in os.listdir(os.getcwd()):
            os.remove('test2.txt')
        

if __name__ == '__main__':
    unittest.main()






        




