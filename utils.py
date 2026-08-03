import cv2
import numpy as np

def preprocess_image(image):

    # image is a grayscale NumPy array

    # Invert colors (white digit on black background)
    image = 255 - image

    # Threshold
    _, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)

    # Find all white pixels
    coords = cv2.findNonZero(thresh)

    if coords is None:
        return np.zeros((1,28,28,1), dtype=np.float32)

    # Crop digit
    x, y, w, h = cv2.boundingRect(coords)
    digit = thresh[y:y+h, x:x+w]

    # Keep aspect ratio
    h1, w1 = digit.shape

    if h1 > w1:
        new_h = 20
        new_w = int(w1 * 20 / h1)
    else:
        new_w = 20
        new_h = int(h1 * 20 / w1)

    digit = cv2.resize(digit, (new_w, new_h))

    # Create 28×28 black image
    canvas = np.zeros((28,28), dtype=np.uint8)

    x_offset = (28-new_w)//2
    y_offset = (28-new_h)//2

    canvas[y_offset:y_offset+new_h,
           x_offset:x_offset+new_w] = digit

    canvas = canvas.astype("float32") / 255.0

    canvas = canvas.reshape(1,28,28,1)

    return canvas