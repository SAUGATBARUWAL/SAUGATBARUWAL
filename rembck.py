from rembg import remove

input_file = "last.jpg"
output_file = "lastly.png"

with open(input_file, "rb") as input_image:
    input_data = input_image.read()

output_data = remove(input_data)

with open(output_file, "wb") as output_image:
    output_image.write(output_data)

print("Background removed successfully!")