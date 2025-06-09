import os
from PIL import Image
import numpy as np
import cv2

k = 60  # 커널 사이즈 이걸로 조절

# Define the path to the dataset folder
dataset_path = 'vtonHD/test/image-parse-v3'
output_path = f'vtonHD/test/{k}-erosion-parse-v3'

# Erosion parameters
kernel_size = (k, k)  # Reduced kernel size for more effective erosion
iterations = 1  # Number of iterations for erosion

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
        color_indices = np.array(image.getdata(), dtype=np.uint8).reshape(image.size[1], image.size[0])

        # Find the color index corresponding to the orange color (in this case, index 5)
        orange_index = 5

        # Create a binary mask for the orange region
        mask = (color_indices == orange_index).astype(np.uint8)

        # Apply erosion using OpenCV
        erosion_kernel = np.ones(kernel_size, np.uint8)  # Use defined kernel size for erosion
        eroded_mask = cv2.erode(mask, erosion_kernel, iterations=iterations)

        # Create a new mask preserving all original colors but applying erosion to the orange region
        combined_indices = color_indices.copy()
        combined_indices[mask == 1] = 0  # Set original orange areas to 0
        combined_indices[eroded_mask == 1] = orange_index  # Set eroded orange areas back to orange index

        # Convert the combined indices back to an image, preserving all colors from the original
        combined_image = Image.fromarray(combined_indices.astype('uint8'), mode='P')
        combined_image.putpalette(palette)

        # Save the combined image to the output directory
        combined_image.save(os.path.join(output_path, filename))
