"""
This example shows that Sentence is iterable since it implements
an __iter__ method.
"""
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()

        self.index += 1
        return word

    # implementing __iter__ in an iterator is not necessary to make the iterator
    # work. It's the right thing to do though, to make the iterator pass the
    # `issubclass(SentenceIterator, abc.Iterator)` test.
    def __iter__(self):
        return self
