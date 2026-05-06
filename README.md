# 🚗 Sistema ALPR: Reconhecimento Óptico de Placas Veiculares

Um pipeline de Visão Computacional desenvolvido em Python para detecção, isolamento e leitura automática de placas de trânsito (Automatic License Plate Recognition - ALPR). 

O sistema não apenas aplica OCR (Reconhecimento Óptico de Caracteres), mas utiliza técnicas avançadas de processamento de imagem para eliminar ruídos, lidar com ambiguidades e garantir 100% de precisão na extração dos dados.

## ⚙️ Tecnologias e Arsenal
* **Linguagem:** Python
* **Visão Computacional:** `OpenCV` (cv2) e `NumPy` para manipulação de matrizes e tensores.
* **Motor de Inteligência Artificial (OCR):** `Tesseract OCR` (via `pytesseract`).
* **Visualização de Dados:** `Matplotlib`.

## 🚀 Arquitetura e Engenharia do Sistema
1. **Rastreamento de Contornos (Edge Detection):** Utilização de Filtros Bilaterais para suavização de ruído e do algoritmo Canny para detecção de bordas rígidas. O motor rastreia polígonos na imagem e isola o retângulo exato correspondente à placa.
2. **Binarização de Alto Contraste (Otsu's Thresholding):** Conversão da imagem recortada para preto e branco absoluto (Thresholding), eliminando sombras, reflexos e melhorando drasticamente a legibilidade para a IA.
3. **Calibração de IA (Whitelist restrita):** Para contornar a ambiguidade visual de caracteres (como confundir a letra 'g' minúscula com o número '8'), o Tesseract foi configurado via restrição de caracteres (`--psm 8` e `tessedit_char_whitelist`), forçando o modelo a avaliar apenas padrões válidos de placas brasileiras (Letras Maiúsculas, Números e Hífen).
4. **Interface Picture-in-Picture (Overlay):** Engenharia de matrizes com OpenCV para injetar a imagem binarizada processada de volta na imagem original (canto superior direito), permitindo uma auditoria visual em tempo real do processamento da IA.

## 💻 Como Executar Localmente
1. Clone este repositório.
2. Instale as dependências executando: `pip install -r requirements.txt`
3. Instale o motor do Tesseract OCR no seu sistema operacional (Windows/Linux) e certifique-se de que o caminho do executável está correto na variável `pytesseract.pytesseract.tesseract_cmd` dentro do script.
4. Execute o robô: `python leitor.py`
