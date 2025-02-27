# import csv
# import os
# from datetime import datetime

# import cv2
# import face_recognition
# import numpy as np
# import pandas as pd

# # Load pretrained face detection model
# net = cv2.dnn.readNetFromCaffe(
#     "./saved_model/deploy.prototxt.txt",
#     "./saved_model/res10_300x300_ssd_iter_140000.caffemodel",
# )


# def save_attendance(attendance_str: str, location: str):
#     # Split the input string into parts
#     parts = attendance_str.split("-")
#     name = parts[0]
#     matric_number = parts[1]
#     department = parts[2]
#     # Get the current date and time
#     now = datetime.now()
#     current_date = now.strftime("%Y-%m-%d")
#     current_time = now.strftime("%H:%M:%S")
#     date_string = now.strftime("%Y-%m-%d")
#     filename = f"{date_string}-attendance.csv".capitalize()
#     # check if the file already exists
#     if os.path.exists(f"{location}/{filename}"):

#         # print("True")
#         with open(f"{location}/{filename}", "r") as attendance_file:
#             attendance_reader = csv.reader(attendance_file)
#             # Check if the name and date is already in the file
#             for row in attendance_reader:
#                 if name == row[0] and current_date == row[3]:
#                     # print(f'Attendance for {name} on {current_date} already recorded')
#                     return False
#     else:
#         # print("False")
#         # Write the headers
#         with open(f"{location}/{filename}", "w", newline="") as attendance_file:
#             attendance_writer = csv.writer(
#                 attendance_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
#             )
#             attendance_writer.writerow(
#                 ["Name", "Matric Number", "Department", "Date", "Time"]
#             )
#     # Write the attendance data
#     with open(f"{location}/{filename}", "a", newline="") as attendance_file:
#         attendance_writer = csv.writer(
#             attendance_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
#         )
#         attendance_writer.writerow(
#             [name, matric_number, department, current_date, current_time]
#         )


# def gen(file_path):
#     global capture, out, face
#     IMAGE_FILES = []
#     filename = []
#     dir_path = "./registered_faces"

#     cap = cv2.VideoCapture(0)

#     for imagess in os.listdir(dir_path):
#         img_path = os.path.join(dir_path, imagess)
#         img_path = face_recognition.load_image_file(
#             img_path
#         )  # reading image and append to list
#         IMAGE_FILES.append(img_path)
#         filename.append(imagess.split(".", 1)[0])

#     def encoding_img(IMAGE_FILES):
#         encodeList = []
#         for img in IMAGE_FILES:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             try:
#                 encode = face_recognition.face_encodings(img)[0]
#                 encodeList.append(encode)
#             except Exception as e:
#                 e = "error"
#         return encodeList

#     encodeListknown = encoding_img(IMAGE_FILES)

#     while True:
#         success, img = cap.read()

#         imgc = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#         # converting image to RGB from BGR
#         imgc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         fasescurrent = face_recognition.face_locations(imgc)
#         encode_fasescurrent = face_recognition.face_encodings(imgc, fasescurrent)

#         # faceloc- one by one it grab one face location from fasescurrent
#         # than encodeFace grab encoding from encode_fasescurrent
#         # we want them all in same loop so we are using zip
#         for encodeFace, faceloc in zip(encode_fasescurrent, fasescurrent):
#             matches_face = face_recognition.compare_faces(encodeListknown, encodeFace)
#             face_distence = face_recognition.face_distance(encodeListknown, encodeFace)
#             # print(face_distence)
#             # finding minimum distence index that will return best match
#             matchindex = np.argmin(face_distence)

#             if matches_face[matchindex]:
#                 name = filename[matchindex].upper()
#                 y1, x2, y2, x1 = faceloc
#                 # Multiply locations by 4 because we reduced the webcam input image by 0.25
#                 text = (
#                     f"{name}"
#                     if save_attendance(name, file_path) != False
#                     else "Attendance already recorded"
#                 )
#                 text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
#                 text_x = int((img.shape[1] - text_size[0]) / 2)
#                 text_y = int((img.shape[0] + text_size[1]) / 2)
#                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                 cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
#                 cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), 2, cv2.FILLED)

#                 if save_attendance(name, file_path) != False:
#                     cv2.putText(
#                         img,
#                         text,
#                         (text_x, text_y),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         1,
#                         (255, 255, 255),
#                         2,
#                     )
#                 else:
#                     cv2.putText(
#                         img,
#                         text,
#                         (text_x, text_y),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         1,
#                         (255, 255, 255),
#                         2,
#                     )

#         frame = cv2.imencode(".jpg", img)[1].tobytes()
#         yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
#         key = cv2.waitKey(20)
#         if key == 27:
#             break


# def gen_frames():  # generate frame by frame from camera
#     global out, capture, rec_frame, frame
#     camera = cv2.VideoCapture(0)  # initialize camera outside of loop
#     while True:
#         success, frame = camera.read()
#         if success:
#             if capture:
#                 capture = 0
#             try:
#                 # Optimization: remove unnecessary flip function
#                 ret, buffer = cv2.imencode(".jpg", frame)
#                 frame = buffer.tobytes()
#                 yield (
#                     b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
#                 )
#             except Exception as e:
#                 pass
#         else:
#             pass


# def count_name_in_files(directory_path, name):
#     count = 0
#     num_files = 0

#     for dirpath, dirnames, filenames in os.walk(directory_path):
#         for filename in filenames:
#             if filename.endswith(".csv"):
#                 file_path = os.path.join(dirpath, filename)
#                 with open(file_path, newline="") as csvfile:
#                     reader = csv.reader(csvfile)
#                     for row in reader:
#                         if row and row[0] == name:
#                             count += 1
#                 num_files += 1

#     if num_files == 0:
#         return 0

#     message = (
#         f"{name}'s Attendance for this course is "
#         + f"{str(count / num_files * 100)}% \nYou are eligible to write your exam!"
#     )

#     return message


# def get_total_attendance(directory_path):
#     student_attendance = {}

#     for filename in os.listdir(directory_path):
#         if filename.endswith(".csv"):
#             file_path = os.path.join(directory_path, filename)
#             with open(file_path, newline="") as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 for row in reader:
#                     name = row["Name"]
#                     matric_number = row["Matric Number"]
#                     department = row["Department"]

#                     if name not in student_attendance:
#                         student_attendance[name] = {
#                             "Matric Number": matric_number,
#                             "Department": department,
#                             "Attendance": 0,
#                         }

#                     student_attendance[name]["Attendance"] += 1

#     data = []
#     for name, attendance_data in student_attendance.items():
#         total_classes = len(os.listdir(directory_path))
#         attendance_percentage = attendance_data["Attendance"] / total_classes * 100
#         data.append(
#             {
#                 "Name": name,
#                 "Matric Number": attendance_data["Matric Number"],
#                 "Department": attendance_data["Department"],
#                 "Attendance Percentage": attendance_percentage,
#             }
#         )

#     df = pd.DataFrame(
#         data, columns=["Name", "Matric Number", "Department", "Attendance Percentage"]
#     )
#     # df.set_index("Name", inplace=True)
#     df.to_csv("total_attendance.csv")
#     return df
