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


class MorphologicalOperations(BaseEstimator, TransformerMixin):
    def __init__(self, operation='opening', kernel_size=(5, 5), iterations=1):
        self.operation = operation
        self.kernel = np.ones(kernel_size, np.uint8)
        self.iterations = iterations

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        processed_images = []
        for img in X:
            if len(img.shape) == 2:  # Imagem em escala de cinza
                gray = img
            elif len(img.shape) == 3: # Imagem colorida, converter para escala de cinza
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                raise ValueError("Imagem com formato não suportado.")

            if self.operation == 'erosion':
                processed_img = cv2.erode(gray, self.kernel, iterations=self.iterations)
            elif self.operation == 'dilation':
                processed_img = cv2.dilate(gray, self.kernel, iterations=self.iterations)
            elif self.operation == 'opening':
                processed_img = cv2.morphologyEx(gray, cv2.MORPH_OPEN, self.kernel, iterations=self.iterations)
            elif self.operation == 'closing':
                processed_img = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, self.kernel, iterations=self.iterations)
            else:
                raise ValueError(f"Operação morfológica '{self.operation}' não suportada.")

            if len(img.shape) == 3: # Retornar na forma original (mantendo 3 canais)
                processed_images.append(cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB))
            else:
                processed_images.append(processed_img)

        return np.array(processed_images)

class Watershed(BaseEstimator, TransformerMixin):
    """
    Aplica o algoritmo Watershed para segmentação de imagens.

    Args:
        threshold_method (str, optional): Método de limiarização a ser usado ('otsu' ou 'binary').
            Defaults to 'otsu'.
        structuring_element_size (int, optional): Tamanho do elemento estruturante para operações morfológicas.
            Defaults to 3.
    """
    def __init__(self, threshold_method='otsu', structuring_element_size=3):
        self.threshold_method = threshold_method
        self.structuring_element_size = structuring_element_size

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        processed_images = []
        for img in X:
            # Converter para escala de cinza se a imagem for colorida
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img.copy()

            # 1. Limiarização para obter marcadores binários
            if self.threshold_method == 'otsu':
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            elif self.threshold_method == 'binary':
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
            else:
                raise ValueError(f"Método de limiarização '{self.threshold_method}' não suportado.")

            # 2. Remoção de ruído com operações morfológicas
            kernel = np.ones((self.structuring_element_size, self.structuring_element_size), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

            # 3. Encontrando a área de fundo garantida
            sure_bg = cv2.dilate(opening, kernel, iterations=3)

            # 4. Encontrando a área de primeiro plano garantida
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
            sure_fg = np.uint8(sure_fg)

            # 5. Encontrando regiões desconhecidas
            unknown = cv2.subtract(sure_bg, sure_fg)

            # 6. Criação dos marcadores
            _, markers = cv2.connectedComponents(sure_fg)
            markers = markers + 1  # Adiciona 1 para que o fundo não seja 0
            markers[unknown == 255] = 0 # Marca a região desconhecida com 0

            # 7. Aplicando o Watershed
            if len(img.shape) == 3:
                segmented_img = cv2.watershed(img, markers)
            else:
                # Se a imagem original era em escala de cinza, precisa converter para 3 canais para o watershed
                img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                segmented_img = cv2.watershed(img_color, markers)

            processed_images.append(segmented_img)

        return np.array(processed_images)