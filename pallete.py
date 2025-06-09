from PIL import Image
import numpy as np
# Define the function to map colors while maintaining visual similarity
def match_color_to_palette(color, palette):
    distances =np.sqrt(np.sum((palette -color) **2, axis=1))
    return np.argmin(distances)
# Function to strictly map the colors in image2 to the exact palette of image1 while keeping visual similarity
def strict_visual_mapping(source_image, source_palette, target_palette):
    image_data =np.array(source_image)
    new_image_data =np.zeros_like(image_data)
 
 # Map each color from the source palette to the closest color in the target palette
    for i in range(len(source_palette)):
        closest_color_index =match_color_to_palette(source_palette[i], target_palette)
        new_image_data[image_data == i] = closest_color_index
    return new_image_data
# Load the original and target images
image1 =Image.open('00006_01.png') # Target image (with the desired palette)
rgba_image =Image.open('00006_00.png') # Source RGBA image
# Convert RGBA to RGB (Palette mode doesn't support alpha channel directly)
rgb_image =rgba_image.convert("RGB")
# Convert the RGB image to Palette mode
image2 =rgb_image.convert("P", palette=Image.ADAPTIVE)
# Get the palettes of both images
palette1 =np.array(image1.getpalette()).reshape(-1, 3) # Target palette
palette2 =np.array(image2.getpalette()).reshape(-1, 3) # Source palette
# Perform the initial visual mapping to map the source image colors to the target palette
strictly_mapped_pixels =strict_visual_mapping(image2, palette2, palette1)
# Create a new image using the mapped pixels and the target image's palette
final_strict_visual_image =Image.fromarray(strictly_mapped_pixels, mode='P')
final_strict_visual_image.putpalette(image1.getpalette())
# Define the exact color index mapping that needs to be preserved
index_mapping_corrected_strict ={
 0: 0, # Background color, most common
 2: 2, # Second color
 5: 5, # Third color
 9: 9, # Fourth color
 10: 10, # Fifth color
 13: 13, # Sixth color
 14: 14, # Seventh color
 15: 15 # Eighth color
}
# Apply the corrected index mapping to the image data
strict_image_data =np.array(final_strict_visual_image)
remapped_image_data_strict =np.zeros_like(strict_image_data)
for old_index, new_index in index_mapping_corrected_strict.items():
    remapped_image_data_strict[strict_image_data ==old_index] =new_index
# Create the corrected remapped image with the palette of the target image
    remapped_final_image_strict =Image.fromarray(remapped_image_data_strict, mode='P')
    remapped_final_image_strict.putpalette(image1.getpalette())
# Save the strictly remapped image
remapped_final_image_strict_path ="0000006.png"
remapped_final_image_strict.save(remapped_final_image_strict_path)