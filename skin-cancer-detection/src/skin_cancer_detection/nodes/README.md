## ✅ Pré-processamentos Recomendados para Imagens de Câncer de Pele

### Remoção de Ruído (Tratamento de Ruídos)

Filtros como **mediana** ou **Gaussian blur** podem ajudar a suavizar a pele sem perder a lesão.

### Filtragem Espacial e Convolução

Pode-se usar **kernels** para realçar bordas da lesão (ex: Sobel, Laplaciano) e facilitar segmentações posteriores.

### Realce e Restauração

Técnicas de contraste adaptativo (ex: CLAHE) ajudam a destacar regiões escuras ou claras da lesão.

### Histograma e Equalização

A **equalização de histograma** pode melhorar o contraste da imagem e facilitar a detecção da lesão.

### Segmentação de Imagens

Detecção da lesão na imagem com segmentação baseada em:

*   **Thresholding adaptativo**
*   **Transformada de distância**
*   **Watershed**
*   **k-means**
*   **Deep Learning** (U-Net, por exemplo)

### Amostragem e Quantização

Pode-se reduzir a resolução e a profundidade de cor para simplificar o modelo, se necessário.
