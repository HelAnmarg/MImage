import os
import PySimpleGUI as sg
from image_utils import open_image, mirror_image, save_image

layout = [
    [sg.Text("Введіть шлях до зображення:", background_color="#FCFD7F", text_color="black"), sg.InputText(key="image_path"), sg.FileBrowse(button_color=("white", "#25C8C2"), target=(sg.ThisRow, -1), pad=((10, 5), 10))],
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
                saved_path = save_image(mirrored_img, original_dir, original_filename)
                if saved_path:
                    window["output_message"].update(f"Зображення {original_filename} відзеркалено та збережено в {saved_path}")

window.close()