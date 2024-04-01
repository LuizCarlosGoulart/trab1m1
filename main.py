import numpy as np
import cv2
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
from skimage import metrics

# Função para adicionar ruído gaussiano (usando numpy)
def add_gaussian_noise(image, mean=0, var=0.1):
    row, col = image.shape
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, (row, col))
    noisy_image = image + gauss
    noisy_image = np.clip(noisy_image, 0, 255)  # Limita os valores entre 0 e 255
    return noisy_image.astype(np.uint8)

# Operações pontuais implementadas manualmente
def adjust_brightness(image, brightness):
    # Assegura que a operação é realizada dentro dos limites de 0 e 255
    return np.clip(image + brightness, 0, 255).astype(np.uint8)

def adjust_contrast(image, contrast):
    # Fator de ajuste de contraste
    f = (259 * (contrast + 255)) / (255.0 * (259 - contrast))
    # Aplica o ajuste de contraste
    contrast_adjusted = f * (image - 118) + 128
    return np.clip(contrast_adjusted, 0, 255).astype(np.uint8)

def invert_image(image):
    return 255 - image

# Funções de filtros espaciais usando convolve do scipy
def apply_average_filter(image):
    kernel = np.ones((3, 3)) / 9
    return convolve(image, kernel, mode='reflect').astype(np.uint8)

def apply_gaussian_filter(image, sigma=1.0):
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
    return convolve(image, kernel, mode='reflect').astype(np.uint8)

def apply_median_filter(image):
    # Implementação manual do filtro mediano seria ineficiente sem numpy/scipy,
    # mas aqui usamos cv2 por simplicidade e foco nas operações pontuais.
    return cv2.medianBlur(image, 3)

# Carregar e converter a imagem para escala de cinza usando OpenCV
image_path = 'lena.jpg'  # Assegure-se de ter essa imagem ou substitua pelo caminho correto
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Adicionar ruído
noisy_image = add_gaussian_noise(gray_image)

# Aplicar operações pontuais
bright_image = adjust_brightness(noisy_image, 30)
contrast_image = adjust_contrast(noisy_image, 50)
inverted_image = invert_image(noisy_image)

# Aplicar filtros de remoção de ruído
average_filtered = apply_average_filter(bright_image)
gaussian_filtered = apply_gaussian_filter(contrast_image)
median_filtered = apply_median_filter(inverted_image)

# A partir daqui, você pode usar o matplotlib para exibir as imagens e os histogramas,
# e calcular métricas como MSE e SSIM para avaliar as diferenças.
def plot_image_and_its_histogram(image, title, position):
    # Define o subplot para a imagem
    plt.subplot(2, 2, position)
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')

    # Define o subplot para o histograma da imagem
    plt.subplot(2, 2, position + 2)
    plt.hist(image.ravel(), bins=256, color='black')
    plt.title('Histograma')
    plt.xlim([0, 256])

def plot_original_and_selected_image_with_histograms(selected_image, selected_title):
    plt.figure(figsize=(12, 12))

    # Plotar a imagem original e seu histograma
    plot_image_and_its_histogram(gray_image, 'Original', 1)

    # Plotar a imagem selecionada e seu histograma
    plot_image_and_its_histogram(selected_image, selected_title, 2)

    plt.tight_layout()
    plt.show()

# Solicitar ao usuário que selecione a imagem para visualização
print("Selecione a imagem para visualização:")
print("1 - Original")
print("2 - Com Ruído")
print("3 - Brilho Ajustado")
print("4 - Contraste Ajustado")
print("5 - Imagem Invertida")
print("6 - Filtro Média")
print("7 - Filtro Gaussiano")
print("8 - Filtro Mediana")
escolha = input("Digite o número da imagem: ")

# Dicionário para mapear a escolha para a função correspondente
imagens = {
    '1': (gray_image, 'Original'),
    '2': (noisy_image, 'Com Ruído'),
    '3': (bright_image, 'Brilho Ajustado'),
    '4': (contrast_image, 'Contraste Ajustado'),
    '5': (inverted_image, 'Imagem Invertida'),
    '6': (average_filtered, 'Filtro Média'),
    '7': (gaussian_filtered, 'Filtro Gaussiano'),
    '8': (median_filtered, 'Filtro Mediana'),
}

# Obter a imagem e o título baseado na escolha do usuário
selected_image, selected_title = imagens.get(escolha, (gray_image, 'Original'))

# Exibir a imagem original e a imagem selecionada, junto com seus histogramas
plot_original_and_selected_image_with_histograms(selected_image, selected_title)