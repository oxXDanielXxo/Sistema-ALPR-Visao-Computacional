import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt

# 1. Caminho do Tesseract (Ajuste se necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 2. Carregando o Alvo (Crie uma cópia para o display final)
caminho_imagem = "placa_teste.jpg"
imagem = cv2.imread(caminho_imagem)

if imagem is None:
    print(f"❌ Erro crítico: Alvo '{caminho_imagem}' não encontrado.")
    exit()

imagem_final_display = imagem.copy() # Cópia onde faremos a montagem visual
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

print("🔍 Fase 1: Rastreando a placa no veículo...")

# 3. O Caçador de Contornos
filtro = cv2.bilateralFilter(imagem_cinza, 11, 17, 17) 
bordas = cv2.Canny(filtro, 30, 200) 
contornos, _ = cv2.findContours(bordas.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:10]

placa_contorno = None
for c in contornos:
    perimetro = cv2.arcLength(c, True)
    aproximacao = cv2.approxPolyDP(c, 0.018 * perimetro, True)
    if len(aproximacao) == 4:
        placa_contorno = aproximacao
        break

if placa_contorno is None:
    print("❌ Falha na Fase 1: Não foi possível isolar a placa.")
else:
    print("✅ Fase 1 Concluída: Retângulo da placa localizado!")
    
    # 4. O Recorte Cirúrgico
    mascara = np.zeros(imagem_cinza.shape, np.uint8)
    cv2.drawContours(mascara, [placa_contorno], 0, 255, -1)
    (x, y) = np.where(mascara == 255)
    (topo_x, topo_y) = (np.min(x), np.min(y))
    (base_x, base_y) = (np.max(x), np.max(y))
    placa_isolada = imagem_cinza[topo_x:base_x+1, topo_y:base_y+1]
    
    # 4.5. O Polimento Final (Binarização de Alto Contraste)
    _, placa_binaria = cv2.threshold(placa_isolada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    print("🤖 Fase 2: Extraindo caracteres com o Tesseract restrito...")
    
    # 5. O Leitor (Tesseract) com "Rédeas" (Whitelist)
    config_tesseract = '--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
    texto_extraido = pytesseract.image_to_string(placa_binaria, config=config_tesseract)
    
    placa_final = texto_extraido.strip()
    
    print("\n🎯 ==== RELATÓRIO DE EXTRAÇÃO ====")
    print(f"Placa detectada: {placa_final}")
    print("==================================\n")

    # ============================================================
    # FASE 3: ENGENHARIA VISUAL DE COMPARAÇÃO (NOVO MÓDULO)
    # ============================================================
    print("🖼️  Fase 3: Gerando montagem visual para o usuário...")
    
    # Passo A: O OpenCV precisa converter a imagem preto e branco da placa
    # de volta para o formato de cores (BGR) para conseguir colar na imagem do carro.
    placa_para_colar = cv2.cvtColor(placa_binaria, cv2.COLOR_GRAY2BGR)
    
    # Passo B: Pegamos as dimensões da imagem original do carro
    altura_carro, largura_carro, _ = imagem_final_display.shape
    
    # Passo C: Calculamos o tamanho do "Picture-in-Picture".
    # Queremos que a placa processada ocupe 25% (um quarto) da largura total do carro.
    largura_overlay = int(largura_carro * 0.25)
    # Mantemos a proporção da placa original para não esticá-la
    proporcao = largura_overlay / placa_para_colar.shape[1]
    altura_overlay = int(placa_para_colar.shape[0] * proporcao)
    
    # Passo D: Redimensionamos a imagem da placa para o tamanho calculado
    placa_redimensionada = cv2.resize(placa_para_colar, (largura_overlay, altura_overlay))
    
    # Passo E: Definimos as coordenadas matemáticas do "Canto Superior Direito"
    # O 'y' (linhas) começa no 0 e vai até a altura da placa
    y_start = 0
    y_end = altura_overlay
    # O 'x' (colunas) começa no final da imagem e volta o tamanho da largura da placa
    x_start = largura_carro - largura_overlay
    x_end = largura_carro
    
    # Passo F: A "Cola". Substituímos os pixels originais pelos pixels da placa.
    imagem_final_display[y_start:y_end, x_start:x_end] = placa_redimensionada
    
    # Passo G (Opcional Tático): Desenha uma borda verde ao redor da placa colada
    # para destacar que aquilo é o processamento da IA.
    cv2.rectangle(imagem_final_display, (x_start, y_start), (x_end-1, y_end-1), (0, 255, 0), 2)
    
    # Passo H: Exibição Final
    # Adicionamos o texto lido no título da janela
    titulo_janela = f"Leitura da IA: {placa_final}"
    
    plt.figure(figsize=(10, 7)) # Janela maior para melhor visualização
    plt.imshow(cv2.cvtColor(imagem_final_display, cv2.COLOR_BGR2RGB))
    plt.title(titulo_janela, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()