import cv2
import mediapipe as mp
import math

# Load Mediapipe Pose model
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

save_as = 'image4.jpg'

# Define the threshold angle for correct posture
CORRECT_POSTURE_THRESHOLD = {
    'shoulder': 160,
    'hip': 30,
    'knee': 40,
    'neck': 150,
    'upper_neck': 40 
}

# Define a function to calculate the angle between two lines
def calculate_angle(point1, point2, point3):
    x1, y1, z1 = point1.x, point1.y, point1.z
    x2, y2, z2 = point2.x, point2.y, point2.z
    x3, y3, z3 = point3.x, point3.y, point3.z

    vector1 = [x2 - x1, y2 - y1]
    vector2 = [x3 - x2, y3 - y2]

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    angle_rad = math.acos(dot_product / (magnitude1 * magnitude2))
    angle_deg = math.degrees(angle_rad)
    angle_deg = round(angle_deg)
    return angle_deg


# Define a function to check the posture
def check_posture(pose_landmarks):
    left_neck_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR],
                                      pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
                                      pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW])

    right_neck_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR],
                                       pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
                                       pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW])

    left_shoulder_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW],
                                          pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
                                          pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP])

    right_shoulder_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW],
                                           pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
                                           pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP])

    left_hip_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
                                     pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP],
                                     pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE])

    right_hip_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
                                      pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP],
                                      pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE])

    left_knee_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP],
                                      pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE],
                                      pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE])

    right_knee_angle = calculate_angle(pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP],
                                       pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE],
                                       pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE])

    # Define threshold values for posture angles
    CORRECT_POSTURE_THRESHOLD = {
        'shoulder': 160,
        'hip': 30,
        'knee': 40,
        'neck': 150
    }

    # Check each posture angle against the threshold
    posture_problems = []

    if left_neck_angle > CORRECT_POSTURE_THRESHOLD['neck'] or right_neck_angle > CORRECT_POSTURE_THRESHOLD['neck']:
        posture_problems.append("Forward Head")

    if left_shoulder_angle < CORRECT_POSTURE_THRESHOLD['shoulder'] or right_shoulder_angle < CORRECT_POSTURE_THRESHOLD['shoulder']:
        posture_problems.append("Kyphosis")

    if left_hip_angle > CORRECT_POSTURE_THRESHOLD['hip'] or right_hip_angle > CORRECT_POSTURE_THRESHOLD['hip']:
        posture_problems.append("Flat Back")

    if not posture_problems:
        print("Healthy") 
    else:
        print(posture_problems)

# it reads the image file and convert it to RGB from BGR and process the landmarks and draw the landmarks on the image
img = cv2.imread(save_as, 1)

if img is None:
    print("Error loading the image.")
    exit(1)

imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = pose.process(imgRGB)

# Call the check_posture function with the pose landmarks
check_posture(result.pose_landmarks)

# print(result.pose_landmarks).

# if result.pose_landmarks:
#     mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
    # for id, lm in enumerate(result.pose_landmarks.landmark):
    #     h, w, c = img.shape
    #     # print(id, lm)
    #     cx, cy = int(lm.x * w), int(lm.y * h)
    #     cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

# This is the code for the image resize and display
# original_shape = img.shape[:2]

# desired_width = 500  # Desired window width
# desired_height = int(desired_width * original_shape[0] / original_shape[1])

# cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Image', desired_width, desired_height)
# cv2.imshow('Image', img)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()