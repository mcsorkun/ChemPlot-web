"""
Web Application for ChemPlot using Streamlit

@author: Dajt Mullaj
"""

######################
# Import libraries
######################
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64

from chemplot import Plotter
from bokeh.embed import file_html
from bokeh.resources import CDN

######################
# Logos
######################
from PIL import Image
tab_logo = Image.open("logo_mol.png")
sidebar_logo = Image.open("chemplot_logo.png")

######################
# Coefficients
######################

# Tailored
PCA_TAIL_COEF_2 = 9.47299622e-08
PCA_TAIL_COEF_1 = 2.90093365e-03
PCA_TAIL_INTERC = 4.19205131

TSNE_TAIL_COEF_2 = 3.31581244e-07
TSNE_TAIL_COEF_1 = 6.10031290e-03
TSNE_TAIL_INTERC = 5.16853254

UMAP_TAIL_COEF_2 = 9.51843773e-08
UMAP_TAIL_COEF_1 = 3.51897483e-03
UMAP_TAIL_INTERC = 7.53709917

# Structural
PCA_STRU_COEF_2 = 1.63232808e-08
PCA_STRU_COEF_1 = 1.40949297e-03
PCA_STRU_INTERC = 0.61769033

TSNE_STRU_COEF_2 = 3.79038881e-06
TSNE_STRU_COEF_1 = 1.33859978e-03
TSNE_STRU_INTERC = 7.28995309

UMAP_STRU_COEF_2 = 2.87861709e-08
UMAP_STRU_COEF_1 = 1.89154853e-03
UMAP_STRU_INTERC = 3.65305908

#########################
# Running time functions
#########################

def get_running_time(n_samples, coef2, coef1, interc):
    return int((n_samples**2)*coef2+n_samples*coef1+interc)

def running_time(n_samples, sim_type, dim_red_algo):
    if sim_type=="tailored":
        if dim_red_algo=="t-SNE":
            return get_running_time(n_samples, TSNE_TAIL_COEF_2, TSNE_TAIL_COEF_1, TSNE_TAIL_INTERC)
        elif dim_red_algo=="PCA":
            return get_running_time(n_samples, PCA_TAIL_COEF_2, PCA_TAIL_COEF_1, PCA_TAIL_INTERC)
        else:
            return get_running_time(n_samples, UMAP_TAIL_COEF_2, UMAP_TAIL_COEF_1, UMAP_TAIL_INTERC)
    else:
        if dim_red_algo=="t-SNE":
            return get_running_time(n_samples, TSNE_STRU_COEF_2, TSNE_STRU_COEF_1, TSNE_STRU_INTERC)
        elif dim_red_algo=="PCA":
            return get_running_time(n_samples, PCA_STRU_COEF_2, PCA_STRU_COEF_1, PCA_STRU_INTERC)
        else:
            return get_running_time(n_samples, UMAP_STRU_COEF_2, UMAP_STRU_COEF_1, UMAP_STRU_INTERC)

#########################
# Session state functions
#########################
    
def update_plot():
    if dataset == 'Sample Dataset':
        update_html_plot()
    else:
        update_custom_plot()
        
def update_html_plot():
    if sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/BBBP_t_s_s.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/BBBP_t_s_h.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/BBBP_t_p_s.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/BBBP_t_p_h.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/BBBP_t_u_s.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/BBBP_t_u_h.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/BBBP_s_s_s.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/BBBP_s_s_h.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/BBBP_s_p_s.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/BBBP_s_p_h.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/BBBP_s_u_s.html", 'r', encoding='utf-8')
    elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/BBBP_s_u_h.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/AQSOLDB_t_s_s.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/AQSOLDB_t_s_h.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/AQSOLDB_t_p_s.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/AQSOLDB_t_p_h.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/AQSOLDB_t_u_s.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/AQSOLDB_t_u_h.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/AQSOLDB_s_s_s.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/AQSOLDB_s_s_h.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/AQSOLDB_s_p_s.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/AQSOLDB_s_p_h.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "scatter":
        HtmlFile = open("Sample_Plots/AQSOLDB_s_u_s.html", 'r', encoding='utf-8')
    elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "hex":
        HtmlFile = open("Sample_Plots/AQSOLDB_s_u_h.html", 'r', encoding='utf-8')
    
    st.session_state.plot_html = HtmlFile.read() 
    HtmlFile.close()
    
def update_custom_plot():
    st.session_state.new_plot = True
    
def generate_custom_plot():
    cp = Plotter.from_smiles(data_SMILES, target=data_target, sim_type=sim_type)
    if dim_red_algo=='PCA':
        cp.pca()
    elif dim_red_algo=='t-SNE':
        cp.tsne(random_state=random_state)
    elif dim_red_algo=='UMAP':
        cp.umap(random_state=random_state)
    
    st.session_state.custom_plot = cp.interactive_plot(kind=plot_type,remove_outliers=rem_out)
    st.session_state.new_plot = False
                    
######################
# Page Title
######################
st.set_page_config(page_title="ChemPlot WebApplication", page_icon=tab_logo)

st.write("""# ChemPlot: A Tool For Chemical Space Visualization""")

