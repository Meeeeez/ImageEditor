import cv2
import PIL
from PIL import Image
import time
import keyboard
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile


def get_rgb_value(clicks):
    # print("Coordinates:" + str(left_clicks))
    image = PIL.Image.open(path_image)
    image_rgb = image.convert("RGB")
    white_rgb = image_rgb.getpixel(clicks[0])
    print("Pixel 1 RGB:" + str(white_rgb))
    yuv_from_rgb(white_rgb[0], white_rgb[1], white_rgb[2])
    white_balance(white_rgb)


def rgb_to_y():
    y_img = Image.open("img/takenPictureY.jpg")
    y_pixels = y_img.load()
    for i in range(y_img.size[0]):  # for every pixel:
        for j in range(y_img.size[1]):
            y_red = y_pixels[i, j][0]
            y_green = y_pixels[i, j][1]
            y_blue = y_pixels[i, j][2]
            y = y_red * .299000 + y_green * .587000 + y_blue * .114000
            y = int(round(y))
            y_pixels[i, j] = (y, y, y)
    print("test")
    y_img.save("img/yPicture.jpg")
    # open_image("img/yPicture.jpg", "Y Image")


def yuv_from_rgb(r, g, b):
    y = r * .299000 + g * .587000 + b * .114000
    u = r * -.168736 + g * -.331264 + b * .500000 + 128
    v = r * .500000 + g * -.418688 + b * -.081312 + 128


# this function will be called whenever the mouse is left-clicked
def mouse_callback(event, x, y, flags, params):
    # left-click event value is 1
    if event == 1:
        left_clicks = list()
        # store the coordinates of the left-click event
        left_clicks.append((x, y))

        # global img
        # radius = 3
        # thickness = -1

        # if len(left_clicks) % 2 == 0:
        #    center_coordinates = (left_clicks[1])
        #    color = (255, 0, 0)
        #    img = cv2.circle(img, center_coordinates, radius, color, thickness)
        #    cv2.imshow('image', img)

        # if len(left_clicks) == 1:
        get_rgb_value(left_clicks)
        left_clicks.clear()
        rgb_to_y()
        cv2.destroyWindow("Taken Image")

        # rgb_to_u()


def take_picture_and_save():
    global frame
    cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if camera.isOpened():  # try to get the first frame
        return_value, frame = camera.read()

    while cv2.getWindowProperty('Camera', 0) >= 0:  # show image as long as window is open
        cv2.imshow("Camera", frame)
        return_value, frame = camera.read()
        key_code = cv2.waitKey(1)

        if key_code == 27:
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


def white_balance(white_rgb):
    img_to_change = Image.open("img/takenPicture.jpg")
    img_to_change.save("img/takenPictureY.jpg")
    pixels = img_to_change.load()  # create the pixel map
    for i in range(img_to_change.size[0]):  # for every pixel:
        for j in range(img_to_change.size[1]):
            img_red = pixels[i, j][0]
            img_green = pixels[i, j][1]
            img_blue = pixels[i, j][2]
            lum = (white_rgb[0] + white_rgb[1] + white_rgb[2]) / 3
            if white_rgb[0] == 0:
                white_rgb = (1, white_rgb[1], white_rgb[2])
            if white_rgb[1] == 0:
                white_rgb = (white_rgb[0], 1, white_rgb[2])
            if white_rgb[2] == 0:
                white_rgb = (white_rgb[0], white_rgb[1], 1)
            img_red = img_red * lum / white_rgb[0]
            img_green = img_green * lum / white_rgb[1]
            img_blue = img_blue * lum / white_rgb[2]

            pixels[i, j] = (int(img_red), int(img_green), int(img_blue))

    img_to_change.save("img/modifiedPicture.jpg")
    # open_image("img/modifiedPicture.jpg", "Modified Image")


def open_image(path, name):
    global path_image
    path_image = path
    global img
    img = cv2.imread(path_image, None)
    scale_width = 640 / img.shape[1]
    scale_height = 480 / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, window_width, window_height)
    if name == "Taken Image":
        # set mouse callback function for window
        cv2.setMouseCallback(name, mouse_callback)

    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def update_gui():
    pic = Image.open("img/takenPicture.jpg")
    pic = ImageTk.PhotoImage(pic)
    pic_label = tk.Label(image=pic)
    pic_label.image = pic
    pic_label.grid(column=1, row=0)


def gui():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)

    pic = Image.open("img/takenPicture.jpg")
    pic = ImageTk.PhotoImage(pic)
    pic_label = tk.Label(image=pic)
    pic_label.image = pic
    pic_label.grid(column=1, row=0)

    browse_text = tk.StringVar()
    browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: modified_image(), font="Raleway")
    browse_text.set("Modified Image")
    browse_btn.grid(column=1, row=3)

    browse_text = tk.StringVar()
    browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: y_image(), font="Raleway")
    browse_text.set("Y Image")
    browse_btn.grid(column=1, row=4)

    root.mainloop()


def modified_image():
    # pic
    pic = Image.open("img/modifiedPicture.jpg")
    pic = ImageTk.PhotoImage(pic)
    pic_label = tk.Label(image=pic)
    pic_label.image = pic
    pic_label.grid(column=2, row=0)
    pic_label.size()


def y_image():
    # pic
    pic = Image.open("img/yPicture.jpg")
    pic = ImageTk.PhotoImage(pic)
    pic_label = tk.Label(image=pic)
    pic_label.image = pic
    pic_label.grid(column=2, row=0)
    pic_label.size()


if __name__ == '__main__':
    take_picture_and_save()
    open_image("img/takenPicture.jpg", 'Taken Image')
    gui()