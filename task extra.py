import cv2
import numpy as np


def circle_detector():
    cap = cv2.VideoCapture(0)
    fly = cv2.imread("images/fly64.png", cv2.IMREAD_UNCHANGED)

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Поиск кругов
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9, 9), 0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100,
                                   param1=80, param2=40, minRadius=30, maxRadius=250)

        if circles is not None:
            x, y, r = np.uint16(np.around(circles))[0][0]
            print(f"Center: ({x}, {y})")

            # Позиция мухи
            h, w = fly.shape[:2]
            x1 = x - w // 2
            y1 = y - h // 2
            x2 = x1 + w
            y2 = y1 + h

            # Проверка границ кадра
            if x1 >= 0 and y1 >= 0 and x2 <= frame.shape[1] and y2 <= frame.shape[0]:
                # Наложение с прозрачностью
                if fly.shape[2] == 4:
                    alpha = fly[:, :, 3] / 255.0
                    for c in range(3):
                        frame[y1:y2, x1:x2, c] = (1 - alpha) * frame[y1:y2, x1:x2, c] + alpha * fly[:, :, c]
                else:
                    frame[y1:y2, x1:x2] = fly

        cv2.imshow('Fly Tracking', frame)
        if cv2.waitKey(1) == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    circle_detector()