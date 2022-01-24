"""
Web Application for ChemPlot using Streamlit

@author: Dajt Mullaj, Murat 
"""

######################
# Import libraries
######################
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import gspread
import time

from chemplot import Plotter
from bokeh.embed import file_html
from bokeh.resources import CDN
from PIL import Image
from datetime import datetime
from google.oauth2 import service_account

######################
# Logos
######################
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
# Spreadsheet functions
#########################

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
gc = gspread.authorize(credentials)
sht = gc.open_by_url(st.secrets["private_gsheets_url"])
worksheet = sht.worksheet("Logs")

# Uses st.cache to only rerun when the query changes or after 10 min.
def add_session_info(plot, name, length, gen_t, sim, dim, p_type):
    if 'id' in st.session_state:
        st.session_state.id += 1
    else:
        st.session_state.id = 0
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    worksheet.append_row([st.session_state.id, t, plot, name, length, gen_t, sim, dim, p_type])

def log_error_info(smiles, targets, error):
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    worksheet = sht.add_worksheet(title=t, rows=max(len(smiles), len(targets)), cols=3)
    if len(targets) > 0: 
        values = list(zip(smiles, targets))
        worksheet.update([['SMILES', 'targets']] + values)
        worksheet.update('C1', 'ERROR')
        worksheet.update('C2', error)
    else:
        values = list(zip(smiles))
        worksheet.update([['SMILES']] + values)
        worksheet.update('B1', 'ERROR')
        worksheet.update('B2', error)

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
             [Paper](https://chemrxiv.org/engage/chemrxiv/article-details/617180aaff3ba991f99af550).
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

if dataset == 'Upload Dataset':
    rem_out = st.sidebar.checkbox("Do you want to remove outliers?",
    help='Remove the outliers from the plot.')

    random_state = st.sidebar.number_input("Enter the random state (-1 for None)", min_value=-1, step=1,
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
    data_expander = st.expander("Explore the Dataset", expanded=False)
    with data_expander:
        st.dataframe(data)
            
    data_plot = st.expander("Visualize the Chemical Space", expanded=True)
    with data_plot:
        st.write(''' 
        Select the visualization parameters from the sidebar and click on
        **Create Visualization** to generate the desired plot.
        ''')
        #Initialize plot
        t1 = time.time()
        if 'plot_html' not in st.session_state:
            update_html_plot()
        
        components.html(st.session_state.plot_html, width=900, height=680)
        t2 = time.time()

        st.sidebar.download_button(
            label="Download Plot",
            data=st.session_state.plot_html,
            file_name='interactive_plot.html',
            mime='file/html',
            help='Download the current plot in HTML format.',
        )

        add_session_info('Sample', sample, length, int(t2 - t1), sim_type, dim_red_algo, plot_type)

    references = st.expander("Sample Datasets Refereces", expanded=False)
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
            add_session_info('Custom', 'TOO_LONG', len(data), 0, '', '', '')
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
            data_expander = st.expander("Explore the Dataset", expanded=False)
            with data_expander:
                st.dataframe(data)
            
            data_plot = st.expander('Visualize the Chemical Space', expanded=True)
            with data_plot:
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
                                    t1 = time.time()
                                    generate_custom_plot()
                                    t2 = time.time()
                                except Exception as error:
                                    add_session_info('Custom', 'ERROR_CHEMPLOT', len(data), 0, '', '', '')
                                    log_error_info(data_SMILES, data_target, str(error))
                                    st.error("""
                                    Invalid input data. 
                                    Check if you selected the correct
                                    column names for **SMILES** and **target**. If so 
                                    your data might be corrupted.
                                    """)
                                    st.session_state.pop('custom_plot', None)
                            

                    if 'custom_plot' in st.session_state:
                        st.bokeh_chart(st.session_state.custom_plot, use_container_width=True)
                        html = file_html(st.session_state.custom_plot, CDN)
                        st.sidebar.download_button(
                            label="Download Plot",
                            data=html,
                            file_name='interactive_plot.html',
                            mime='file/html',
                            help='Download the current plot in HTML format.',
                        )
                    
                        add_session_info('Custom', uploaded_file.name, len(data), 
                            int(t2 - t1), sim_type, dim_red_algo, plot_type)
    
contacts = st.expander("Contact", expanded=False)
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
             
          


