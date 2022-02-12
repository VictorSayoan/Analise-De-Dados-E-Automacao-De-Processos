import matplotlib.pyplot as plt


def controi_grafico(prop1, prop2, dado1, dado2, estilo, cor, marcador, titulo, msg_x, msg_y):
    plt.figure(figsize=(prop1, prop2))
    plt.plot(dado1, dado2, linestyle=estilo, color=cor, marker=marcador)
    plt.title(titulo)
    plt.xlabel(msg_x)
    plt.ylabel(msg_y)
    plt.show()