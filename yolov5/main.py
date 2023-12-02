import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import mysql.connector
import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QScrollArea, QDialog, QDialogButtonBox, QTextBrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import trial 
import fashion_detector as fs

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

link = ""

def store_data_in_database(gender, age, fashion):
    with lock:
        cursor = conn.cursor()
        cursor.execute("update userdata2 set gender = %s , age = %s, fashion_type = %s where id = 1", (gender, age, fashion))
        conn.commit()

def fetch_latest_data_from_database():
    with lock:
        cursor = conn.cursor()
        cursor.execute("SELECT gender, age, fashion_type FROM userdata2 where id = 1")
        row = cursor.fetchone()
        if row:
            return row[0], row[1], row[2]
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

# paused = False
# last_selected_image = None

# def toggle_pause():
#     global paused
#     paused = not paused


class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("More Info")
        self.setMinimumWidth(400)  # Set the minimum width of the dialog
        
        layout = QVBoxLayout()
        
        text = QTextBrowser(self)
        text.setOpenExternalLinks(True)  # Enable clickable links
        text.setText('''<html><div style="text-align: center; text-justify: auto;">
    <p style="font-size: 30px;">For more information, click the button below and know more about the exciting product:</p>
</div></html>''')
        layout.addWidget(text)
        
        self.more_button = QPushButton("More Info", self)
        self.more_button.setStyleSheet("background-color: #000000; color: #ffffff; padding: 20px 30px; font-size: 24px; border: 2px solid #ffffff; border-radius: 20px;")
        self.more_button.clicked.connect(self.open_link)
        layout.addWidget(self.more_button)
        
        self.setLayout(layout)
        
    def open_link(self):
        QDesktopServices.openUrl(QUrl(link))
    
class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")

        central_widget = QScrollArea(self)
        self.setCentralWidget(central_widget)

        central_container = QWidget(self)
        central_widget.setWidget(central_container)
        central_widget.setWidgetResizable(True)

        layout = QVBoxLayout(central_container)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.load_button = QPushButton("Pause", self)
        self.load_button.setStyleSheet("background-color: #000000; color: #ffffff; padding: 20px 30px; font-size: 24px; border: 2px solid #ffffff; border-radius: 20px;")
        self.load_button.clicked.connect(self.toggle_pause)
        layout.addWidget(self.load_button)

        self.more_button = QPushButton("More Info", self)
        self.more_button.setStyleSheet("background-color: #000000; color: #ffffff; padding: 20px 30px; font-size: 24px; border: 2px solid #ffffff; border-radius: 20px;")
        self.more_button.hide()
        self.more_button.clicked.connect(self.show_info_dialog)
        layout.addWidget(self.more_button)

        self.image_paths = []  # Replace with your image paths
        self.paused = False
        self.image_timer = QTimer(self)
        self.image_timer.timeout.connect(self.update_image)
        self.update_image()
        
    def show_info_dialog(self):
        dialog = InfoDialog(self)
        dialog.exec_()

    def toggle_pause(self):
        if self.paused:
            self.load_button.setText("Pause")
            self.paused = False
            self.more_button.hide()
            self.image_timer.start(3000)
        else:
            self.load_button.setText("Resume")
            self.paused = True
            self.more_button.show()
            self.image_timer.stop()
            self.show_info_dialog()
            
    
    def load_image(self):
        global link
        gender, age, fashion_type = fetch_latest_data_from_database()
        img_path, link = trial.fetch_data(gender, age, fashion_type)
        # img_path = trial.fetch_data("Male", "(18-28)", "Headphones")
        return img_path

    def update_image(self):
        if not self.paused:
            img_path = self.load_image()
            pixmap = QPixmap()
            pixmap.loadFromData(img_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


faceProto = "S:/Projects/Advertisement personalisation system for digital screens/models/opencv_face_detector.pbtxt"
faceModel = "S:/Projects/Advertisement personalisation system for digital screens/models/opencv_face_detector_uint8.pb"

ageProto = "S:/Projects/Advertisement personalisation system for digital screens/models/age_deploy.prototxt"
ageModel = "S:/Projects/Advertisement personalisation system for digital screens/models/age_net.caffemodel"

genderProto = "S:/Projects/Advertisement personalisation system for digital screens/models/gender_deploy.prototxt"
genderModel = "S:/Projects/Advertisement personalisation system for digital screens/models/gender_net.caffemodel"

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
    fashion = ""
    video = cv2.VideoCapture(0)
    fs.load_model()
    while True:
        ret , frame = video.read()
        frame , bboxs = facebox(faceNet, frame)
        lfashion = fs.detect_fashion(frame)
        for bbox in bboxs:
            face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPred=genderNet.forward()
            lgender=genderList[genderPred[0].argmax()]

            ageNet.setInput(blob)
            agePrediction = ageNet.forward()
            lage = ageList[agePrediction[0].argmax()]

            label = "{}, {}, {}".format(lgender, lage, lfashion)
            # label = "{}, {}, {}".format("Male", "(18-28)", "Headphones")
            print("Age is ", lage, " and gender is ", lgender, " and fashion is ", fashion)
            # store_data_in_database(gender=lgender, age= lage)
            cv2.rectangle(frame,(bbox[0], bbox[1]-30), (bbox[2], bbox[1]), (0,255,0),-1) 
            cv2.putText(frame, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
            gender , age, fashion = fetch_latest_data_from_database()
            if lgender != gender or lage != age or lfashion != fashion:
                store_data_in_database(lgender, lage, lfashion)
                
            # showad(gender, age)
        cv2.imshow("Detection Window", frame)
        k =cv2.waitKey(1)
        if k == ord('q'):
            break
    
    video.release()
    cv2.destroyAllWindows()
    
def runad():
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    t1 = threading.Thread(target=rundetector)
    t2 = threading.Thread(target=runad)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()