import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import cv2
import csv


def convertImage(filepath):
    def createImageFile(filename):
        '''
        Create new file in the same directory with the given file name
        '''
        filename = filename + ".png"
        f = open(filename, "w+")
        f.close()
        return "./static/" + filename

    # read the input dicom image
    ds = dicom.dcmread(filepath)

    # print(ds.data_element)
    pixel_array_numpy = ds.pixel_array

    # convert to float to avoid overflow or underflow losses
    image_2d = pixel_array_numpy.astype(float)

    # rescaling to gray image
    image_2d_gray = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # convert to uint8
    image_2d_gray = np.uint8(image_2d_gray)

    # create output image file
    dest = createImageFile('result')

    # write image to output file
    cv2.imwrite(dest, image_2d_gray)

    # read the image from the output file
    image = cv2.imread(dest)

    # show the original image & output image
    # plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.imshow(pixel_array_numpy, cmap='gray')
    # plt.subplot(1, 2, 2)
    # plt.imshow(image)
    # plt.show()

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
