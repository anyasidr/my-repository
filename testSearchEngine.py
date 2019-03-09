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
            "my":{"text.txt": [Position(0, 2),
                               Position(3, 5)]},
            "test":{"text.txt": [Position(0, 4)]
        }}
        self.assertEqual(words1, words2)

    def test_lines(self):
        test = open("text.txt", 'w' )
        test.write("testing\nground")
        test.close()
        self.indexer.indextie_with_lines("text.txt")
        words1 = dict(shelve.open("database"))
        words2 = {
            "testing":{"text.txt": [Position(0, 7, 0)]},
            "ground":{"text.txt": [Position(0, 6, 1)]
        }}
        self.assertEqual(words1, words2)






        




