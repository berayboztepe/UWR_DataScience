import timeit

def is_perfect(num):
    if num < 2:
        return False
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisors_sum == num

def perfect_imperative(n):
    perfect_numbers = []
    for num in range(2, n + 1):
        if is_perfect(num):
            perfect_numbers.append(num)
    return perfect_numbers

def perfect_comprehension(n):
    return [num for num in range(2, n + 1) if is_perfect(num)]

def perfect_functional(n):
    return list(filter(is_perfect, range(2, n + 1)))

n = 10000
print("Imperative:", perfect_imperative(n))
print("List Comprehension:", perfect_comprehension(n))
print("Functional:", perfect_functional(n))


print("--------------------------------------")
for n in [100, 500, 1000]:
    imp_time = timeit.timeit(lambda: perfect_imperative(n), number=100)
    composite_time = timeit.timeit(lambda: perfect_comprehension(n), number=100)
    functional_time = timeit.timeit(lambda: perfect_functional(n), number=100)
    print(f"n = {n} | Imperative: {imp_time:.3f} | Composite: {composite_time:.3f} | Functional: {functional_time:.3f}")
