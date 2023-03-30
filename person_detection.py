import cv2
import numpy as np
import gc
# Load the YOLOv3 model
def detect_person(img):
	net = cv2.dnn.readNet("weights/yolov3.weights", "weights/yolov3.cfg")

	# Load the input image
	img = cv2.resize(img,(416,416))
	# Get the dimensions of the input image
	(H, W) = img.shape[:2]
	# Get the output layer names of the YOLOv3 model
	ln = net.getLayerNames()
	layer_indices = net.getUnconnectedOutLayers()

	ln = [ln[i-1] for i in layer_indices]

	# Create a blob from the input image
	blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
	# Perform forward propagation through the YOLOv3 network
	net.setInput(blob)
	layerOutputs = net.forward(ln)

	# Initialize the lists to store the bounding box coordinates, confidences and class IDs
	boxes = []
	confidences = []
	classIDs = []

	# Loop through the layer outputs
	for output in layerOutputs:
		# Loop through each of the detections
		for detection in output:
			# Get the class ID and confidence of the current detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# Filter out detections with low confidence
			if confidence > 0.5:
				# Get the bounding box coordinates of the current detection
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# Update the lists with the results
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# Perform non-maximum suppression to suppress weak, overlapping detections
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

	# Define the colors for the bounding boxes and labels
	COLORS = np.random.randint(0, 255, size=(len(classIDs), 3), dtype="uint8")

	flag = False
	# Loop through the indexes of the detections that passed non-maximum suppression
	for i in idxs.flatten():
		classID = classIDs[i]
		# Get the bounding box coordinates and class ID
		if classID == 0:
			flag = True
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# Draw the bounding box and label on the image

	if flag:
		cropped = img[y:y+h, np.abs(x):x+w]
		cropped = cv2.resize(cropped,(224,224))
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		# Read an image and convert it to grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		# Apply the classifier to detect faces in the grayscale image
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		# Draw rectangles around the detected faces on the original image
		for i, (x, y, w, h) in enumerate(faces):
			# Crop the face
			face = img[y:y + h, x:x + w]
		face = cv2.resize(face,(224,224))
		gc.collect()
		del face_cascade
		return cropped,face,flag
	else:
		cropped = 0
		return cropped, flag