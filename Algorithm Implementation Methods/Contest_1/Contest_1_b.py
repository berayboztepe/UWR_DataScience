# for the rule of divisibility by 8, it is enough just to look max last 3 digit from subnumbers 

def main():
    num = input().strip()

    # checking for 1 digit nums
    for digit in num:
        if check_divisibility(int(digit)):
            print("YES")
            print(digit)
            return
    

    # checking for 2 digit nums
    for starting_digit in range(0, len(num) - 1):
        for ending_digit in range(starting_digit + 1, len(num)):
            sub_num = int(num[starting_digit] + num[ending_digit])
            if check_divisibility(sub_num):
                print("YES")
                print(sub_num)
                return
    
    # checking for 3 digit nums
    for starting_digit in range(0, len(num) - 2):
        for middle_digit in range(starting_digit + 1, len(num) - 1):
            for ending_digit in range(middle_digit + 1, len(num)):
                sub_num = int(num[starting_digit] + num[middle_digit] + num[ending_digit])
                if check_divisibility(sub_num):
                    print("YES")
                    print(sub_num)
                    return
                
    print("NO")
    return
                
def check_divisibility(num):
    return num % 8 == 0

if __name__ == "__main__":
    main()