import gensim.downloader as api
import random
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn
import pandas as pd

print("Loading Word2Vec model...")
word2vec = api.load("glove-wiki-gigaword-100")
print("Model loaded!")

#nltk.download('averaged_perceptron_tagger_eng')
#nltk.download('punkt_tab')
#nltk.download("punkt")
#nltk.download("averaged_perceptron_tagger")
#nltk.download("wordnet")

def find_synonym(word):
    if word in word2vec:
        synonyms = word2vec.most_similar(word, topn=5)
        return random.choice([syn[0] for syn in synonyms])
    return word

def augment_review_with_word2vec(review):
    words = word_tokenize(review)
    pos_tags = pos_tag(words)
    
    augmented_words = []
    for word, tag in pos_tags:
        if tag.startswith("NN") or tag.startswith("JJ") or tag.startswith("VB"):
            synonym = find_synonym(word.lower())
            augmented_words.append(synonym if synonym != word else word)
        else:
            augmented_words.append(word)
    
    return " ".join(augmented_words)

sampled_reviews_file = r'C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_100.csv'
sampled_reviews = pd.read_csv(sampled_reviews_file)

augmented_reviews = []
for review in sampled_reviews['text']:
    augmented_review = augment_review_with_word2vec(review)
    augmented_reviews.append(augmented_review)

sampled_reviews['augmented_review'] = augmented_reviews

output_file = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_3_c_100.csv"
sampled_reviews.to_csv(output_file, index=False)
print(f"Augmented reviews saved to {output_file}.")


"""
Went for lunch and found that my burger was meh.  
What was obvious was that the focus of the burgers is the amount of different and random crap they 
can pile on it and not the flavor of the meat.  My burger patty seemed steamed and appeared to be a preformed patty, 
contrary to what is stated on the menu.    I can get ground beef from Kroger and make a burger that blows them out of the water.

gone for breakfast and discovered that my kfc been meh . 
What been reasons had that the emphasis of the fries has the amounts of various and searches whack they 
can garbage on it and not the sweetness of the chicken . My taco huber seems sauteed and later to should a digitalised caroline , 
contradict to what this stating on the menus . I can n't over pork from safeway and come a taco that knocks them out of the natural .



"""