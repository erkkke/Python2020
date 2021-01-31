list1 = [2,6,3,1,5]

for i in list1:
    print(i)


it = iter(list1)
while True:
    try:                      # Если будет ошибка переводит на except
        i = next(it)
        print(i)
    except StopIteration:     # Используется только при ошибке и прекращает цикл
        break