import numpy as np
import cv2
import math
from scipy.signal import convolve2d


#@@ PSNR
def psnr(img1, img2):
    mse = np.mean((img1-img2)**2)
    if mse == 0:
        return 100
    else:
        L=255.0 #L:maximum pixel value
        return 10*math.log10(L*L/mse)
    

#@@ SSIM : structural similarity index
def ssim(img1, img2):
    # ssim parameters
    k1 = 0.01
    k2 = 0.03
    L = 255.0
    C1 = (k1*L)**2 #**2 = square
    C2 = (k2*L)**2
    
    arr1 = np.asarray(img1)
    arr2 = np.asarray(img2)
    mean1 = np.mean(arr1)
    mean2 = np.mean(arr2)
    #std1 = np.sqrt(np.sum((arr1-mean1)**2)/(arr1.size-1)) #unbaised estimator 1/(N-1)
    std1 = np.std(arr1, ddof=1) # unbaised estimator 1/(N-1)
    std2 = np.std(arr2, ddof=1)

    cor = 1.0/(arr1.size-1) * np.sum((arr1-mean1)*(arr2-mean2)) # correlation coefficient
#    print("mean1:%f std1:%f" %(mean1, std1))
#    print("mean2:%f std2:%f" %(mean2, std2))
#    print("cor:%f" %cor)
    return ((2*mean1*mean2+C1) * (2*cor+C2))/((mean1**2+mean2**2+C1) * (std1**2+std2**2+C2))

#@@ MSSIM : mean structural similarity 
def mssim(img1, img2):
    # ssim parameters
    k1 = 0.01
    k2 = 0.03
    L = 255.0
    C1 = (k1*L)**2 #**2 = square
    C2 = (k2*L)**2
    N = 5

    arr1 = np.asarray(img1)
    arr2 = np.asarray(img2)
    arr1 = arr1.reshape((img1.shape[2], img1.shape[0], img1.shape[1]))# channels, height, width
    arr2 = arr2.reshape((img1.shape[2], img1.shape[0], img1.shape[1]))
    # define MSSIM mat
    mean1_map = np.zeros((img1.shape[2], img1.shape[0], img1.shape[1]))
    mean2_map = np.zeros((img1.shape[2], img1.shape[0], img1.shape[1]))
    std1_map = np.zeros((img1.shape[2], img1.shape[0], img1.shape[1]))
    std2_map = np.zeros((img1.shape[2], img1.shape[0], img1.shape[1]))
    cor_map = np.zeros((img1.shape[2], img1.shape[0], img1.shape[1]))
    ssim_map = np.zeros((img1.shape[2], img1.shape[0], img1.shape[1]))
    # kernel
    kernel = np.ones((2*N+1, 2*N+1), dtype=int)
    kernel_size = (2*N+1)**2-1

    mean1_map[0] = convolve2d(arr1[0], kernel, mode="same", boundary="symm")/((2*N+1)**2) #same:output size is same as arr1
    mean1_map[1] = convolve2d(arr1[1], kernel, mode="same", boundary="symm")/((2*N+1)**2)
    mean1_map[2] = convolve2d(arr1[2], kernel, mode="same", boundary="symm")/((2*N+1)**2)
    mean2_map[0] = convolve2d(arr2[0], kernel, mode="same", boundary="symm")/((2*N+1)**2) #same:output size is same as arr1
    mean2_map[1] = convolve2d(arr2[1], kernel, mode="same", boundary="symm")/((2*N+1)**2)
    mean2_map[2] = convolve2d(arr2[2], kernel, mode="same", boundary="symm")/((2*N+1)**2)
    
    std1_map[0] = convolve2d((arr1[0]-mean1_map[0])**2, kernel, mode="same", boundary="symm") #multiple windows
    std1_map[0] = np.sqrt(std1_map[0]/kernel_size)
    std1_map[1] = convolve2d((arr1[1]-mean1_map[1])**2, kernel, mode="same", boundary="symm")
    std1_map[1] = np.sqrt(std1_map[1]/kernel_size)
    std1_map[2] = convolve2d((arr1[2]-mean1_map[2])**2, kernel, mode="same", boundary="symm")
    std1_map[2] = np.sqrt(std1_map[2]/kernel_size)
    std2_map[0] = convolve2d((arr2[0]-mean2_map[0])**2, kernel, mode="same", boundary="symm") #multiple windows
    std2_map[0] = np.sqrt(std2_map[0]/kernel_size)
    std2_map[1] = convolve2d((arr2[1]-mean2_map[1])**2, kernel, mode="same", boundary="symm")
    std2_map[1] = np.sqrt(std2_map[1]/kernel_size)
    std2_map[2] = convolve2d((arr2[2]-mean2_map[2])**2, kernel, mode="same", boundary="symm")
    std2_map[2] = np.sqrt(std2_map[2]/kernel_size)
    
    cor_map[0] = convolve2d(((arr1[0]-mean1_map[0])*(arr2[0]-mean2_map[0])), kernel, mode="same", boundary="symm") #multiple windows
    cor_map[0] = cor_map[0]/kernel_size
    cor_map[1] = convolve2d(((arr1[1]-mean1_map[1])*(arr2[1]-mean2_map[1])), kernel, mode="same", boundary="symm")
    cor_map[1] = cor_map[1]/kernel_size
    cor_map[2] = convolve2d(((arr1[2]-mean1_map[2])*(arr2[2]-mean2_map[2])), kernel, mode="same", boundary="symm")
    cor_map[2] = cor_map[2]/kernel_size
    
    ssim_map[0] = ((2*mean1_map[0]*mean2_map[0]+C1) * (2*cor_map[0]+C2))/((mean1_map[0]**2+mean2_map[0]**2+C1) * (std1_map[0]**2+std2_map[0]**2+C2))
    ssim_map[1] = ((2*mean1_map[1]*mean2_map[1]+C1) * (2*cor_map[1]+C2))/((mean1_map[1]**2+mean2_map[1]**2+C1) * (std1_map[1]**2+std2_map[1]**2+C2))
    ssim_map[2] = ((2*mean1_map[2]*mean2_map[2]+C1) * (2*cor_map[2]+C2))/((mean1_map[2]**2+mean2_map[2]**2+C1) * (std1_map[2]**2+std2_map[2]**2+C2))
    
    return np.mean(ssim_map)
    
    
    
org_img = cv2.imread("Lenna.png")
filter_img = cv2.imread("Lenna.png")
psnr_v = psnr(org_img, filter_img)
ssim_v = ssim(org_img, filter_img)
mssim_v = mssim(org_img, filter_img)

print("PSNR:%fdB, SSIM:%f MSSIM:%f" %(psnr_v,ssim_v, mssim_v))


