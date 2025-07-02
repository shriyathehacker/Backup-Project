def toBinary(num):
    listA = []
    while num != 0:
        listA.append(num % 2)
        num = num // 2

    return "".join(listA[::-1])

print(toBinary(int(input())))