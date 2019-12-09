
import indexer


def main():
    i = indexer.Indexator('database')
    print(1)
    i.indextie_with_lines('tolstoy1.txt')
    print(2)
    i.indextie_with_lines('tolstoy2.txt')
    print(3)
    i.indextie_with_lines('tolstoy3.txt')
    print(4)
    i.indextie_with_lines('tolstoy4.txt')

if __name__=='__main__':
    main()