import cv2
import numpy as np

prototxt_path = "models/colorization_deploy_v2.prototxt"
model_path = "models/colorization_release_v2.caffemodel"
points_path = "models/pts_in_hull.npy"

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
pts = np.load(points_path)

points = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype("float32")]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [
    np.full([1, 313], 2.606, dtype="float32")
]


def colorize_image(file, extension):
    image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))

    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))

    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    L = cv2.split(lab)[0]

    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = (255 * colorized).astype("uint8")

    cv2.imwrite("colorized_image." + extension, colorized)

    return colorized
