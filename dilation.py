import os
from PIL import Image
import numpy as np
import cv2

k = 60  # 커널 사이즈 이걸로 조절

# Define the path to the dataset folder
dataset_path = 'vtonHD/test/image-parse-v3'
output_path = f'vtonHD/test/{k}-dilation-parse-v3'

# Dilation parameters
kernel_size = (k, k)  # Kernel 
iterations = 1 

# Create output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Iterate over all files in the dataset folder
for filename in os.listdir(dataset_path):
    if filename.endswith('.png'):
        # Load the image using PIL
        image_path = os.path.join(dataset_path, filename)
        image = Image.open(image_path)

        # Get the palette and the unique color indices in the image
        palette = image.getpalette()
        color_indices = list(image.getdata())

        # Convert the palette into a list of RGB tuples
        palette_colors = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]

        # Find the color index corresponding to the orange color (in this case, index 5)
        orange_index = 5

        # Create a binary mask for the orange region
        mask = np.array([1 if pixel == orange_index else 0 for pixel in color_indices], dtype=np.uint8)
        mask = mask.reshape(image.size[1], image.size[0])  # Reshape to image dimensions (height, width)

        # Apply dilation using OpenCV
        dilation_kernel = np.ones(kernel_size, np.uint8)  # Use defined kernel size for dilation
        dilated_mask = cv2.dilate(mask, dilation_kernel, iterations=iterations)

        # Create a new image from the original with the dilated orange region
        combined_indices = np.array(color_indices).reshape(image.size[1], image.size[0])
        combined_indices[dilated_mask > 0] = orange_index  # Replace dilated region with orange index

        # Convert the combined indices back to an image
        combined_image = Image.fromarray(combined_indices.astype('uint8'), mode='P')
        combined_image.putpalette(palette)

        # Save the combined image to the output directory
        combined_image.save(os.path.join(output_path, filename))
