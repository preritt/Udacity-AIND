# a = tuple()
# print a
# print set(a)
# a = {a}

# a.add((1,1))
# print tuple(a)
# print a.add((2,3))
# print tuple(a)
# print a.add((2,32))
# print tuple(a)
# print a.add((22,32))
# print tuple(a)
# print "="*50
# print set(a)
# print tuple(set(a))
a = (1,1)
print a
print tuple(a)
print set(tuple(set(a)))
print set([(1,1)])