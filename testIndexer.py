import unittest
import moytokenizer
import os
import shelve
from indexator import Indexator, Position, Position_with_lines


class TestIndexator(unittest.TestCase):
    def setUp(self):
        self.indexator = Indexator('database')
        
    def test_input_digit(self):
        with self.assertRaises(ValueError):
            self.indexator.indextie(1234)

    def test_input_none(self):
        with self.assertRaises(ValueError):
            self.indexator.indextie("lalala")

    def test_input_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            self.indexator.indextie("abracadabra.txt")

    def test_one_word(self):      
        file = open('test.txt', 'w')
        file.write('indexator')
        file.close()        
        self.indexator.indextie('test.txt')        
        data_dict = dict(shelve.open('database'))
        dictionary = {'indexator': {'test.txt': [Position(0, 9)]}}
        self.assertEqual(data_dict, dictionary)

    def test_same_words(self):      
        file = open('test.txt', 'w')
        file.write('well well well')
        file.close()        
        self.indexator.indextie('test.txt')        
        data_dict = dict(shelve.open('database'))
        dictionary = {
            'well': {
                'test.txt': [(Position(0, 4), Position(6, 10), Position(12, 16))]}}
        self.assertEqual(data_dict, dictionary)
        
    def test_many_words(self):      
        file = open('test.txt', 'w')
        file.write('testing my indexator')
        file.close()        
        self.indexator.indextie('test.txt')        
        data_dict = dict(shelve.open('database'))
        dictionary = {
            'testing': {
                'test.txt': [Position(0, 7)]
            },
            'my': {
                'test.txt': [Position(8, 10)]
            },
            'indexator': {
                'test.txt': [Position(11, 20)]}}
        self.assertEqual(data_dict, dictionary) 

    def test_two_files(self):      
        file1 = open('test1.txt', 'w')
        file1.write('file number one')
        file1.close()        
        self.indexator.indextie('test1.txt')        
        test2 = open('test2.txt', 'w')
        test2.write('file number two')
        test2.close()  
        self.indexator.indextie('test2.txt')
        data_dict = dict(shelve.open('database'))
        dictionary = {
            'file': {
                'test1.txt': [Position(0, 4)],
                'test2.txt': [Position(0, 4)]
            },
            'number': {
                'test1.txt': [Position(5, 11)],
                'test2.txt': Position(5, 11)
            },
            'one': {
                'test1.txt': [Position(12, 15)]
            },
            'two': {
                'test2.txt': [Position(12, 15)]}}
        self.assertEqual(data_dict, dictionary)

    
    def tearDown(self):
        del self.indexator
        myfiles = os.listdir(path = ".")
        for file in myfiles:            
            if file == 'database':
                os.remove(file)
            if file.startswith('database.'):
                os.remove(file)



if __name__=='__main__':
    unittest.main()
