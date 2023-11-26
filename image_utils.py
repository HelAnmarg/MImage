import os
import PySimpleGUI as sg
from PIL import Image

def open_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        sg.popup_error(f"Виникла помилка при відкритті зображення: {e}")
        return None

def mirror_image(img):
    try:
        mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        return mirrored_img
    except Exception as e:
        sg.popup_error(f"Виникла помилка при відзеркаленні зображення: {e}")
        return None

def save_image(img, output_dir, original_filename):
    try:
        mirrored_dir = os.path.join(output_dir, "mirrored")
        os.makedirs(mirrored_dir, exist_ok=True)

        full_path = os.path.join(mirrored_dir, original_filename)
        if os.path.exists(full_path):
            layout = [
                [sg.Text(f"Файл {original_filename} вже існує. Оберіть дію:")],
                [sg.Button("Зробити копію", size=(20, 2), button_color=("white", "#25C8C2")),
                 sg.Button("Замінити", size=(20, 2), button_color=("white", "#25C8C2")),
                 sg.Button("Відмінити", size=(20, 2), button_color=("white", "#25C8C2"))]
            ]
            choice_window = sg.Window("Конфлікт імен", layout, size=(560, 120), finalize=True)
            event, _ = choice_window.read()
            choice_window.close()
            if event == "Зробити копію":
                i = 1
                while os.path.exists(os.path.join(mirrored_dir, f"{os.path.splitext(original_filename)[0]}_{i}{os.path.splitext(original_filename)[1]}")):
                    i += 1
                original_filename = f"{os.path.splitext(original_filename)[0]}_{i}{os.path.splitext(original_filename)[1]}"
            elif event == "Замінити":
                os.remove(full_path)
            else:
                return None

        mirrored_path = os.path.join(mirrored_dir, original_filename)
        img.save(mirrored_path)
        return mirrored_path
    except Exception as e:
        sg.popup_error(f"Виникла помилка при збереженні зображення: {e}")
        return None
