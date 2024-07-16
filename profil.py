import pandas as pd
import matplotlib.pyplot as plt
import glob
import math

# Function to read data from the provided folder
def read_data_files():
    folder_path = 'dane'
    all_files = glob.glob(folder_path + "/2*.csv")
    data_list = []

    for filename in all_files:
        df = pd.read_csv(filename)
        data_list.append(df)
    return data_list

# Function to calculate the Lagrange interpolation polynomial
def lagrange_interpolation(x, y, x_new):
    def L(k, x_new):
        terms = [(x_new - x[j]) / (x[k] - x[j]) for j in range(len(x)) if j != k]
        result = 1

        for term in terms:
            result *= term
        return result
    
    y_new = [sum(y[k] * L(k, xi) for k in range(len(x))) for xi in x_new]
    return y_new

# Function to generate a list of linearly spaced values
def linspace(start, stop, num):
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]

# Function to generate Chebyshev nodes
def chebyshev_nodes(start, stop, num):
    return [(start + stop) / 2 + (stop - start) / 2 * math.cos((2 * k + 1) * math.pi / (2 * num)) for k in range(num)]

# Function to perform linear interpolation to find y-values for given x-values
def linear_interpolation(x, y, x_new):
    y_new = []
    for xi in x_new:
        for i in range(len(x) - 1):
            if x[i] <= xi <= x[i + 1]:
                yi = y[i] + (y[i + 1] - y[i]) * (xi - x[i]) / (x[i + 1] - x[i])
                y_new.append(yi)
                break
    return y_new

# Function to calculate cubic spline interpolation
def cubic_spline_interpolation(x, y, x_new):
    n = len(x) - 1
    h = [x[i + 1] - x[i] for i in range(n)]
    alpha = [3 * (y[i + 1] - y[i]) / h[i] - 3 * (y[i] - y[i - 1]) / h[i - 1] for i in range(1, n)]

    l = [1] + [0] * n
    mu = [0] + [0] * n
    z = [0] + [0] * n

    for i in range(1, n):
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i - 1] - h[i - 1] * z[i - 1]) / l[i]

    l[n] = 1
    z[n] = 0

    c = [0] * (n + 1)
    b = [0] * n
    d = [0] * n

    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y[j + 1] - y[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    spline = []
    for xi in x_new:
        for j in range(n):
            if x[j] <= xi <= x[j + 1]:
                dx = xi - x[j]
                yi = y[j] + b[j] * dx + c[j] * dx**2 + d[j] * dx**3
                spline.append(yi)
                break

    return spline

# Function to plot the interpolation results
def plot_interpolation(data, num_points_list):
    for df in data:
        x = list(df['distance'])
        y = list(df['elevation'])
        x_interp = linspace(min(x), max(x), 1000)

        plt.figure(figsize=(15, 10))

        for i, num_points in enumerate(num_points_list):
            indices = [int(round(j)) for j in linspace(0, len(x) - 1, num_points)]
            x_nodes = [x[idx] for idx in indices]
            y_nodes = [y[idx] for idx in indices]

            y_interp = lagrange_interpolation(x_nodes, y_nodes, x_interp)

            plt.subplot(3, 1, i + 1)
            plt.plot(x, y, '-', label='Dane oryginalne')
            plt.plot(x_nodes, y_nodes, 's', label=f'Węzły interpolacji (n={num_points})')
            plt.plot(x_interp, y_interp, '-', label='Interpolacja Lagrange’a')
            plt.title(f'Interpolacja Lagrange’a z {num_points} węzłami')
            plt.xlabel('Odległość [m]')
            plt.ylabel('Wysokość [m]')
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.5)
        plt.show()

# Function to plot the interpolation results with Chebyshev nodes
def plot_interpolation_chebyshev(data, num_points_list):
    for df in data:
        x = list(df['distance'])
        y = list(df['elevation'])
        x_interp = linspace(min(x), max(x), 1000)

        plt.figure(figsize=(15, 10))

        for i, num_points in enumerate(num_points_list):
            chebyshev_x = chebyshev_nodes(min(x), max(x), num_points)
            y_nodes = linear_interpolation(x, y, chebyshev_x)

            y_interp = lagrange_interpolation(chebyshev_x, y_nodes, x_interp)

            plt.subplot(3, 1, i + 1)
            plt.plot(x, y, '-', label='Dane oryginalne')
            plt.plot(chebyshev_x, y_nodes, 's', label=f'Węzły Czebyszewa (n={num_points})')
            plt.plot(x_interp, y_interp, '-', label='Interpolacja Lagrange’a')
            plt.title(f'Interpolacja Lagrange’a z węzłami Czebyszewa ({num_points})')
            plt.xlabel('Odległość [m]')
            plt.ylabel('Wysokość [m]')
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.5)
        plt.show()

# Function to plot the interpolation results with cubic splines
def plot_interpolation_cubic_spline(data, num_points_list):
    for df in data:
        x = list(df['distance'])
        y = list(df['elevation'])
        x_interp = linspace(min(x), max(x), 1000)

        plt.figure(figsize=(15, 10))

        for i, num_points in enumerate(num_points_list):
            indices = [int(round(j)) for j in linspace(0, len(x) - 1, num_points)]
            x_nodes = [x[idx] for idx in indices]
            y_nodes = [y[idx] for idx in indices]

            y_interp = cubic_spline_interpolation(x_nodes, y_nodes, x_interp)

            plt.subplot(3, 1, i + 1)
            plt.plot(x, y, '-', label='Dane oryginalne')
            plt.plot(x_nodes, y_nodes, 's', label=f'Węzły interpolacji (n={num_points})')
            plt.plot(x_interp, y_interp, '-', label='Interpolacja funkcjami sklejanymi')
            plt.title(f'Interpolacja funkcjami sklejanymi z {num_points} węzłami')
            plt.xlabel('Odległość [m]')
            plt.ylabel('Wysokość [m]')
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.5)
        plt.show()

# Read the data files from the folder 'dane'
data_files = read_data_files()

# Define the number of interpolation nodes
num_points_list = [6, 12, 15]

# Plot the interpolation results
plot_interpolation(data_files, num_points_list)

# Plot the interpolation results with Chebyshev nodes
plot_interpolation_chebyshev(data_files, num_points_list)

# Plot the interpolation results with cubic splines
plot_interpolation_cubic_spline(data_files, num_points_list)