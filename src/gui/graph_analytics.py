from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QTableWidget
import networkx as nx
import numpy as np

from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

shades = plt.get_cmap('Pastel1')

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
class GraphAnalytics(QWidget):
    """
    Graph analytics page, contains metrics and visualizations
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)

        # Create a vertical layout for the plots
        plots_layout = QVBoxLayout()
        
        node_features = self.parent.graph_page.graph_page.features
        disc_attribute_labels = sorted([k for k, v in list(node_features.values())[0].items() if type(v)==str or int(v)==v], key=lambda x: x.lower())
        cont_attribute_labels = sorted([k for k, v in list(node_features.values())[0].items() if type(v)==float and int(v)!=v], key=lambda x: x.lower())

        # Add discrete attribute distribution plot
        if len(disc_attribute_labels) > 0:
            attribute_distribution_plot = self.attribute_distribution_plot()
            plots_layout.addWidget(attribute_distribution_plot)

        # Add attribute distribution plot continuous variables
        if len(cont_attribute_labels) > 0:
            attribute_distribution_cont = self.attribute_distribution_cont()
            plots_layout.addWidget(attribute_distribution_cont)

        # Add adjacency matrix plot
        adj_matrix_plot = self.adjacency_matrix()
        plots_layout.addWidget(adj_matrix_plot)

        # Add the plots layout to the container layout
        container_layout.addLayout(plots_layout)

        # Add graph analytics table
        graph_analytics_table = self.graph_analytics_table()
        container_layout.addWidget(graph_analytics_table)

        scroll_area.setWidget(container_widget)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)


        # Add descriptive table
    def graph_analytics_table(self):
        graph = self.parent.graph_page.graph_page.graph.graph
        n = graph.number_of_nodes()
        graph_metrics = {
            'Number of Nodes': graph.number_of_nodes(),
            'Number of Edges': graph.number_of_edges(),
            'Density': round(nx.density(graph), 3),
            'Diameter': nx.diameter(graph),
            'Average Degree': round(sum([d for _, d in graph.degree()]) / n,3),
            'Average Clustering': round(nx.average_clustering(graph), 3),
            'Average Shortest Path': round(nx.average_shortest_path_length(graph), 3),
            'Average Betweenness Centrality': round(sum([b for _, b in nx.betweenness_centrality(graph).items()]) / n,3),
            'Average Closeness Centrality': round(sum([c for _, c in nx.closeness_centrality(graph).items()]) / n,3),
            'Average Eigenvector Centrality': round(sum([e for _, e in nx.eigenvector_centrality(graph).items()]) / n,3),
            'Average PageRank': round(sum([p for _, p in nx.pagerank(graph).items()]) / n,3),
            'Average Degree Centrality': round(sum([d for _, d in nx.degree_centrality(graph).items()]) / n,3)
         }
        table = QTableWidget()
        table.setRowCount(len(graph_metrics))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Metric', 'Value'])
        # table.setVerticalHeaderLabels(graph_metrics.keys())
        for i, (metric, value) in enumerate(graph_metrics.items()):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(metric))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        return table



    
    def update_ui(self):
        self.setup_ui()

    def adjacency_matrix(self):
        fig = Figure(figsize=(6,5), dpi=100)
        graph = self.parent.graph_page.graph_page.graph.graph
        bi_adj_matrix = nx.adjacency_matrix(graph, weight=None)
        # adj_matrix = nx.adjacency_matrix(graph, weight='weight')

        ax = fig.add_subplot(111)
        ax.set_title('Binary Adjacency Matrix')
        im = ax.matshow(bi_adj_matrix.todense(), cmap='binary')
        nodes = list(graph.nodes)
        ax.set_xticks(np.arange(len(nodes)))
        ax.set_yticks(np.arange(len(nodes)))
        ax.set_xticklabels(nodes)
        ax.set_yticklabels(nodes)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

        fig.colorbar(im, ax=ax, label="Edge Existence", cmap='binary', ticks=[0, 1])

        # ax = fig.add_subplot(122)
        # ax.set_title('Adjacency Matrix')
        # im = ax.matshow(adj_matrix.todense())
        # nodes = list(graph.nodes)
        # ax.set_xticks(np.arange(len(nodes)))
        # ax.set_yticks(np.arange(len(nodes)))
        # ax.set_xticklabels(nodes)
        # ax.set_yticklabels(nodes)
        # plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
        # fig.colorbar(im, ax=ax, label="Interaction Count")


        return FigureCanvasQTAgg(fig)
    
    def attribute_distribution_cont(self):
        fig = Figure(figsize=(7, 5), dpi=100)
        node_features = self.parent.graph_page.graph_page.features
        attribute_labels = sorted([k for k, v in list(node_features.values())[0].items() if type(v)==float and int(v)!=v], key=lambda x: x.lower())
        n = len(attribute_labels)
        fig.suptitle('Attribute Distribution (cont)')

        m = np.gcd(n, 12)
        k = int(n / m)
        for i in range(n):
            ax = fig.add_subplot(m, k, i+1)
            attribute = attribute_labels[i]
            attribute_values = [features[attribute] for features in node_features.values() if attribute in features.keys()]
            ax.bar(np.arange(len(attribute_values)), attribute_values, width=0.5)
            ax.tick_params(axis='y', labelsize=5)
            ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax.set_title(attribute, fontsize=6)

        fig.tight_layout(pad=3.0)        
        return FigureCanvasQTAgg(fig)

    def attribute_distribution_plot(self):
        fig = Figure(figsize=(7, 5), dpi=100)
        node_features = self.parent.graph_page.graph_page.features
        attribute_labels = sorted([k for k, v in list(node_features.values())[0].items() if type(v)==str or int(v)==v], key=lambda x: x.lower())
        # attribute_labels = sorted(set([key for _, value in node_features.items() for key, v in value.items() if type(v) == str or int(v) == v]), key=lambda x: x.lower())
        n = len(attribute_labels)
        fig.suptitle('Attribute Distribution')
        fig.tight_layout(pad=3.0)
        bars = []
        for i in range(n):
            ax = fig.add_subplot(n, 1, i+1)
            attribute = attribute_labels[i]
            attribute_values = [features[attribute] for features in node_features.values() if attribute in features.keys()]
            element_counts = Counter(attribute_values)
            values = list(element_counts.keys())
            count = list(element_counts.values())
 
            for i in range(len(values)):
                bar = ax.barh(attribute, count[i], left=sum(count[:i]), label=values[i], color=shades(i))
                bars.extend(bar)
            ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

            # for bar in bars:
            #     bar.set_picker(True)
            
        
        def onclick(event):
            ax_save = None
            for bar in bars:
                if bar.contains(event)[0]:
                    ax = bar.axes
                    ax.legend(bbox_to_anchor=(1, 1), loc='best', borderaxespad=0.1)
                    fig.canvas.draw_idle()
                    ax_save = ax
                    break

            # This seems like a round-about way, but is necessary since mulitple bars are part of the same axes
            for bar in bars:
                ax = bar.axes
                if ax != ax_save:
                    ax.legend().remove()
                    fig.canvas.draw_idle()
            

        fig.canvas.mpl_connect("button_press_event", onclick)

        return FigureCanvasQTAgg(fig)
