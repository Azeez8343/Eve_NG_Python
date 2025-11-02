# import os
# import sys

# with open("output_192-168-91-115_2025-02-22.txt", "r") as file:
#    lines = file.readlines()
#    word_search = "boot nxos bootflash:/nxos64-cs.10.2.3.F.bin"



# for row in lines:
   
#    if search_line = row.find(word_search)
#     print(search_line)
#     print('string exists in file')
#     print('line Number:', lines.index(row))
#    else:
#     print ('not found')



with open(r"output_192-168-91-115_2025-02-22.txt", 'r') as f:
	for index, line in enumerate(f):
		word_search = "boot nxos bootflash:/nxos64-cs.10.2.3.F.bin"
		# search string
		if 'word_search' in line:
			print('string found in a file')		 
			# don't look for next lines
			break
		
	print('string does not exist in a file')
