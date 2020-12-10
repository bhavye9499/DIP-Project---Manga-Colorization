from src.constants import *
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

    return np.nan_to_num(np.minimum(np.maximum(kappa, -1 / dot_pitch), 1 / dot_pitch))


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

    return np.nan_to_num((np.maximum(f, 0) * (grad_plus - c)) + (np.minimum(f, 0) * (grad_minus - c)))


def get_phi_0(shape, center, radius):
    P, Q = shape
    y = np.linspace(0, P - 1, P)
    x = np.linspace(0, Q - 1, Q)
    X, Y = np.meshgrid(x, y)
    phi_0 = (X - center[0]) ** 2 + (Y - center[1]) ** 2 - (radius ** 2)
    return phi_0


def perform_LSM(img, scribbled_img, dt, max_iter=10000, lsm_type='intensity', leak_proofing=False):
    start_pixel = random.choice(get_scribbled_pixels(scribbled_img))

    dot_pitch = 1
    phi = get_phi_0(img.shape, start_pixel, dot_pitch)

    h = halting_filter(img, lsm_type)

    # For intensity-continuous propagation only
    FI = 0
    if leak_proofing:
        temp = (1 / h) - 1
        M1 = np.max(temp)
        M2 = np.min(temp)
        FI = -FA * np.clip((temp - M2) / (M1 - M2 - RELAX_FACTOR), 0, 1)

    prev_omega = np.sum(phi <= 0)

    for itr in range(max_iter):
        FG = -EPSILON * curvature(phi, dot_pitch)
        F = h * (FA + FG)
        if leak_proofing:
            F += h * FI

        phi = phi - (dt * f_abs_grad_phi(phi, dot_pitch, F))

        for _ in range(NR):
            phi = phi - (dt * f_abs_grad_phi(phi, dot_pitch, phi / np.sqrt(phi ** 2 + (2 * dot_pitch) ** 2), 1))

        if (itr + 1) % JUMP == 0:
            plt.imshow(img, cmap='gray')
            plt.contour(phi, colors='red', levels=0, linewidths=2)
            plt.show(block=False)
            plt.pause(1e-4)
            plt.clf()

            cur_omega = np.sum(phi <= 0)
            if cur_omega - prev_omega < LSM_THRESHOLD:
                break
            prev_omega = cur_omega

        itr += 1

    print('Segmentation Completed')
    plt.imshow(img, cmap='gray')
    plt.contour(phi, colors='red', levels=0, linewidths=2)
    plt.show()
