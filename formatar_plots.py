import matplotlib.pyplot as plt
import seaborn as sns
from config import cinza_escuro

def add_labels(ax, data, max_value, percentages=None, horizontal_offset=None):
    for index, value in enumerate(data):
        formatted_value = f"{value:,}".replace(",", ".")
        if percentages is not None:
            percentage = percentages[index]
            text = f"{formatted_value}\n({percentage:.1f}%)"
        else:
            text = f"{formatted_value}"
        
        if horizontal_offset is not None:
            offset = horizontal_offset[index % 2]  # Alternar entre os offsets
            ax.text(index + offset, value + max_value * 0.02, text, ha='center', fontsize=12)
        else:
            ax.text(index, value + max_value * 0.02, text, ha='center', fontsize=12)

def format_plot(ax, max_value, y_label = 'Número de Vítimas', y_min=0):
    plt.xticks(fontsize=13, color=cinza_escuro)
    plt.xlabel('')
    plt.ylabel(y_label, fontsize=15, color=cinza_escuro)
    plt.ylim(y_min, max_value * 1.2)
    ax.margins(y=0)
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
    sns.despine()