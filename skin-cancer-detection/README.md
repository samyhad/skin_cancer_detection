# Skin Cancer Detection Project

Este projeto tem como objetivo desenvolver um modelo para detecção de câncer de pele com base em imagens. O fluxo de trabalho inclui pré-processamento dos dados e treinamento do modelo utilizando redes neurais.

## Project Structure

O projeto é organizado da seguinte maneira:

```
skin-cancer-detection
├── data
│   ├── 03_primary               # Primary datasets for analysis
├── notebooks
│   └── preprocess_pipeline_slin_lesion.ipynb        # Notebook onde exploramos as técnicas de PDI e treinamos o modelo
│   └── skin_cancer.ipynb                            # Notebook onde executamos o SPI sem uso de uma aplicação WEB
│   ├── requirements.txt             # Dependencias do projeto
└── README.md                        # Documentação do projeto

## Instruções de Configuração

1. Clone o repositório:
   ```bash
   git clone <repository-url>
   cd skin-cancer-detection
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
## Como rodar o SPI pelo colab
1. Faça uma cópia do skin_cancer.ipynb e depois aba no colab
2. Dentro da pasta content do colab crie uma nova pasta chama modules
3. Coloque os arquivos presentes na pasta app/modules dentro dessa nova pasta do colab
4. Além disso, insira na pasta de content o modelo que iremos executar, no caso, o modelo presente na pasta app/static/model/skin_cancer.keras
5. Execute o notebook seguindo a sequência pré estabelecida. 

## Licença
Projeto adota a licença MIT
