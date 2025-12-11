"""Analysis of the provided code
The code tries to model the process of deleting numbers from a list according to the rules:
We start with the smallest number (1).
We look for the next number (s+1) in the list.
If it is to the right, we delete it and continue.
If it is to the left, this ends the round, and we start a new one.
The problem with the code:
numbers.index(s) works in O(n) time — it looks for the index in the list.
numbers.pop(index) also works in O(n) time for an arbitrary index.
For large n (for example, 100000) this results in O(n²), which is very slow.
Optimal solution
The key idea: do not model the deletion, but simply count how many times the next number is to the left of the current one.
Algorithm:
Create a mapping pos[number] = index in the original list.
Go through the numbers from 1 to n.
If the current position is less than the previous one (the number is in reverse order relative to the original order),
 then this is the start of a new round.
Number of rounds = 1 + number of times pos[i] < pos[i-1].
"""

def count_rounds(numbers):
    n = len(numbers)
    pos = [0] * (n + 1)
    for i, num in enumerate(numbers):
        pos[num] = i

    round = 1

    for i in range(2, n + 1):
        if pos[i] < pos[i - 1]:
            round += 1
    return round

if __name__ == "__main__":
    print(count_rounds([1, 2, 3, 4])) # 1
    print(count_rounds([1, 3, 2, 4])) # 2
    print(count_rounds([4, 3, 2, 1])) # 4
    print(count_rounds([1])) # 1
    print(count_rounds([2, 1, 4, 7, 5, 3, 6, 8])) # 4

    n = 10**5
    numbers = list(reversed(range(1, n+1)))
    print(count_rounds(numbers)) # 100000