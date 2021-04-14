import time
import cv2
import keyboard


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

        if keyboard.is_pressed(' '):    # take picture and save it if space is pressed
            img_name = 'img/takenPicture.jpg'
            print(img_name + " written to img/")
            if not cv2.imwrite(img_name, frame):
                raise Exception("Could not write image")
            time.sleep(.2)
            break
    camera.release()
    cv2.destroyWindow("Camera")


if __name__ == "__main__":
    takePictureAndSave()
