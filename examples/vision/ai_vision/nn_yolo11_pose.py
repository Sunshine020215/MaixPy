from maix import camera, display, image, nn, app, sys

if sys.device_name().lower() == "maixcam2":
    detector = nn.YOLO11(model="/root/models/yolo11s_pose.mud", dual_buff = True)
else:
    detector = nn.YOLOv8(model="/root/models/yolov8n_pose.mud", dual_buff = True)

cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th = 0.5, iou_th = 0.45, keypoint_th = 0.5)
    for obj in objs:
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color = image.COLOR_RED)
        msg = f'{detector.labels[obj.class_id]}: {obj.score:.2f}'
        img.draw_string(obj.x, obj.y, msg, color = image.COLOR_RED)
        detector.draw_pose(img, obj.points, 8 if detector.input_width() > 480 else 4, image.COLOR_RED)
    disp.show(img)
