import cv2
from pyzbar import pyzbar


def capture_qr():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objs = pyzbar.decode(frame)
        for obj in decoded_objs:
            qr_data = obj.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return qr_data

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None