import tensorflow as tf
import cv2
import numpy as np

def saliency_map(model, image):
    image = tf.convert_to_tensor(image[None, ...])  
    image = tf.cast(image, tf.float32)
    
    with tf.GradientTape() as tape:
        tape.watch(image)
        predictions = model(image)
        loss = predictions[0][0]  # valor da saída (classe)

    grads = tape.gradient(loss, image)[0]  # gradiente em relação à imagem
    saliency = tf.reduce_max(tf.abs(grads), axis=-1)  # maior influência entre canais (1 canal no caso)
    
    # Normaliza o mapa
    saliency = (saliency - tf.reduce_min(saliency)) / (tf.reduce_max(saliency) - tf.reduce_min(saliency) + 1e-10)

    return saliency.numpy()

def visualize_saliency(img, saliency, alpha=0.5, cmap='jet'):
    saliency_resized = cv2.resize(saliency, (img.shape[1], img.shape[0]))
    saliency_normalized = (saliency_resized - np.min(saliency_resized)) / (np.max(saliency_resized) - np.min(saliency_resized) + 1e-8)
    saliency_colored = cv2.applyColorMap(np.uint8(255 * saliency_normalized), cv2.COLORMAP_JET)
    saliency_colored = saliency_colored.astype(np.float32) / 255.0
    cam = cv2.addWeighted(img.astype(np.float32) / 255.0, 1 - alpha, saliency_colored, alpha, 0)
    return (cam * 255).astype(np.uint8)