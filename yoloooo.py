from yolov4.tf import YOLOv4
import time
from matplotlib import image,pyplot
import numpy as np

# yolo = YOLOv4()
yolo = YOLOv4(tiny=True)

yolo.classes = "coco.names"
yolo.input_size = (640, 480)

yolo.make_model()
# yolo.load_weights("yolov4.weights", weights_type="yolo")
yolo.load_weights("yolov4-tiny.weights", weights_type="yolo")

def AreaOfIntersection(obj,frame,IMG_HEIGHT,IMG_WIDTH,SLOT,fTop,fBottom):
    # x, y, w, h, class id, prob
    fLeft = IMG_WIDTH*frame/SLOT
    fRight = IMG_WIDTH*(frame+1)/SLOT
    
    left = max((IMG_WIDTH*obj[0])-(IMG_WIDTH*obj[2]*0.5),fLeft)
    right = min((IMG_WIDTH*obj[0])+(IMG_WIDTH*obj[2]*0.5),fRight)
    top = max((IMG_HEIGHT*obj[1])-(IMG_HEIGHT*obj[3]*0.5),fTop)
    bottom = min((IMG_HEIGHT*obj[1])+(IMG_HEIGHT*obj[3]*0.5),fBottom)
    
    intersection = 0
    if (left < right and bottom > top):
        intersection = (right - left) * (bottom - top)
        
    return intersection

def app(SLOT,fTop,fBottom,img_todrawn=None):
    SLOTS = [x for x in range(1,SLOT+1)]
    img = image.imread("car5crop1.jpg")
    IMG_WIDTH = img.shape[1]
    IMG_HEIGHT = img.shape[0]

    startTime= time.time()
    objs = yolo.predict(img)
    elapseTime = time.time() - startTime

    car = []
    pos = []
    for obj in objs:
        frame = obj[0]*100//20
        
        AOI= AreaOfIntersection(obj, frame, IMG_HEIGHT, IMG_WIDTH, SLOT, fTop, fBottom)

        IOF = AOI/((fBottom-fTop)*IMG_WIDTH/SLOT) # Area of intersection over area of frame
        IOO = AOI/(obj[2]*obj[3]*IMG_HEIGHT*IMG_WIDTH) # Area of intersection over area of obj

        if  IOF >= 0.7 and IOO >= 0.7 and obj[4] == 2.:
            print("Intersection over frame :",IOF,", ","Intersection over obj :",IOO)
            car.append(obj) 
            pos.append(int(frame+1))
    print('----------------------------------------')
        
    car = np.array(car)

    Available = []
    for slot in SLOTS:
        if slot not in pos:
            Available.append(slot)
            
    try:
        if img_todrawn is not None:
            img = img_todrawn
        result = yolo.draw_bboxes(img,car)
        return result,Available,elapseTime
    except:
        return img,Available,elapseTime

    # yolo.inference(media_path="Cars Driving.mp4", is_image=False)

if __name__ == '__main__':
    img = app(5,710,930)
    pyplot.imshow(img)
    pyplot.show()