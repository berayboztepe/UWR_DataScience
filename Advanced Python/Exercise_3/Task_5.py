import itertools

def word_to_number(word, letter_map):
        return int("".join(str(letter_map[letter]) for letter in word))

def solve_cryptarithm(word1, word2, result, operator):
    unique_letters = set(word1 + word2 + result)

    if len(unique_letters) > 10:
        raise ValueError("More than 10 unique letters")
    
    for perm in itertools.permutations(range(10), len(unique_letters)):
        letter_map = dict(zip(unique_letters, perm))
        
        if any(letter_map[word[0]] == 0 for word in [word1, word2, result]): # numbers can not start with 0
            continue
        
        num1 = word_to_number(word1, letter_map)
        num2 = word_to_number(word2, letter_map)
        result_num = word_to_number(result, letter_map)
        
        if (operator == '+' and num1 + num2 == result_num) or \
           (operator == '-' and num1 - num2 == result_num) or \
           (operator == '*' and num1 * num2 == result_num) or \
           (operator == '/' and num2 != 0 and num1 / num2 == result_num):
            yield letter_map

for solution in solve_cryptarithm("KIOTO", "OSAKA", "TOKIO", "+"):
    print("Solution found:", solution)
