for i in range(10):
    for j in ['a', 'b', 'c']:
        output = 'ok'+j
        if j == 'b':
            break
    print(output)
