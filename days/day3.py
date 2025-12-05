"""
Day 3. A persistent counter solves the joltage problem. Solved by creating a list of digits and comparing
the digit. You then use a sliding window pointer to keep track of which digit you are comparing against. You
have to be careful though as you run out of room for using digits from the bank as if you pick one, you need to make
sure that there are enough consecutive entries in the bank to then fill the rest of the digits. Resetting anything to the
right also ensures you don't improperly use a digit in places you shouldn't.
"""
from utils import puzzle


@puzzle
def part1(puzzle_input):
    total = 0
    for bank in puzzle_input:
        first, second = 0, 0
        for i, battery in enumerate(bank):
            val = int(battery)
            if val > first and i != len(bank) - 1:
                first = val
                second = 0
            elif val > second:
                second = val
        total += int(str(first) + str(second))
        print(f'Bank: {bank}, max joltage:{int(str(first) + str(second))}')
    print(total)

@puzzle
def part2(puzzle_input):
    total = 0
    for bank in puzzle_input:
        max_digits = [0] * 12
        for i, battery in enumerate(bank):
            # You can only populate digits if you have enough consecutive batteries to then also fill the 12 digit
            # number. This means you only iterate batteries you have room with the window closing as you iterate.
            left = max(0, len(max_digits) - (len(bank) - i))
            val = int(battery)
            while left < len(max_digits):
                if val > max_digits[left]:
                    max_digits[left] = val
                    if left < len(max_digits) - 1:
                        # Must reset any digits to the right as taking a digit at this index means that
                        # the joltage will always increase and you will therefore need to take the next
                        # digit you find on the right as well.
                        for j in range(left + 1, len(max_digits)):
                            max_digits[j] = 0
                    break
                left += 1
        joltage = int("".join([str(digit) for digit in max_digits]))
        total += joltage
        print(f'Bank: {bank}, max joltage:{joltage}')
    print(total)



if __name__ == '__main__':
    part2()