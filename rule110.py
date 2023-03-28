import sys

def rule(rule = 110, n = 110):
    x = 1
    for i in range(n):
        print(' ' * (n - i) + ''.join(('@' if i == '1' else ' ' for i in bin(x)[2:])))

        j = 0
        y = 0
        x <<= 1
        while x:
            y += (2 ** j) * ((rule & (2 ** (x & 7))) > 0)
            x >>= 1
            j += 1
        x = y

if __name__ == "__main__":
    try:    rule(110, int(sys.argv[1]))
    except: rule(110, 110)