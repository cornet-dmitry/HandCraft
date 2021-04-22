def convert_to_binary(image):
    file = open(image, 'rb')
    image = file.read()
    return image