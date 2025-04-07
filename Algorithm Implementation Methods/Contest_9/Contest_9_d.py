# submit later

def find_switch_positions(arr, num_elements):
    positions = []
    for i in range(num_elements - 1):
        if arr[i] == 1 and arr[i + 1] == 0:
            positions.append(i)
    return positions

def challenges_in_school(num_elements, steps_limit, sequence):
    numeric_array = [0 if ch == 'L' else 1 for ch in sequence]

    max_steps = 0
    min_steps = 0
    contiguous_zeroes = 0
    last_min_steps = -1

    for i in range(num_elements - 1, -1, -1):
        if numeric_array[i] == 0:
            contiguous_zeroes += 1
        else:
            if contiguous_zeroes == 0:
                continue
            max_steps += contiguous_zeroes
            min_steps = max(contiguous_zeroes, last_min_steps + 1)
            last_min_steps = min_steps

    if steps_limit < min_steps or steps_limit > max_steps:
        print(-1)
        return

    is_in_min_steps_mode = False
    saved_positions = []

    for step in range(steps_limit):
        if not is_in_min_steps_mode:
            switch_positions = find_switch_positions(numeric_array, num_elements)

            switches_to_make = min(len(switch_positions), max_steps - steps_limit + step + 1)
            print(switches_to_make, end=' ')

            current_switch = 0
            while steps_limit - step - 1 < max_steps and current_switch < len(switch_positions):
                switch_index = switch_positions[current_switch]
                print(switch_index + 1, end=' ')
                numeric_array[switch_index] = 0
                numeric_array[switch_index + 1] = 1
                current_switch += 1
                max_steps -= 1

            if max_steps == steps_limit - step - 1:
                is_in_min_steps_mode = True
                saved_positions = find_switch_positions(numeric_array, num_elements)

        else:
            switch_index = saved_positions.pop()
            print(1, switch_index + 1)
            numeric_array[switch_index] = 0
            numeric_array[switch_index + 1] = 1

            if switch_index > 0 and numeric_array[switch_index - 1] == 1:
                saved_positions.append(switch_index - 1)
            if switch_index + 2 < num_elements and numeric_array[switch_index + 2] == 0:
                saved_positions.append(switch_index + 1)
        print()

if __name__ == "__main__":
    num_elements, steps_limit = map(int, input().split())
    sequence = input().strip()
    challenges_in_school(num_elements, steps_limit, sequence)
