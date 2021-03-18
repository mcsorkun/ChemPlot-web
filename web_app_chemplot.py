"""
Web Application for ChemPlot using Streamlit

@author: Dajt Mullaj
"""

######################
# Import libraries
######################
import streamlit as st
import streamlit.components.v1 as components
import interactive_plot
import pandas as pd
import base64

######################
# Custom Functions
######################
            
######################
# Page Title
######################
st.set_page_config(page_title="ChemPlot WebApplication")

st.write("""# ChemPlot: A Tool For Chemical Space Visualization""")

dataset = st.selectbox(
     'Choose if to upload your dataset or use a sample',
     ('Sample Dataset', 'Upload Dataset'))

######################
# Side Panel 
######################
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

######################
# Input Data
######################

if dataset == 'Sample Dataset':
    #Example Dataset
    sample = st.selectbox(
    'Choose an Sample Dataset',
     ('BBBP', 'AqSolDB'))
    
    if sample == "BBBP":
        data =  pd.read_csv(".\Sample_Plots\\C_2039_BBBP_2.csv")
    else:
        data =  pd.read_csv(".\Sample_Plots\\R_9982_AQSOLDB.csv")
    data_expander = st.beta_expander("Explore the Dataset", expanded=False)
    with data_expander:
        st.dataframe(data)
            
    data_plot = st.beta_expander("Visualize the Chemical Space", expanded=True)
    with data_plot:
        if sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\BBBP_t_s_s.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\BBBP_t_s_h.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\BBBP_t_p_s.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\BBBP_t_p_h.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\BBBP_t_u_s.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\BBBP_t_u_h.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\BBBP_s_s_s.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\BBBP_s_s_h.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\BBBP_s_p_s.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\BBBP_s_p_h.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\BBBP_s_u_s.html", 'r', encoding='utf-8')
        elif sample == "BBBP" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\BBBP_s_u_h.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\AQSOLDB_t_s_s.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "t-SNE" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\AQSOLDB_t_s_h.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\AQSOLDB_t_p_s.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "PCA" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\AQSOLDB_t_p_h.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\AQSOLDB_t_u_s.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "tailored" and dim_red_algo == "UMAP" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\AQSOLDB_t_u_h.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\AQSOLDB_s_s_s.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "t-SNE" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\AQSOLDB_s_s_h.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\AQSOLDB_s_p_s.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "PCA" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\AQSOLDB_s_p_h.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "scatter":
            HtmlFile = open("Sample_Plots\\AQSOLDB_s_u_s.html", 'r', encoding='utf-8')
        elif sample == "AqSolDB" and sim_type == "structural" and dim_red_algo == "UMAP" and plot_type == "hex":
            HtmlFile = open("Sample_Plots\\AQSOLDB_s_u_h.html", 'r', encoding='utf-8')
        
        plot_html = HtmlFile.read() 
        components.html(plot_html, width=900, height=740)
        
        b64 = base64.b64encode(plot_html.encode()).decode('utf-8')
        btn_download = f'<a href="data:file/html;base64,{b64}" download="interactive_plot.html"><input type="button" value="Download Plot"></a>'
        st.markdown(btn_download, unsafe_allow_html=True)
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
            data_target=data["target"] 
        data_expander = st.beta_expander("Explore the Dataset", expanded=False)
        with data_expander:
            st.dataframe(data)
        
        data_plot = st.beta_expander("Visualize the Chemical Space", expanded=True)
        with data_plot:
            run = st.button('Create Visualization')
            if run:
                with st.spinner('Plotting your data...'):
                    
                    if random_state == -1:
                        random_state = None
                    else:
                        random_state = random_state
            
                    p = interactive_plot.get_plot(data_SMILES, target=data_target, sim_type=sim_type,
                                              dim_red_algo=dim_red_algo, plot_type=plot_type,
                                              rem_out=rem_out, random_state=random_state)
                    st.bokeh_chart(p, use_container_width=True)
                    
                    html = interactive_plot.get_html(p)
                    b64 = base64.b64encode(html.encode()).decode('utf-8')
                    btn_download = f'<a href="data:file/html;base64,{b64}" download="interactive_plot.html"><input type="button" value="Download Plot as HTML"></a>'
                    st.markdown(btn_download, unsafe_allow_html=True)
                    
                    run = False
          


