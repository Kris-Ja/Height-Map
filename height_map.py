import matplotlib.pyplot as plt
import numpy as np
import colorsys

def hsv2rgb(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)

def gradient_h(v):
    return 1.0/3-v/3

def main():
    plt.tick_params(top='True', right='True', direction='in')
    height_map = np.loadtxt('big.dem', skiprows=1)
    file = open('big.dem', 'r')
    width, height, distance = map(int, file.readline().split())
    normal = np.zeros((height, width, 3))
    for i in range(0, height):
        for j in range(0, width):
            p = height_map[i][j]
            if j+1<width:
                p_right = height_map[i][j+1]
            else:
                p_right = height_map[i][j]
            if i+1<height:
                p_down = height_map[i+1][j]
            else:
                p_right = height_map[i][j]
            normal[i][j] = np.cross((0, distance, 900*(p_down-p)), (distance, 0, 900*(p_right-p)))
            normal[i][j] /= np.linalg.norm(normal[i][j])
    height_map = height_map	- height_map.min()
    height_map = height_map / height_map.max()
    img = np.zeros((height, width, 3))
    light_vector = (1.7, 1, -2)
    light_vector /= np.linalg.norm(light_vector)
    for i in range(0, height):
        for j in range(0, width):
            reflected = -light_vector - 2*np.dot(-light_vector, normal[i][j])*normal[i][j]
            reflected /= np.linalg.norm(reflected)
            reflected = np.dot(reflected, (0, 0, -1))
            if reflected<0:
                reflected = 0.0
            reflected = reflected ** 30
            img[i][j] = hsv2rgb(gradient_h(height_map[i][j]), 1, np.dot(light_vector, normal[i][j])+0.2 )
            img[i][j][0] += reflected
            img[i][j][1] += reflected
            img[i][j][2] += reflected
    plt.imshow(img)
    plt.show()

if __name__ == '__main__':
    main()
