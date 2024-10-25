import os
from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, filedialog, messagebox, Button, Label, Entry, StringVar, IntVar, Frame, OptionMenu, StringVar

class ImageProcessor:
    def __init__(self, watermark_text='', output_path='', quality=85, font_size=20, image_format='JPEG'):
        self.watermark_text = watermark_text
        self.output_path = output_path
        self.quality = quality
        self.font_size = font_size
        self.image_format = image_format 

    # Compress the image
    def compress_image(self, input_path):
        compressed_image_path = f'compressed_{os.path.basename(input_path)}'
        with Image.open(input_path) as img:
            img.save(compressed_image_path, "JPEG", optimize=True, quality=self.quality)
        return compressed_image_path

    # Add watermark to the image
    def add_watermark(self, input_path):
        output_path = self.output_path or os.path.basename(input_path)
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)

            # Load the custom font with the specified font size
            try:
                font = ImageFont.truetype("SouthernAire_Personal_Use_Only.ttf", self.font_size)
            except IOError:
                font = ImageFont.load_default()

            # Calculate text bounding box to adjust position
            text_bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Get size of the original image
            width, height = img.size

            # Define watermark position
            # Ensure the watermark does not exceed the image bounds
            position_x = max(width - text_width - 10, 0)
            position_y = max(height - text_height - 10, 0)

            # Adjust position if the watermark is too large for the image
            if text_width > width:
                position_x = 0  # Place at the left if too wide
            if text_height > height:
                position_y = 0  # Place at the top if too tall

            draw.text((position_x, position_y), self.watermark_text, font=font, fill=(255, 255, 255, 128))
            img.save(output_path)
        return output_path

    # Process the image by compressing it and adding a watermark
    def process_image(self, input_image_path):
        return self.add_watermark(self.compress_image(input_image_path))

    @staticmethod
    # Open the processed image
    def show_image(image_path):
        Image.open(image_path).show()

    # Run the GUI for the image processing tool
    def run_gui(self):
        root = Tk()
        root.title("Image Processing Tool")

        # Frame for watermark and font size
        watermark_frame = Frame(root)
        watermark_frame.pack(pady=5)

        Label(watermark_frame, text="Watermark Text:").pack(side='left')
        self.watermark_var = StringVar(value=self.watermark_text)
        Entry(watermark_frame, textvariable=self.watermark_var).pack(side='left', padx=5)

        Label(watermark_frame, text="Font Size:").pack(side='left')
        self.font_size_var = IntVar(value=self.font_size)
        Entry(watermark_frame, textvariable=self.font_size_var, width=5).pack(side='left', padx=5)

        # Frame for compression quality and image format
        quality_format_frame = Frame(root)
        quality_format_frame.pack(pady=5)

        Label(quality_format_frame, text="Compression Quality (1-100):").pack(side='left')
        self.quality_var = IntVar(value=self.quality)
        Entry(quality_format_frame, textvariable=self.quality_var, width=5).pack(side='left', padx=5)

        Label(quality_format_frame, text="Image Format:").pack(side='left')
        self.image_format_var = StringVar(value=self.image_format)
        formats = ['JPEG', 'PNG']
        OptionMenu(quality_format_frame, self.image_format_var, *formats).pack(side='left', padx=5)

        # Frame for buttons
        button_frame = Frame(root)
        button_frame.pack(pady=10)

        # Button to choose image
        Button(button_frame, text="Choose an Image", command=self.select_image).pack(side='left', padx=5)

        # Button to choose output path
        Button(button_frame, text="Choose Output Path", command=self.select_output_path).pack(side='left', padx=5)

        # Confirm button
        Button(button_frame, text="Confirm", command=self.confirm_selection).pack(side='left', padx=5)

        root.mainloop()

    # Select an image and store the path
    def select_image(self):
        self.input_image_path = filedialog.askopenfilename(title="Choose an Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if self.input_image_path:
            messagebox.showinfo("Selected Image", f"Selected Image: {os.path.basename(self.input_image_path)}")

    # Select output path for the processed image
    def select_output_path(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if self.output_path:
            messagebox.showinfo("Selected Output Path", f"Output Path: {os.path.basename(self.output_path)}")

    # Confirm the selection and process the image
    def confirm_selection(self):
        if hasattr(self, 'input_image_path'):
            self.watermark_text = self.watermark_var.get()
            self.quality = self.quality_var.get()
            self.font_size = self.font_size_var.get()  # Get font size
            self.image_format = self.image_format_var.get()  # Get image format
            final_image = self.process_image(self.input_image_path)
            messagebox.showinfo("Done", f"Processed Image Path: {final_image}")
            self.show_image(final_image)
        else:
            messagebox.showwarning("No Image Selected", "Please select an image before confirming.")

    # Run the program in terminal mode
    def run_terminal_mode(self):
        self.watermark_text = input("Enter watermark text: ")
        self.quality = int(input("Enter compression quality (1-100): "))
        self.font_size = int(input("Enter font size: "))  # Get font size in terminal mode
        self.input_image_path = input("Enter path to the image file (with filename): ")
        self.output_path = input("Enter output path (with filename): ")

        try:
            final_image = self.process_image(self.input_image_path)
            print(f"Processed Image Path: {final_image}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    mode = input("Choose mode (gui/terminal): ").strip().lower()
    image_processor = ImageProcessor()

    if mode == 'gui':
        image_processor.run_gui()
    elif mode == 'terminal':
        image_processor.run_terminal_mode()
    else:
        print("Invalid mode selected. Please choose 'gui' or 'terminal'.")
