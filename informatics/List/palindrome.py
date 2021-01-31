def isPalindrome(a):
    b = a[::-1]
    if a == b:
        return 'yes'
    else: 'no'

print(isPalindrome(input()))

