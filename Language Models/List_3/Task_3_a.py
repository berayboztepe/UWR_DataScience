import pandas as pd
import random

def introduce_typos(text):
    words = text.split()
    typo_text = []
    for word in words:
        if random.random() < 0.2:
            i = random.randint(0, len(word) - 1)
            word = word[:i] + random.choice("abcdefghijklmnopqrstuvwxyz") + word[i + 1:]
        typo_text.append(word)
    return " ".join(typo_text)

def change_case(text):
    return "".join(c.upper() if random.random() < 0.2 else c.lower() for c in text)

def mechanical_augmentation(text):
    text = introduce_typos(text)
    text = change_case(text)
    return text

sample_reviews_path = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_100.csv"
sampled_reviews = pd.read_csv(sample_reviews_path)

sampled_reviews['augmented_review'] = sampled_reviews['text'].apply(mechanical_augmentation)

output_path = r"C:\Users\beray\Code Projects\Language Models\Exercise_3\sampled_reviews_3_a_100.csv"
sampled_reviews.to_csv(output_path, index=False)

"""
Went for lunch and found that my burger was meh. 
 What was obvious was that the focus of the burgers is the amount of different and random crap they 
 can pile on it and not the flavor of the meat.  My burger patty seemed steamed and appeared to be a preformed patty, 
 contrary to what is stated on the menu.    I can get ground beef from Kroger and make a burger that blows them out of the water.

 
 PenT for lUnch aNd found thAT mY BUrger waS mEh. 
 whAt was obviOUs was That the focus oF thE burGerS iS The amount of diFfEreNt and ranDom crap theY 
 chn pILe On it and not the flaVor of the meat. my burGer pAttY seemeD stEameD And appeared to be a PrEformed paTtyz 
 contrarY to what Is StaTeD on tHe meNu. r can get groUnd Ceef From kRoger aNd maKe a burger thAT bkows them out Of the waTeR.


"""