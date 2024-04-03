import cv2
import numpy as np
import matplotlib.pyplot as plt

def image_grayscale(image_path):
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def median_filter(image, kernel_size):
    pad_size = kernel_size // 2
    padded_image = np.pad(image, pad_size, mode='constant', constant_values=0)
    filtered_image = np.zeros_like(image)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i+kernel_size, j:j+kernel_size]
            filtered_image[i, j] = np.median(region)
    return filtered_image.astype(np.uint8)

def plot_comparison(original_image, filtered_image, filter_title):
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))

    axs[0, 0].imshow(original_image, cmap='gray')
    axs[0, 0].set_title('Imagem Original')
    axs[0, 0].axis('off')
    
    axs[0, 1].hist(original_image.ravel(), bins=256, color='black')
    axs[0, 1].set_title('Histograma Original')
    axs[0, 1].set_xlim([0, 256])

    axs[1, 0].imshow(filtered_image, cmap='gray')
    axs[1, 0].set_title(f'Imagem com Filtro - {filter_title}')
    axs[1, 0].axis('off')
    
    axs[1, 1].hist(filtered_image.ravel(), bins=256, color='black')
    axs[1, 1].set_title(f'Histograma - {filter_title}')
    axs[1, 1].set_xlim([0, 256])

    plt.tight_layout()
    plt.show()

# Imagem em escala de cinza
gray_image = image_grayscale('lena.jpg')

# Aplica os filtros
filtered_median = median_filter(gray_image, 3)

filters = {
    '1': ('Mediana', filtered_median),
    '0': ('Sair', None)
}

while True:
    print("\nEscolha o filtro de ruído:")
    print("1 - Filtro Mediana")
    print("0 - Sair")
    choice = input("Digite sua escolha: ")

    if choice == '0':
        break
    elif choice in filters:
        title, image = filters[choice]
        plot_comparison(gray_image, image, title)
    else:
        print("Escolha inválida. Por favor, tente novamente.")
