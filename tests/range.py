indices = []
for x in range(9):
    indices += range(x * 10, x*10 + 9)

print indices


test = []
for x in range(90):
    if (x + 1) % 10 != 0:
        test.append(x)

print test
