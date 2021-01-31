a = {'abracadabra'}
l = [1, 3, 4, 7, 7, 1]
g = set(l)
g.add(12)
g.update({1, 2, 3,4, 10, 'hello'})
g.discard(10)
print(g)