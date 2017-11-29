"""Program to find factorial of a number."""


def fact(n):
    """Return factorial."""
    if n == 1:
        return n
    else:
        return n*fact(n-1)


num = int(input("Enter the number to find factorial: "))
print(fact(num))
