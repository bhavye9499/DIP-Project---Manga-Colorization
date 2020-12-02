def get_pixel_neighbourhood(mat, location, shape):
    x, y = location
    P, Q = shape
    x_max = min(x + P // 2, mat.shape[0])
    y_max = min(y + Q // 2, mat.shape[1])
    x_min = max(x - P // 2, 0)
    y_min = max(y - Q // 2, 0)
    return mat[x_min:x_max, y_min:y_max]
