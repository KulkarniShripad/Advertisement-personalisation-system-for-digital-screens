import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import mysql.connector
import random

conn = mysql.connector.connect(
host="localhost",
user="root",
password="shripad2005",
database="project_data"
)
cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS user_data
#               (id INT AUTO_INCREMENT PRIMARY KEY, gender VARCHAR(255), age VARCHAR(255))''')
# conn.commit()

def store_data_in_database(gender, age):
    with lock:
        cursor = conn.cursor()
        cursor.execute("update userdata2 set gender = %s , age = %s where id = 1", (gender, age))
        conn.commit()

def fetch_latest_data_from_database():
    with lock:
        cursor = conn.cursor()
        cursor.execute("SELECT gender, age FROM userdata2 where id = 1")
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
    return None, None

# gender = ""
# age = ""
lock = threading.Lock()

def facebox(faceNet, frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], swapRB= False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs = []
    for i in range(detection.shape[2]):
        confidence = detection[0,0,i,2]
        if confidence > 0.7:
            x1 = int(detection[0,0,i,3]*frameWidth)
            y1 = int(detection[0,0,i,4]*frameHeight)
            x2 = int(detection[0,0,i,5]*frameWidth)
            y2 = int(detection[0,0,i,6]*frameHeight)
            bboxs.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    return frame, bboxs

# def display_image(image_path):
#     root = tk.Tk()
#     root.title("Image Viewer")

#     img = Image.open(image_path)
#     img = img.resize((800, 600), Image.ANTIALIAS)
#     img = ImageTk.PhotoImage(img)

#     label = tk.Label(root, image=img)
#     label.pack()

#     root.mainloop()

paused = False
last_selected_image = None

def toggle_pause():
    global paused
    paused = not paused


def showad():
    def update_image():
        if not paused:
            gender, age = fetch_latest_data_from_database()
            if gender == "Male" and age == "(18-28)":
                start = 0
                end = 12
                num = random.randint(start, end)
                img_path = f"S:\Projects\pp\\assets\\18-28\Male\{num}.jpg"
            elif gender == "Female" and age == "(18-28)":
                start = 0
                end = 12
                num = random.randint(start, end)
                img_path = f"S:\Projects\pp\\assets\\18-28\Female\{num}.jpg"
            elif gender == "Male" and age == "(0-4)":
                start = 0
                end = 2
                num = random.randint(start, end)
                img_path = f"S:\Projects\pp\\assets\\0-3\{num}.jpg"
            elif gender == "Female" and age == "(0-4)":
                start = 0
                end = 2
                num = random.randint(start, end)
                img_path = f"S:\Projects\pp\\assets\\0-3\{num}.jpg"
            elif gender == "Male" and age == "(30-40)":
                start = 0
                end = 20
                num = random.randint(start,end)
                img_path =  f"S:\Projects\pp\\assets\\25-35\Male\{num}.jpg" 
            elif gender == "Female" and age =="(30-40)":
                 start = 1
                 end = 14
                 num = random.randint(start,end)
                 img_path =  f"S:\Projects\pp\\assets\\25-35\Female\{num}.jpg" 
            elif gender == "Male" and age == "(40-50)":
                start = 0
                end = 5
                num = random.randint(start,end)
                img_path =  f"S:\Projects\pp\\assets\\35-50\Male\{num}.jpg" 
            elif  gender == "Female" and age == "(40-50)":
                start = 0
                end = 6
                num = random.randint(start,end)
                img_path =  f"S:\Projects\pp\\assets\\35-50\Female\{num}.jpg"
            elif  gender == "Male" and age == "(50-75)":
                start = 0
                end = 3
                num = random.randint(start,end)
                img_path =  f"S:\Projects\pp\\assets\\50-75\Male\{num}.jpg"
            elif  gender == "Female" and age == "(50-75)":
                start = 0
                end = 4
                num = random.randint(start,end)
                img_path =  f"S:\Projects\pp\\assets\\50-75\Female\{num}.jpg"            
            else:
                img_path = "S:\Projects\pp\\assets\default.jpg"
                last_selected_image = img_path
                
            img = Image.open(img_path)
            img = img.resize((800, 600), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            label.configure(image=img)
            label.image = img
            # Create a canvas widget to hold the image and graphics
            canvas.delete("all")  # Clear the canvas
            
        else:
            if last_selected_image is not None:
                # Display the last selected image when updates are paused
                img = Image.open(last_selected_image)
                img = img.resize((800, 600), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)

                label.configure(image=img)
                label.image = img
                
                canvas.delete("all")
                
            # Continue to check if updates should be resumed
        root.after(5000, update_image)    
            
    root = tk.Tk()
    root.title("Image Viewer")
    
    frame = tk.Frame(root)
    frame.pack()

    label = tk.Label(root)
    label.pack()

    # Create a canvas widget
    canvas = tk.Canvas(root, width=820, height=620)
    canvas.pack()

    pause_button = tk.Button(root, text="Pause/Resume", command=toggle_pause)
    pause_button.pack()

    update_image()   # Call the showad function to display ads

    root.mainloop()

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-4)', '(4-10)', '(10-15)', '(15-18)', '(18-28)', '(30-40)', '(40-50)', '(50-75)']
genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

padding = 20

def rundetector():
    gender = ""
    age = ""
    video = cv2.VideoCapture(0)
    while True:
        ret , frame = video.read()
        frame , bboxs = facebox(faceNet, frame)
        for bbox in bboxs:
            face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPred=genderNet.forward()
            lgender=genderList[genderPred[0].argmax()]

            ageNet.setInput(blob)
            agePrediction = ageNet.forward()
            lage = ageList[agePrediction[0].argmax()]

            label = "{}, {}".format(lgender, lage)
            print("Age is ", lage, " and gender is ", lgender)
            store_data_in_database(gender=lgender, age= lage)
            cv2.rectangle(frame,(bbox[0], bbox[1]-30), (bbox[2], bbox[1]), (0,255,0),-1) 
            cv2.putText(frame, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
            gender , age = fetch_latest_data_from_database()
            if lgender != gender or lage != age:
                store_data_in_database(lgender, lage)
                
            # showad(gender, age)
        cv2.imshow("Age_Gender", frame)
        k =cv2.waitKey(1)
        if k == ord('q'):
            break
    
    video.release()
    cv2.destroyAllWindows()
    
def runad():
    # gen = gender
    # ag = age
    showad()
        
if __name__ == "__main__":
    t1 = threading.Thread(target=rundetector)
    t2 = threading.Thread(target=runad)
    
    t1.start()
    t2.start()

    
    # t1.join()
    # t2.join()
