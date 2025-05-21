import cv2
import numpy as np


def detect_circles():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret: break
        h, w = frame.shape[:2]
        size = 200
        x1, y1 = (w - size) // 2, (h - size) // 2
        x2, y2 = x1 + size, y1 + size
        color = (255, 0, 0)  # Синий по умолчанию


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9, 9), 0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100,
                                   param1=80, param2=40, minRadius=30, maxRadius=250)


        if circles is not None:
            x, y, r = np.uint16(np.around(circles))[0][0]
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

            if x1 < x < x2 and y1 < y < y2:
                color = (0, 0, 255)  # Красный если в зоне
                cv2.putText(frame, "CENTER", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 50, 200), 2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.imshow('Circle Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_circles())