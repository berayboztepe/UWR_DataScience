import random
import math

def generate_random_point():
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    return x, y

def is_in_circle(x, y):
    return x**2 + y**2 <= 1

def throw_dart():
    x, y = generate_random_point()
    return is_in_circle(x, y)

def approximate_pi(epsilon=0.000001, max_throws=1000000):
    total_throws = 0
    in_circle = 0

    while True:
        total_throws += 1
        if throw_dart():
            in_circle += 1

        calculated_pi = 4 * in_circle / total_throws

        print(f'pi = {calculated_pi} after {total_throws} throws')

        if abs(calculated_pi - math.pi) <= epsilon:
            print('calculated pi is close enough')
            print(f'(pi = {math.pi})')
            break
        if total_throws >= max_throws:
            print('max throws reached')
            break

approximate_pi()