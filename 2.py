from teachable_machine import TeachableMachine
import cv2

# 모델 로딩
my_model = TeachableMachine(model_path = 'keras_model.h5', model_type='h5')

# 라벨
names = []
with open('labels.txt', 'rt') as f:
    names = f.readlines()

def write_input_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

input_file = 'input.txt'

# 0: webcam+

# 1: external cam 
cap = cv2.VideoCapture(1)
while cap.isOpened():
    # 영상을 한 프레임씩 읽어옵니다.
    ret, frame = cap.read()
    if not ret:
        break 

    if ret:
        # 읽어온 프레임을 화면에 출력합니다.
        cv2.imwrite("frame.png", frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText1 = (170, 60)
        bottomLeftCornerOfText2 = (170, 120)
        fontScale = 2.0
        fontColor = (255, 0, 0)
        lineType = 2

        res = my_model.classify_image("frame.png")
        target = names[res['highest_class_id']].replace('\n', '')
        if target == "0 UP":
            pass
        elif target == "3 down":
            pass
        elif target == "2 right":
            cv2.putText(frame, "W",
                bottomLeftCornerOfText1,
                font,
                fontScale,
                fontColor,
                lineType)
            write_input_file(input_file, 'w')
        elif target == "1 left":
            cv2.putText(frame, "S",
                bottomLeftCornerOfText2,
                font,
                fontScale,
                fontColor,
                lineType)
            write_input_file(input_file, 's')

        cv2.imshow('Frame', frame)
        # 'q' 키를 누르면 종료합니다.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print(">>> Camera open failed.")
        break

# 사용한 자원을 해제합니다.
cap.release()
cv2.destroyAllWindows()