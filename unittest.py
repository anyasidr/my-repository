import unittest
from moytokenizer import Tokenizer

class Test(unittest.TestCase):
    def setUp(self):
        self.Tokenizer = Tokenizer()
        
    #unittest for method tokenize
    def test_type_output(self):
        result = self.Tokenizer.tokenize('text')
        self.assertIsInstance(result, list)

    def test_type_input_notlist(self):
        with self.assertRaises(ValueError):
            self.Tokenizer.tokenize(['eto', 'ne', 'spisok'])

    def test_type_input_number(self):
        with self.assertRaises(ValueError):
            self.Tokenizer.tokenize(5)

    def test_result_words(self):
        result = self.Tokenizer.tokenize('we ^&* are testing- *&$^ this thing')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 30)

    def test_result_characters_beginning(self):
        result = self.Tokenizer.tokenize('$%$we ^&* are testing- *&$^ this thing')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 3)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 33)

    def test_result_characters_end(self):
        result = self.Tokenizer.tokenize('we ^&* are testing- *&$^ this thing()(')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 30)

    def test_result_characters_begin_end(self):
        result = self.Tokenizer.tokenize('720@!we ^&* are testing- *&$^ this thing*%@3')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 5)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 35)

        
if __name__ == '__main__':
    unittest.main()
            

    


    
