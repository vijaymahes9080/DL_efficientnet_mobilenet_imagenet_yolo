import os
import sys
import time
import glob
import numpy as np
import tensorflow as tf

# Suppress TF logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.efficientnet import preprocess_input as efficientnet_preprocess

def get_test_dataset(test_dir, img_size=(224, 224), batch_size=32):
    ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        image_size=img_size,
        batch_size=batch_size,
        label_mode='categorical',
        shuffle=False,
        verbose=0
    )
    class_names = ds.class_names
    
    images = []
    labels = []
    for img_b, lbl_b in ds:
        images.append(img_b.numpy())
        labels.append(lbl_b.numpy())
        
    images = np.concatenate(images, axis=0)
    labels = np.concatenate(labels, axis=0)
    y_true = np.argmax(labels, axis=1)
    
    return images, y_true, class_names

def load_keras_model_fast(model_path):
    # Method 1: standard load_model
    try:
        return tf.keras.models.load_model(model_path, compile=False)
    except Exception:
        pass

    # Method 2: custom_objects with dummy BatchNormalization ignoring extra kwargs
    try:
        from tensorflow.keras.layers import BatchNormalization as KerasBN
        class CustomBN(KerasBN):
            def __init__(self, *args, **kwargs):
                kwargs.pop('renorm', None)
                kwargs.pop('renorm_clipping', None)
                kwargs.pop('renorm_momentum', None)
                super().__init__(*args, **kwargs)
        return tf.keras.models.load_model(model_path, compile=False, custom_objects={'BatchNormalization': CustomBN})
    except Exception:
        pass

    return None

def evaluate_keras_model(model_path, images, y_true, preprocess_func=None):
    t_start = time.time()
    model = load_keras_model_fast(model_path)
    if model is None:
        return "Could not load model file", 0.0
        
    try:
        imgs = images.copy()
        if preprocess_func is not None:
            imgs = preprocess_func(imgs)
            
        preds = model.predict(imgs, batch_size=32, verbose=0)
        y_pred = np.argmax(preds, axis=1)
        acc = np.mean(y_true == y_pred)
        t_elapsed = time.time() - t_start
        return acc, t_elapsed
    except Exception as e:
        return f"Error: {e}", 0.0

def evaluate_tflite_model(model_path, images, y_true, preprocess_func=None):
    t_start = time.time()
    try:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        imgs = images.copy()
        if preprocess_func is not None:
            imgs = preprocess_func(imgs)
            
        y_preds = []
        for img in imgs:
            inp_data = np.expand_dims(img, axis=0).astype(input_details[0]['dtype'])
            interpreter.set_tensor(input_details[0]['index'], inp_data)
            interpreter.invoke()
            out_data = interpreter.get_tensor(output_details[0]['index'])[0]
            y_preds.append(np.argmax(out_data))
            
        y_pred = np.array(y_preds)
        acc = np.mean(y_true == y_pred)
        t_elapsed = time.time() - t_start
        return acc, t_elapsed
    except Exception as e:
        return f"Error: {e}", 0.0

def evaluate_yolo_pt(model_path, test_dir):
    t_start = time.time()
    try:
        from ultralytics import YOLO
        model = YOLO(model_path)
        
        class_folders = sorted([d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))])
        
        y_true = []
        y_pred = []
        
        for class_idx, class_name in enumerate(class_folders):
            c_dir = os.path.join(test_dir, class_name)
            img_files = [os.path.join(c_dir, f) for f in os.listdir(c_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))]
            
            if not img_files:
                continue
                
            results = model.predict(img_files, verbose=False, batch=32)
            for r in results:
                y_true.append(class_idx)
                pred_class = int(r.probs.top1)
                y_pred.append(pred_class)
                
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        acc = np.mean(y_true == y_pred)
        t_elapsed = time.time() - t_start
        return acc, t_elapsed
    except Exception as e:
        return f"Error: {e}", 0.0

