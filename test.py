

set1 = set()
set2 = set(range(11, 20))
set3 = set(range(21, 30))
set1.update(set2)
print(set1)

set1.update(set3)
print(set1)