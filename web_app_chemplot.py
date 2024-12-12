"""
Web Application for ChemPlot using Streamlit

@author: Dajt, Murat, Jackson
"""

######################
# Import libraries
######################
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from chemplot import Plotter
from bokeh.embed import file_html
from bokeh.resources import CDN

from constants import *

######################
# Page Config
######################
st.set_page_config(page_title="ChemPlot WebApplication", layout="wide", page_icon=TAB_LOGO)

#########################
# Running time functions
#########################
@st.cache_data
def compute_runtime_coefficients(sim_type, dim_red_algo):
    if sim_type == "tailored":
        if dim_red_algo == "t-SNE":
            return TSNE_TAIL_COEF_2, TSNE_TAIL_COEF_1, TSNE_TAIL_INTERC
        elif dim_red_algo=="PCA":
            return PCA_TAIL_COEF_2, PCA_TAIL_COEF_1, PCA_TAIL_INTERC
        else:
            return UMAP_TAIL_COEF_2, UMAP_TAIL_COEF_1, UMAP_TAIL_INTERC
    else:
        if dim_red_algo == "t-SNE":
            return TSNE_STRU_COEF_2, TSNE_STRU_COEF_1, TSNE_STRU_INTERC
        elif dim_red_algo=="PCA":
            return PCA_STRU_COEF_2, PCA_STRU_COEF_1, PCA_STRU_INTERC
        else:
            return UMAP_STRU_COEF_2, UMAP_STRU_COEF_1, UMAP_STRU_INTERC

def running_time(n_samples, sim_type, dim_red_algo):
    coef2, coef1, interc = compute_runtime_coefficients(sim_type, dim_red_algo)
    return int((n_samples**2) * coef2 + n_samples * coef1 + interc)

#########################
# Session state functions
#########################
    
def update_plot():
    if dataset == 'Sample Dataset':
        update_html_plot()
    else:
        update_custom_plot()

def update_html_plot():
    file_path = PLOT_MAP.get((sample, sim_type, dim_red_algo, plot_type))
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as HtmlFile:
            st.session_state.plot_html = HtmlFile.read()
    else:
        st.warning("No matching plot found.")
    
def update_custom_plot():
    st.session_state.new_plot = True

def generate_custom_plot():
    cp = Plotter.from_smiles(data_SMILES, target=data_target, sim_type=sim_type)
    if dim_red_algo=='PCA':
        df_2_components = cp.pca()
    elif dim_red_algo=='t-SNE':
        df_2_components = cp.tsne(random_state=random_state)
    elif dim_red_algo=='UMAP':
        df_2_components = cp.umap(random_state=random_state)
    
    if clusters > 1:
        df_2_components = cp.cluster(n_clusters=clusters)

    st.session_state.custom_plot = cp.interactive_plot(kind=plot_type,remove_outliers=rem_out,clusters=True)
    st.session_state.df_2_components = df_2_components
    st.session_state.new_plot = False

#########################
# Cached download files
#########################

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

######################
# Page Title
######################
st.write("""# ChemPlot: A Tool For Chemical Space Visualization""")

about_expander = st.expander("About ChemPlot", expanded=True)
with about_expander:
    st.write('''
             ChemPlot is a python package that allows users to visualize the 
             chemical space of their datasets. With this web application you 
             can make use of ChemPlot algorithms to create interactive plots
             of your molecular dataset. Use the side panel to select define the
             parameters ChemPlot will use when generating a visualization. 
             
             If you are intrested in a more detailed explanation about ChemPlot
             please visit the official library's documentation at 
             [Read the docs](https://chemplot.readthedocs.io/en/latest/).

             You can read about the theoretical background on ChemPlot in our 
             paper. You can find our paper at the following link: 
             [Paper](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/cmtd.202200005).
             ''', unsafe_allow_html=False)
             
st.subheader('Select the Dataset') 
         
dataset = st.selectbox(
     'Choose if to upload your dataset or use a sample',
     ('Sample Dataset', 'Upload Dataset'))

######################
# Side Panel 
######################
st.sidebar.image(SIDEBAR_LOGO)

st.sidebar.write('**Visualization Parameters**') 

sim_type = st.sidebar.radio(
     "Which similarity type do you want to use?",
     ('tailored', 'structural'),
     help='Use tailored when you have a target value. Use structural to plot your molecules based on structure only.')

dim_red_algo = st.sidebar.radio(
     "Which algorithm you want to use?",
     ('t-SNE', 'PCA', 'UMAP'),
     help='t-SNE and UMAP are non linear resulting in better clusters. PCA is linear resulting in a more global view.')
 
plot_type = st.sidebar.radio(
     "Which plot type do you want to display?",
     ('scatter', 'hex'),
     help='Visualize a scatter plot or an hexagonal plot.')

with st.sidebar.expander("Advanced Options", expanded=False):
    if dataset == 'Upload Dataset':
        rem_out = st.checkbox("Do you want to remove outliers?",
        help='Remove the outliers from the plot.')

        clusters = st.number_input("Enter the number of clusters you want to separate your data in", min_value=1, step=1,
        help='You can see your dataset separated in clusters by clicking on the "cluster" tab on the top of the visualization.')

        random_state = st.number_input("Enter the random state (-1 for None)", min_value=-1, step=1,
        help='Add a random state greater or equal to 0 for reproducible results.')
        
create_viz = st.sidebar.button('Create Visualization', 
                help='Generate visualization with the current parameters.',
                on_click=update_plot)

######################
# Input Data
######################

