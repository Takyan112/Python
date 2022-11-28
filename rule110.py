rule = 110
n = 110

x = 1
for i in range(n):
	print(f"{''.join(('@' if i == '1' else ' ' for i in bin(x)[2:])):>{n}}")

	j = 0
	y = 0
	x <<= 1
	while x:
		y += (2 ** j) * ((rule & (2 ** (x & 7))) > 0)
		x >>= 1
		j += 1
	x = y
	
	