from src.constants import *
from src.generic_imports import *
from src.halting_filter import *
from src.utils import *


def curvature(phi, dot_pitch):
    phi_xx = np.diff(np.vstack([phi[0, :], phi, phi[-1, :]]), axis=0)
    phi_xx = np.diff(phi_xx, axis=0) / (dot_pitch ** 2)
    phi_yy = np.diff(np.hstack([np.reshape(phi[:, 0], (-1, 1)), phi, np.reshape(phi[:, -1], (-1, 1))]), axis=1)
    phi_yy = np.diff(phi_yy, axis=1) / (dot_pitch ** 2)

    phi_x = (phi[2:, :] - phi[:-2, :]) / (2 * dot_pitch)
    phi_x = np.vstack([phi_x[0, :], phi_x, phi_x[-1, :]])
    phi_y = (phi[:, 2:] - phi[:, :-2]) / (2 * dot_pitch)
    phi_y = np.hstack([np.reshape(phi_y[:, 0], (-1, 1)), phi_y, np.reshape(phi_y[:, -1], (-1, 1))])

    phi_xy = (phi_x[:, 2:] - phi_x[:, :-2]) / (2 * dot_pitch)
    phi_xy = np.hstack([np.reshape(phi_xy[:, 0], (-1, 1)), phi_xy, np.reshape(phi_xy[:, -1], (-1, 1))])

    kappa = (phi_xx * phi_y ** 2 - 2 * phi_x * phi_y * phi_xy + phi_yy * phi_x ** 2) / (phi_x ** 2 + phi_y ** 2) ** 1.5

    return np.minimum(np.maximum(kappa, -1 / dot_pitch), 1 / dot_pitch)


def f_abs_grad_phi(phi, dot_pitch, f, c=0):
    Dx = np.diff(phi, axis=0) / dot_pitch
    Dy = np.diff(phi, axis=1) / dot_pitch

    Dx_minus = np.vstack([Dx[0, :], Dx])
    Dx_plus = np.vstack([Dx, Dx[-1, :]])

    Dy_minus = np.hstack([np.reshape(Dy[:, 0], (-1, 1)), Dy])
    Dy_plus = np.hstack([Dy, np.reshape(Dy[:, -1], (-1, 1))])

    grad_plus = np.sqrt(np.maximum(Dx_minus, 0) ** 2 + np.minimum(Dx_plus, 0) ** 2 +
                        np.maximum(Dy_minus, 0) ** 2 + np.minimum(Dy_plus, 0) ** 2)
    grad_minus = np.sqrt(np.minimum(Dx_minus, 0) ** 2 + np.maximum(Dx_plus, 0) ** 2 +
                         np.minimum(Dy_minus, 0) ** 2 + np.maximum(Dy_plus, 0) ** 2)

    return (np.maximum(f, 0) * (grad_plus - c)) + (np.minimum(f, 0) * (grad_minus - c))


def perform_LSM(img, scribbled_img, dt, iterations, type='intensity', leak_proofing=True):
    plt.show()
    P, Q = img.shape
    x = np.linspace(0, P, P)
    y = np.linspace(0, Q, Q)
    dot_pitch = x[1] - x[0]
    X, Y = np.meshgrid(x, y)

    # scribbled_pixels = get_scribbled_pixels(scribbled_img)
    # rand_pixel = scribbled_pixels[np.random.randint(0, len(scribbled_pixels), 1)[0]]
    # print(rand_pixel)
    rand_pixel = [45, 100]
    phi = (X - rand_pixel[0]) ** 2 + (Y - rand_pixel[1]) ** 2 - (dot_pitch ** 2)
    phi = phi.astype(np.float_)
    print(f'phi shape = {phi.shape}')

    plt.figure(figsize=(7, 7))
    # visualize_scribbled_pixels(np.copy(img), scribbled_pixels)
    # plt.contour(x, y, phi, [0])
    # plt.show()
    # exit(-1)

    h = None
    if type == 'intensity':
        h = get_halting_filter_intensity(img)
    elif type == 'pattern':
        h = get_halting_filter_pattern(img)
    # Image.fromarray(log_transform(h)).show()

    # TODO fast marching method for complexity O(n.logn)
    for i in range(iterations):
        FG = -EPSILON * curvature(phi, dot_pitch)
        F = h * (FA + FG)
        if leak_proofing:
            temp = (1 / h) - 1
            M1 = np.max(temp)
            M2 = np.min(temp)
            FI = -FA * np.clip((temp - M2) / (M1 - M2 - RELAX_FACTOR), 0, 1)
            F += h * FI

        # phi = phi - (dt * F * |grad|)
        phi = phi - (dt * f_abs_grad_phi(phi, dot_pitch, F))

        for _ in range(NR):
            phi = phi - (dt * f_abs_grad_phi(phi, dot_pitch, phi / np.sqrt(phi ** 2 + (2 * dot_pitch) ** 2), 1))

        plt.contour(x, y, phi, [0])
        plt.show(block=False)
        plt.pause(0.01)
        plt.clf()
