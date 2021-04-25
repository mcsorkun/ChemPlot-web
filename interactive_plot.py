# -*- coding: utf-8 -*-
"""
Functions for creating interactive HTML ChemPlot plots

@author: Dajt Mullaj
"""

from bokeh.plotting import figure, show, save
from bokeh.models import ColorBar, HoverTool
from bokeh.transform import transform, factor_cmap
from bokeh.palettes import Category10, Inferno
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models.mappers import LinearColorMapper
from chemplot import Plotter
import pandas as pd 
import mordred
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
import math
from io import BytesIO
import base64
import numpy as np
from scipy import stats


def get_plot(SMILES, target=[], title="", sim_type=None,
             dim_red_algo="t-SNE", plot_type="scatter", rem_out=False, 
             random_state=None):
    """
    Takes SMILES and target and returns bokeh plot.
    
    :param SMILES: List of the SMILES representation of the molecules to plot.
    :type SMILES: dict
    :param target: target values
    :type target: dict
    """
    
    cp = Plotter.from_smiles(SMILES, target=target, sim_type=sim_type)
    if dim_red_algo == "t-SNE":
        cp.tsne(random_state=random_state)
    elif dim_red_algo == "PCA":
        cp.pca()
    elif dim_red_algo == "UMAP":
        cp.umap(random_state=random_state)
    
    df_data = cp.df_2_components
    
    if len(cp.target) > 0:
        # Target exists
        if cp.target_type == 'C':
            df_data['target'] = list(map(str, cp.target))
        else:
            df_data['target'] = cp.target
           
    x = df_data.columns[0]
    y = df_data.columns[1]
        
    if plot_type == "scatter":
        #Scatter Plot

        source = get_source(cp, SMILES, df_data)
        # Set tools
        tools = "pan, lasso_select, wheel_zoom, hover, save, reset"
        
        if len(cp.target) == 0:
            TOOLTIPS = """
                <div>
                    <div>
                        <img
                            src="@imgs" height="210" alt="@imgs" width="210"
                            style="float: left; margin: 0px 15px 15px 0px;"
                            border="2"
                        ></img>
                    </div>
                </div>
            """
        else:
            # Target exists
            TOOLTIPS = """
                <div>
                    <div>
                        <img
                            src="@imgs" height="210" alt="@imgs" width="210"
                            style="float: left; margin: 0px 15px 15px 0px;"
                            border="2"
                        ></img>
                    </div>
                    <div>
                        <span style="font-size: 15px;">Target Value:</span>
                        <span style="font-size: 13px; color: #696;">@target</span>
                    </div>
                </div>
            """
        
        if rem_out: 
            z_scores = stats.zscore(source[[x,y]])
            abs_z_scores = np.abs(z_scores)
            filtered_entries = (abs_z_scores < 3).all(axis=1)
            source = source[filtered_entries]
        
        # Create plot
        p = figure(title=title, plot_width=700, plot_height=700, tools=tools, tooltips=TOOLTIPS)
        
        if len(cp.target) == 0:
                p.circle(x=x, y=y, size=2.5, alpha=0.8, source=source)
        else:
            # Target exists
            if cp.target_type == 'C':
                index_cmap = factor_cmap('target', Category10[10], list(set(df_data['target'])))
                p.circle(x=x, y=y, size=2.5, alpha=0.8, line_color=index_cmap, fill_color=index_cmap,
                     legend_group="target", source=source)
                p.legend.location = "top_left"
                p.legend.title = "Target"
                
            else:
                color_mapper = LinearColorMapper(Inferno[256], low=min(df_data['target']), high=max(df_data['target']))
                index_cmap = transform('target', color_mapper)
                p.circle(x=x, y=y, size=2.5, alpha=0.8, line_color=index_cmap, fill_color=index_cmap,
                     source=source)
                color_bar = ColorBar(color_mapper=color_mapper, location=(0,0))
                p.add_layout(color_bar, 'right')
            
    else:
        # Hex Plot
        tools = "pan, wheel_zoom, save, reset"

        p = figure(title=title, plot_width=700, plot_height=700, match_aspect=True,
           tools=tools)
        p.background_fill_color = '#440154'
        p.grid.visible = False
        
        if rem_out: 
            z_scores = stats.zscore(df_data[[x,y]])
            abs_z_scores = np.abs(z_scores)
            filtered_entries = (abs_z_scores < 3).all(axis=1)
            df_data = df_data[filtered_entries]
            
        max_x = max(df_data[x])
        min_x = min(df_data[x])
        max_y = max(df_data[y])
        min_y = min(df_data[y])
        
        diff_x = max_x - min_x
        diff_y = max_y - min_y
        size = max(diff_y, diff_x) / 20
        
        p.hexbin(df_data[x], df_data[y], size=size, hover_color="pink", hover_alpha=0.8)
        
        hover = HoverTool(tooltips=[("count", "@c")])
        p.add_tools(hover)

        
    p.xaxis[0].axis_label = x
    p.yaxis[0].axis_label = y
    
    p.xaxis.major_tick_line_color = None  
    p.xaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None  
    p.yaxis.minor_tick_line_color = None 
    p.xaxis.major_label_text_font_size = '0pt'  
    p.yaxis.major_label_text_font_size = '0pt' 
    
    return p

def get_source(cp, SMILES, df_data):
    """
    Takes Plotter object and returns a DataFrame with SMILES and images columns.
    
    :param target: Plotter object used for dimensionality reduction.
    :type target: chemplot.Plotter
    :param SMILES: List of the SMILES representation of the molecules to plot.
    :type SMILES: dict
    :param df_data: Dataframe with coordinates and target values.
    :type df_data: Dataframe
    """
    
    if cp.sim_type == 'tailored':
        calc_b = mordred.Calculator()  
            
        calc_b.register(mordred.AtomCount)        #16
        calc_b.register(mordred.RingCount)        #139
        calc_b.register(mordred.BondCount)        #9   
        calc_b.register(mordred.HydrogenBond)     #2  
        calc_b.register(mordred.CarbonTypes)      #10
        calc_b.register(mordred.SLogP)            #2
        calc_b.register(mordred.Constitutional)   #16    
        calc_b.register(mordred.TopoPSA)          #2
        calc_b.register(mordred.Weight)           #2
        calc_b.register(mordred.Polarizability)   #2
        calc_b.register(mordred.McGowanVolume)    #1
    
    
    smiles_list = []
    images_mol=[]
    
    # Clean SMILES
    for smiles in SMILES:
        mol=Chem.MolFromSmiles(smiles)
        if mol is not None:
            mol=Chem.AddHs(mol)
            if cp.sim_type == 'tailored':
                calculated_descriptors = calc_b(mol)
                val = True
                for i in range(len(calculated_descriptors._values)):
                    if math.isnan(calculated_descriptors._values[i]):
                        val = False
                        break
                if val:
                    smiles_list.append(smiles)
            else:
                smiles_list.append(smiles)
    
    # Create molecule images            
    for smiles in smiles_list:
        mol=Chem.MolFromSmiles(smiles)
        mol=Chem.AddHs(mol)
        
        try:
            png = Draw.MolToImage(mol)
        except:
            png = Image.open("No_image_available.png")
            
        out = BytesIO()
        png.save(out, format='png')
        png = out.getvalue()
        url = 'data:image/png;base64,' + base64.b64encode(png).decode('utf-8')
        images_mol.append(url)
    
    # Add data to dataframe
    
    df_data['SMILES'] = smiles_list        
    df_data['imgs'] = images_mol
    
    return df_data
   
def get_html(p):
    html = file_html(p, CDN)
    return html
 
   
