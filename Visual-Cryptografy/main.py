from PIL import Image
import random

def generate_shares(image_path, share1_path, share2_path):
    original = Image.open(image_path).convert('1')
    width, height = original.size

    share1 = Image.new('1', (width * 2, height))
    share2 = Image.new('1', (width * 2, height))

    for y in range(height):
        for x in range(width):
            pixel = original.getpixel((x, y))
            pattern = random.randint(0, 1)
            if pixel == 255:
                if pattern == 0:
                    p1 = [0, 255]
                    p2 = [255, 0]
                else:
                    p1 = [255, 0]
                    p2 = [0, 255]
            else:
                if pattern == 0:
                    p1 = [0, 255]
                    p2 = [0, 255]
                else:
                    p1 = [255, 0]
                    p2 = [255, 0]

            share1.putpixel((x * 2, y), p1[0])
            share1.putpixel((x * 2 + 1, y), p1[1])

            share2.putpixel((x * 2, y), p2[0])
            share2.putpixel((x * 2 + 1, y), p2[1])

    share1.save(share1_path)
    share2.save(share2_path)
    print("Shares saved successfully!")

def overlay_shares(share1_path, share2_path, output_path):
    share1 = Image.open(share1_path).convert('1')
    share2 = Image.open(share2_path).convert('1')

    width, height = share1.size
    result = Image.new('1', (width, height))

    for y in range(height):
        for x in range(width):
            p1 = share1.getpixel((x, y))
            p2 = share2.getpixel((x, y))
            result.putpixel((x, y), 0 if p1 == 0 or p2 == 0 else 255)

    result.save(output_path)
    print("Overlay image saved successfully!")

generate_shares("input.png", "share1.png", "share2.png")
overlay_shares("share1.png", "share2.png", "reconstructed.png")
