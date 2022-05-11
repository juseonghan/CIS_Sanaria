import sys
import os 
import cv2 as cv
import glob
import numpy as np
import json

def main():
    
    img_dir = 'data'
    checked = []
    legend = {}
    i = 0

    for img in os.listdir(img_dir):
        f = os.path.join(img_dir, img)
        code = f[14:20]
        
        if code in checked:
            continue 

        print('Processing', code, '...')
        checked.append(code)

        temp_strings = '/home/juseonghan/cis/qa_exudate/data/*' + str(code) + '*.png'
        same_imgs = glob.glob(temp_strings)
        if (len(same_imgs) != 2):
            continue

        first = same_imgs[0]
        if (first[-6:] == 'si.png'):
            same_imgs.reverse()

        # first the si img
        img_si = cv.imread(same_imgs[1])
        cropped_si = img_si[400:700, 350:700,:]

        # next the fr imgd
        img_fr = cv.imread(same_imgs[0])
        cropped_fr = img_fr[400:700, 585:935,:]

        # combine them together
        appended = np.vstack((cropped_si, cropped_fr))

        # add to legend 
        legend[i] = code 

        # imwrite
        save_path = '/home/juseonghan/cis/qa_exudate/res/' + str(i) + '.png'
        cv.imwrite(save_path, appended)
    
        i = i + 1 
        
    
    with open('legend.json', 'w') as f:
        f.write(json.dumps(legend))

    print('wrote to legend.json')

if __name__ == "__main__":
    main()