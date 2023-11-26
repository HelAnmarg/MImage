import os
import PySimpleGUI as sg
import cv2
from image_utils import open_image, mirror_image, save_image, show_image_diff
import filecmp

def main():
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
                    handle_mirror_action(image_path, mirrored_img)

    window.close()

def handle_mirror_action(original_path, mirrored_img):
    original_dir, original_filename = os.path.split(original_path)
    mirrored_dir = os.path.join(original_dir, "mirrored")
    mirrored_path = os.path.join(mirrored_dir, original_filename)

    if os.path.exists(mirrored_path):
        files_are_equal = filecmp.cmp(original_path, mirrored_path)

        if not files_are_equal:
            action = show_image_diff(original_path, mirrored_path)
            handle_diff_action(action, original_filename, mirrored_dir)
            return

    saved_path = save_image(mirrored_img, original_dir, original_filename)

    if saved_path:
        sg.popup_ok(f"Зображення {original_filename} відзеркалено та збережено в {saved_path}")

def handle_diff_action(action, original_filename, mirrored_dir):
    if action == "Зробити копію":
        i = 1

        while os.path.exists(os.path.join(mirrored_dir, f"{os.path.splitext(original_filename)[0]}_{i}{os.path.splitext(original_filename)[1]}")):
            i += 1

        original_filename = f"{os.path.splitext(original_filename)[0]}_{i}{os.path.splitext(original_filename)[1]}"

    elif action == "Замінити":
        os.remove(mirrored_path)

    else:
        return

    save_image(mirrored_img, mirrored_dir, original_filename)

if __name__ == "__main__":
    main()
