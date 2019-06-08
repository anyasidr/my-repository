import unittest
import shelve
import os
from indexer import Indexator, Position, Position_with_lines
from searchengine import SearchEngine, ContextWindow

test1 = "this is my test"
test2 = "my test"

database = {'this': {'test1.txt': [Position_with_lines(0, 4,0)]},
            'is': {'test1.txt': [Position_with_lines(5, 7,0)]},
            'my': {'test1.txt': [Position_with_lines(8, 10,0)],
                   'test2.txt': [Position_with_lines(0, 2,0)]},
            'test': {'test1.txt': [Position_with_lines(11, 15,0)],
                     'test2.txt': [Position_with_lines(3, 7,0)]}}


class TestContextWindow(unittest.TestCase):

    def setUp(self):
        with open("test1.txt", 'w') as file:
            file.write(test1)
        with open("test2.txt", 'w') as file:
            file.write(test2)

    def test_input(self):
        with self.assertRaises(ValueError):
            ContextWindow.load_from_file(0, 0, 50)

    def test_wrong_line(self):
        with self.assertRaises(ValueError):
            ContextWindow.load_from_file("test1.txt", Position_with_lines(0, 4, 3), 3)

    def test_one(self):
        result = ContextWindow.load_from_file("test1.txt", Position_with_lines(5, 7, 0), 1)
        self.assertEqual(result.position, [Position_with_lines(5, 7, 0)])
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 10)
        self.assertEqual(result.line, test1)

    def test_no_context(self):
        result = ContextWindow.load_from_file("test1.txt", Position_with_lines(5, 7, 0), 0)
        self.assertEqual(result.position, [Position_with_lines(5, 7, 0)])
        self.assertEqual(result.start, 5)
        self.assertEqual(result.end, 7)
        self.assertEqual(result.line, test1)

    def tearDown(self):
        if 'test1.txt' in os.listdir(os.getcwd()):
            os.remove('test1.txt')
        if 'test2.txt' in os.listdir(os.getcwd()):
            os.remove('test2.txt')


class TestWindows(unittest.TestCase):

    def setUp(self):
        self.search_engine = SearchEngine("db_name")
        self.search_engine.database.update(database)
        with open("test1.txt", 'w') as file:
            file.write(test1)

    def test_empty2(self):
        result = self.search_engine.get_window({}, 2)
        self.assertEqual(result, {})

    def test_to_sentence(self):
        query = "this my"
        result = self.search_engine.search_to_sentence(query)
        result2 = {'test1.txt': [SearchEngine([Position_with_lines(0, 4, 0),
                                        Position_with_lines(8, 10, 0)],
                                       test1, 0, 15)]}
        self.assertEqual(result, result2)

class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        i = Indexator('db_name')        
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
        result = self.engine.search_one('')
        self.assertEqual(result, {})

    

    def test_search_one(self):
        result = self.engine.search_one('test')
        self.assertEqual(result, {'test1.txt': [Position_with_lines(11, 15, 0)],
                                  'test2.txt': [Position_with_lines(3, 7, 0)]})

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







        