if dataset == 'Sample Dataset':
    st.session_state.new_plot = False
    #Example Dataset
    sample = st.selectbox(
    'Choose an Sample Dataset',
     ('BBBP (Blood-Brain Barrier Penetration) [1]', 'AqSolDB (Aqueous Solubility) [2]'))
    
    if sample == "BBBP (Blood-Brain Barrier Penetration) [1]":
        data =  pd.read_csv("Sample_Plots/C_2039_BBBP_2.csv")
        length = 2039
        sample = 'BBBP'
    else:
        data =  pd.read_csv("Sample_Plots/R_9982_AQSOLDB.csv")
        length = 9982
        sample = 'AqSolDB'
    
    plot_col, data_col = st.columns([3, 2], border=True)
    
    with plot_col:
        st.subheader("ChemPlot Visualization")
        st.write(''' 
        Select the visualization parameters from the sidebar and click on
        **Create Visualization** to generate the desired plot.
        ''')
        #Initialize plot
        if 'plot_html' not in st.session_state:
            update_html_plot()
        
        components.html(st.session_state.plot_html,  height=680, scrolling=True)

        st.sidebar.download_button(
            label="Download Plot",
            data=st.session_state.plot_html,
            file_name='interactive_plot.html',
            mime='file/html',
            help='Download the current plot in HTML format.',
        )
    
    with data_col:
        st.subheader("Explore the Dataset")
        st.write(''' 
            Datasets must contain a SMILES column which ChemPlot can process.
        ''')
        st.dataframe(data, height=680, use_container_width=True)

    references = st.expander("Sample Datasets Refereces", expanded=False)
    with references:
        st.write("""
                 [1] Martins, Ines Filipa, et al. [A Bayesian approach to in 
                 silico blood-brain barrier penetration modeling.](https://pubs.acs.org/doi/abs/10.1021/ci300124c)
                 Journal of chemical information and modeling 52.6 (2012): 1686-1697.
                 
                 [2] Sorkun, M. C., Khetan, A., & Er, S. (2019). [AqSolDB, a 
                 curated reference set of aqueous solubility and 2D descriptors 
                 for a diverse set of compounds.](https://www.nature.com/articles/s41597-019-0151-1) 
                 Scientific data, 6(1), 1-8.
                 """)

else:
    #Uploaded Dataset
    uploaded_file = st.file_uploader("Upload a CSV file with your data", type='csv')
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, on_bad_lines='skip')
        # Check if dataset is too big
        if len(data) > 5000:
            st.error("""
                     Currently the web app does not support datasets with more
                     than 5000 instances. For bigger datasets please install and 
                     use the [ChemPlot Python library.]
                     (https://github.com/mcsorkun/ChemPlot)
                     """)
        else:
            # Get data from dataframe
            col_SMILES, col_target = st.columns(2)
            columns_values = ['There is no target'] + data.columns.tolist()
            with col_SMILES:
                column_SMILES = st.selectbox(
                 'Which one is the SMILES column?',
                 (data.columns))
            with col_target:
                column_target = st.selectbox(
                 'Which one is the target column?',
                 (columns_values))
            data_SMILES=data[column_SMILES] 
            if column_target == 'There is no target':
                data_target=[]
            else:
                data_target=data[column_target] 
            
            plot_col, data_col = st.columns([3, 2], border=True)
            
            with plot_col:
                st.subheader("ChemPlot Visualization")
                st.write(''' 
                Select the visualization parameters from the sidebar and click on
                **Create Visualization** to generate the desired plot.
                ''')
                # Check if there is a target if the similarity type is tailored
                if len(data_target) == 0 and sim_type == 'tailored':
                    st.warning('Please select a target to use tailored similarity')
                else:
                    run_time = running_time(len(data_SMILES), sim_type, dim_red_algo)
                    if random_state == -1:
                        random_state = None

                    if 'new_plot' in st.session_state:
                        if st.session_state.new_plot:
                            with st.spinner(f'Plotting your data in about {run_time} seconds'):  
                                try:
                                    generate_custom_plot()
                                except Exception as error:
                                    st.error("""
                                    Invalid input data. 
                                    Check if you selected the correct
                                    column names for **SMILES** and **target**. If so 
                                    your data might be corrupted.
                                    """)
                                    st.session_state.pop('custom_plot', None)
                            

                    if 'custom_plot' in st.session_state:
                        html = file_html(st.session_state.custom_plot, CDN)
                        components.html(html, height=680, scrolling=True)
                        st.sidebar.download_button(
                            label="Download Plot",
                            data=html,
                            file_name='interactive_plot.html',
                            mime='file/html',
                            help='Download the current plot in HTML format.',
                        )
                        csv = convert_df(st.session_state.df_2_components)
                        st.sidebar.download_button(
                            label="Download Reduced Dataset",
                            data=csv,
                            file_name='df_2_components.csv',
                            mime='text/csv',
                            help='Download the current reduced dataset in CSV format.',
                        )

            with data_col:
                st.subheader("Explore the Dataset")
                st.write(''' 
                    Datasets must contain a SMILES column which ChemPlot can process.
                ''')
                st.dataframe(data, height=680, use_container_width=True)
    
contacts = st.expander("Contact", expanded=False)
with contacts:
    st.write('''
             #### Report an Issue 
             
             You are welcome to report a bug or contribuite to the web 
             application by filing an issue on [Github](https://github.com/mcsorkun/ChemPlot-web/issues).
             
             #### Contact
             
             For any question you can contact us through email:
                 
             - [Murat Cihan Sorkun](mailto:mcsorkun@gmail.com)
             - [Dajt Mullaj](mailto:dajt.mullai@gmail.com)
             - [Jackson Warner Burns](mailto:jwburns@mit.edu)
             ''')
             
          
