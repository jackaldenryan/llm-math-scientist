import matplotlib.pyplot as plt


def plot_multiple_curves(y_val_lists, x_val_lists=None, title=None, filename=None, show_plot=True):
    plt.figure(figsize=(10, 6))

    for i, curve_data in enumerate(y_val_lists):
        if x_val_lists is None:
            x_values = list(range(len(curve_data)))
        else:
            x_values = x_val_lists[i]
        plt.plot(x_values, curve_data, label=f'Curve {i+1}')

    if filename:
        plt.savefig(filename)

    if show_plot:
        plt.show()
    else:
        plt.close()
