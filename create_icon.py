from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        bg_color = (42, 130, 218)
        draw.ellipse([size*0.1, size*0.1, size*0.9, size*0.9], fill=bg_color)
        
        bar_width = size * 0.08
        bar_spacing = size * 0.05
        bar_heights = [0.3, 0.5, 0.4, 0.6]
        
        start_x = size * 0.25
        for i, height in enumerate(bar_heights):
            x = start_x + i * (bar_width + bar_spacing)
            y = size * (0.7 - height * 0.4)
            draw.rectangle([x, y, x + bar_width, size * 0.7], fill=(255, 255, 255))
        
        img.save(f'assets/icon_{size}x{size}.png')
    
    icon_img = Image.open('assets/icon_256x256.png')
    icon_img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
    
    print("Icon files created successfully!")
    print("Note: For macOS .icns file, use the following command on a Mac:")
    print("  mkdir icon.iconset")
    print("  sips -z 16 16     assets/icon_1024x1024.png --out icon.iconset/icon_16x16.png")
    print("  sips -z 32 32     assets/icon_1024x1024.png --out icon.iconset/icon_16x16@2x.png")
    print("  sips -z 32 32     assets/icon_1024x1024.png --out icon.iconset/icon_32x32.png")
    print("  sips -z 64 64     assets/icon_1024x1024.png --out icon.iconset/icon_32x32@2x.png")
    print("  sips -z 128 128   assets/icon_1024x1024.png --out icon.iconset/icon_128x128.png")
    print("  sips -z 256 256   assets/icon_1024x1024.png --out icon.iconset/icon_128x128@2x.png")
    print("  sips -z 256 256   assets/icon_1024x1024.png --out icon.iconset/icon_256x256.png")
    print("  sips -z 512 512   assets/icon_1024x1024.png --out icon.iconset/icon_256x256@2x.png")
    print("  sips -z 512 512   assets/icon_1024x1024.png --out icon.iconset/icon_512x512.png")
    print("  sips -z 1024 1024 assets/icon_1024x1024.png --out icon.iconset/icon_512x512@2x.png")
    print("  iconutil -c icns icon.iconset -o assets/icon.icns")

if __name__ == '__main__':
    create_icon()
