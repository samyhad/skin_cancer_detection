import cv2
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from io import BytesIO
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import FunctionTransformer

# Visualização
def show_images(img_list, titles=None):
    """
    Função auxiliar para exibir uma lista de imagens.

    Args:
        img_list (list): Lista de imagens a serem exibidas.
        titles (list, optional): Lista de títulos para cada imagem. Defaults to None.
    Returns:
        bytes: Bytes da imagem combinada em formato PNG.
    """
    num_images = len(img_list)
    plt.figure(figsize=(15, 5))
    for i, img in enumerate(img_list):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(img, cmap='viridis')
        if titles:
            plt.title(titles[i])
        plt.axis('off')

    # Salvar a figura em um buffer de bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    # Codificar para base64
    base64_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return base64_image

# Etapa 1.1: Redimensionamento
class Resize(BaseEstimator, TransformerMixin):
    """
    Redimensiona as imagens para um tamanho fixo.
    
    Args:
        size (tuple, optional): O tamanho para o qual as imagens serão redimensionadas.
            Defaults to (128, 128).
    """
    def __init__(self, size=(128, 128)):
        self.size = size
        
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([cv2.resize(img, self.size) for img in X])

# Etapa 1.2: Normalização
class Normalize(BaseEstimator, TransformerMixin):
    def __init__(self, scaling='minmax'):
        """
        Normaliza as imagens.

        Args:
            scaling (str, optional): O tipo de escalonamento a ser aplicado.
                'minmax': Escala os valores para o intervalo [0, 1].
                'meanstd': Centraliza os dados com média zero e desvio padrão unitário (por canal).
                Defaults to 'minmax'.
        """
        self.scaling = scaling
        self.mean = None
        self.std = None

    def fit(self, X):
        if self.scaling == 'meanstd':
            # Calcula a média e o desvio padrão por canal para o conjunto de treinamento
            X = np.array(X)
            if X.ndim == 4: 
                self.mean = np.mean(X, axis=(0, 1, 2), keepdims=True)
                self.std = np.std(X, axis=(0, 1, 2), keepdims=True)
            elif X.ndim == 3: 
                self.mean = np.mean(X, axis=(0, 1), keepdims=True)
                self.std = np.std(X, axis=(0, 1), keepdims=True)
            else:
                raise ValueError("Formato de entrada não suportado para 'meanstd' scaling.")
        return self

    def transform(self, X):
        X = np.array(X, dtype=np.float32)
        if self.scaling == 'minmax':
            min_val = np.min(X)
            max_val = np.max(X)
            # Evita divisão por zero se min_val == max_val
            return (X - min_val) / (max_val - min_val + 1e-8)
        elif self.scaling == 'meanstd':
            if self.mean is None or self.std is None:
                raise ValueError("O método 'fit' deve ser chamado antes de 'transform' com scaling='meanstd'.")
            return (X - self.mean) / (self.std + 1e-8)
        else:
            raise ValueError(f"Tipo de escalonamento '{self.scaling}' não suportado.")
    
    def fit_transform(self, X):
        return self.fit(X).transform(X)
    
# Etapa 2: Filtro Gaussiano (remoção de ruído)
class GaussianBlur(BaseEstimator, TransformerMixin):
    """
    Aplica um filtro gaussiano para remoção de ruído.
    
    Args:
        ksize (tuple, optional): Tamanho do kernel gaussiano. Defaults to (5, 5).
        sigma (float, optional): Desvio padrão da distribuição gaussiana. Defaults to 0.
    """
    def __init__(self, ksize=(5, 5), sigma=0):
        self.ksize = ksize
        self.sigma = sigma

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([cv2.GaussianBlur(img, self.ksize, self.sigma) for img in X])

# Etapa 3  (versão 1): CLAHE (Equalização de histograma adaptativa)
class CLAHE(BaseEstimator, TransformerMixin):
    """
    Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization) em imagens.

    Args:
        clip_limit (float, optional): Limite de recorte para CLAHE. Defaults to 2.0.
        tile_grid_size (tuple, optional): Tamanho da grade para CLAHE. Defaults to (8, 8).
    """
    def __init__(self, clip_limit=2.0, tile_grid_size=(8, 8)):
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([self.clahe.apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)) for img in X])

# Etapa 3 (versão 2): CLAHE aplicado em cada canal de cor (BGR)
class CLAHE_Color(BaseEstimator, TransformerMixin):
    """
    Aplica CLAHE em cada canal de cor (BGR) de uma imagem.

    Args:
        clip_limit (float, optional): Limite de recorte para CLAHE. Defaults to 2.0.
        tile_grid_size (tuple, optional): Tamanho da grade para CLAHE. Defaults to (8, 8).
    """
    def __init__(self, clip_limit=2.0, tile_grid_size=(8, 8)):
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        processed_images = []
        for img in X:
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=self.clip_limit, tileGridSize=self.tile_grid_size)
            cl = clahe.apply(l)
            merged_lab = cv2.merge((cl, a, b))
            processed_img = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
            processed_images.append(processed_img)
        return np.array(processed_images)

# Etapa 4: Segmentação simples usando Otsu
class OtsuThreshold(BaseEstimator, TransformerMixin):
    """
    Aplica o método de Otsu para segmentação de imagens.

    Args:
        threshold (int, optional): Valor do limiar. Defaults to 0.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        binarized = []
        for img in X:
            if len(img.shape) == 3:  # Converte se for imagem colorida
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binarized.append(binary)
        return binarized
