h, w = img.shape[:2]
#img = cv.resize(img, (w*2, h*2))
# mejor guardarlo en un json
# (h, w) = image_rectangulos.shape[:2]
# percentage = 960 / w
# if h* percentage >= 1080:
#     percentage = 1
# image_rectangulos = cv.resize(image_rectangulos, (int(960),int(h*percentage)))
image_rectangulos = cv.resize(image_rectangulos, (w, h))
color_img = cv.resize(color_img, (w, h))