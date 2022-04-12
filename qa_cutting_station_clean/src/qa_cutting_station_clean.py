""" LCSR-CIIS-Sanaria Mosquito Vision - Image Processing
    Main Script for Cutting Station Clean Detection
    Cascaded Image Processing approach
    by John Han 
"""

import glob
import os
import numpy as np
import cv2 as cv
import math

# TODO: implement the ROI parameters (need to somehow handle that automatically)
# TODO: make it so that there is no hardcoded absolute path
# TODO: instead of counting pixels, use calibration to measure the actual size of white pixels 

def blob_detection(img_path):
    
    # first read in the image
    img = cv.imread(img_path)

    # convert to grayscale and get the ROI
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    height = img_gray.shape[0]
    img_roi = img_gray[1:math.floor(height/13), 450:1300]

    # adaptive thresholding 
    img_thresh = cv.adaptiveThreshold(img_roi, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 251, 13)
    img_thresh = 255 - img_thresh

    # morphological denoising
    kernel = np.ones((4,2), np.uint8)
    img_thresh_open = cv.morphologyEx(img_thresh, cv.MORPH_OPEN, kernel)

    kernel3 = np.ones((7,7), np.uint8)
    img_close = cv.morphologyEx(img_thresh_open, cv.MORPH_CLOSE, kernel3)

    kernel4 = np.ones((2,2), np.uint8)
    img_dilate = cv.dilate(img_close, kernel4, iterations = 1)

    kernel2 = np.ones((6,5), np.uint8)
    img_thresh_open2 = cv.morphologyEx(img_dilate, cv.MORPH_OPEN, kernel2)

    # count number of white pixels
    count_ones = np.count_nonzero(img_thresh_open2 != 0)

    # debugging
    temp = np.vstack((img_roi, img_thresh, img_thresh_open2))
    cv.imshow('hi', temp)
    cv.waitKey(0)

    # print(count_ones)
    if count_ones > 9000:
        return 1 # if dirty
    else:
        return 0 # if clean

def main():
    
    # initialize and hardcode some paths 
    # clean_dir = []
    # dirty_dir = []
    # images_dir = '/home/juseonghan/cis/qa_cutting_station_clean/data'

    # print('Saving results to /home/juseonghan/cis/qa_cutting_station_clean/data')

    # print('Processing images...')

    # # clean the results directory
    # os.system('rm /home/juseonghan/cis/qa_cutting_station_clean/results/clean/*.png')
    # os.system('rm /home/juseonghan/cis/qa_cutting_station_clean/results/dirty/*.png')

    # # loop through all images and detect mosquitos; if so, copy them to the results dir
    # for img in os.listdir(images_dir):
    #     result = blob_detection(os.path.join(images_dir, img))
    #     if result == 0:
    #         clean_dir.append(os.path.join(images_dir, img))
    #         os.system('cp ' + os.path.join(images_dir, img) + ' /home/juseonghan/cis/qa_cutting_station_clean/results/clean')
    #     else:
    #         dirty_dir.append(os.path.join(images_dir, img))
    #         os.system('cp ' + os.path.join(images_dir, img) + ' /home/juseonghan/cis/qa_cutting_station_clean/results/dirty')

    # print('Saving Results...')

    # # write results to textfile
    # output_file = open('clean_res.txt', 'w')
    # for clean in clean_dir:
    #     output_file.write(clean)
    #     output_file.write('\n')
    # output_file.close()

    # output_file = open('dirty_res.txt', 'w')
    # for dirty in dirty_dir:
    #     output_file.write(dirty)
    #     output_file.write('\n')
    # output_file.close()

    # print('Wrote result txtfile to /home/juseonghan/cis/qa_cutting_station_clean/src')

    blob_detection('/home/juseonghan/cis/qa_cutting_station_clean/data/20220213-163212.808_pick.png')

if __name__ == '__main__':
    main()