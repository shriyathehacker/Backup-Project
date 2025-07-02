def modExponent(a, b, n): #a^b mod n
    if b == 0:
        return 1
    elif b & 1 == 1:
        return (a * modExponent(a, b-1, n)) % n
    else:
        _ = modExponent(a, b // 2, n)
        return (_ * _) % n
    
def millerRabin(prime):
    if prime == 2:
        return True
    if prime == 1 or prime == 0:
        return False
    
    l = []
    power = prime - 1
    
    while power & 1 == 0:
        l.append(modExponent(2, power, prime))
        power = power // 2

    l.append(modExponent(2, power, prime))
        
    if l[0] == 1:
        for i in range(len(l) - 1):
            if l[i] == 1:
                if l[i + 1] in [1, prime - 1]:
                    pass
                else:
                    return False
                
        return True

    else:
        return False
    
_ = int(input())

for i in [int(x) for x in input().split()]:
    a = i ** 0.5
    if a == int(a):
        if millerRabin(int(a)):
            print("YES")
        else:
            print("NO")
    else:
        print("NO")