about_expander = st.beta_expander("About ChemPlot", expanded=False)
with about_expander:
    st.write('''
             ChemPlot is a python package that allows users to visualize the 
             chemical space of their datasets. With this web application you 
             can make use of ChemPlot algorithms to create interactive plots
             of your molecular dataset. Use the side panel to select define the
             parameters ChemPlot will use when generating a visualization. 
             
             If you are intrested in a more detailed explanation about ChemPlot
             and in the theory behind the library please visit the official 
             documentation at [Read the docs](https://chemplot.readthedocs.io/en/latest/).
             ''', unsafe_allow_html=False)
             
st.write('**Select the Dataset**') 
         
dataset = st.selectbox(
     'Choose if to upload your dataset or use a sample',
     ('Sample Dataset', 'Upload Dataset'))

######################
# Side Panel 
######################
st.sidebar.image(sidebar_logo)

st.sidebar.write('**Visualization Parameters**') 

sim_type = st.sidebar.radio(
     "Which similarity type do you want to use?",
     ('tailored', 'structural'))

dim_red_algo = st.sidebar.radio(
     "Which algorithm you want to use?",
     ('t-SNE', 'PCA', 'UMAP'))
 
plot_type = st.sidebar.radio(
     "Which plot type do you want to display?",
     ('scatter', 'hex'))

if dataset == 'Upload Dataset':
    rem_out = st.sidebar.checkbox("Do you want to remove outliers?")
    random_state = st.sidebar.number_input("Enter the random state (-1 for None)", min_value=-1, step=1)

create_viz = st.sidebar.button('Create Visualization', 
                               help='Generate visualization with the current parameters.',
                               on_click=update_plot)

######################
# Input Data
######################

if dataset == 'Sample Dataset':
    #Example Dataset
    sample = st.selectbox(
    'Choose an Sample Dataset',
     ('BBBP (Blood-Brain Barrier Penetration) [1]', 'AqSolDB (Aqueous Solubility) [2]'))
    
    if sample == "BBBP (Blood-Brain Barrier Penetration) [1]":
        data =  pd.read_csv("Sample_Plots/C_2039_BBBP_2.csv")
        sample = 'BBBP'
    else:
        data =  pd.read_csv("Sample_Plots/R_9982_AQSOLDB.csv")
        sample = 'AqSolDB'
    data_expander = st.beta_expander("Explore the Dataset", expanded=False)
    with data_expander:
        st.dataframe(data)
            
    data_plot = st.beta_expander("Visualize the Chemical Space", expanded=True)
    with data_plot:
        #Initialize plot
        if 'plot_html' not in st.session_state:
            update_html_plot()
        
        components.html(st.session_state.plot_html, width=900, height=740)
        
        b64 = base64.b64encode(st.session_state.plot_html.encode()).decode('utf-8')
        btn_download = f'<a href="data:file/html;base64,{b64}" download="interactive_plot.html"><input type="button" value="Download Plot"></a>'
        st.markdown(btn_download, unsafe_allow_html=True) 
    references = st.beta_expander("Sample Datasets Refereces", expanded=False)
    with references:
        st.write("""
                 [1] Martins, Ines Filipa, et al. [A Bayesian approach to in 
                 silico blood-brain barrier penetration modeling.] 
                 (https://pubs.acs.org/doi/abs/10.1021/ci300124c) Journal of 
                 chemical information and modeling 52.6 (2012): 1686-1697.
                 
                 [2] Sorkun, M. C., Khetan, A., & Er, S. (2019). [AqSolDB, a 
                 curated reference set of aqueous solubility and 2D descriptors 
                 for a diverse set of compounds.] 
                 (https://www.nature.com/articles/s41597-019-0151-1) Scientific 
                 data, 6(1), 1-8.
                 """)

else:
    #Uploaded Dataset
    uploaded_file = st.file_uploader("Upload a CSV file with your data")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        # Get data from dataframe
        col_SMILES, col_target = st.beta_columns(2)
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
        data_expander = st.beta_expander("Explore the Dataset", expanded=False)
        with data_expander:
            st.dataframe(data)
        
        data_plot = st.beta_expander("Visualize the Chemical Space", expanded=True)
        with data_plot:
            # Check if there is a target if the similarity type is tailored
            if len(data_target) == 0 and sim_type == 'tailored':
                st.warning('Please select a target to use tailored similarity')
            else:
                time = running_time(len(data_SMILES), sim_type, dim_red_algo)
                if random_state == -1:
                    random_state = None
                    
                #Initialize plot
                if 'new_plot' not in st.session_state:
                    update_custom_plot()
                
                if st.session_state.new_plot:
                    with st.spinner(f'Plotting your data in about {time} seconds'):  
                        generate_custom_plot()
        
                st.bokeh_chart(st.session_state.custom_plot, use_container_width=True)
                
                html = file_html(st.session_state.custom_plot, CDN)
                b64 = base64.b64encode(html.encode()).decode('utf-8')
                btn_download = f'<a href="data:file/html;base64,{b64}" download="interactive_plot.html"><input type="button" value="Download Plot as HTML"></a>'
                st.markdown(btn_download, unsafe_allow_html=True)
    
contacts = st.beta_expander("Contact", expanded=False)
with contacts:
    st.write('''
             #### Report an Issue 
             
             You are welcome to report a bug or contribuite to the web 
             application by filing an issue on [Github] (https://github.com/mcsorkun/ChemPlot-web/issues).
             
             #### Contact
             
             For any question you can contact us through email:
                 
             - [Murat Cihan Sorkun] (mailto:mcsorkun@gmail.com)
             - [Dajt Mullaj] (mailto:dajt.mullai@gmail.com)
             ''')

          


