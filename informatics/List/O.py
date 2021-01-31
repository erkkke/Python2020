lst = [0, 1, 2, 3, 5] # Начальный список
steps = 1 # Количество позиций для сдвига
lst = lst[steps:] + lst[:steps]
print(lst)