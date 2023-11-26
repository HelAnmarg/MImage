import os
import PySimpleGUI as sg
from image_utils import open_image, mirror_image, save_image
import cv2
import filecmp

def show_image_diff(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    diff = cv2.absdiff(img1, img2)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)

    diff_window_layout = [
        [sg.Image(filename=image1, key="image1"), sg.Image(filename=image2, key="image2")],
        [sg.Button("Зробити копію", key="copy_button", size=(20, 2), button_color=("white", "#25C8C2")),
         sg.Button("Замінити", key="replace_button", size=(20, 2), button_color=("white", "#25C8C2")),
         sg.Button("Відмінити", key="cancel_button", size=(20, 2), button_color=("white", "#25C8C2"))]
    ]

    diff_window = sg.Window("Порівняння зображень", diff_window_layout, finalize=True)

    while True:
        event, _ = diff_window.read()

        if event == sg.WINDOW_CLOSED or event == "cancel_button":
            diff_window.close()
            break
        elif event == "copy_button":
            diff_window.close()
            return "Зробити копію"
        elif event == "replace_button":
            diff_window.close()
            return "Замінити"

layout = [
    [sg.Text("Введіть шлях до зображення:", background_color="#FCFD7F", text_color="black"),
     sg.InputText(key="image_path"), sg.FileBrowse(button_color=("white", "#25C8C2"), target=(sg.ThisRow, -1),
                                                   pad=((10, 5), 10))],
    [sg.Button("Відзеркалити і зберегти", size=(30, 2), button_color=("white", "#25C8C2"))],
    [sg.Text("", size=(100, 3), key="output_message", background_color="#FCFD7F", text_color="black")]
]

window = sg.Window("Відзеркалення зображення", layout, size=(640, 480), finalize=True, background_color="#FCFD7F")

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Відзеркалити і зберегти":
        image_path = values["image_path"]
        original_img = open_image(image_path)
        if original_img:
            mirrored_img = mirror_image(original_img)
            if mirrored_img:
                original_dir, original_filename = os.path.split(image_path)

                mirrored_dir = os.path.join(original_dir, "mirrored")
                mirrored_path = os.path.join(mirrored_dir, original_filename)
                if os.path.exists(mirrored_path):
                    files_are_equal = filecmp.cmp(image_path, mirrored_path)
                    if not files_are_equal:
                        action = show_image_diff(image_path, mirrored_path)
                        if action == "Зробити копію":
                            i = 1
                            while os.path.exists(os.path.join(mirrored_dir, f"{os.path.splitext(original_filename)[0]}_{i}{os.path.splitext(original_filename)[1]}")):
                                i += 1
                            original_filename = f"{os.path.splitext(original_filename)[0]}_{i}{os.path.splitext(original_filename)[1]}"
                        elif action == "Замінити":
                            os.remove(mirrored_path)
                        else:
                            continue

                saved_path = save_image(mirrored_img, original_dir, original_filename)
                if saved_path:
                    window["output_message"].update(f"Зображення {original_filename} відзеркалено та збережено в {saved_path}")

window.close()