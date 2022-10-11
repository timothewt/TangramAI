import cv2 as cv


class TangramSolver:
    def __init__(self, image_path):
        self.image = self.load_image(image_path)  # image of the shape we want to reproduce with the tangram pieces

    def load_image(self, path):
        """
        loads the image into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white
        :param path: path of the image
        :return: a 2d numpy array of the resized b&w image
        """
        img = cv.imread(path)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        b_w_img = self.to_b_w(gray_img)
        resized_img = self.resize_image(b_w_img)
        resized_img_b_w = self.to_b_w(resized_img)  # to b&w to eliminate gray pixels
        return resized_img_b_w

    def resize_image(self, img):
        """
        resizes the image for the area of the drawing to match the area of all the tangram pieces, which is 360*360
        :param img: image we want to resize
        :return: the np array of the black and white resized image
        """
        (h, w) = img.shape[:2]
        resize_ratio = pow(280, 2) / (img < 10).sum()  # 280 being the side of the tangram pieces square, divided by the
        # number of black pixel on the image which represent the area of the goal shape
        (new_h, new_w) = (int(resize_ratio * h), int(resize_ratio * w))
        resized_image = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)
        return resized_image

    def to_b_w(self, image):
        """
        turns a picture to black and white
        :param image: image we want to convert to b&w
        :return: the np array of the black (0) and white (255) pixels
        """
        b_w_image = cv.threshold(image, 230, 255, cv.THRESH_BINARY)[1]
        return b_w_image


if __name__ == "__main__":
    ai_tangram = TangramSolver('tangram_unsolved.png')
    cv.imshow("dqsf",ai_tangram.image)
    cv.waitKey(0)
