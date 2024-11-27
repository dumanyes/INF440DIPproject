import cv2
import numpy as np


def apply_grayscale(image_path, output_path):
    img = cv2.imread(image_path)
    r, g, b = 0.2989, 0.5870, 0.1140
    grayscale_img = img[:, :, 0] * b + img[:, :, 1] * g + img[:, :, 2] * r
    grayscale_img = grayscale_img.astype(np.uint8)  # Ensure it's in proper data type
    grayscale_img = cv2.merge([grayscale_img, grayscale_img, grayscale_img])
    cv2.imwrite(output_path, grayscale_img)


def apply_edge_detection(image_path, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # Apply kernels using cv2.filter2D
    grad_x = cv2.filter2D(img, cv2.CV_64F, sobel_x)
    grad_y = cv2.filter2D(img, cv2.CV_64F, sobel_y)

    # Combine gradients
    edges = np.sqrt(grad_x ** 2 + grad_y ** 2)
    edges = np.clip(edges, 0, 255).astype(np.uint8)

    # Convert to a 3-channel image for consistency
    edges_colored = cv2.merge([edges, edges, edges])
    cv2.imwrite(output_path, edges_colored)


def apply_gaussian_blur(image_path, output_path):
    img = cv2.imread(image_path)
    # Define a Gaussian kernel with larger kernel size and sigma
    kernel_size = 15  # Increase kernel size for stronger blur
    sigma = 2.0  # Higher sigma for more noticeable blur

    # Generate Gaussian kernel
    ax = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
    gauss = np.exp(-0.5 * (ax / sigma) ** 2)
    kernel = np.outer(gauss, gauss)
    kernel /= kernel.sum()  # Normalize the kernel

    # Apply Gaussian blur using cv2.filter2D
    blurred_img = cv2.filter2D(img, -1, kernel)

    # Save the blurred image
    cv2.imwrite(output_path, blurred_img)

def apply_sepia(image_path, output_path):
    img = cv2.imread(image_path)
    # Define the sepia kernel
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])

    # Apply the sepia transformation
    sepia_img = cv2.transform(img, kernel)
    # Clip values to ensure they stay within [0, 255]
    sepia_img = np.clip(sepia_img, 0, 255)
    cv2.imwrite(output_path, sepia_img)


def apply_sharpening(image_path, output_path):
    img = cv2.imread(image_path)
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    # Apply the sharpening filter
    sharpened_img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(output_path, sharpened_img)


def apply_embossing(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Define the embossing kernel
    kernel = np.array([[0, -1, -1],
                       [1, 0, -1],
                       [1, 1, 0]])

    # Apply the embossing filter
    embossed_img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(output_path, embossed_img)
