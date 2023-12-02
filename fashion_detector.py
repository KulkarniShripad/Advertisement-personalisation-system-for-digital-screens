import argparse
import torch
import cv2
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression
from torchvision import transforms
from PIL import Image
import numpy as np

class_label = ""
# Class labels
class_labels = [
    'Shirt', 'Mobile_phone', 'Glasses', 'Headphones', 'Human_beard', 
    'Necklace', 'Watch', 'Coat', 'Earrings', 'Jeans', 'Pen', 'Tie'
]

def load_model():
    global model
    global args
    global imgsz
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='content\yolov5\\runs\\train\exp\weights\last.pt', help='Path to custom model weights')
    parser.add_argument('--img-size', type=int, default=640, help='Inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='Confidence threshold for detections')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IoU threshold for non-maximum suppression')
    parser.add_argument('--device', default='cpu', help='Cuda device (e.g., 0 or cpu)')
    args = parser.parse_args()

    # Load the custom model
    model = attempt_load(args.weights)
    stride = int(model.stride.max())
    imgsz = check_img_size(args.img_size, s=stride)

def detect_fashion(frame):
    global class_label
    # Load and preprocess the frame
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # Resize the frame to the model's expected size (3, 640, 640)
    transform = transforms.Compose([
        transforms.Resize((640, 640), interpolation=Image.BILINEAR),
        transforms.ToTensor(),
    ])
    
    img = transform(img_pil).unsqueeze(0).to(args.device)

    # Run inference
    pred = model(img, augment=False)[0]
    pred = non_max_suppression(pred, args.conf_thres, args.iou_thres, max_det=1000)[0]

    # Process and draw bounding boxes
    if len(pred):
        pred[:, :4] = pred[:, :4].clamp(0, 1)
        for det in pred:
            xyxy = (det[:4] * imgsz).int().cpu().numpy()
            label = int(det[5])
            confidence = det[4].cpu().numpy()
            class_label = class_labels[label]
            
            # Draw bounding boxes
            # color = (0, 255, 0)  # Green color
            # frame = cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
            print("Class label : ",class_label)
            # cv2.putText(frame, f'{class_label} {confidence:.2f}', (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    if class_label == "":
        return "None"
    else :
        return class_label 