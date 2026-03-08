import cv2
import tempfile
import os

from core.svg_importer import import_svg


MAX_SIZE = 1200


def import_image(path, log=None):

    img = cv2.imread(path)

    if img is None:
        raise Exception("Failed to read image")

    h, w = img.shape[:2]

    if log:
        log(f"Image size: {w}x{h}")

    if max(w, h) > MAX_SIZE:

        scale = MAX_SIZE / max(w, h)

        new_w = int(w * scale)
        new_h = int(h * scale)

        img = cv2.resize(img, (new_w, new_h))

        if log:
            log(f"Resized image to: {new_w}x{new_h}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    if log:
        log("Detecting contours...")

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_NONE
    )

    if log:
        log(f"Detected {len(contours)} shapes")

    # create temporary svg
    tmp_svg = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
    tmp_svg_path = tmp_svg.name
    tmp_svg.close()

    try:

        with open(tmp_svg_path, "w") as f:

            f.write('<svg xmlns="http://www.w3.org/2000/svg">\n')

            for contour in contours:

                if len(contour) < 3:
                    continue

                path_data = "M "

                for p in contour:
                    x, y = p[0]
                    path_data += f"{x},{y} "

                path_data += "Z"

                f.write(f'<path d="{path_data}" />\n')

            f.write("</svg>")

        # reuse your working svg importer
        objects = import_svg(tmp_svg_path)

        return objects

    finally:

        if os.path.exists(tmp_svg_path):
            os.remove(tmp_svg_path)