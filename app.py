import cv2
import PIL
from PIL import Image
import time
import keyboard

# the [x, y] for each right-click event will be stored here
left_clicks = list()


def getRGBValue():
    print("Coordinates:" + str(left_clicks))
    image = PIL.Image.open(path_image)
    image_rgb = image.convert("RGB")
    rgb_pixel_value = image_rgb.getpixel(left_clicks[0])
    print("Pixel 1 RGB:" + str(rgb_pixel_value))
    YUVfromRGB(rgb_pixel_value[0], rgb_pixel_value[1], rgb_pixel_value[2])
    rgb_pixel_value2 = image_rgb.getpixel(left_clicks[1])
    print("Pixel 2 RGB:" + str(rgb_pixel_value2))
    YUVfromRGB(rgb_pixel_value2[0], rgb_pixel_value2[1], rgb_pixel_value2[2])


def YUVfromRGB(r, g, b):
    y = r * .299000 + g * .587000 + b * .114000
    u = r * -.168736 + g * -.331264 + b * .500000 + 128
    v = r * .500000 + g * -.418688 + b * -.081312 + 128
    print("YUV: (" + str(y) + " " + str(u) + " " + str(v) + ")")


# this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):
    # right-click event value is 2
    if event == 1:
        global left_clicks

        # store the coordinates of the right-click event
        left_clicks.append((x, y))

        # this just verifies that the mouse data is being collected
        # you probably want to remove this later
        global img
        radius = 3
        thickness = -1
        if len(left_clicks) % 2 == 1:
            img = cv2.imread("img/takenPicture.jpg")
            center_coordinates = (left_clicks[0])
            color = (255, 0, 0)
            img = cv2.circle(img, center_coordinates, radius, color, thickness)
            cv2.imshow('image', img)
        if len(left_clicks) % 2 == 0:
            center_coordinates = (left_clicks[1])
            color = (255, 0, 0)
            img = cv2.circle(img, center_coordinates, radius, color, thickness)
            cv2.imshow('image', img)

        if len(left_clicks) == 2:
            getRGBValue()
            left_clicks.clear()


def takePictureAndSave():
    global frame
    cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if camera.isOpened():  # try to get the first frame
        return_value, frame = camera.read()

    while cv2.getWindowProperty('Camera', 0) >= 0:  # show image as long as window is open
        cv2.imshow("Camera", frame)
        return_value, frame = camera.read()
        keyCode = cv2.waitKey(1)

        if keyCode == 27:
            break

        if keyboard.is_pressed(' '):  # take picture and save it if space is pressed
            img_name = 'img/takenPicture.jpg'
            print(img_name + " written to img/")
            if not cv2.imwrite(img_name, frame):
                raise Exception("Could not write image")
            time.sleep(.2)
            break
    camera.release()
    cv2.destroyWindow("Camera")


def openImage():
    global path_image
    path_image = "img/takenPicture.jpg"
    global img
    img = cv2.imread(path_image, None)
    scale_width = 640 / img.shape[1]
    scale_height = 480 / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', window_width, window_height)

    # set mouse callback function for window
    cv2.setMouseCallback('image', mouse_callback)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    takePictureAndSave()
    openImage()
