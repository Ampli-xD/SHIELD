import os

from PIL import Image


class ImagePreprocessor:
    def __init__(self, image_data):
        self.image_data = image_data

    def check_integrity(self):
        """Check if the image file is valid and not corrupted."""
        try:
            with Image.open(self.image_data.file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def convert_to_png(self):
        """Convert the image file to PNG format."""
        try:
            with Image.open(self.image_data.file_path) as img:
                output_path = os.path.splitext(self.image_data.file_path)[0] + '.png'
                img.save(output_path, format='PNG')
            return output_path
        except Exception:
            return None

# Example usage
# if __name__ == "__main__":
#     class ImageData:  # Example placeholder for image data structure
#         def __init__(self, file_path):
#             self.file_path = file_path
#
#     image_path = "path/to/your/image.jpg"  # Update with your image path
#     image_data = ImageData(file_path=image_path)
#     preprocessor = ImagePreprocessor(image_data)
#
#     if preprocessor.check_integrity():
#         print("Image file is valid.")
#     else:
#         print("Image file is corrupted or invalid.")
#         exit()
#
#     converted_path = preprocessor.convert_to_png()
#     if converted_path:
#         print(f"Converted image file saved at: {converted_path}")
