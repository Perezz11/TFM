from ultralytics import YOLO


while True:
    Q = input("train or predict? (train, predi): ")
    if Q.lower() == "train":
        print("Let's train")
        # CLASIFICACION
        # Load model and load weights
        # model_s1 = YOLO("yolov8s-cls.pt")
        # model_n2 = YOLO("yolov8n-cls.yaml").load("yolov8n-cls.pt")
        # Pongo uno que se quedo a medias
        # model_s = YOLO(
        #   "/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/runs/classify/train5/weights/last.pt") YA ESTA ENTRENADO
        # model_m = YOLO("yolov8m-cls.pt")

        # DETECTION
        model_n = YOLO("yolov8n.pt")

        patience = 30
        epochs = 300
        # Train the model
        results_n = model_n.train(
            data="/home/perez/Desktop/Roboflow/data.yaml", epochs=epochs, imgsz=640, task='detect', patience=patience, plots=True)
        # results_n2 = model_n2.train(
        #   data="/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/dataset/", epochs=epochs, imgsz=640, task='classify', patience=patience, plots=True)
        # results_s = model_s.train(
        #   data="/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/dataset/", epochs=epochs, imgsz=640, task='classify', patience=15, plots=True, resume=True)
        break

    elif Q.lower() == "predi":
        # Test the model
        # load the trained model
        # model_n = YOLO(
        # "/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/runs/classify/train4/weights/best.pt") # First training
        # results_n = model_n.predict(
        #   "/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/examples/*png", save_txt=True, show_boxes=False, save=True)

        # CLASIFFY MODEL
        model_n = YOLO(
            "C:/Users/yeben/Desktop/Code/Trains/train8/weights/best.pt")
        results_n = model_n.predict(
            "C:/Users/yeben/Desktop/13May2024_clusters/*png", save_txt=True, show_boxes=True, save=True)

        # Test the model
        # metrics = model_n.test()  # no arguments needed, dataset and settings remembered
        # model_s = YOLO(
        #   "/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/runs/classify/train5/weights/best.pt")

        # TEST DETECTION MODEL
        # model_n = YOLO(
        #    "/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/runs/detect/train3/weights/best.pt")

        # results_n = model_n.predict(
        # "/home/perez/Desktop/Master_particulas/Segundo_cuatrimestre/TFM/Neural_Network/examples2/*png", save_txt=True, show_boxes=True, save=True, save_conf=True)
        
        print("Prediction finished")
        break
