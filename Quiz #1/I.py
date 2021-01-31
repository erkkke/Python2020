import re
l1, l2 = [], []
for i in str(input()):    
    l1.append(i)
for i in  str(input()):
    l2.append(i)
if sorted(l1) == sorted(l2):
    print("Anagram")
else:
    print("Not anagram")