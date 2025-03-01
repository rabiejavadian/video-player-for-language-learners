from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with a dark background
    size = 256
    img = Image.new('RGBA', (size, size), (42, 42, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a play button triangle
    triangle_points = [
        (size//3, size//4),
        (size//3, size*3//4),
        (size*3//4, size//2)
    ]
    draw.polygon(triangle_points, fill=(255, 255, 255, 255))
    
    # Draw two lines representing subtitles
    line_width = size*2//3
    line_height = size//20
    line_x = (size - line_width)//2
    line_y1 = size*3//4 + 10
    line_y2 = line_y1 + line_height + 5
    
    draw.rectangle([line_x, line_y1, line_x + line_width, line_y1 + line_height], 
                  fill=(255, 255, 255, 180))
    draw.rectangle([line_x, line_y2, line_x + line_width*2//3, line_y2 + line_height], 
                  fill=(255, 255, 255, 140))
    
    # Save as ICO file
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_icon() 