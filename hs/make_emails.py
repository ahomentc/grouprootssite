f = open('high_schools_california_filtered.txt', 'r')

school_counts = dict()

for line in f.readlines():
	line = line.rstrip('\n')
	acronym = ""
	for word in line.split(' '):
		acronym += word[0].upper()

	username = ""
	if acronym in school_counts:
		current_count = school_counts[acronym]
		new_count = int(current_count) + 1
		username = acronym + str(new_count)
		school_counts[acronym] = new_count
	else:
		school_counts[acronym] = 1
		username = acronym


	print(username + "@grouproots.com")

