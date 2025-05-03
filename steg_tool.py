from PIL import Image

# Helper to convert text to binary
def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

# Helper to convert binary to text
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

# Encode text into image
def encode(image_path, message):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    encoded = img.copy()
    width, height = img.size

    message += "####"  # Delimiter to know when the message ends
    binary_msg = text_to_bin(message)
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index < len(binary_msg):
                r, g, b = img.getpixel((x, y))
                r = (r & ~1) | int(binary_msg[data_index])  # Replace LSB
                data_index += 1
                if data_index < len(binary_msg):
                    g = (g & ~1) | int(binary_msg[data_index])
                    data_index += 1
                if data_index < len(binary_msg):
                    b = (b & ~1) | int(binary_msg[data_index])
                    data_index += 1
                encoded.putpixel((x, y), (r, g, b))
            else:
                break

    encoded.save("encrypted_image.png")
    print("✅ Message encoded into 'encrypted_image.png'")

# Decode text from image
def decode(image_path):
    img = Image.open(image_path)
    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    decoded_text = bin_to_text(binary_data)
    final_msg = decoded_text.split("####")[0]  # Remove delimiter
    print(f"🔓 Hidden Message: {final_msg}")

# UI
if __name__ == "__main__":
    print("1. Encrypt text into image")
    print("2. Decrypt text from image")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        path = input("Enter path to JPEG or PNG image: ")
        message = input("Enter secret text to hide: ")
        encode(path, message)
    elif choice == "2":
        path = input("Enter path to image with hidden message: ")
        decode(path)
    else:
        print("❌ Invalid choice.")
