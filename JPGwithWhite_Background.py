from PIL import Image
import os
    
def convert_and_process_image(image_path, output_dir):
    try:
        Image.MAX_IMAGE_PIXELS = None  

        img = Image.open(image_path)
        if img.mode == "CMYK":
            img = img.convert("RGB")

        filename = os.path.basename(image_path)
        base_name, ext = os.path.splitext(filename)

        png_path = None  # Initialize png_path
        if ext.lower() in (".jpg", ".jpeg"):
            png_path = os.path.join(output_dir, base_name + ".png")
            img.save(png_path)
            image_path = png_path

        png_img = Image.open(image_path).convert("RGBA")
        background = Image.new("RGBA", png_img.size, (255, 255, 255, 255))
        composite = Image.alpha_composite(background, png_img)
        jpg_path = os.path.join(output_dir, base_name + ".jpg")  
        composite.convert('RGB').save(jpg_path, "JPEG")
        print(f"Converted {image_path} to {jpg_path} with white background")

        # Delete the PNG file *after* successful conversion
        if png_path and os.path.exists(png_path):  
            os.remove(png_path)
            print(f"Deleted PNG file: {png_path}") 

        return "True"  
    except (OSError, ValueError) as e: 
        print(f"Error converting {image_path}: {e}")
        return "False" 
    
def process_images(directory_path, output_folder="converted"):
    """Processes all images (JPG and PNG) in the given directory."""
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(directory_path, filename)
            convert_and_process_image(image_path, output_folder)

# Get the directory path from the user
directory_path = input("Enter the directory path containing the images: ")

# Call the function to process the images
process_images(directory_path)