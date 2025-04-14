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
```

Claro! Aqui está a tradução completa da sua documentação inicial para o português:

---

## Instruções de Configuração

1. Clone o repositório:
   ```bash
   git clone <repository-url>
   cd skin-cancer-detection
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install -r src/requirements.txt
   ```

3. Configure seu ambiente local atualizando o arquivo `conf/local/credentials.yml` com as credenciais necessárias.

## Diretrizes de Uso

- Utilize o notebook `notebooks/exploratory.ipynb` para realizar uma análise exploratória e entender melhor o conjunto de dados.
- O pré-processamento dos dados e o treinamento do modelo são orquestrados pelo pipeline do Kedro definido em `src/skin_cancer_detection/pipelines/pipeline.py`.
- Ajuste os parâmetros no arquivo `conf/base/parameters.yml` para refinar o processo de treinamento do modelo.

## Licença
Projeto adota a licença MIT
