import unittest
import shelve
import os
from indexer import Indexator, Position, Position_with_lines, SearchEngine


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
       

    

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







        




