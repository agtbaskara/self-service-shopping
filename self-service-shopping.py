import face_recognition
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import time
import os
from threading import Thread

def decode_qr(input_frame):
    """
    Decode QR in frame return a list of detected QR
    """
    detected_list = []
    input_frame = FrameThread.frame_qr
    for i in range (0, 50):
        decodedObjects = pyzbar.decode(input_frame)
        for obj in decodedObjects:
            if obj.data.decode('ascii') not in detected_list:
                detected_list.append(obj.data.decode('ascii'))
            points = obj.polygon
            if len(points) > 4 : 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else : 
                hull = points
            n = len(hull)
            for j in range(0, n):
                cv2.rectangle(input_frame, hull[j], hull[ (j+1) % n], (0,0,0), 3)
    return detected_list

class FrameCapture:
    """
    Class for getting frame from cap
    """
    def __init__(self):
        self.video_capture_face = cv2.VideoCapture(0)
        self.video_capture_qr = cv2.VideoCapture(1)
        (self.grabbed_face, self.frame_face) = self.video_capture_face.read()
        (self.grabbed_qr, self.frame_qr) = self.video_capture_qr.read()
        self.stopped = False

        self.frame_face_small = cv2.resize(self.frame_face.copy(), (0, 0), fx=0.25, fy=0.25)
        self.frame_qr_small = cv2.resize(self.frame_qr.copy(), (0, 0), fx=0.25, fy=0.25)
        self.preview = np.concatenate((self.frame_face_small, self.frame_qr_small), axis=1)
    
    def start(self):
        """
        Start get thread
        """
        Thread(target = self.get, args = ()).start()
        return self

    def stop(self):
        """
        Stop Image Processing thread
        """
        self.stopped = True
        self.video_capture_face.release()
        self.video_capture_qr.release()
    
    def get(self):
        """
        Thread to capture frame from camera
        """
        while not self.stopped:
            if not (self.grabbed_face or self.grabbed_qr):
                self.stop()
            else:
                (self.grabbed_face, self.frame_face) = self.video_capture_face.read()
                (self.grabbed_qr, self.frame_qr) = self.video_capture_qr.read()
            self.frame_face_small = cv2.resize(self.frame_face.copy(), (0, 0), fx=0.7, fy=0.7)
            self.frame_qr_small = cv2.resize(self.frame_qr.copy(), (0, 0), fx=0.7, fy=0.7)
            self.preview = np.concatenate((self.frame_face_small, self.frame_qr_small), axis=0)
            cv2.imshow('Preview', self.preview)
            cv2.waitKey(1)
                
# Initialize Frame Capture Thread
FrameThread = FrameCapture()
FrameThread.start()

# Load Face Image
a_image = face_recognition.load_image_file("face/a.jpg")
b_image = face_recognition.load_image_file("face/b.jpg")
c_image = face_recognition.load_image_file("face/c.jpg")

# Recognize Face Image
a_face_encoding = face_recognition.face_encodings(a_image)[0]
b_face_encoding = face_recognition.face_encodings(b_image)[0]
c_face_encoding = face_recognition.face_encodings(c_image)[0]

# Create List Of Face Encoding
known_face_encodings = [
    a_face_encoding,
    b_face_encoding,
    c_face_encoding
]

# Create List Names
known_face_names = [
    "Alpha",
    "Baskara",
    "Charlie"
]

# Create List Saldo
saldo = [
    90000,
    20000,
    30000
]

# Create Product List
product_index = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
]

product_name = [
    "Indomie",
    "Beng-Beng",
    "Permen",
    "Choki-Choki",
    "Aqua",
    "Teh Gelas"
]

# Initialize variable
face_locations = []
face_encodings = []
face_names = []

while True:
    # Get Frame from Frame Capture Thread
    frame_face = FrameThread.frame_face

    # Resize then convert to RGB
    small_frame = cv2.resize(frame_face, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Detect All Face
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Match Face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    if face_names == []:
        os.system('clear')
        print("TOKO SEPI GAN")
    elif "Unknown" in face_names:
        os.system('clear')
        print("Anda Siapa ?")
    else:
        list_produk = []
        list_produk = decode_qr(FrameThread.frame_qr)
        shopping_time = 15
        os.system('clear')
        start_time = time.time()
        print("Halo", face_names[0], "Selamat Berbelanja")
        print("Saldo Anda", saldo[first_match_index])
        print("-!!- PROMO HARGA FLAT 1000 SADJA -!!-")
        print("Produk Yang Tersedia:")
        for obj in list_produk:
            print(product_name[product_index.index(obj)])
        time.sleep(shopping_time)
        list_produk_akhir = []
        list_produk_akhir = decode_qr(FrameThread.frame_qr)
        jumlah_terambil = len(list_produk)-len(list_produk_akhir)
        if jumlah_terambil == 0:
            print("Anda tidak berbelanja apapun :(")
        elif jumlah_terambil > 0:
            print("Anda mengambil", jumlah_terambil, "barang")
            print("Total Belanja", jumlah_terambil*1000)
            saldo[first_match_index] = saldo[first_match_index] - jumlah_terambil*1000
            print("Saldo Anda Sekarang", saldo[first_match_index])
            print("Terima Kasih Sudah Berbelanja", face_names[0], "!")
            time.sleep(5)
        elif jumlah_terambil < 0:
            print("Anda mengambil", jumlah_terambil, "barang")
            print("Hmm... Anda kok malah menjual barang ?")
            print("Total Belanja", jumlah_terambil*1000)
            saldo[first_match_index] = saldo[first_match_index] - jumlah_terambil*1000
            print("Saldo Anda Sekarang", saldo[first_match_index])
            print("Terima Kasih Sudah Berbelanja (Berjualan)", face_names[0], "!")
            time.sleep(5)

    time.sleep(0.5)