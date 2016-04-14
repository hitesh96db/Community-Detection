fp = open("acl-metadata_processed.txt")
target = open("acl-metadata_new.txt", 'w')
lines=fp.readlines()
for i in range (0,125933,60):
	print lines[i], lines[i+1], lines[i+2], lines[i+3], lines[i+4], lines[i+5]
	target.write(lines[i]+ lines[i+1] +lines[i+2] +lines[i+3] +lines[i+4]+ lines[i+5])
fp.close()
