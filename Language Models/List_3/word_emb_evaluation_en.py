# -*- encoding: utf8 -*-

from collections import defaultdict as dd
import numpy as np
import random

random.seed(42)

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

def best(w, K, vectors):
    v = vectors[w]
    L = sorted([(v.dot(vectors[w]), w) for w in vectors])
    L.reverse()
    return L[:K]


def choose_another(A, a):
    while True:
        b = random.choice(A)
        if a != b:
            return b


def evaluate_embeddings(file_name, vectors, C, words, groups, N=500000):
    vectors.clear()

    for x in open(file_name):
        L = x.split()
        if len(L) < 2:
            continue
        w = L[0]
        values = [float(x) for x in L[1:]]
        v = np.array(values)
        length = v.dot(v) ** 0.5
        vectors[w] = v / length

    bad, all_words = 0.0, 0.0
    for w in words:
        if w not in vectors:
            print(w, end=' ')
            bad += 1
        all_words += 1
    print('\nPROBLEMS:', bad / all_words)

    # ABX test
    score = 0.0
    for i in range(N):
        g1 = random.choice(groups)
        A = C[g1]
        B = C[choose_another(groups, g1)]

        a1 = random.choice(A)
        a2 = choose_another(A, a1)
        b = random.choice(B)

        if a1 not in vectors or a2 not in vectors or b not in vectors:
            score += 0.5
            continue

        va1 = vectors[a1]
        va2 = vectors[a2]
        vb = vectors[b]

        if va1.dot(va2) > va1.dot(vb):
            score += 1.0

    return score / N


C = {}
words = set()

for x in clusters_txt.split('\n'):
    L = x.split()
    if len(L) < 2:
        continue
    C[L[0]] = L[1:]
    words.update(L[1:])

groups = list(C.keys())
vectors = {}

files = [
    r'C:\Users\beray\Code Projects\Language Models\Exercise_3\word_embedings_file_1_a.txt',
    r'C:\Users\beray\Code Projects\Language Models\Exercise_3\word_embedings_file_1_b.txt',
]

for file_name in files:
    print(f"\nEvaluating {file_name}")
    score = evaluate_embeddings(file_name, vectors, C, words, groups)
    print(f'TOTAL SCORE for {file_name}:', score)
