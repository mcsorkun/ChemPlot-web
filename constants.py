from PIL import Image

TAB_LOGO = Image.open("logo_mol.png")
SIDEBAR_LOGO = Image.open("chemplot_logo.png")

PCA_TAIL_COEF_2 = 9.47299622e-08
PCA_TAIL_COEF_1 = 2.90093365e-03
PCA_TAIL_INTERC = 4.19205131
TSNE_TAIL_COEF_2 = 3.31581244e-07
TSNE_TAIL_COEF_1 = 6.10031290e-03
TSNE_TAIL_INTERC = 5.16853254
UMAP_TAIL_COEF_2 = 9.51843773e-08
UMAP_TAIL_COEF_1 = 3.51897483e-03
UMAP_TAIL_INTERC = 7.53709917

PCA_STRU_COEF_2 = 1.63232808e-08
PCA_STRU_COEF_1 = 1.40949297e-03
PCA_STRU_INTERC = 0.61769033
TSNE_STRU_COEF_2 = 3.79038881e-06
TSNE_STRU_COEF_1 = 1.33859978e-03
TSNE_STRU_INTERC = 7.28995309
UMAP_STRU_COEF_2 = 2.87861709e-08
UMAP_STRU_COEF_1 = 1.89154853e-03
UMAP_STRU_INTERC = 3.65305908

PLOT_MAP = {
    # BBBP Tailored
    ("BBBP", "tailored", "t-SNE", "scatter"): "Sample_Plots/BBBP_t_s_s.html",
    ("BBBP", "tailored", "t-SNE", "hex"): "Sample_Plots/BBBP_t_s_h.html",
    ("BBBP", "tailored", "PCA", "scatter"): "Sample_Plots/BBBP_t_p_s.html",
    ("BBBP", "tailored", "PCA", "hex"): "Sample_Plots/BBBP_t_p_h.html",
    ("BBBP", "tailored", "UMAP", "scatter"): "Sample_Plots/BBBP_t_u_s.html",
    ("BBBP", "tailored", "UMAP", "hex"): "Sample_Plots/BBBP_t_u_h.html",
    
    # BBBP Structural
    ("BBBP", "structural", "t-SNE", "scatter"): "Sample_Plots/BBBP_s_s_s.html",
    ("BBBP", "structural", "t-SNE", "hex"): "Sample_Plots/BBBP_s_s_h.html",
    ("BBBP", "structural", "PCA", "scatter"): "Sample_Plots/BBBP_s_p_s.html",
    ("BBBP", "structural", "PCA", "hex"): "Sample_Plots/BBBP_s_p_h.html",
    ("BBBP", "structural", "UMAP", "scatter"): "Sample_Plots/BBBP_s_u_s.html",
    ("BBBP", "structural", "UMAP", "hex"): "Sample_Plots/BBBP_s_u_h.html",
    
    # AqSolDB Tailored
    ("AqSolDB", "tailored", "t-SNE", "scatter"): "Sample_Plots/AQSOLDB_t_s_s.html",
    ("AqSolDB", "tailored", "t-SNE", "hex"): "Sample_Plots/AQSOLDB_t_s_h.html",
    ("AqSolDB", "tailored", "PCA", "scatter"): "Sample_Plots/AQSOLDB_t_p_s.html",
    ("AqSolDB", "tailored", "PCA", "hex"): "Sample_Plots/AQSOLDB_t_p_h.html",
    ("AqSolDB", "tailored", "UMAP", "scatter"): "Sample_Plots/AQSOLDB_t_u_s.html",
    ("AqSolDB", "tailored", "UMAP", "hex"): "Sample_Plots/AQSOLDB_t_u_h.html",
    
    # AqSolDB Structural
    ("AqSolDB", "structural", "t-SNE", "scatter"): "Sample_Plots/AQSOLDB_s_s_s.html",
    ("AqSolDB", "structural", "t-SNE", "hex"): "Sample_Plots/AQSOLDB_s_s_h.html",
    ("AqSolDB", "structural", "PCA", "scatter"): "Sample_Plots/AQSOLDB_s_p_s.html",
    ("AqSolDB", "structural", "PCA", "hex"): "Sample_Plots/AQSOLDB_s_p_h.html",
    ("AqSolDB", "structural", "UMAP", "scatter"): "Sample_Plots/AQSOLDB_s_u_s.html",
    ("AqSolDB", "structural", "UMAP", "hex"): "Sample_Plots/AQSOLDB_s_u_h.html",
}