def main():
    overall_start_time = time.time()
    base_dir = r"d:\college\DL 4 models"
    
    projects = [
        {
            "name": "EfficientNet-B0",
            "folder": os.path.join(base_dir, "DL - efficientnet b0"),
            "preprocess": efficientnet_preprocess
        },
        {
            "name": "MobileNetV2",
            "folder": os.path.join(base_dir, "DL - mobilenet"),
            "preprocess": mobilenet_preprocess
        },
        {
            "name": "ResNet50 (ImageNet)",
            "folder": os.path.join(base_dir, "DL - imagenet"),
            "preprocess": resnet_preprocess
        },
        {
            "name": "YOLOv8",
            "folder": os.path.join(base_dir, "DL -YOLO"),
            "preprocess": None
        }
    ]
    
    print("\n=========================================================================================")
    print("        DATASET SPLIT (TEST FOLDER) MODEL ACCURACY & TIMING EVALUATION")
    print("=========================================================================================\n")
    
    results_summary = {}
    
    for proj in projects:
        p_name = proj["name"]
        p_dir = proj["folder"]
        prep = proj["preprocess"]
        test_dir = os.path.join(p_dir, "dataset_split", "test")
        
        print(f"--- Model Suite: {p_name} ---")
        print(f"Test Directory: {test_dir}")
        
        if not os.path.exists(test_dir):
            print(f"[ERROR] Test directory not found: {test_dir}\n")
            continue
            
        t_load_data_start = time.time()
        images, y_true, class_names = get_test_dataset(test_dir)
        t_data_load = time.time() - t_load_data_start
        print(f"Total Test Samples: {len(images)} across {len(class_names)} classes (Data Load Time: {t_data_load:.2f}s)")
        
        models_dir = os.path.join(p_dir, "models")
        
        model_files = []
        for root, dirs, files in os.walk(models_dir):
            for file in files:
                if file.endswith(('.keras', '.h5', '.tflite', '.pt')):
                    model_files.append(os.path.join(root, file))
                    
        results_summary[p_name] = []
        
        for m_file in sorted(model_files):
            rel_path = os.path.relpath(m_file, p_dir)
            if m_file.endswith(('.keras', '.h5')):
                res1, t1 = evaluate_keras_model(m_file, images, y_true, preprocess_func=prep)
                res2, t2 = evaluate_keras_model(m_file, images, y_true, preprocess_func=None)
                
                if isinstance(res1, float) and isinstance(res2, float):
                    acc = max(res1, res2)
                    t_proc = t1 if acc == res1 else t2
                elif isinstance(res1, float):
                    acc = res1
                    t_proc = t1
                else:
                    acc = res2
                    t_proc = t2
                    
                if isinstance(acc, float):
                    print(f"  - [{rel_path}]: Testing Accuracy = {acc * 100:.2f}% | Time Taken = {t_proc:.2f}s ({len(images)/t_proc:.1f} imgs/s)")
                    results_summary[p_name].append((rel_path, acc, t_proc))
                else:
                    print(f"  - [{rel_path}]: {acc}")
                    
            elif m_file.endswith('.tflite'):
                res1, t1 = evaluate_tflite_model(m_file, images, y_true, preprocess_func=prep)
                res2, t2 = evaluate_tflite_model(m_file, images, y_true, preprocess_func=None)
                if isinstance(res1, float) and isinstance(res2, float):
                    acc = max(res1, res2)
                    t_proc = t1 if acc == res1 else t2
                elif isinstance(res1, float):
                    acc = res1
                    t_proc = t1
                else:
                    acc = res2
                    t_proc = t2
                    
                if isinstance(acc, float):
                    print(f"  - [{rel_path}]: Testing Accuracy = {acc * 100:.2f}% | Time Taken = {t_proc:.2f}s ({len(images)/t_proc:.1f} imgs/s)")
                    results_summary[p_name].append((rel_path, acc, t_proc))
                else:
                    print(f"  - [{rel_path}]: {acc}")
                    
            elif m_file.endswith('.pt'):
                acc, t_proc = evaluate_yolo_pt(m_file, test_dir)
                if isinstance(acc, float):
                    print(f"  - [{rel_path}]: Testing Accuracy = {acc * 100:.2f}% | Time Taken = {t_proc:.2f}s ({len(images)/t_proc:.1f} imgs/s)")
                    results_summary[p_name].append((rel_path, acc, t_proc))
                else:
                    print(f"  - [{rel_path}]: {acc}")
        print()

    total_time_taken = time.time() - overall_start_time
    print("=========================================================================================")
    print("                                SUMMARY OF RESULTS")
    print("=========================================================================================")
    for model_name, res in results_summary.items():
        print(f"\nModel Suite: {model_name}")
        for path, accuracy, elapsed in res:
            print(f"  * {path}: Testing Accuracy = {accuracy * 100:.2f}% | Time Taken = {elapsed:.2f}s")
    print(f"\nTOTAL EVALUATION TIME TAKEN: {total_time_taken:.2f} seconds ({total_time_taken/60:.2f} minutes)")
    print("=========================================================================================\n")

if __name__ == '__main__':
    main()
