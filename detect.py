import cv2
import cv2.aruco as aruco
import numpy as np
import csv
import time

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

cap = cv2.VideoCapture(0)

camera_width = 1280
camera_height = 720
camera_frame_rate = 40

cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
cap.set(cv2.CAP_PROP_FPS, camera_frame_rate)

with open('camera_calibration.npy', 'rb') as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)

marker_size = 150
rover_id = 5
rover_mark = 'Rover'
rover_marker_size = 44

distances_list = {}
csv_filename = 'distances_data.csv'
csv_header = ['Czas_pomiaru', 'Id1', 'Id2', 'Dystans']

def save_distanceslist(id1, id2, distances_list, distance):
    if (id2, id1) in distances_list:
        distances_list[(id2, id1)].append(distance)
    else:
        distances_list[(id1, id2)] = [distance]

def count_distance_between_markers(ids, tvecs, distances_list):
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            id1 = ids[i][0]
            id2 = ids[j][0]

            marker_tvector1 = tvecs[i][0]
            marker_tvector2 = tvecs[j][0]

            distance_vector = marker_tvector1 - marker_tvector2
            distance = np.linalg.norm(distance_vector)

            if id1 == rover_id:
                id1 = rover_mark
            elif id2 == rover_id:
                id2 = rover_mark

            save_distanceslist(id1, id2, distances_list, distance)

def aruco_3d_pose_display(corners, tvecs, rvecs, frame):
    aruco.drawDetectedMarkers(frame, corners)

    for marker in range(len(ids)):
        aruco.drawAxis(frame, camera_matrix, camera_distortion, rvecs[marker], tvecs[marker], 100)
        cv2.putText(
            frame,
            str(ids[marker][0]),
            (int(corners[marker][0][0][0]) - 30,
             int(corners[marker][0][0][1])),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (255, 0, 0),
            2,
            cv2.LINE_AA
        )

def aruco_distances_display(corners, ids, rejected, frame):
    if len(corners) > 0:
        ids = ids.flatten()
        center_points = []

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            center = (cX, cY)
            center_points.append(center)

        for i in range(len(center_points) - 1):
            for j in range(len(center_points)):
                cv2.line(frame, center_points[i], center_points[j], (255, 255, 255), 2)

def adjust_marker_size(ids, tvecs, rvecs, marker_size, rover_id, rover_marker_size):
    for marker in range(len(ids)):
        id = ids[marker][0]
        marker_tvector = tvecs[marker][0]
        marker_rvector = rvecs[marker][0]

        if id == rover_id:
            scale_factor = rover_marker_size / marker_size
            tvecs[marker] = np.multiply(tvecs[marker], scale_factor)
            rvecs[marker] = np.multiply(rvecs[marker], scale_factor)

    return tvecs, rvecs

def save_distances_to_csv(csv_writer, measurment_time, distances_list):
    for (id1, id2), distance_list in distances_list.items():
        avg_distance = np.mean(distance_list)
        csv_writer.writerow([measurment_time, id1, id2, avg_distance])

csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(csv_header)

start_time = time.time()
frame_count = 0
csv_interval = 10


while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

    if ids is not None:
        rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
        tvecs, rvecs = adjust_marker_size(ids, tvecs, rvecs, marker_size, rover_id, rover_marker_size)

        count_distance_between_markers(ids, tvecs, distances_list)

        aruco_3d_pose_display(corners, tvecs, rvecs, frame)
        aruco_distances_display(corners, ids, rejected, frame)

        measurment_time = time.time() - start_time
        frame_count += 1
        
        if frame_count == csv_interval:
            save_distances_to_csv(csv_writer, measurment_time, distances_list)
            distances_list = {}
            frame_count = 0

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

csv_file.close()
cv2.destroyAllWindows()
cap.release()



