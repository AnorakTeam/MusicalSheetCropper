from email.mime import image
import os
import re
import img2pdf


def num_sort(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))[0]


directory_path = "C:\\Users\\UFPS\\Downloads\\merry goes high on life or som idk\\merry goes high on life or som idk\\cropped"

# path to all the 
image_files = [f"{directory_path}\\{x}" for x in os.listdir(directory_path) if x.endswith(".png")]

image_files.sort(key=num_sort)

for i in image_files:
    print(i)

pdf_data = img2pdf.convert(image_files)

# Write the PDF content to a file
with open("output.pdf", "wb") as file:
    file.write(pdf_data)
