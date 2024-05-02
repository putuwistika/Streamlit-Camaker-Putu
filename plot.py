import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Plotter:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(self.data_path)
        self.process_data()

    def process_data(self):
        self.data['IPK_categories'] = pd.cut(
            self.data['IP'],
            bins=[0, 2.50, 3.00, 3.50, 4.00],
            labels=['<2.50', '2.50-3.00', '3.00-3.50', '3.50-4.00'],
            include_lowest=True
        )
        self.ipk_category_counts = self.data['IPK_categories'].value_counts().reindex(['<2.50', '2.50-3.00', '3.00-3.50', '3.50-4.00'])

    def create_ipk_plot(self):
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Distribusi IPK", "Boxplot IPK"),
            specs=[[{"type": "bar"}, {"type": "box"}]],
            column_widths=[0.7, 0.3],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Bar(
                y=self.ipk_category_counts.index,
                x=self.ipk_category_counts.values,
                marker_color='#c84781',
                orientation='h',
                name='IPK'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Box(
                y=self.data['IP'],
                boxpoints='all',
                jitter=0.3,
                marker_color='#c84781',
                name='IPK'
            ),
            row=1, col=2
        )

        fig.update_layout(
            title_text="Analisis Distribusi IPK",
            showlegend=False,
            height=400,
            width=900
        )

        fig.update_xaxes(title_text="Jumlah", row=1, col=1)
        fig.update_yaxes(title_text="Kategori IPK", row=1, col=1)

        return fig

    def plot_ip_per_prodi(self):
        prodi_grouped = self.data.groupby('Prodi')['IP'].agg(['mean', 'size']).reset_index()
        prodi_grouped_sorted = prodi_grouped.sort_values(by='mean', ascending=True)
        prodi_grouped_sorted['y_labels'] = prodi_grouped_sorted.apply(lambda x: f"{x['Prodi']} [{x['size']}]", axis=1)

        # Calculate the height based on the number of data points
        num_bars = len(prodi_grouped_sorted)
        height_per_bar = 75  # You can adjust this value based on your visual preference
        total_height = num_bars * height_per_bar

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=prodi_grouped_sorted['y_labels'],
                x=prodi_grouped_sorted['mean'],
                orientation='h',
                text=prodi_grouped_sorted['mean'].round(2),
                textposition='inside',
                marker_color='#5661d2'
            )
        )

        fig.update_layout(
            title='Indeks Prestasi per Program Studi',
            xaxis_title='Rata-Rata IP',
            yaxis_title='Program Studi [Jumlah Data]',
            height=total_height,  # Use the dynamic height based on the number of bars
            xaxis=dict(range=[prodi_grouped_sorted['mean'].min() - 0.1, prodi_grouped_sorted['mean'].max() + 0.1])
        )

        return fig


    def plot_job_distribution(self):
        job_counts = self.data['Pekerjaan Utama'].value_counts().reset_index()
        job_counts.columns = ['Pekerjaan Utama', 'Count']
        fig = go.Figure(data=[go.Pie(
            labels=job_counts['Pekerjaan Utama'],
            values=job_counts['Count'],
            textinfo='value+percent',
            insidetextorientation='radial'
        )])
        fig.update_layout(title='Distribusi Pekerjaan Utama')
        return fig

    def plot_job_distribution_per_prodi(self):
        pivot_df = self.data.pivot_table(index='Prodi', columns='Pekerjaan Utama', aggfunc='size', fill_value=0)
        percent_df = pivot_df.div(pivot_df.sum(axis=1), axis=0).multiply(100)
        job_categories = self.data['Pekerjaan Utama'].unique()
        labels_df = np.round(percent_df, 1).astype(str) + '%'
        prodi_counts = pivot_df.sum(axis=1)
        sorted_prodi_counts = prodi_counts.sort_values(ascending=True)
        sorted_percent_df = percent_df.loc[sorted_prodi_counts.index]
        sorted_labels_df = labels_df.loc[sorted_prodi_counts.index]
        sorted_y_labels = [f'{index} [{count}]' for index, count in sorted_prodi_counts.items()]

        job_colors = {'Bekerja': '#5661d2', 'Bekerja dan wiraswasta': '#ffcd46', 'Wirausaha': '#f6abbf'}
        color_list = list(job_colors.values())

        fig = go.Figure()
        for idx, job in enumerate(job_categories):
            color = job_colors.get(job, color_list[idx % len(color_list)])
            fig.add_trace(go.Bar(
                name=job,
                y=sorted_y_labels,
                x=sorted_percent_df[job],
                text=sorted_labels_df[job],
                textposition='inside',
                orientation='h',
                marker_color=color,
                hoverinfo='name+y+x'
            ))
        fig.update_layout(
            barmode='stack',
            title='Pekerjaan Utama per Prodi',
            yaxis_title='Prodi [Jumlah Data]',
            xaxis=dict(title='Persentase (%)', tickformat='.1f', range=[0, 100]),
            height=800,
            font=dict(
                family="Courier New, monospace",
                size=15
            )
        )
        return fig
    
    def plot_ip_per_prodi_filtered(self, faculty=None):
        if faculty:
            filtered_data = self.data[self.data['Fakultas'] == faculty]
        else:
            filtered_data = self.data
        
        prodi_grouped = filtered_data.groupby('Prodi')['IP'].agg(['mean', 'size']).reset_index()
        prodi_grouped_sorted = prodi_grouped.sort_values(by='mean', ascending=True)
        prodi_grouped_sorted['y_labels'] = prodi_grouped_sorted.apply(lambda x: f"{x['Prodi']} [{x['size']}]", axis=1)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=prodi_grouped_sorted['y_labels'],
                x=prodi_grouped_sorted['mean'],
                orientation='h',
                marker_color='#5661d2'
            )
        )

        fig.update_layout(
            title='Indeks Prestasi per Program Studi',
            xaxis_title='Rata-Rata IP',
            yaxis_title='Program Studi [Jumlah Data]',
            height=800
        )
        return fig

    def plot_job_distribution_per_prodi_filtered(self, faculty=None):
        if faculty:
            filtered_data = self.data[self.data['Fakultas'] == faculty]
        else:
            filtered_data = self.data
        
        pivot_df = filtered_data.pivot_table(index='Prodi', columns='Pekerjaan Utama', aggfunc='size', fill_value=0)
        percent_df = pivot_df.div(pivot_df.sum(axis=1), axis=0).multiply(100)

        fig = go.Figure()
        for job in percent_df.columns:
            fig.add_trace(go.Bar(
                name=job,
                y=percent_df.index,
                x=percent_df[job],
                orientation='h'
            ))
        
        fig.update_layout(
            barmode='stack',
            title='Pekerjaan Utama per Prodi',
            yaxis_title='Program Studi [Jumlah Data]',
            xaxis_title='Persentase (%)',
            height=800
        )
        return fig

# if __name__ == "__main__":
#     # plotter = Plotter('Data.csv')
#     # plotter.process_data()
#     # ipk_fig = plotter.create_ipk_plot()
#     # ipk_fig.show()
#     # prodi_fig = plotter.plot_ip_per_prodi()
#     # prodi_fig.show()
#     # job_dist_fig = plotter.plot_job_distribution()
#     # job_dist_fig.show()
#     # job_per_prodi_fig = plotter.plot_job_distribution_per_prodi()
#     # job_per_prodi_fig.show()
