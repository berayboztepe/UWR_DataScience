import urllib.request

def compress_text(text):
    if(len(text) == 0): 
        return list()

    result_list = list()
    letter_checkpoint = text[0]
    count = 0

    for letter in text:
        if letter == letter_checkpoint:
            count+=1
        else:
            result_list.append((count, letter_checkpoint))
            letter_checkpoint = letter
            count = 1

    if count != 0: 
        result_list.append((count, letter_checkpoint))

    return result_list

def decompress_text(compressed_text):
    res = ''

    for count, letter in compressed_text:
        res += count*letter

    return res

def get_text_from_url(url, max_read = 100000):
    return urllib.request.urlopen(url).read().decode('utf-8')[:max_read]

print(compress_text("suuuuper"))
print(decompress_text(compress_text("suuuuper")))

print(compress_text("ooooottthhheeerrrr exxxxammmmmpppllleeee"))
print(decompress_text(compress_text("ooooottthhheeerrrr exxxxammmmmpppllleeee")))

url = 'https://www.gutenberg.org/cache/epub/1342/pg1342.txt'
text = get_text_from_url(url, 150)
print(compress_text(text))
print(decompress_text(compress_text(text)))