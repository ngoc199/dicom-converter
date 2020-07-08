import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import cv2
import csv


def createImageFile(filename):
    '''
    Create new file in the same directory with the given file name
    '''
    filename = filename + ".png"
    path = './static/'+filename
    f = open(path, "w+")
    f.close()
    return path


def convertImage(filepath, filename):

    # read the input dicom image
    ds = dicom.dcmread(filepath)

    # print(ds.data_element)
    pixel_array_numpy = ds.pixel_array

    # convert to float to avoid overflow or underflow losses
    image_2d = pixel_array_numpy.astype(float)

    # convert to uint8
    image_2d_gray = np.uint8(image_2d)

    # create output image file
    dest = createImageFile(filename)

    # write image to output file
    cv2.imwrite(dest, image_2d_gray)

    # read the image from the output file
    image = cv2.imread(dest)

    # Extract information to csv file
    with open('Patient_Detail.csv', 'w', newline='') as csvfile:
        fieldnames = list(ds.dir())
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldnames)
        row = []

        # get data from all fields
        for field in fieldnames:
            if (ds.data_element(field) is None):
                row.append('')
            else:
                data_row = str(ds.data_element(field)).replace("'", "")
                print(data_row)
                begin_index = data_row.find(':')
                data_row = data_row[begin_index+2:]
                row.append(data_row)

        # Write data row to csv file
        writer.writerow(row)
        return dest


def get_dicom_data():
    '''Get the patient detail data from csv file'''
    with open('Patient_Detail.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
        return data
