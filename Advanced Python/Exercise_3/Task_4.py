import timeit

def sum_of_divisors(num):
    return sum(i for i in range(1, num // 2 + 1) if num % i == 0)

def amicable_imperative(n):
    amicable_pairs = []
    for a in range(2, n + 1):
        b = sum_of_divisors(a)
        if b > a and b <= n:
            if sum_of_divisors(b) == a:
                amicable_pairs.append((a, b))
    return amicable_pairs

def amicable_comprehension(n):
    return [(a, b) for a in range(2, n + 1) for b in [sum_of_divisors(a)] 
            if b > a and b <= n and sum_of_divisors(b) == a]

def amicable_functional(n):
    return list(filter(lambda pair: sum_of_divisors(pair[1]) == pair[0],
                ((a, sum_of_divisors(a)) for a in range(2, n + 1) 
                 if sum_of_divisors(a) > a and sum_of_divisors(a) <= n)))

n = 1300
print("Imperative:", amicable_imperative(n))
print("List Comprehension:", amicable_comprehension(n))
print("Functional:", amicable_functional(n))

print("--------------------------------------")
for n in [1000, 2000, 3000]:
    imp_time = timeit.timeit(lambda: amicable_imperative(n), number=10)
    composite_time = timeit.timeit(lambda: amicable_comprehension(n), number=10)
    functional_time = timeit.timeit(lambda: amicable_functional(n), number=10)
    print(f"n = {n} | Imperative: {imp_time:.3f} | Composite: {composite_time:.3f} | Functional: {functional_time:.3f}")
