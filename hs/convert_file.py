f = open('high_schools_california.txt', 'r')
st = ""
for line in f.readlines():
	st = st + "\"" + line + "\", "
print(st)
