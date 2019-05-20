# self-service-shopping

A Proof-of-Concept program of cashierless self service shopping with image processing.
Final Project Pengolahan Citra Digital 2018

## Requirment

- Linux (Tested on Ubuntu 18.04)
- 2 Webcam (1 for Face Recognition, 1 for QR Code Reader)
- Anaconda 3
- OpenCV 3
- dlib
- numpy
- face_recognition
- pyzbar

## How to Install

Setup a Python 3 Anaconda Environment

- Install `numpy`
    ```bash
    conda install -c conda-forge numpy
    ```
- Install `opencv`
    ```bash
    conda install -c conda-forge opencv
    ```
- Install `dlib`
    ```bash
    conda install -c conda-forge dlib  
    ```
- Install `face_recognition`
    ```bash
    pip install face_recognition
    ```
- Install `pyzbar`
    ```bash
    sudo apt-get install libzbar0
    ```
    ```bash
    pip install pyzbar
    ```

## How to Run

```python
python3 self-service-shopping.py
```
