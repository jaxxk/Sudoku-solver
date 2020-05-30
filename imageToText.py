import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'assets\Tesseract-OCR\tesseract.exe'
from PIL import Image

img = Image.open('assets/Images/testImages/test.png')

# Settings
psmSetting = 10 # 6,7,10
dimOfGrid = (img.width + img.height) // 2 # assume this as the size of 9x9 grid for now
padding = dimOfGrid // 100 + 3 # number of pixels to ignore from edges
print("A side of a grid is " + str(dimOfGrid) + "px long; choosing padding as " + str(padding) + "px\nAttempted Conversion:\n\n")

def printHelper(s):
	if not s:
		return "\\"
	return s

for x in range(9):
	for y in range(9):
		# calculate boundaries for each of the 81 squares
		tleft = int(img.width * y / 9) + padding
		tright = int(img.height * x / 9) + padding
		bleft = int(img.width * (y + 1) / 9) - padding
		bright = int(img.height * (x + 1) / 9) - padding

		tempImg = img.crop((tleft, tright, bleft, bright))
		tempImg.save('boxes/{}_{}.png'.format(x, y), quality = 100)
		tempNum = tess.image_to_string(tempImg, lang='eng', config='--psm {}'.format(psmSetting))
		num = ''.join([i for i in tempNum if i.isdigit()]) # eliminate any non-digit characters from string
		print("\t" + printHelper(num), end = "")
	print("\n\n")



#txt = tess.image_to_string(img, lang='eng', config='--psm 10')

# from lxml import html
# import requests

# page = requests.get('http://sudoku9x9.com')
# tree = html.fromstring(page.content)

# print("Generated Sudoku Board:\n")

# """
# for x in range(80):
# 	list = tree.xpath('//*[@id="cell{}"]//text()'.format(x))
# 	if list:
# 		print(list[0])
# """

# i = 0

# for x in range(9):
# 	for y in range(9):
# 		list = tree.xpath('//*[@id="cell{}"]//text()'.format(i))
# 		if list:
# 			print("  " + list[0], end = "")
# 		else:
# 			print("  " + "\\", end = "")
# 		i += 1
# 	print("")
	

# #print(page.text)