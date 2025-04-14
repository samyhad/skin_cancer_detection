# Título: Medivisão - Auxílio ao Diagnóstico de Câncer de Pele

## Descrição

Este repositório contém o código e a documentação de um projeto a etapa de treinamento do modelo que irá realizar a detecção precoce de câncer de pele. O projeto explora o uso de técnicas de Processamento Digital de Imagens (PDI) para o tratamento e análise de imagens de lesões cutâneas, com o objetivo de auxiliar na identificação de padrões sugestivos de malignidade.

O avanço da inteligência artificial tem o potencial de transformar a área da saúde, especialmente em um cenário com limitações de acesso a especialistas médicos. A detecção precoce de doenças como o câncer de pele é crucial para aumentar as chances de tratamento bem-sucedido.

Este projeto se concentra no **pré-processamento das imagens de pele** utilizando os fundamentos do Processamento Digital de Imagens (PDI) aprendidos na disciplina. O objetivo é preparar as imagens para análises subsequentes, que podem incluir técnicas de aprendizado de máquina, como **redes neurais**. Redes neurais profundas têm demonstrado grande potencial na análise de imagens médicas, sendo capazes de aprender padrões complexos e realizar classificações precisas. No contexto deste projeto, após o pré-processamento das imagens utilizando as técnicas de PDI, modelos de redes neurais poderiam ser treinados para identificar características visuais indicativas de câncer de pele.

As etapas de pré-processamento com PDI visam otimizar a qualidade das imagens e realçar informações relevantes para a detecção, incluindo:

* **Tratamento de ruídos:** Redução de artefatos para melhorar a clareza das imagens.
* **Filtragem e Convolução:** Aplicação de filtros para destacar bordas e texturas importantes das lesões.
* **Realce e Restauração:** Melhoria do contraste e da nitidez para facilitar a visualização de detalhes.
* **Ajuste de Histograma:** Otimização da distribuição de cores para melhor análise visual.
* **Segmentação:** Isolamento da área da lesão para análise focada.

Embora a implementação de modelos de redes neurais para a classificação final das lesões possa ser um objetivo futuro, o foco inicial deste repositório é demonstrar como as técnicas de PDI podem ser aplicadas para o **pré-processamento eficaz das imagens de câncer de pele**, preparando-as para uma análise mais aprofundada com inteligência artificial. Este projeto busca contribuir para o desenvolvimento de ferramentas que auxiliem no diagnóstico precoce, potencialmente melhorando o acesso e a precisão na detecção do câncer de pele.

### Identificação
Equipe: 1 //

### Membros:

Lorena Silva Sampaio - 11201212025 //
Samira Haddad - 11201812350 //
Larissa Rodrigues de Almeida - 11201812076 //
William Fernandes Dias - 11202020043

Data de Publicação:: 13 de Abril de 2025

## Project Structure

O projeto é organizado da seguinte maneira:

```
skin-cancer-detection
├── app                          # Estrutura de aplicação primária (MVP) do uso do modelo
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

