from __future__ import print_function
from __future__ import division

import cv2
import argparse
import os
import math

# Algorithm parameters
COMBINE_FACE_WEIGHT = 10
COMBINE_FEATURE_WEIGHT = 10
FEATURE_DETECT_MAX_CORNERS = 50
FEATURE_DETECT_QUALITY_LEVEL = 0.1
FEATURE_DETECT_MIN_DISTANCE = 10
FACE_DETECT_REJECT_LEVELS = 1.3
FACE_DETECT_LEVEL_WEIGHTS = 5

cascade_path = os.path.dirname(__file__) + '/cascades/haarcascade_frontalface_default.xml'


def center_from_faces(matrix):
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(matrix, FACE_DETECT_REJECT_LEVELS, FACE_DETECT_LEVEL_WEIGHTS)

    x, y = (0, 0)
    weight = 0

    # iterate over our faces array
    for (x, y, w, h) in faces:
        print('Face detected at ', x, y, w, h)
        weight += w * h
        x += (x + w / 2) * w * h
        y += (y + h / 2) * w * h

    if len(faces) == 0:
        return False

    return {
        'x': x / weight,
        'y': y / weight,
        'count': len(faces)
    }


def center_from_good_features(matrix):
    x, y = (0, 0)
    weight = 0
    corners = cv2.goodFeaturesToTrack(matrix, FEATURE_DETECT_MAX_CORNERS, FEATURE_DETECT_QUALITY_LEVEL,
                                      FEATURE_DETECT_MIN_DISTANCE)

    for point in corners:
        weight += 1
        x += point[0][0]
        y += point[0][1]

    return {
        'x': x / weight,
        'y': y / weight,
        'count': weight
    }


def exact_crop(center, original_width, original_height, target_width, target_height):
    top = max(center['y'] - math.floor(target_height / 2), 0)
    offset_h = top + target_height
    if offset_h > original_height:
        # overflowing
        # print("Top side over by ", offsetH - original_height)
        top = top - (offset_h - original_height)
    top = max(top, 0)
    bottom = min(offset_h, original_height)

    left = max(center['x'] - math.floor(target_width / 2), 0)
    offset_w = left + target_width
    if offset_w > original_width:
        # overflowing
        # print("Left side over by ", offsetW - original_width)
        left = left - (offset_w - original_width)
    left = max(left, 0)
    right = min(left + target_width, original_width)

    return {
        'left': left,
        'right': right,
        'top': top,
        'bottom': bottom
    }


def auto_resize(image, target_width, target_height):
    height, width, depth = image.shape

    ratio = target_width / width
    w, h = width * ratio, height * ratio
    p = 1

    # if there is still height or width to compensate, let's do it
    if w - target_width < 0 or h - target_height < 0:
        ratio = max(target_width / w, target_height / h)
        w, h = w * ratio, h * ratio
        p = 2

    image = cv2.resize(image, (int(w), int(h)))
    print("Image resized by", w - width, "*", h - height, "in", p, "pass(es)")

    return image


def auto_center(matrix):
    face_center = center_from_faces(matrix)
    center = {'x': 0, 'y': 0}

    if not face_center:
        print('Using Good Feature Tracking method')
        center = center_from_good_features(matrix)
    else:
        print('Combining with Good Feature Tracking method')
        features_center = center_from_good_features(matrix)
        face_w = features_center['count'] * COMBINE_FACE_WEIGHT
        feat_w = features_center['count'] * COMBINE_FEATURE_WEIGHT
        t_w = face_w + feat_w
        center['x'] = (face_center['x'] * face_w + features_center['x'] * feat_w) / t_w
        center['y'] = (face_center['y'] * face_w + features_center['y'] * feat_w) / t_w

        print('Face center', face_center)
        print('Feat center', features_center)

    return center


def smart_crop(image, target_width, target_height, destination, do_resize):
    # read grayscale image
    original = cv2.imread(image)

    if original is None:
        print("Could not read source image")
        exit(1)

    target_height = int(target_height)
    target_width = int(target_width)

    if do_resize:
        original = auto_resize(original, target_width, target_height)

    # build the grayscale image we will work onto
    matrix = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    height, width, depth = original.shape

    if target_height > height:
        print('Warning: target higher than image')

    if target_width > width:
        print('Warning: target wider than image')

    # center = center_from_faces(matrix)
    #
    # if not center:
    #     print('Using Good Feature Tracking method')
    #     center = center_from_good_features(matrix)
    center = auto_center(matrix)

    print('Found center at', center)

    crop_pos = exact_crop(center, width, height, target_width, target_height)
    print('Crop rectangle is', crop_pos)

    cropped = original[int(crop_pos['top']): int(crop_pos['bottom']), int(crop_pos['left']): int(crop_pos['right'])]
    cv2.imwrite(destination, cropped)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-W", "--width", required=True, help="Target width")
    ap.add_argument("-H", "--height", required=True, help="Target height")
    ap.add_argument("-i", "--image", required=True, help="Image to crop")
    ap.add_argument("-o", "--output", required=True, help="Output")
    ap.add_argument("-n", "--no-resize", required=False, default=False, action="store_true",
                    help="Don't resize image before treating it")

    args = vars(ap.parse_args())

    smart_crop(args["image"], args["width"], args["height"], args["output"], not args["no_resize"])


if __name__ == '__main__':
    img_input = "input.jpg"
    img_output = "output.jpg"
    img_width = 400
    img_height = 300
    smart_crop(img_input, img_width, img_height, img_output, None)

    img_input = "input2.jpg"
    img_output = "output2.jpg"
    img_width = 400
    img_height = 300
    smart_crop(img_input, img_width, img_height, img_output, None)
