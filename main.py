import streamlit as st
import pandas as pd
from plot import Plotter

# Load the data
data_path = '/Users/putuwistika/Documents/0.InternshipCareerCenterITB/1.STREAMLIT/data.csv'
data = pd.read_csv(data_path)

plotter = Plotter(data_path)
plotter.process_data()

# Layout the navigational controls
st.title('Tracer Study ITB')

# Year navigation
year_to_filter = st.slider('Pilih Tahun Survey', min_value=int(data['Tahun Survey'].min()), max_value=int(data['Tahun Survey'].max()), value=int(data['Tahun Survey'].min()))

# Faculty navigation
all_faculties = ['All'] + sorted(data['Fakultas'].unique().tolist())
selected_faculty = st.selectbox('Pilih Fakultas', all_faculties)

# Based on selected faculty, filter the available programs
if selected_faculty == 'All':
    filtered_prodi = ['All'] + sorted(data['Prodi'].unique().tolist())
else:
    filtered_prodi = ['All'] + sorted(data[data['Fakultas'] == selected_faculty]['Prodi'].unique().tolist())

selected_prodi = st.selectbox('Pilih Program Studi', filtered_prodi)

# Apply filters to the data based on user selections
filtered_data = data[data['Tahun Survey'] == year_to_filter]
if selected_faculty != 'All':
    filtered_data = filtered_data[filtered_data['Fakultas'] == selected_faculty]
if selected_prodi != 'All':
    filtered_data = filtered_data[filtered_data['Prodi'] == selected_prodi]

# Update the data within Plotter and generate plots
plotter.data = filtered_data
ipk_fig = plotter.create_ipk_plot()
st.plotly_chart(ipk_fig, use_container_width=True)




# Display plots based on the filters
if selected_prodi == 'All':
    prodi_fig = plotter.plot_ip_per_prodi()
    st.plotly_chart(prodi_fig, use_container_width=True)
    job_dist_fig = plotter.plot_job_distribution()
    st.plotly_chart(job_dist_fig, use_container_width=True)
    job_per_prodi_fig = plotter.plot_job_distribution_per_prodi()
    st.plotly_chart(job_per_prodi_fig, use_container_width=False)
    if selected_faculty != 'All':
        ip_per_prodi_fig = plotter.plot_ip_per_prodi_filtered(selected_faculty)
        st.plotly_chart(ip_per_prodi_fig, use_container_width=True)
        job_per_prodi_fig = plotter.plot_job_distribution_per_prodi_filtered(selected_faculty)
        st.plotly_chart(job_per_prodi_fig, use_container_width=True)



