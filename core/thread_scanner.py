import cv2
from pyzbar import pyzbar

from PySide6.QtCore import QObject, Signal


class ThreadScanner(QObject):

    barcode_found = Signal(str)
    finished = Signal()

    def run(self):

        cap = None

        # Find working camera
        for i in range(5):

            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

            if cap.isOpened():
                print(f"Using camera index {i}")
                break

        if not cap or not cap.isOpened():
            print("No camera found")
            self.finished.emit()
            return

        # Set resolution (helps barcode detection)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        print("Camera started")

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:

                x, y, w, h = barcode.rect

                # Draw detection rectangle
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                code = barcode.data.decode("utf-8")

                # Show barcode value
                cv2.putText(
                    frame,
                    code,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                print("Barcode detected:", code)

                cap.release()
                cv2.destroyAllWindows()

                self.barcode_found.emit(code)
                self.finished.emit()

                return

            cv2.imshow(
                "Scan Thread Barcode (ESC to cancel)",
                frame
            )

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        print("Scanner closed")

        self.finished.emit()