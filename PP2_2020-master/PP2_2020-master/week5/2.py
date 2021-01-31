import re

pattern = r"\n{1}(?P<raw_count>.*)\n{1}(?P<price>.*)\n{1}(Стоимость)\n{1}(?P<price2>.*)"


f = open('row.txt', 'r')
text = f.read()

print(re.search(pattern, text).group("raw_count"))
