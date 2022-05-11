import glob 
import math
import numpy as np
import cv2 as cv


def calculate_blob_volume_fr(img_path):
    # first read in the image
    img = cv.imread(img_path)

    # grayscale conversion with ROI def
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_roi = img_gray[400:800, 680:980]
    img_blur = cv.blur(img_roi, (10,10))
    img_histeq = cv.equalizeHist(img_blur)
    img_contrast = 255 - img_histeq

    # threshold the image for binarization
    img_thresh = cv.adaptiveThreshold(img_contrast, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 121, 1)

    #_, img_thresh = cv.threshold(img_histeq, 140, 255, cv.THRESH_BINARY)
    
    # erode the image for connected component 
    kernel = np.ones((3,3), np.uint8)
    img_erode = cv.erode(img_thresh, kernel)

    mask = np.zeros_like(img_roi)
    #mask[math.floor(mask.shape[0]/2 - 5):math.floor(mask.shape[0]/2 + 5), math.floor(mask.shape[1]/2 - 5): math.floor(mask.shape[1]/2) + 5] = 255
    mask[140:145, 140:150] = 255

    img_reconstruct = imreconstruct(mask, img_erode, 2)

    kernel2 = np.ones((15,15), np.uint8)
    img_dilate = cv.dilate(img_reconstruct, kernel2)

    # apply the mask to the original grayscale image 
    img_seg = cv.bitwise_and(img_roi, img_roi, mask=img_dilate)

    temp = np.hstack((img_roi, img_histeq, img_thresh, img_erode, img_reconstruct, img_seg))
    cv.imshow('hi', temp)
    cv.waitKey(0)
    cv.destroyAllWindows()

def calculate_blob_volume_si(img_path):
    # first read in the image
    img = cv.imread(img_path)

    # grayscale conversion with ROI def
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_roi = img_gray[560:650, 450:510]

    #img_blur = cv.blur(img_roi, (10,10))
    #img_histeq = cv.equalizeHist(img_blur)
    img_contrast = 255 - img_roi

    # threshold the image for binarization
    img_thresh = cv.adaptiveThreshold(img_contrast, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 213, 3)
    #_, img_thresh = cv.threshold(img_contrast,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    #_, img_thresh = cv.threshold(img_histeq, 140, 255, cv.THRESH_BINARY)
    
    # erode the image for connected component 
    kernel = np.ones((5,5), np.uint8)
    #img_erode = cv.erode(img_thresh, kernel)
    opening = cv.morphologyEx(img_thresh, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

    mask = np.zeros_like(img_roi)
    #mask[math.floor(mask.shape[0]/2 - 5):math.floor(mask.shape[0]/2 + 5), math.floor(mask.shape[1]/2 - 5): math.floor(mask.shape[1]/2) + 5] = 255
    mask[140:145, 140:150] = 255

    # img_reconstruct = imreconstruct(mask, img_erode, 2)

    kernel2 = np.ones((5,5), np.uint8)
    img_erode = cv.erode(closing, kernel2)
    #img_dilate = cv.dilate(img_reconstruct, kernel2)

    # apply the mask to the original grayscale image 
    #img_seg = cv.bitwise_and(img_roi, img_roi, mask=img_dilate)

    temp = np.hstack((img_roi, img_thresh, img_erode))
    cv.imshow('hi', temp)
    cv.waitKey(0)
    cv.destroyAllWindows()

def imreconstruct(marker: np.ndarray, mask: np.ndarray, radius: int = 1):
    """Iteratively expand the markers white keeping them limited by the mask during each iteration.

    :param marker: Grayscale image where initial seed is white on black background.
    :param mask: Grayscale mask where the valid area is white on black background.
    :param radius Can be increased to improve expansion speed while causing decreased isolation from nearby areas.
    :returns A copy of the last expansion.
    Written By Semnodime
    
    """
    kernel = np.ones(shape=(radius * 2 + 1,) * 2, dtype=np.uint8)
    while True:
        expanded = cv.dilate(src=marker, kernel=kernel)
        cv.bitwise_and(src1=expanded, src2=mask, dst=expanded)

        # Termination criterion: Expansion didn't change the image at all
        if (marker == expanded).all():
            return expanded
        marker = expanded

def main():
    #calculate_blob_volume_fr('/home/juseonghan/cis/qa_exudate/data/20220317-170036.700_squeez_t1_fr.png')
    calculate_blob_volume_si('/home/juseonghan/cis/qa_exudate/data/20220213-163833.598_squeez_t1_si.png')
    # im = cv.imread('/home/juseonghan/cis/qa_exudate/data/20220213-163833.598_squeez_t1_si.png')
    # cv.imshow('hi', im)
    # cv.waitKey(0)

if __name__ == '__main__':
    main()