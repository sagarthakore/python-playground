def fib_to(n):
    fibs = [0, 1]
    for i in range(2, n+1):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs



input_num = int(input("Enter a number: "))
fibnums = fib_to(input_num)
for num in fibnums:
    print(num)