import cv2
import dlib
from matplotlib import pyplot as plt


detector = dlib.get_frontal_face_detector()

image_path = '../test/test_image_2.jpg'
image = cv2.imread(image_path)

grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = detector(grey_image)

for face in faces:
    x, y, w, h = face.left(), face.top(), face.right(), face.bottom()
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image_rgb)
plt.show()