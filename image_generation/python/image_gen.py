import json
from PIL import Image, ImageDraw, ImageFont
import sys
import os

def load_external_data(file_path):
    clone = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            clone_info = json.loads(line)
            clone[clone_info['character']] = clone_info
    return clone

def get_radical(character, characters):
    if character in characters:
        return characters[character]['radical']
    else:
        return "Character not found in data"

def get_decomposition(character, characters):
    if character in characters:
        return characters[character]['decomposition']
    else:
        return "Character not found in data"

def composite_LTR_character(character, characters_data, mapping_data, font_path, font_size, image_size):
    decomposition = characters_data[character]['decomposition']
    radical = characters_data[character]['radical']

    if decomposition[0] != '⿰':
        print("Character is not composed from Left to Right")
        return

    if radical in mapping_data:
        left_component_img_path = mapping_data[radical]['path']
    else:
        print("Conversion not yet supported")
        return

    right_component = decomposition[2]
    right_img = Image.new('RGBA', (image_size[0] // 2, image_size[1]), (255, 255, 255, 0))
    draw = ImageDraw.Draw(right_img)
    font = ImageFont.truetype(font_path, font_size)
    x1, y1, x2, y2 = draw.textbbox((0 ,0), right_component, font=font)
    draw.text((0, (right_img.height - y2 + y1) // 2 - y1), right_component, font=font, fill='black')

    base_width = image_size[0] // 6
    left_component = Image.open(left_component_img_path)
    wpercent = (base_width / float(left_component.size[0]))
    hsize = int((float(left_component.size[1]) * float(wpercent)))
    left_component = left_component.resize((base_width, hsize), Image.Resampling.LANCZOS)

    left_img = Image.new('RGBA', (image_size[0] // 2, image_size[1]), (255, 255, 255, 0))
    left_img.paste(left_component, (left_img.width - left_component.width, (left_img.height - left_component.height) // 2))

    combined_img = Image.new('RGBA', image_size, (255, 255, 255, 0))
    combined_img.paste(left_img, (0, 0))
    combined_img.paste(right_img, (image_size[0] // 2, 0), right_img)

    combined_img.save("img", 'PNG')  # Change 'PNG' to the desired image format if needed
    return combined_img

def generate_character_image(character, characters_data, mapping_data, font_path, font_size, image_size, save_path):
    radical = get_radical(character, characters_data)
    print(f"The radical of '{character}' is: {radical}")
    img = composite_LTR_character(character, characters_data, mapping_data, font_path, font_size, image_size)
    if img:
        save_folder = '../public/images/'  # Change to your web server's accessible folder
        save_filename = f'generated_image.png'  # Example filename
        
        save_full_path = os.path.join(save_folder, save_filename)
        img.save(save_full_path, 'PNG')  # Save the image to the specified folder
        
        return save_full_path  # Return the image path
    else:
        return None  # Return None if image generation fails

if __name__ == "__main__":
    dictionary_path = 'dictionary.txt'
    mapping_path = 'mapping.txt'

    characters_data = load_external_data(dictionary_path)
    mapping_data = load_external_data(mapping_path)

    character = sys.argv[1]  # Get character input from command line argument
    font_path = 'Arial Unicode.ttf'
    font_size = 200
    image_size = (520, 520)

    save_path = '../public/images/Combined.png'  # Replace 'path_to_save' and 'image_name' with your desired path and image name
    generated_image_path = generate_character_image(character, characters_data, mapping_data, font_path, font_size, image_size, save_path)

    if generated_image_path:
        print(generated_image_path)  # Output the image path
    else:
        print("Image generation failed")  # Output a message if image generation fails
