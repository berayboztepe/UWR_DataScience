import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import random

model_name = 'distilbert-base-uncased'
device = 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)

clusters_txt = '''
Writing-tools: marker, highlighter, pencil, pen
Small-mammals: mouse, rat, hamster, weasel, marten, beaver
Ships: destroyer, carrier, minesweeper, cruiser, battleship, frigate, corvette
Doctors: doctor, pediatrician, gynecologist, cardiologist, internist, geriatrician
Emotions: love, friendship, hatred, anger, sadness, joy, fear
Mathematical-fields: algebra, analysis, topology, logic, geometry
Sacred-buildings: church, basilica, chapel, cathedral, temple, synagogue, congregation
Military-rank: warrant officer, second lieutenant, lieutenant, captain, major, colonel, general, lieutenant colonel
Philosophical: empiricism, stoicism, rationalism, existentialism, Marxism, Romanticism
Religions: Christianity, Buddhism, Islam, Orthodoxy, Protestantism, Calvinism, Lutheranism, Judaism
Musical works: sonata, symphony, concerto, prelude, fugue, suite
Digits: one, two, three, four, five, six, seven, eight, nine
Insects: dragonfly, ladybug, beetle, ant, fly, wasp, bee, weevil
Bladed-weapons: sword, axe, dagger, knife, hatchet
Firearms: rifle, pistol, revolver, musket, shotgun
Computers: computer, laptop, calculator, notebook
Colors: white, yellow, red, blue, green, brown, black
Clergy: vicar, bishop, priest, parish priest, rabbi, pope, archbishop, cardinal, pastor
Fish: carp, herring, salmon, cod, perch, pike-perch, pike, roach
Sports-activities: running, jumping, swimming, marching, walk, jog
Clothing: suit, tuxedo, tailcoat, blazer, jacket, shirt, blouse, sweater, jumper, dress, vest, skirt, trousers
Furniture: chair, armchair, couch, bed, sofa, table, small table, coffee table
Criminals: murderer, killer, rapist, thief, bandit, pickpocket, scoundrel, thug
Meat and cold cuts: pork, beef, lamb, veal, bacon, smoked ham, sausage, ham, loin, pork neck, venison
Tree: oak, maple, elm, ash, spruce, pine, larch, plane, beech, yew, sycamore, rowan, acacia
Lights: lamp, flashlight, small lamp, chandelier, light bulb, spotlight, lantern, desk lamp
Organs: liver, lung, heart, pancreas, stomach, kidney, uterus, fallopian tube, prostate, spleen
Military: company, platoon, battalion, brigade, army, division, regiment
Alcoholic-beverages: beer, wine, vodka, gin, liqueur, moonshine, cider, cognac
Cats: puma, panther, leopard, tiger, lion, lynx, wildcat, cheetah, jaguar
Metal: iron, gold, silver, copper, nickel, tin, zinc, potassium, platinum, chromium, aluminum
Aircraft: airplane, jet, small plane, bomber, helicopter
Fruit: apple, pear, plum, peach, lemon, orange, grapefruit, currant, nectarine
Bedding: pillow, bedsheet, duvet, featherbed, blanket, plaid
Appliances: refrigerator, stove, dishwasher, mixer, juicer, oven, microwave
'''

def get_contextual_embedding(word):
    inputs = tokenizer(word, return_tensors='pt').to(device)
    outputs = model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy().flatten()
    return cls_embedding

def swapAdjacent(word):
    if len(word) > 1:
        i = random.randint(0, len(word) - 2)
        return word[:i] + word[i + 1] + word[i] + word[i + 2:]
    return word

def replaceVowel(word):
    vowels = "aeiou"
    word_list = list(word)
    for i, char in enumerate(word_list):
        if char in vowels:
            word_list[i] = random.choice(vowels)
            break
    return ''.join(word_list)

output_file = r'C:\Users\beray\Code Projects\Language Models\Exercise_3\word_embedings_file_1_b.txt'
with open(output_file, 'w') as f:
    for line in clusters_txt.strip().split('\n'):
        for word in line.split()[1:]:
            original_embedding = get_contextual_embedding(word)
            f.write(f'{word} ' + ' '.join(map(str, original_embedding)) + "\n")
            
            swapped = swapAdjacent(word)
            vowel_replaced = replaceVowel(word)
            
            swapped_embedding = get_contextual_embedding(swapped)
            f.write(f'{swapped} ' + ' '.join(map(str, swapped_embedding)) + "\n")
            
            vowel_embedding = get_contextual_embedding(vowel_replaced)
            f.write(f'{vowel_replaced} ' + ' '.join(map(str, vowel_embedding)) + "\n")