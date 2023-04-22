import cv2 as cv
import numpy as np
import pytesseract as pt

pt.pytesseract.tesseract_cmd = 'Car_Num_Plate_Detection\\pytessereact\\tesseract.exe'

class PlateDetect:
    def __init__(self, verbose=True):
        self.img = None
        self.verbose = verbose

    def process_img(self):
        '''Basic processing of color image'''
        if self.verbose: print('Processing Image ...')
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        blurred = cv.bilateralFilter(gray, 11, 17, 17)
        edged = cv.Canny(blurred, 170, 200)
        return edged

    def detect_rects(self, img):
        '''Detects all possible rectangle which could be number plates from a processed image'''
        eligible_rects = []
        blank = np.zeros((*img.shape, 3), dtype=np.uint8)
        blank[:, :, 0] = img.copy()
        blank[:, :, 1] = img.copy()
        blank[:, :, 2] = img.copy()
        contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours

    def box_check(self, contour_list):
        eligible_rects = []
        if self.verbose: print('Searching for possible plates ...')
        for cnt in contour_list:
            # minAreaRect returns center(x, y), (width, height), angle
            # boxPoints gives the vertices of rotated rect
            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.intp(box) # Converts float values to int
            width = rect[1][0]
            height = rect[1][1]
            if width == 0 or height == 0:
                continue
            eligible_rects.append(box)
        
        return eligible_rects

    def clean_cords(self, cord_list):
        '''Removes coordinates which are repeated'''
        if self.verbose: print('Filtering unwanted plates ...')
        cord_list = np.array(cord_list)
        rem_rows = [*np.where(cord_list<0)[0]]
        for i, cord in enumerate(cord_list):
            flag = (np.where((cord_list[:i] - cord) == 0)[0]).tolist()
            if flag:
                rem_rows.append(i)

        cord_list = np.delete(cord_list, rem_rows, axis=0)
        return cord_list

    def detect_plate(self, img):
        '''Returns final values conataining number plate'''
        text_list = []
        self.img = img
        draw_img = img.copy()
        edged_img = self.process_img()
        contours = self.detect_rects(edged_img)

        top_plates = sorted(contours, key=cv.contourArea, reverse=True)[:5]
        boxes = self.box_check(top_plates)

        cropped_img = np.zeros((25, 25, 3), dtype=np.uint8)
        if self.verbose:
            print('Reading the plate ...')
            cv.drawContours(draw_img, top_plates, -1, (255, 0, 0), 2)
            cv.imshow("Most", draw_img)

        for id, box in enumerate(boxes):
            x, y, w, h = cv.boundingRect(box)
            if x < 0 or y < 0 or w < 0 or h < 0:
                continue
            cropped_img = img[y:y+h, x:x+w]

            cv.imwrite(str(id) + '.png', cropped_img)
            img_rgb = cv.cvtColor(cropped_img, cv.COLOR_BGR2RGB)
            text = pt.image_to_string(img_rgb)
            # print(text)
            if len(text) >= 7:
                text_list.append(text)
                # if self.verbose: cv.drawContours(img, [box], -1, (0, 255, 0), 2)
                # if self.verbose: cv.imshow('Detected Plate', img)
                break
        # print(f'Numbers: {text_list}')
        if not text_list:
            return False, ''
        return True, text_list[0]

def main():
    img_path = 'Car_Num_Plate_Detection\\Data\\Pictures\\005.png'
    img_arr = cv.imread(img_path)
    detector = PlateDetect()
    plate_num = detector.detect_plate(img_arr)
    print(f'Number Plate detected: {plate_num}')

    cv.waitKey(0)

if __name__ == "__main__":
    main()

