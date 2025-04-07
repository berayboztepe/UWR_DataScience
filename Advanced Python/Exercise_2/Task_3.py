import urllib.request
import string

def dict_prob_for_letters(url):
    url = urllib.parse.quote(url, safe=':/')
    url_cleansed = urllib.request.urlopen(url).read().decode('utf-8')        
    url_cleansed = (word for word in url_cleansed if word.isalnum())                           
    url_cleansed = filter(lambda x: x in set(string.printable), url_cleansed)         
    url_cleansed = (''.join(url_cleansed)).lower()                               

    letter_dict = dict()

    for letter in url_cleansed:
        if not letter in letter_dict:
            letter_dict[letter] = 1
        else: 
            letter_dict[letter] += 1

    for letter, count in letter_dict.items():
        letter_dict[letter] = count / len(url_cleansed)

    return letter_dict

def guess_language(languages, url):
    prob_dict = dict_prob_for_letters(url)
    min = 1
    language = ''

    for lang_name, lang_dict, _ in languages:
        if len(lang_dict) == 0: 
            continue

        difference = 0
        for letter, prob in lang_dict.items():
            if letter in prob_dict: 
                difference += abs(prob - prob_dict[letter])
            else: 
                difference += prob
                
        difference /= len(lang_dict)

        if difference < min:
            min = difference
            language = lang_name

    return language

english_dict = {}
english_source = 'https://en.wikipedia.org/wiki/Galileo_project'

polish_dict = {}
polish_source = 'https://pl.wikipedia.org/wiki/Zamek_Książęcy_w_Oleśnicy'

spanish_dict = {}
spanish_source = 'https://es.wikipedia.org/wiki/Planetas_más_allá_de_Neptuno'

turkish_dict = {}
turkish_source = 'https://tr.wikipedia.org/wiki/Bayağı_doğan'

languages = [
    ('english', english_dict, english_source),
    ('polish', polish_dict, polish_source),
    ('spanish', spanish_dict, spanish_source),
    ('turkish', turkish_dict, turkish_source)
]

for lang_name, language_dict, source in languages:
    letter_probs = dict_prob_for_letters(source)
    for letter, prob in letter_probs.items():
        if letter in language_dict:
            language_dict[letter] += prob
        else:
            language_dict[letter] = prob


test = [
    ('https://en.wikipedia.org/wiki/Museum_of_Bad_Art', 'english'),
    ('https://en.wikipedia.org/wiki/Equestrian_statue_of_Edward_Horner', 'english'),
    ('https://pl.wikipedia.org/wiki/Polska', 'polish'),
    ('https://pl.wikisource.org/wiki/Joan._VIII_1-12/V', 'polish'),
    ('https://es.wikisource.org/wiki/El_Domingo_de_Ramos', 'spanish'),
    ('https://es.wikipedia.org/wiki/Mormyroidea', 'spanish'),
    ('https://tr.wikipedia.org/wiki/Galatasaray_(futbol_takımı)', 'turkish'),
    ('https://tr.wikipedia.org/wiki/Sonsuz_maymun_teoremi', 'turkish')
    ]

for url, language in test:
    print(f'Real Language: {language} -> Guessed Language: {guess_language(languages, url)} (Given URL: {url})')