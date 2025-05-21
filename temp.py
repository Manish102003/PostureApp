import cv2
import mediapipe as mp
import math
import os

# 1. Define corrective exercises for each posture problem
EXERCISE_RECOMMENDATIONS = {
    "Forward Head": [
        "Chin Tucks: Sit or stand tall, gently tuck your chin in as if making a double chin. Hold for 5 seconds. Repeat 10 times.",
        "Neck Stretch: Tilt your head towards each shoulder and hold for 20 seconds per side."
    ],
    "Kyphosis": [
        "Thoracic Extensions: Sit on a chair, clasp hands behind your head, gently arch your upper back over the chair. Hold for 5 seconds. Repeat 10 times.",
        "Rows: Use resistance bands or weights to strengthen your upper back."
    ],
    "Flat Back": [
        "Pelvic Tilts: Lie on your back with knees bent, flatten your lower back against the floor by tightening your abs. Hold for 5 seconds. Repeat 10 times.",
        "Hip Flexor Stretch: Kneel on one knee, push hips forward to stretch the front of your hip. Hold for 20 seconds per side."
    ],
    "Swayback (Lordosis)": [
        "Planks: Strengthen your core and glutes by holding a straight-body plank for 30+ seconds.",
        "Pelvic Tilts: Lie on your back, knees bent, tilt your pelvis upward, and flatten your lower back against the floor.",
        "Glute Bridges: Lie on your back, lift your hips by squeezing your glutes, hold, then lower."
    ],
    "Possible Scoliosis": [
        "Side Plank: Lie on your side, prop up on your elbow, and lift your hips. Hold for 10–30 seconds per side.",
        "Consult a physical therapist for a personalized exercise plan."
    ]
}

def calculate_angle(point1, point2, point3):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y

    vector1 = [x2 - x1, y2 - y1]
    vector2 = [x3 - x2, y3 - y2]

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    if magnitude1 * magnitude2 == 0:
        return 0

    angle_rad = math.acos(max(-1, min(1, dot_product / (magnitude1 * magnitude2))))
    angle_deg = math.degrees(angle_rad)
    return round(angle_deg)

def check_posture(pose_landmarks, mpPose):
    posture_problems = []

    # Calculate relevant angles
    left_neck_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW]
    )
    right_neck_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW]
    )
    left_shoulder_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP]
    )
    right_shoulder_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP]
    )
    left_hip_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE]
    )
    right_hip_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE]
    )
    # Swayback (Lordosis) detection: exaggerated lumbar curve
    left_lordosis_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP],
        pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE]
    )
    right_lordosis_angle = calculate_angle(
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP],
        pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE]
    )

    # Scoliosis detection: asymmetry in shoulders or hips
    left_shoulder_y = pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y
    right_shoulder_y = pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y
    left_hip_y = pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y
    right_hip_y = pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y

    # Thresholds for posture issues
    CORRECT_POSTURE_THRESHOLD = {
        'shoulder': 160,
        'hip': 30,
        'neck': 150,
        'lordosis': 200,
        'scoliosis_y_diff': 0.05  # 5% of image height
    }

    # Forward Head
    if left_neck_angle > CORRECT_POSTURE_THRESHOLD['neck'] or right_neck_angle > CORRECT_POSTURE_THRESHOLD['neck']:
        posture_problems.append("Forward Head")

    # Kyphosis (rounded shoulders)
    if left_shoulder_angle < CORRECT_POSTURE_THRESHOLD['shoulder'] or right_shoulder_angle < CORRECT_POSTURE_THRESHOLD['shoulder']:
        posture_problems.append("Kyphosis")

    # Flat Back (hip angle too open)
    if left_hip_angle > CORRECT_POSTURE_THRESHOLD['hip'] or right_hip_angle > CORRECT_POSTURE_THRESHOLD['hip']:
        posture_problems.append("Flat Back")

    # Swayback (Lordosis)
    if left_lordosis_angle > CORRECT_POSTURE_THRESHOLD['lordosis'] or right_lordosis_angle > CORRECT_POSTURE_THRESHOLD['lordosis']:
        posture_problems.append("Swayback (Lordosis)")

    # Possible Scoliosis
    if abs(left_shoulder_y - right_shoulder_y) > CORRECT_POSTURE_THRESHOLD['scoliosis_y_diff'] or \
       abs(left_hip_y - right_hip_y) > CORRECT_POSTURE_THRESHOLD['scoliosis_y_diff']:
        posture_problems.append("Possible Scoliosis")

    if not posture_problems:
        return {
            "status": "Healthy",
            "problems": [],
            "exercises": []
        }
    else:
        exercises = []
        for problem in posture_problems:
            exercises.extend(EXERCISE_RECOMMENDATIONS.get(problem, []))
        return {
            "status": "Posture Issue Detected",
            "problems": posture_problems,
            "exercises": exercises
        }

def posture(image_path):
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(static_image_mode=True)

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Error loading the image.")

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    if not result.pose_landmarks:
        output = {
            "status": "No person detected",
            "problems": [],
            "exercises": []
        }
    else:
        output = check_posture(result.pose_landmarks, mpPose)

    # Delete the image file after processing
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Image '{image_path}' deleted after processing.")  # Optional: remove or keep this print[1][2][3]
    else:
        print(f"Image '{image_path}' not found for deletion.")    # Optional: remove or keep this print[1][2][3]

    return output

# Example usage:
result = posture("media/photos/image24.png")  # Change path to your image
print(result)
