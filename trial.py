import mysql.connector
from PIL import Image
import base64
import io
import cv2
import random

conn = mysql.connector.connect(
host="localhost",
user="root",
password="shripad2005",
database="project_data"
)
cursor = conn.cursor()

fashion = ["Shirt", "Mobile_phone", "Glasses", "Headphones", "Human_beard", "Necklace", "Watch", "Coat", "Earrings", "Jeans", "Pen", "Tie"]


def fetch_data(gender, age, fashion):
    if fashion == "None":
        cursor.execute("select img, link from image_data where gender = %s and age = %s", (gender, age))
    else:
        cursor.execute("select img, link from image_data where gender = %s and age = %s and fashion_type = %s", (gender, age, fashion))
    path = cursor.fetchall()
    if path:
        data = random.choice(path)
        img_path = data[0]
        link = data[1]
        # bdata = base64.b64decode(path[0][0])
        # photo = Image.open(io.BytesIO(bdata))
        # photo.show()
        return img_path, link
        
        

# img_path , link = fetch_data("Male", "(18-28)", "Glasses")
# print("link",link)
# print("image : ",img_path)
# cursor.execute("select (img) from image_data where id = 325")
# path = cursor.fetchall()
# print(path[0][0])
# "select (img) from image_data where gender = %s and age = %s and fashion_type = %s", (gender, age, fashion)