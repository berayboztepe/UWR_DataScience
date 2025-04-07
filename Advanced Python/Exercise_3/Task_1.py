import math
import timeit

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def  prime_imperative(n):
    primes = []
    for num in range(2, n):
        if is_prime(num):
            primes.append(num)
    return primes

def  prime_comprehension(n):
    return [num for num in range(2, n) if is_prime(num)]

def  prime_functional(n):
    return list(filter(is_prime, range(2, n)))

n = 20
print("Imperative:", prime_imperative(n))
print("List Comprehension:",  prime_comprehension(n))
print("Functional:",  prime_functional(n))

print("--------------------------------------")
for n in [10, 20, 30, 40, 50]:
    imp_time = timeit.timeit(lambda: prime_imperative(n), number=1000)
    comprehension_time = timeit.timeit(lambda:  prime_comprehension(n), number=1000)
    functional_time = timeit.timeit(lambda:  prime_functional(n), number=1000)
    print(f"n = {n} | Imperative: {imp_time:.3f} | Comprehension: {comprehension_time:.3f} | Functional: {functional_time:.3f}")
