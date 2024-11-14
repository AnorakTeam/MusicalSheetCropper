from typing import Tuple
from PIL import Image


def crop_sheet(im, left, top, right, bottom):
    """
    crops an image with the 4 coordinates in pixels, and returns the cropped version.
    """
    im1 = im.crop((left, top, right, bottom))
    
    # optional, just to see how it cropped
    # im1.show()
    return im1


def save_image_inside_cropped(im:Image, name:str, extension:str):
    """
    Saves the image in the cropped folder, with a given name and extensions (png, jpg, etc)
    """
    im.save(f"cropped/{name}.{extension}")


def cut_first_half_sheet(im:Image) -> Image:
    """
    Returns an image that contains only the first part of the arrangement 
    with the necessary padding.
    """
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
    """
    Returns an image that contains only the second part of the arrangement 
    with the necessary padding.
    """
    # Setting the points for cropped image
    left = 0
    top = im.size[1] // 2 
    right = im.size[0]
    bottom = im.size[1] - 325

    return crop_sheet(im, left, top, right, bottom)


def cut_merry_sheets_in_half():
    """
    Just an experiment, saves the first and second half of all the images inside cropped.
    """
    # number of images, ig: merry go round has 21 images in this folder.
    number_of_images = 6
    
    for i in range(1, number_of_images):
        
        im = Image.open(f"merry{i+1}.png")
        
        top_part:Image = cut_first_half_sheet(im)
        bottom_part:Image = cut_second_half_sheet(im)
        
        top_part.save(f"cropped/merryTop{i+1}.png")
        bottom_part.save(f"cropped/merryBottom{i+1}.png")


def cut_violin_parts(im:Image) -> Tuple:
    """
    returns a tuple containing the first and second part of the current page that are 
    for the violin parts. WIP
    """
    left = 0
    top = 215
    right = im.size[0]
    bottom = int(im.size[1] * 0.15)
    first_half = crop_sheet(im, left, top, right, bottom)
    second_half = crop_sheet(im, left, im.size[1] // 2 , right, int(bottom + im.size[1] * 0.45) )

    return (first_half, second_half)


def cut_parts(im:Image) -> Tuple:
    """
    
    """
    pass



def create_violin_pages(number_of_images:int, max_width:int, max_height:int) -> None:
    """
    Given the cutted parts separated and ordered by number, attaches them in a complete page
    of the original size. Gives multiple pages if there are too many cropped parts. The pages are
    saved inside the cropped folder with the name "violinPage#.png" # = number of the page.
    """
    page_number = 1
    current_cropped_img = 2 # TODO: change this back to 1, since we're not taking in count the number 1
                            # wait, should i change it back to 1? the first page is always different from the rest

    while number_of_images > 0:
        canva = Image.new("RGB", (max_width, max_height), (250, 250, 250))
        
        current_height = int(max_height * 0.025) # a little bit of padding at the top of the canvas
        space_left = max_height - current_height - 20
        heigth_of_this_img = 0

        while heigth_of_this_img < space_left:
            img = Image.open(f"cropped/violin{current_cropped_img}.png")
            canva.paste(img, (0, current_height))
            heigth_of_this_img = img.size[1] + 20

            current_cropped_img += 1
            current_height += img.size[1] + 20 # 20 pixels of padding between each img
            space_left = max_height - current_height - 20
            print(f"there are {space_left} pixels left")
            number_of_images -= 1

            if number_of_images == 0:
                break


        save_image_inside_cropped(canva, f"violinPage{page_number}", "png")
        page_number += 1



if __name__ == "__main__":
    number_of_images = 21
    
    for i in range(1, number_of_images):
        
        im = Image.open(f"merry{i+1}.png")
        parts = cut_violin_parts(im)

        # A bit weird, but it makes sense: the current merry image is, for example, 2,
        # and the parts that come from this page are violin2 and violin3, which is 
        # 2*2 - 2 and 2*2 - 1 respectively, and it happens for any merry image number.
        save_image_inside_cropped(parts[0], f"violin{(i+1)*2 - 2}", "png")
        save_image_inside_cropped(parts[1], f"violin{(i+1)*2 - 1}", "png")

    im = Image.open("merry2.png")

    # TODO: remove the -2 from this argument, it is just because we are not croping the first page. 
    create_violin_pages(number_of_images*2 - 2, im.size[0], im.size[1])



