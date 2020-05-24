from lxml import html
import requests

page = requests.get('http://sudoku9x9.com')
tree = html.fromstring(page.content)

print("Generated Sudoku Board:\n")


# for x in range(80):
# 	list = tree.xpath('//*[@id="cell{}"]//text()'.format(x))
# 	if list:
# 		print(list[0])


i = 0
arr = []

for x in range(9):
	for y in range(9):
		list = tree.xpath('//*[@id="cell{}"]//text()'.format(i))
		if list:
			print("  " + list[0], end = "")
			arr.append(list[0])
		else:
			print("  " + "\\", end = "")
			arr.append(" ")
		i += 1
	print("")
	

print(arr)