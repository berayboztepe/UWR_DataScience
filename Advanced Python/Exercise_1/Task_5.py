from string import ascii_lowercase

def find_common_prefix(words, level=0):
    longest_prefix = ""
    for letter in ascii_lowercase:
        filtered_words = [word for word in words if len(word) > level and word[level] == letter]
        if len(filtered_words) < 3:
            continue

        prefix = find_common_prefix(filtered_words, level + 1)

        if len(prefix) + 1 > len(longest_prefix):
            longest_prefix = letter + prefix
    
    return longest_prefix

def get_common_prefix(words):
    return find_common_prefix([word.lower() for word in words])

def print_prefix(word_list):
    common_prefix = get_common_prefix(word_list)

    if common_prefix == "":
        print("No prefix found!")
    
    else:
        print(common_prefix)

print_prefix(["Cyprian", "cyberotoman", "cynik", "ceniąc", "czule"])
print_prefix(["Cyprian", "cyberotoman", "cynik", "ceniąc", "czule", "cybaaaaooo", "cybbbbbbbbbbbbb"])
print_prefix(["caca", "casq", "cbsq", "cbfg", ""])
print_prefix(["z", "y", "x", "t", "s"])
