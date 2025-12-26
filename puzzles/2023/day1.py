"""
An interesting two pointer problem. Because of the ability to have numbers contained in other numbers such as threeight,
you can't just string replace. Also rather than having a lookup dictionary, you can simply just move two pointers across
and keep looking at the substring. If you hit a digit, check to see if the substring is a number. If it is, move the
pointers. If the substring is a word, increment the left bound in order to check for numbers inside numbers.
"""
from utils import puzzle


_CHOICES = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def solve_single(line: str) -> int:
    s = ""
    i, j = 0, 0

    # Want to check all substrings
    while j < (len(line) + 1) and i < (len(line) + 1):
        # If the current char is a digit, add it but first check to see if the previous substring is a valid number and
        # append that before the current digit.
        if j < len(line) and line[j].isdigit():
            if i != j:
                if val := convert_to_digit(line[i:j]):
                    s += str(val)
            s += line[j]
            # Moves both bounds past the digit that was appended.
            i = j + 1
            j = i
        # Check to see if the substring is a valid number. If so, append the value and move the lower bound. Only this
        # is done in order to account for words inside of words.
        elif val := convert_to_digit(line[i:j]):
            s += str(val)
            i += 1
        # Check to see if the current substring could be a number. If so then move the upper bound to build the word.
        elif any(choice.startswith(line[i:j]) for choice in _CHOICES):
            j += 1

        # If not, then the left most character we know to be invalid, increment.
        else:
            i += 1

    return int(s[0] + s[-1])









@puzzle
def part2(puzzle_input):
    val = 0
    for line in puzzle_input:
        single_val = solve_single(line)
        print(f'Line: {line}, val: {single_val}')
        val += single_val
    print(val)


def convert_to_digit(s) -> int | None:
    s = s.lower()
    if s == 'one':
        return 1
    elif s == 'two':
        return 2
    elif s == 'three':
        return 3
    elif s == 'four':
        return 4
    elif s == 'five':
        return 5
    elif s == 'six':
        return 6
    elif s == 'seven':
        return 7
    elif s == 'eight':
        return 8
    elif s == 'nine':
        return 9
    else:
        return None



if __name__ == '__main__':
    part2()