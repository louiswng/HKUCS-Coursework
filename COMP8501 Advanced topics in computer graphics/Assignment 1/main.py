import cv2
import argparse

from poisson import poisson_edit


def main(args):
    source = cv2.imread(args.src_img)
    target = cv2.imread(args.tgt_img)
    mask = cv2.imread(args.mask_img)[:, :, 0]
    height, width = target.shape[:2]
    center = (width // 2, height // 2)
    output = poisson_edit(source, target, mask, center)
    cv2.imwrite(args.res_img, output)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_img", type=str, default="source.jpg")
    parser.add_argument("--tgt_img", type=str, default="target.jpg")
    parser.add_argument("--mask_img", type=str, default="mask.jpg")
    parser.add_argument("--res_img", type=str, default="result.jpg")
    args = parser.parse_args()

    main(args)