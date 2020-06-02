from PIL import Image, ImageTk

def selectImage(x, y, value):
    imagePath = "assets/images/"
    colorVariant = ""
    if 2 < y and y < 6:
        colorVariant = "o"
        if 2 < x and x < 6:
            colorVariant = "e"
    else:
        colorVariant = "e"
        if 2 < x and x < 6:
            colorVariant = "o"

    return Image.open(imagePath + str(colorVariant) + str(value) + ".jpg")