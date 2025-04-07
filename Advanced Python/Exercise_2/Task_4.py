import random
import urllib.request

def simplify_text(text, word_length, word_count):
    text = text.split()
    text = [word for word in text if len(word) < word_length]

    while len(text) > word_count:
        text.pop(random.randint(0, len(text) - 1))

    return ' '.join(text)

def get_text_from_url(url, max_read = 100000):
    return urllib.request.urlopen(url).read().decode('utf-8')[:max_read]

text = "Podział peryklinalny inicjałów wrzecionowatych \
 kambium charakteryzuje się ścianą podziałową inicjowaną \
 w płaszczyźnie maksymalnej."

url = 'https://www.gutenberg.org/cache/epub/1342/pg1342.txt'
print(simplify_text(get_text_from_url(url), 7, 25))
print(simplify_text(text, 10, 5))