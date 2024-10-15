import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def try_mkdir(path):
    try:
        os.mkdir(path)
        bail(f"Info: Pasta de evidências criada em '{path}'.")
    except FileExistsError:
        pass


def list_files_in(path):
    try:
        all_files = os.scandir(path)
    except NotADirectoryError:
        bail("Erro: caminho informado não é uma pasta.")
    except FileNotFoundError:
        bail("Erro: caminho informado não existe.")

    receipt_files = []

    for one_file in all_files:
        if one_file.name.endswith(".png"):
            receipt_files.append(one_file)
        elif one_file.name.endswith(".jpg"):  # FIXME: JpEg eXiStS
            receipt_files.append(one_file)
        elif one_file.name.endswith(".bmp"):
            receipt_files.append(one_file)

    receipt_files.sort(key=lambda x: x.name.replace(".", ""))

    return receipt_files


def create_empty_page():
    a4_width = 2480
    a4_height = 3508

    return Image.new(mode="RGB", size=(a4_width, a4_height), color=(255, 255, 255))


def draw_logo(page):
    logo_font = ImageFont.truetype(font="Arial Bold.ttf", size=100)
    draw_sheet.text((100, 100), "X", anchor="lt", fill=(0, 0, 0), font=logo_font)
    draw_sheet.text((263, 100), "X", anchor="lt", fill=(0, 0, 0), font=logo_font)

    mark_font = ImageFont.truetype(font="Arial Bold.ttf", size=40)
    draw_sheet.text((655, 100), "®", anchor="lt", fill=(0, 0, 0), font=mark_font)


def draw_pagenum(page, page_num, total_pages):
    font = ImageFont.truetype(font="Arial Bold.ttf", size=30)
    draw_sheet.text((2380, 3408), f"Pág. {page_num} de {total_pages}", anchor="rs", fill=(0, 0, 0), font=font)


def bail(msg):
    print(msg)
    # input("Pressione Enter para encerrar.")
    sys.exit()


os.system('cls||clear')

DESIRED_WIDTH = 2000
DESIRED_HEIGHT = 1100

try:
    src_path = sys.argv[1]
except IndexError:
    src_path = input(f"Digite o caminho onde estão salvas as evidências: ")

list_of_files = list_files_in(src_path)

if len(list_of_files) < 1:
    bail("Erro: caminho informado não possui arquivos de imagem válidos.")

while True:
    answer = input(f"Padronizar largura das imagens ({DESIRED_WIDTH}px)? (s/n): ")
    if answer.lower() == "s":
        normalize_size = True
        break
    elif answer.lower() == "n":
        normalize_size = False
        break

base_page = create_empty_page()
final_pdf = []
num_pages = round(len(list_of_files) / 2)

for num, file in enumerate(list_of_files):
    evidence_number = file.name[:-4]  # FIXME: this assumes a 3 letter extension, but JpEg eXiStS
    page = (num + 2) // 2
    quadrant = 1 if (num % 2) == 0 else 3

    with Image.open(os.path.join(src_path, file.name)) as screen_print:

        if normalize_size:
            # Resize all images to the desired width.
            aspect_ratio = screen_print.height / screen_print.width
            new_height = round(DESIRED_WIDTH * aspect_ratio)
            screen_print = screen_print.resize((DESIRED_WIDTH, new_height), resample=Image.Resampling.LANCZOS)
        else:
            # Resize only images that are larger than the page.
            screen_print.thumbnail((DESIRED_WIDTH, DESIRED_HEIGHT), resample=Image.Resampling.LANCZOS)

        if quadrant == 1:
            base_page = create_empty_page()

        distance = 100 if quadrant == 1 else -100
        box_width = round((base_page.width / 2) - (screen_print.width / 2))
        box_height = round((base_page.height / 4) * quadrant + distance - (screen_print.height / 2))
        box_pos = (box_width, box_height)

        draw_sheet = ImageDraw.Draw(base_page)

        if quadrant == 1:
            draw_logo(draw_sheet)
            draw_pagenum(draw_sheet, page, num_pages)

        text_font = ImageFont.truetype(font="Arial Bold.ttf", size=50)
        text_width = round(base_page.width / 2)
        text_height = box_height - 50
        text_pos = (text_width, text_height)
        draw_sheet.text(text_pos, evidence_number, anchor="ms", fill=(0, 0, 0), font=text_font)

        line_width = 3
        dimensions = (box_width - line_width,
                      box_height - line_width,
                      box_width + screen_print.width + line_width,
                      box_height + screen_print.height + line_width)
        draw_sheet.rectangle(dimensions, outline=(0, 0, 0), width=line_width * 2)

        base_page.paste(screen_print, box_pos)

        if (quadrant == 3) or ((num + 1) == len(list_of_files)):
            final_pdf.append(base_page)


dst_path = Path.home().joinpath("Desktop", "Evidências.pdf")

final_pdf[0].save(dst_path, "PDF", resolution=100.0, save_all=True, append_images=final_pdf[1:])

print(f"PDF criado em '{dst_path}'.")
