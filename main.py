import cv2
import numpy as np
import HandTrackingModule as htm


def draw_header(frame, selected_color):
    cv2.rectangle(frame, (0, 0), (640, 100), (50, 50, 50), cv2.FILLED)

    cv2.rectangle(frame, (10, 10), (150, 90), (255, 0, 255), cv2.FILLED)
    cv2.putText(frame, "PINK", (50, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    cv2.rectangle(frame, (170, 10), (310, 90), (255, 0, 0), cv2.FILLED)
    cv2.putText(frame, "BLUE", (200, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    cv2.rectangle(frame, (330, 10), (470, 90), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, "GREEN", (360, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

    cv2.rectangle(frame, (490, 10), (630, 90), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, "ERASER", (510, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)

    if selected_color == (255, 0, 255):
        cv2.rectangle(frame, (5, 5), (155, 95), (255, 255, 255), 3)
    elif selected_color == (255, 0, 0):
        cv2.rectangle(frame, (165, 5), (315, 95), (255, 255, 255), 3)
    elif selected_color == (0, 255, 0):
        cv2.rectangle(frame, (325, 5), (475, 95), (255, 255, 255), 3)
    elif selected_color == (0, 0, 0):
        cv2.rectangle(frame, (485, 5), (635, 95), (0, 0, 255), 3)

    return frame

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = htm.handDetector(maxHands=1, detectionCon=0.75)

    drawColor = (255, 0, 255)
    brushThickness = 12
    eraserThickness = 50
    xp, yp = 0, 0
    imgCanvas = np.zeros((480, 640, 3), np.uint8)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = detector.findHands(frame)
        lmList, _ = detector.findPosition(frame, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1], lmList[8][2]

            finger1_open = lmList[8][2] < lmList[6][2]
            finger2_open = lmList[12][2] < lmList[10][2]

            if finger1_open and finger2_open:
                xp, yp = 0, 0
                cv2.circle(frame, (x1, y1), 10, drawColor, cv2.FILLED)

                if y1 < 100:
                    if 0 < x1 < 160:
                        drawColor = (255, 0, 255)
                    elif 160 < x1 < 320:
                        drawColor = (255, 0, 0)
                    elif 320 < x1 < 480:
                        drawColor = (0, 255, 0)
                    elif 480 < x1 < 640:
                        drawColor = (0, 0, 0)

            elif finger1_open and not finger2_open:
                cv2.circle(frame, (x1, y1), 8, drawColor, cv2.FILLED)

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else:
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1
            else:
                xp, yp = 0, 0

        frame = cv2.addWeighted(frame, 0.8, imgCanvas, 0.8, 0)
        frame = draw_header(frame, drawColor)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord('c'):
            imgCanvas = np.zeros((480, 640, 3), np.uint8)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()