import string

def is_palindrom(text):
    text = text.lower()
    text_without_punc = ''.join([char for char in text if char not in string.punctuation and not char.isspace()])
    
    return text_without_punc == text_without_punc[::-1]

print(is_palindrom("Eine güldne, gute Tugend: Lüge nie!"))
print(is_palindrom("Míč omočím."))
print(is_palindrom("rotor"))
print(is_palindrom("eye"))
print(is_palindrom("This is not palindrom"))
