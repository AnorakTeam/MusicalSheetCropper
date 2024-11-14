from PIL import Image


def crop_sheet(im, left, top, right, bottom):
    im1 = im.crop((left, top, right, bottom))
    
    # optional, just to see how it cropped
    # im1.show()
    return im1


def save_image_inside_cropped(im:Image, name:str, extension:str):
    im.save(f"cropped/{name}.{extension}")


def cut_first_half_sheet(im:Image) -> Image:
    # Location of the image (has to be in the same folder to work without route)
    # Size of the image in pixels 
    # (size of original image)
    # (This is not mandatory)
    # width, height = im.size

    # Setting the points for cropped image
    left = 0
    top = 215
    right = im.size[0]
    bottom = im.size[1] // 2 -100
    return crop_sheet(im, left, top, right, bottom)


def cut_second_half_sheet(im:Image) -> Image:
    # Setting the points for cropped image
    left = 0
    top = im.size[1] // 2 
    right = im.size[0]
    bottom = im.size[1] - 325

    return crop_sheet(im, left, top, right, bottom)


def cut_merry_sheets_in_half():
    # number of images, ig: merry go round has 21 images in this folder.
    number_of_images = 6
    
    for i in range(1, number_of_images):
        
        im = Image.open(f"merry{i+1}.png")
        
        top_part:Image = cut_first_half_sheet(im)
        bottom_part:Image = cut_second_half_sheet(im)
        
        top_part.save(f"cropped/merryTop{i+1}.png")
        bottom_part.save(f"cropped/merryBottom{i+1}.png")


def cut_violin_parts(im:Image) -> None:
    left = 0
    top = 215
    right = im.size[0]
    bottom = int(im.size[1] * 0.15)
    return crop_sheet(im, left, top, right, bottom)


def create_violin_pages(number_of_images:int, max_width:int, max_height:int) -> None:
    page_number = 1
    current_cropped_img = 2 # TODO: change this back to 1, since we're not taking in count the number 1

    while number_of_images > 0:
        canva = Image.new("RGB", (max_width, max_height), (250, 250, 250))
        
        current_height = int(max_height * 0.025) # a little bit of padding at the top of the canvas
        space_left = max_height - current_height - 20
        heigth_of_this_img = 0

        while number_of_images > 0 and heigth_of_this_img < space_left:
            img = Image.open(f"cropped/violin{current_cropped_img}.png")
            canva.paste(img, (0, current_height))
            heigth_of_this_img = img.size[1] + 20

            current_cropped_img += 1
            current_height += img.size[1] + 20 # 10 pixels of padding between each img
            space_left = max_height - current_height - 20
            print(f"there are {space_left} pixels left")
            number_of_images -= 1

        save_image_inside_cropped(canva, f"violinPage{page_number}", "png")
        page_number += 1







if __name__ == "__main__":
    number_of_images = 10
    
    for i in range(1, number_of_images+1):
        
        im = Image.open(f"merry{i+1}.png")
        im = cut_violin_parts(im)
        save_image_inside_cropped(im, f"violin{i+1}", "png")

    im = Image.open("merry2.png")

    create_violin_pages(number_of_images, im.size[0], im.size[1])



