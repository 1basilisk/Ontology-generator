from pdf2image import convert_from_path
import os

def convert_pdf_to_images( pdf_path: str) -> str:
        
        images = convert_from_path(pdf_path, dpi=500)

        for i, image in enumerate(images):   
            image.save(f'./data/images/{os.path.basename(pdf_path)}page_{i+1}.jpg', 'JPEG')