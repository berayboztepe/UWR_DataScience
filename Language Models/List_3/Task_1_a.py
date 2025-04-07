import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
import random

model_name = 'distilgpt2'
device = 'cuda' if torch.cuda.is_available() else 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

N = model.transformer.wte.weight.shape[0]

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

emb = model.transformer.wte.weight.detach().cpu().numpy()

def sumEmbeddingStr(word):
    word = ' ' + word
    tokens = [tokenizer.decode(n) for n in tokenizer(word, return_tensors='pt')['input_ids'][0]]
    weights = np.exp(-np.arange(len(tokens), dtype=float) * 0.5)
    
    out = np.zeros(emb.shape[1])
    for w, t in zip(weights, tokens):
        token_id = tokenizer.encode(t)[0]
        out += w * emb[token_id]
    return ' '.join(str(x) for x in out)

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

with open(r'C:\Users\beray\Code Projects\Language Models\Exercise_3\word_embedings_file_1_a.txt', 'w') as f:
    for line in clusters_txt.strip().split('\n'):
        for word in line.split()[1:]:
            f.write(f'{word} {sumEmbeddingStr(word)}\n')

            swapped = swapAdjacent(word)
            vowel_replaced = replaceVowel(word)
            
            f.write(f'{swapped} {sumEmbeddingStr(swapped)}\n')
            f.write(f'{vowel_replaced} {sumEmbeddingStr(vowel_replaced)}\n')