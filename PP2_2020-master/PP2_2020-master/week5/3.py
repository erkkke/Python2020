import re
# pattern = r'(Порядковый номер чека)(.*)'
# pattern = r"(Стоимость)\n{1}(.*)"

pattern = r'(.*)\n{1}(.*)\n{1}(.*)\n{1}(Стоимость)\n{1}(.*)'

f = open('raw.txt', 'r')
text = f.read()

result = re.finditer(pattern, text)
for it in result:
    print(it.group(1), "=", it.group(2), "=", it.group(5))

print(result)