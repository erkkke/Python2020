import re
a = str(input())
result = re.findall(r'^\b[A, a][L, l][M, m][A, a][T, t][Y, y]\b', a)

print(len(result))
