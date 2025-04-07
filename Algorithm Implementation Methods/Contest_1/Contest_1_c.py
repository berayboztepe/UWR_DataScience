def flatten(xss):
    flat_list = []
    for xs in xss:
        for x in xs:
            flat_list.append(x)
    return flat_list
 
def divisors(n: int) -> list[int]:
    if n == 0:
        return [0]
    divisors = ({i, n // i} for i in range(1, int(n**0.5) + 1) if n % i == 0)
    flattened_result = flatten(divisors)
    return flattened_result

def count_frequencies(nums: list[int]) -> dict[int, int]:
    freq = {}
    for num in nums:
        if num in freq:
            freq[num] += 1
        else:
            freq[num] = 1
    return freq

def most_common(nums: list[int], n: int) -> tuple[int, int]:
    freq = count_frequencies(nums)
    return max(freq.items(), key=lambda x: x[1])

def solve(nums: list[int]) -> int:
    n = len(nums)
    half = (n + 1) // 2
    
    common_num, common_count = most_common(nums, n)
    if common_count >= half:
        return -1
    
    candidates = set()
    
    for i, num in enumerate(nums):
        diffs = [abs(num - x) for x in nums[i:]]
        divisors_counter = count_frequencies(flatten(map(divisors, diffs)))
        _same_num_count = divisors_counter.pop(0, 0)
        for divisor, count in sorted(divisors_counter.items(), key=lambda x: -x[1]):
            if count + _same_num_count < half:
                break
            candidates.add(divisor)
    
    return max(candidates)

if __name__ == "__main__":
    for _ in range(int(input())):
        _ = input()
        ans = solve(list(map(int, input().split())))
        print(ans)
