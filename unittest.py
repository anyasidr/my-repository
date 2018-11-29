import unittest
from moytokenizer import Tokenizer

class Test(unittest.TestCase):
    def setUp(self):
        self.Tokenizer = Tokenizer()
        
    # unittest for method tokenize
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

        
    # unittest for method gen_tokenize
    def gen_test_type_input_notlist(self):
        with self.assertRaises(ValueError):
            self.Tokenizer.gen_tokenize(['eto', 'ne', 'spisok'])

    def gen_test_type_input_number(self):
        with self.assertRaises(ValueError):
            self.Tokenizer.gen_tokenize(5)

    def gen_test_result_words(self):
        result = self.Tokenizer.gen_tokenize('we ^&* are testing- *&$^ this thing')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 30)

    def gen_test_result_characters_beginning(self):
        result = self.Tokenizer.gen_tokenize('$%$we ^&* are testing- *&$^ this thing')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 3)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 33)

    def gen_test_result_characters_end(self):
        result = self.Tokenizer.gen_tokenize('we ^&* are testing- *&$^ this thing()(')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 30)

    def gen_test_result_characters_begin_end(self):
        result = self.Tokenizer.gen_tokenize('720@!we ^&* are testing- *&$^ this thing*%@3')
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, 'we')
        self.assertEqual(result[0].position, 5)
        self.assertEqual(result[4].text, 'thing')
        self.assertEqual(result[4].position, 35)

        
    # unittest for method gen_type_tokenize
    def gen_type_test_list(self):
        with self.assertRaises(ValueError):
            result = self.Tokenizer.gen_type_tokenize(['eto', 'ne', 'spisok'])

    def gen_test_type_input_number(self):
        with self.assertRaises(ValueError):
            result = self.Tokenizer.gen_type_tokenize(5)

    def test_type(self):
        result = self.Tokenizer.gen_type_tokenize('Test - thats right')
        sequence = list(result)
        self.assertEqual(len(sequence), 7)
        self.assertEqual(sequence[0].text, 'Test')
        self.assertEqual(sequence[0].position, 0)
        self.assertEqual(sequence[0].typ, "a")
        self.assertEqual(sequence[1].text, ' ')
        self.assertEqual(sequence[1].position, 4)
        self.assertEqual(sequence[1].typ, "s")        
        self.assertEqual(sequence[2].text, '-')
        self.assertEqual(sequence[2].position, 5)
        self.assertEqual(sequence[2].typ, "p")

    def test_type_notlatin(self):
        result = self.Tokenizer.gen_type_tokenize('大好きです。 Мне это нравится')
        sequence = list(result)
        self.assertEqual(len(sequence), 8)
        self.assertEqual(sequence[0].text, '大好きです')
        self.assertEqual(sequence[0].position, 0)
        self.assertEqual(sequence[0].typ, "a")
        self.assertEqual(sequence[1].text, '。')
        self.assertEqual(sequence[1].position, 5)
        self.assertEqual(sequence[1].typ, "p")        
        self.assertEqual(sequence[2].text, ' ')
        self.assertEqual(sequence[2].position, 6)
        self.assertEqual(sequence[2].typ, "s")
        self.assertEqual(sequence[3].text, 'Мне')
        self.assertEqual(sequence[3].position, 7)
        self.assertEqual(sequence[3].typ, "a")

    def test_type_other(self):
        result = self.Tokenizer.gen_type_tokenize('... ой6ой + @')
        sequence = list(result)
        self.assertEqual(len(sequence), 9)
        self.assertEqual(sequence[0].text, '...')
        self.assertEqual(sequence[0].position, 0)
        self.assertEqual(sequence[0].typ, "p")
        self.assertEqual(sequence[3].text, '6')
        self.assertEqual(sequence[3].position, 6)
        self.assertEqual(sequence[3].typ, "d")        
        self.assertEqual(sequence[6].text, '+')
        self.assertEqual(sequence[6].position, 10)
        self.assertEqual(sequence[6].typ, "o")
        
        
if __name__ == '__main__':
    unittest.main()
            

    

    


    
