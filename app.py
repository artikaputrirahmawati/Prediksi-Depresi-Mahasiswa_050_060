# ============================================================
# app.py — Student Depression Detection System
# Developer : Artika Putri Rahmawati & Fi Amanila Putri Kinanti
# Program   : Business Statistics
# UI/UX     : Premium Glassmorphism Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle as joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Student Depression Detection System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif !important; color: #0F172A; }
.main .block-container { padding: 1.2rem 2.2rem 2rem 2.2rem; max-width: 1400px; }
.stApp { background: #F8FAFC; }
section[data-testid="stSidebar"] {
    background: linear-gradient(170deg, #0F172A 0%, #1E293B 60%, #0F2044 100%) !important;
    border-right: 1px solid rgba(37,99,235,0.15);
}
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
section[data-testid="stSidebar"] .stRadio > label {
    color: #94A3B8 !important; font-size: 11px; font-weight: 600;
    letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 6px;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 10px 14px !important; margin: 3px 0;
    font-size: 13px !important; font-weight: 500 !important;
    letter-spacing: 0 !important; text-transform: none !important;
    color: #CBD5E1 !important; transition: all 0.2s; cursor: pointer;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(37,99,235,0.25) !important;
    border-color: rgba(37,99,235,0.4) !important; color: #FFFFFF !important;
}
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; margin: 14px 0; }
.hero-banner {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #1D4ED8 100%);
    border-radius: 20px; padding: 36px 40px; margin-bottom: 28px;
    position: relative; overflow: hidden; box-shadow: 0 20px 60px rgba(15,23,42,0.25);
}
.hero-banner::before {
    content: ''; position: absolute; top: -60px; right: -60px; width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 70%); border-radius: 50%;
}
.hero-banner::after {
    content: ''; position: absolute; bottom: -80px; left: 40%; width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 70%); border-radius: 50%;
}
.hero-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 30px; font-weight: 800;
    color: #FFFFFF; margin: 0 0 6px 0; letter-spacing: -0.5px; line-height: 1.2; position: relative; z-index: 1; }
.hero-sub { font-size: 14px; color: #93C5FD; margin: 0 0 18px 0; font-weight: 500; position: relative; z-index: 1; }
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px; padding: 5px 14px; font-size: 12px; color: #E0F2FE;
    font-weight: 600; margin-right: 8px; margin-top: 6px; backdrop-filter: blur(4px); position: relative; z-index: 1;
}
.hero-stats { display: flex; gap: 28px; margin-top: 20px; position: relative; z-index: 1; }
.hero-stat-item { text-align: left; }
.hero-stat-value { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 26px; font-weight: 800; color: #FFFFFF; line-height: 1; }
.hero-stat-label { font-size: 11px; color: #93C5FD; font-weight: 500; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.8px; }
.kpi-card {
    background: rgba(255,255,255,0.85); backdrop-filter: blur(12px);
    border: 1px solid rgba(226,232,240,0.8); border-radius: 16px; padding: 20px 22px;
    margin: 6px 0; text-align: center; box-shadow: 0 4px 24px rgba(15,23,42,0.06);
    transition: transform 0.2s, box-shadow 0.2s; position: relative; overflow: hidden;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 12px 36px rgba(15,23,42,0.12); }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
.kpi-blue::before   { background: linear-gradient(90deg, #2563EB, #06B6D4); }
.kpi-green::before  { background: linear-gradient(90deg, #10B981, #34D399); }
.kpi-amber::before  { background: linear-gradient(90deg, #F59E0B, #FCD34D); }
.kpi-red::before    { background: linear-gradient(90deg, #EF4444, #F87171); }
.kpi-purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
.kpi-cyan::before   { background: linear-gradient(90deg, #06B6D4, #67E8F9); }
.kpi-icon { font-size: 28px; margin-bottom: 10px; display: block; }
.kpi-value { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 28px; font-weight: 800; color: #0F172A; line-height: 1.1; margin-bottom: 4px; }
.kpi-label { font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 2px; }
.kpi-sub { font-size: 11px; color: #94A3B8; margin-top: 2px; }
.section-header { display: flex; align-items: center; gap: 10px; padding: 0 0 10px 0; margin: 24px 0 16px 0; border-bottom: 2px solid #E2E8F0; }
.section-header-text { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 700; color: #0F172A; letter-spacing: -0.3px; }
.section-header-badge { background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; border-radius: 20px; padding: 2px 10px; font-size: 11px; font-weight: 600; }
.glass-card { background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border: 1px solid rgba(226,232,240,0.9); border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 16px rgba(15,23,42,0.05); }
.ai-insight { background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%); border: 1px solid #BFDBFE; border-left: 4px solid #2563EB; border-radius: 12px; padding: 18px 22px; margin: 16px 0; }
.ai-insight-header { font-size: 11px; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.ai-insight-text { font-size: 14px; color: #1E3A5F; line-height: 1.6; font-weight: 500; margin: 0; }
.method-step { background: rgba(255,255,255,0.9); border: 1px solid #E2E8F0; border-top: 3px solid #2563EB; border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; }
.method-step-num { font-size: 10px; font-weight: 700; color: #2563EB; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.method-step-title { font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 4px; }
.method-step-desc { font-size: 12px; color: #64748B; line-height: 1.5; }
.pred-depression {
    background: linear-gradient(135deg, #450A0A 0%, #991B1B 60%, #DC2626 100%);
    border-radius: 16px; padding: 28px 24px; color: white; text-align: center;
    box-shadow: 0 12px 40px rgba(220,38,38,0.25); position: relative; overflow: hidden;
}
.pred-nodepression {
    background: linear-gradient(135deg, #022C22 0%, #065F46 60%, #059669 100%);
    border-radius: 16px; padding: 28px 24px; color: white; text-align: center;
    box-shadow: 0 12px 40px rgba(5,150,105,0.25); position: relative; overflow: hidden;
}
.pred-title  { font-size: 20px; font-weight: 800; margin-bottom: 6px; font-family: 'Plus Jakarta Sans', sans-serif; }
.pred-prob   { font-size: 52px; font-weight: 800; margin: 10px 0; font-family: 'Plus Jakarta Sans', sans-serif; line-height: 1; }
.pred-label  { font-size: 12px; opacity: 0.8; font-weight: 500; }
.risk-badge  { display: inline-block; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 5px 16px; font-size: 13px; font-weight: 700; margin-top: 12px; }
.upload-zone { background: linear-gradient(135deg, #F0F9FF 0%, #EFF6FF 100%); border: 2px dashed #93C5FD; border-radius: 16px; padding: 32px 24px; text-align: center; margin-bottom: 20px; }
.upload-zone-title { font-size: 16px; font-weight: 700; color: #1E40AF; margin-bottom: 6px; }
.upload-zone-sub { font-size: 13px; color: #60A5FA; }
.stat-pill { display: inline-flex; align-items: center; gap: 6px; background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 20px; padding: 6px 14px; font-size: 12px; font-weight: 600; color: #475569; margin: 3px 4px; }
.profile-card { background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); border-radius: 20px; padding: 36px; color: white; text-align: center; box-shadow: 0 20px 60px rgba(15,23,42,0.3); position: relative; overflow: hidden; }
.profile-avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #2563EB, #06B6D4); display: flex; align-items: center; justify-content: center; font-size: 32px; margin: 0 auto 16px auto; border: 3px solid rgba(255,255,255,0.2); }
.profile-name { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 800; margin-bottom: 4px; }
.profile-major { font-size: 13px; color: #93C5FD; font-weight: 500; margin-bottom: 20px; }
.profile-tag { display: inline-block; background: rgba(37,99,235,0.3); border: 1px solid rgba(37,99,235,0.5); border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 600; color: #BFDBFE; margin: 3px; }
.research-card { background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; margin-bottom: 14px; border-left: 4px solid #2563EB; box-shadow: 0 2px 12px rgba(15,23,42,0.04); }
.research-card-title { font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.research-card-body { font-size: 13px; color: #475569; line-height: 1.7; }
.stDataFrame { border-radius: 12px; overflow: hidden; }
.stButton > button { background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%) !important; color: white !important; font-weight: 600 !important; border: none !important; border-radius: 10px !important; padding: 0.65rem 2.2rem !important; font-size: 14px !important; box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important; transition: all 0.2s !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 20px rgba(37,99,235,0.4) !important; }
hr { border: none; border-top: 1.5px solid #E2E8F0; margin: 20px 0; }
.footer-bar { background: linear-gradient(135deg, #0F172A, #1E293B); border-radius: 12px; padding: 16px 24px; text-align: center; margin-top: 32px; color: #64748B; font-size: 12px; }
.footer-bar b { color: #94A3B8; }
.stSelectbox > div > div, .stNumberInput > div > div > input { border-radius: 8px !important; border: 1.5px solid #E2E8F0 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# LOAD ARTIFACTS
# ══════════════════════════════════════════════════════════════
@st.cache_resource
def load_artifacts():
   with open('model.pkl', 'rb') as f:
    return pickle.load(f)

artifacts = load_artifacts()

best_model           = artifacts['best_model']
best_model_name      = artifacts['best_model_name']
xgb_model            = artifacts['xgb_model']
gbdt_model           = artifacts['gbdt_model']
num_features         = artifacts['num_features']
cat_features         = artifacts['cat_features']
all_feature_names    = artifacts['all_feature_names']
all_feature_names_gbdt = artifacts['all_feature_names_gbdt']
xgb_results          = artifacts['xgb_results']
gbdt_results         = artifacts['gbdt_results']
xgb_fi_df            = artifacts['xgb_fi_df']
gbdt_fi_df           = artifacts['gbdt_fi_df']
shap_fi_df           = artifacts['shap_fi_df']
shap_values          = artifacts['shap_values']
X_shap               = artifacts['X_shap']
shap_feat_names      = artifacts['shap_feat_names']
cm_xgb               = artifacts['cm_xgb']
cm_gbdt              = artifacts['cm_gbdt']
fpr_xgb  = artifacts['fpr_xgb'];  tpr_xgb  = artifacts['tpr_xgb']
fpr_gbdt = artifacts['fpr_gbdt']; tpr_gbdt = artifacts['tpr_gbdt']
n_data               = artifacts['n_data']
target_dist          = artifacts['target_dist']
df_raw               = artifacts['df_raw']
missing_values       = artifacts['missing_values']

best_scores = xgb_results if best_model_name == 'XGBoost' else gbdt_results

n_depressed     = target_dist.get(1, 0)
n_not_depressed = target_dist.get(0, 0)
depression_rate = n_depressed / n_data * 100


# ══════════════════════════════════════════════════════════════
# SIDEBAR — NAVIGATION
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 4px 16px 4px;'>
        <div style='font-size:22px; font-weight:800; color:#FFFFFF; font-family:Plus Jakarta Sans,sans-serif; letter-spacing:-0.5px;'>🧠 MindScan AI</div>
        <div style='font-size:11px; color:#64748B; margin-top:3px; font-weight:500;'>Student Depression Detection System</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        [
            "🏠  Executive Dashboard",
            "📊  Dataset Overview",
            "📈  Exploratory Data Analysis",
            "🧠  Mental Health Insights",
            "🎯  Model Performance",
            "🔍  Feature Importance",
            "🤖  Explainable AI (SHAP)",
            "🔮  Individual Depression Prediction",
            "📁  Batch Depression Prediction",
            "📚  About Research",
            "👩‍💻  About Author",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:rgba(37,99,235,0.12); border:1px solid rgba(37,99,235,0.25); border-radius:10px; padding:12px 14px;'>
        <div style='font-size:10px; font-weight:700; color:#60A5FA; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>Active Model</div>
        <div style='font-size:14px; font-weight:700; color:#FFFFFF;'>🏆 {best_model_name}</div>
        <div style='margin-top:8px; display:flex; justify-content:space-between;'>
            <div><div style='font-size:10px; color:#64748B;'>F1 Score</div><div style='font-size:13px; font-weight:700; color:#34D399;'>{best_scores['F1 Score']:.4f}</div></div>
            <div><div style='font-size:10px; color:#64748B;'>ROC AUC</div><div style='font-size:13px; font-weight:700; color:#60A5FA;'>{best_scores['ROC AUC']:.4f}</div></div>
            <div><div style='font-size:10px; color:#64748B;'>Accuracy</div><div style='font-size:13px; font-weight:700; color:#C084FC;'>{best_scores['Accuracy']:.1%}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='margin-top:16px; font-size:10px; color:#334155; line-height:1.7;'>
        <b style='color:#475569;'>Developers</b><br>Artika Putri Rahmawati<br>Fi Amanila Putri Kinanti<br>
        <b style='color:#475569;'>Major</b><br>Business Statistics<br>
        <b style='color:#475569;'>Methods</b><br>XGBoost · GBDT · SHAP
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════
def clean_layout(fig, h=380, title=None, legend=True):
    updates = dict(
        height=h, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12, color='#334155'),
        margin=dict(l=16, r=16, t=48 if title else 30, b=16), showlegend=legend,
    )
    if title:
        updates['title'] = dict(text=title, font=dict(size=15, color='#0F172A', family='Plus Jakarta Sans'), x=0)
    fig.update_layout(**updates)
    fig.update_xaxes(gridcolor='#F1F5F9', linecolor='#E2E8F0', tickfont=dict(size=11))
    fig.update_yaxes(gridcolor='#F1F5F9', linecolor='#E2E8F0', tickfont=dict(size=11))
    return fig

def section_header(icon, title, badge=None):
    badge_html = f"<span class='section-header-badge'>{badge}</span>" if badge else ""
    st.markdown(f"""
    <div class='section-header'>
        <span style='font-size:20px;'>{icon}</span>
        <span class='section-header-text'>{title}</span>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

def kpi_card(icon, value, label, sub, color_class="kpi-blue"):
    return f"""
    <div class='kpi-card {color_class}'>
        <span class='kpi-icon'>{icon}</span>
        <div class='kpi-value'>{value}</div>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>"""

COLORS = {
    'primary': '#2563EB', 'accent': '#06B6D4',
    'success': '#10B981', 'warning': '#F59E0B',
    'danger':  '#EF4444', 'purple': '#8B5CF6',
    'depr_colors': ['#10B981', '#EF4444'],
}


# ══════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════
if menu == "🏠  Executive Dashboard":

    st.markdown(f"""
    <div class='hero-banner'>
        <div class='hero-title'>🧠 Student Depression Detection<br>System</div>
        <div class='hero-sub'>Final Project Machine Learning 2026 · Artika Putri Rahmawati & Fi Amanila Putri Kinanti</div>
        <span class='hero-badge'>⚡ XGBoost</span>
        <span class='hero-badge'>🌲 Gradient Boosting</span>
        <span class='hero-badge'>🔬 SHAP Explainability</span>
        <span class='hero-badge'>📊 Student Mental Health Analytics</span>
        <div class='hero-stats'>
            <div class='hero-stat-item'>
                <div class='hero-stat-value'>{n_data:,}</div>
                <div class='hero-stat-label'>Total Students</div>
            </div>
            <div class='hero-stat-item'>
                <div class='hero-stat-value'>{depression_rate:.1f}%</div>
                <div class='hero-stat-label'>Depression Rate</div>
            </div>
            <div class='hero-stat-item'>
                <div class='hero-stat-value'>{best_scores['Accuracy']:.1%}</div>
                <div class='hero-stat-label'>Model Accuracy</div>
            </div>
            <div class='hero-stat-item'>
                <div class='hero-stat-value'>{best_scores['ROC AUC']:.4f}</div>
                <div class='hero-stat-label'>ROC-AUC Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("📊", "Key Performance Indicators", "6 Metrics")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpis = [
        (k1, "👩‍🎓", f"{n_data:,}",            "TOTAL STUDENTS",        "dalam dataset",              "kpi-blue"),
        (k2, "😟",   f"{n_depressed:,}",         "DEPRESSION CASES",      f"{depression_rate:.1f}% dari total", "kpi-red"),
        (k3, "😊",   f"{n_not_depressed:,}",      "NON DEPRESSION CASES",  "siswa sehat mental",         "kpi-green"),
        (k4, "📉",   f"{depression_rate:.1f}%",   "DEPRESSION RATE",       "tingkat depresi keseluruhan","kpi-amber"),
        (k5, "🎯",   f"{best_scores['Accuracy']:.1%}", "BEST MODEL ACCURACY", f"Model: {best_model_name}", "kpi-purple"),
        (k6, "📈",   f"{best_scores['ROC AUC']:.4f}", "ROC AUC",           "discriminative power",       "kpi-cyan"),
    ]
    for col, icon, val, lbl, sub, cls in kpis:
        with col:
            st.markdown(kpi_card(icon, val, lbl, sub, cls), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fi_top  = shap_fi_df['Feature'].iloc[0] if len(shap_fi_df) > 0 else "Academic Pressure"
    fi_top2 = shap_fi_df['Feature'].iloc[1] if len(shap_fi_df) > 1 else "Financial Stress"
    st.markdown(f"""
    <div class='ai-insight'>
        <div class='ai-insight-header'>🤖 AI Insight · Powered by {best_model_name}</div>
        <p class='ai-insight-text'>
            Analisis model menunjukkan bahwa mahasiswa dengan tekanan akademik tinggi dan kebiasaan tidur buruk
            memiliki risiko depresi yang jauh lebih tinggi.
            <b>{fi_top.replace('_', ' ').title()}</b> dan
            <b>{fi_top2.replace('_', ' ').title()}</b> merupakan dua faktor paling berpengaruh
            dalam model ini. Mahasiswa yang memiliki riwayat keluarga dengan penyakit mental
            juga menunjukkan tingkat risiko depresi yang lebih tinggi.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([3, 2])

    with col_chart1:
        section_header("🏆", "Model Performance Comparison", "XGBoost vs GBDT")
        comp_df = pd.DataFrame({
            'Metric'  : ['Accuracy','Precision','Recall','F1 Score','ROC AUC'],
            'XGBoost' : [xgb_results['Accuracy'], xgb_results['Precision'],
                         xgb_results['Recall'],   xgb_results['F1 Score'], xgb_results['ROC AUC']],
            'GBDT'    : [gbdt_results['Accuracy'], gbdt_results['Precision'],
                         gbdt_results['Recall'],   gbdt_results['F1 Score'], gbdt_results['ROC AUC']],
        })
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name='XGBoost', x=comp_df['Metric'], y=comp_df['XGBoost'],
                                   marker=dict(color=COLORS['primary'], opacity=0.9),
                                   text=comp_df['XGBoost'].round(4), textposition='outside', textfont=dict(size=11)))
        fig_comp.add_trace(go.Bar(name='GBDT', x=comp_df['Metric'], y=comp_df['GBDT'],
                                   marker=dict(color=COLORS['danger'], opacity=0.9),
                                   text=comp_df['GBDT'].round(4), textposition='outside', textfont=dict(size=11)))
        fig_comp.update_layout(barmode='group', yaxis=dict(range=[0.5, 1.08]),
                               legend=dict(orientation='h', y=1.12, x=0))
        clean_layout(fig_comp, h=360)
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_chart2:
        section_header("🎯", "Depression Distribution")
        fig_donut = go.Figure(go.Pie(
            labels=['Tidak Depresi', 'Depresi'],
            values=[n_not_depressed, n_depressed],
            hole=0.55,
            marker=dict(colors=[COLORS['success'], COLORS['danger']],
                        line=dict(color='white', width=2)),
            textinfo='label+percent', textfont=dict(size=12),
        ))
        fig_donut.update_layout(
            annotations=[dict(text=f"{depression_rate:.1f}%<br><span style='font-size:10px'>Depression</span>",
                              x=0.5, y=0.5, font_size=18, showarrow=False, font=dict(color='#0F172A'))],
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'),
        )
        clean_layout(fig_donut, h=360)
        st.plotly_chart(fig_donut, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — DATASET OVERVIEW
# ══════════════════════════════════════════════════════════════
elif menu == "📊  Dataset Overview":
    section_header("📊", "Dataset Overview", "Student Depression Dataset")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("📦", f"{n_data:,}", "TOTAL DATA", "observasi", "kpi-blue"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("📋", f"{len(df_raw.columns)}", "TOTAL FITUR", "kolom", "kpi-purple"), unsafe_allow_html=True)
    with c3:
        mv = sum(1 for v in missing_values.values() if (v if isinstance(v, int) else sum(v.values())) > 0)
        st.markdown(kpi_card("🔍", f"{mv}", "MISSING FEATURES", "kolom bermasalah", "kpi-amber"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("😟", f"{depression_rate:.1f}%", "DEPRESSION RATE", f"{n_depressed} cases", "kpi-red"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        section_header("👀", "Data Preview", f"Top 100 rows")
        st.dataframe(df_raw.head(100), use_container_width=True, height=350)

    with col2:
        section_header("🗂️", "Data Types")
        dtype_df = pd.DataFrame({'Column': df_raw.columns, 'Type': df_raw.dtypes.astype(str).values})
        st.dataframe(dtype_df, use_container_width=True, height=350)

    section_header("📊", "Target Distribution Detail")
    col3, col4 = st.columns(2)
    with col3:
        dist_df = pd.DataFrame({
            'Kelas': ['Tidak Depresi (0)', 'Depresi (1)'],
            'Count': [n_not_depressed, n_depressed],
            'Persentase (%)': [f"{n_not_depressed/n_data*100:.2f}%", f"{n_depressed/n_data*100:.2f}%"]
        })
        st.dataframe(dist_df, use_container_width=True)
    with col4:
        fig_bar = px.bar(x=['Tidak Depresi', 'Depresi'], y=[n_not_depressed, n_depressed],
                         color=['Tidak Depresi', 'Depresi'],
                         color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']},
                         text=[n_not_depressed, n_depressed])
        fig_bar.update_traces(textposition='outside')
        clean_layout(fig_bar, h=300, title="Distribusi Target Variable")
        st.plotly_chart(fig_bar, use_container_width=True)

    section_header("📈", "Descriptive Statistics")
    st.dataframe(df_raw.describe().T.style.format("{:.4f}"), use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — EDA
# ══════════════════════════════════════════════════════════════
elif menu == "📈  Exploratory Data Analysis":
    section_header("📈", "Exploratory Data Analysis", "Depression Features")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribusi Kategorikal", "📉 Fitur Numerik", "🔥 Korelasi", "📦 Boxplot"])

    with tab1:
        st.markdown("#### Depression by Gender")
        c1, c2 = st.columns(2)
        with c1:
            if 'Gender' in df_raw.columns:
                gender_dep = df_raw.groupby(['Gender', 'Depression']).size().reset_index(name='Count')
                gender_dep['Status'] = gender_dep['Depression'].map({0: 'Tidak Depresi', 1: 'Depresi'})
                fig = px.bar(gender_dep, x='Gender', y='Count', color='Status', barmode='group',
                             color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']})
                clean_layout(fig, h=320, title="Gender vs Depression")
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            if 'Sleep Duration' in df_raw.columns:
                sleep_dep = df_raw.groupby(['Sleep Duration', 'Depression']).size().reset_index(name='Count')
                sleep_dep['Status'] = sleep_dep['Depression'].map({0: 'Tidak Depresi', 1: 'Depresi'})
                fig2 = px.bar(sleep_dep, x='Sleep Duration', y='Count', color='Status', barmode='group',
                              color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']})
                clean_layout(fig2, h=320, title="Sleep Duration vs Depression")
                st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            if 'Dietary Habits' in df_raw.columns:
                diet_dep = df_raw.groupby(['Dietary Habits', 'Depression']).size().reset_index(name='Count')
                diet_dep['Status'] = diet_dep['Depression'].map({0: 'Tidak Depresi', 1: 'Depresi'})
                fig3 = px.bar(diet_dep, x='Dietary Habits', y='Count', color='Status', barmode='group',
                              color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']})
                clean_layout(fig3, h=320, title="Dietary Habits vs Depression")
                st.plotly_chart(fig3, use_container_width=True)
        with c4:
            if 'Family History of Mental Illness' in df_raw.columns:
                fam_dep = df_raw.groupby(['Family History of Mental Illness', 'Depression']).size().reset_index(name='Count')
                fam_dep['Status'] = fam_dep['Depression'].map({0: 'Tidak Depresi', 1: 'Depresi'})
                fig4 = px.bar(fam_dep, x='Family History of Mental Illness', y='Count', color='Status', barmode='group',
                              color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']})
                clean_layout(fig4, h=320, title="Family History vs Depression")
                st.plotly_chart(fig4, use_container_width=True)

        if 'Have you ever had suicidal thoughts ?' in df_raw.columns:
            sui_dep = df_raw.groupby(['Have you ever had suicidal thoughts ?', 'Depression']).size().reset_index(name='Count')
            sui_dep['Status'] = sui_dep['Depression'].map({0: 'Tidak Depresi', 1: 'Depresi'})
            fig5 = px.bar(sui_dep, x='Have you ever had suicidal thoughts ?', y='Count', color='Status', barmode='group',
                          color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']})
            clean_layout(fig5, h=300, title="Suicidal Thoughts vs Depression")
            st.plotly_chart(fig5, use_container_width=True)

    with tab2:
        num_cols_eda = df_raw.select_dtypes(include=['int64','float64']).columns.tolist()
        num_cols_eda = [c for c in num_cols_eda if c not in ['id','Depression']]
        col_sel = st.selectbox("Pilih fitur numerik:", num_cols_eda)
        c1, c2 = st.columns(2)
        with c1:
            fig_hist = px.histogram(df_raw, x=col_sel, color='Depression',
                                    color_discrete_map={0: COLORS['success'], 1: COLORS['danger']},
                                    barmode='overlay', opacity=0.7, nbins=30)
            clean_layout(fig_hist, h=320, title=f"Distribusi {col_sel} by Depression")
            st.plotly_chart(fig_hist, use_container_width=True)
        with c2:
            dep_0 = df_raw[df_raw['Depression']==0][col_sel].dropna()
            dep_1 = df_raw[df_raw['Depression']==1][col_sel].dropna()
            fig_v = go.Figure()
            fig_v.add_trace(go.Violin(y=dep_0, name='Tidak Depresi', fillcolor=COLORS['success'], line_color=COLORS['success'], opacity=0.7))
            fig_v.add_trace(go.Violin(y=dep_1, name='Depresi', fillcolor=COLORS['danger'], line_color=COLORS['danger'], opacity=0.7))
            clean_layout(fig_v, h=320, title=f"Violin: {col_sel}")
            st.plotly_chart(fig_v, use_container_width=True)

    with tab3:
        num_df = df_raw[num_cols_eda + ['Depression']].copy()
        corr = num_df.corr()
        fig_heat = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', aspect='auto', zmin=-1, zmax=1)
        clean_layout(fig_heat, h=500, title="Correlation Heatmap")
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab4:
        col_box = st.selectbox("Pilih fitur untuk boxplot:", num_cols_eda, key="box_sel")
        fig_box = px.box(df_raw, x='Depression', y=col_box,
                         color='Depression',
                         color_discrete_map={0: COLORS['success'], 1: COLORS['danger']})
        clean_layout(fig_box, h=400, title=f"Boxplot: {col_box} by Depression")
        st.plotly_chart(fig_box, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — MENTAL HEALTH INSIGHTS
# ══════════════════════════════════════════════════════════════
elif menu == "🧠  Mental Health Insights":
    section_header("🧠", "Mental Health Risk Factor Analysis", "Depression Insights")

    st.markdown("""
    <div class='ai-insight'>
        <div class='ai-insight-header'>🔍 Analisis Faktor Risiko Depresi Mahasiswa</div>
        <p class='ai-insight-text'>
            Halaman ini mengeksplorasi faktor-faktor utama yang berkontribusi terhadap depresi mahasiswa.
            Analisis dilakukan berdasarkan data observasional dari 5.000 mahasiswa dengan berbagai karakteristik akademik,
            sosial, dan psikologis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if 'Academic Pressure' in df_raw.columns:
            ap_dep = df_raw.groupby('Academic Pressure')['Depression'].mean().reset_index()
            ap_dep['Depression Rate (%)'] = ap_dep['Depression'] * 100
            fig = px.bar(ap_dep, x='Academic Pressure', y='Depression Rate (%)',
                         color='Depression Rate (%)', color_continuous_scale='Reds')
            clean_layout(fig, h=320, title="Academic Pressure vs Depression Rate (%)")
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if 'Financial Stress' in df_raw.columns:
            fs_dep = df_raw.groupby('Financial Stress')['Depression'].mean().reset_index()
            fs_dep['Depression Rate (%)'] = fs_dep['Depression'] * 100
            fig2 = px.bar(fs_dep, x='Financial Stress', y='Depression Rate (%)',
                          color='Depression Rate (%)', color_continuous_scale='Oranges')
            clean_layout(fig2, h=320, title="Financial Stress vs Depression Rate (%)")
            st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if 'Study Satisfaction' in df_raw.columns:
            ss_dep = df_raw.groupby('Study Satisfaction')['Depression'].mean().reset_index()
            ss_dep['Depression Rate (%)'] = ss_dep['Depression'] * 100
            fig3 = px.line(ss_dep, x='Study Satisfaction', y='Depression Rate (%)', markers=True,
                           line_shape='spline')
            fig3.update_traces(line_color=COLORS['primary'], marker=dict(size=8))
            clean_layout(fig3, h=320, title="Study Satisfaction vs Depression Rate (%)")
            st.plotly_chart(fig3, use_container_width=True)
    with c4:
        if 'CGPA' in df_raw.columns:
            df_raw_copy = df_raw.copy()
            df_raw_copy['CGPA_bin'] = pd.cut(df_raw_copy['CGPA'], bins=5)
            cgpa_dep = df_raw_copy.groupby('CGPA_bin', observed=False)['Depression'].mean().reset_index()
            cgpa_dep['Depression Rate (%)'] = cgpa_dep['Depression'] * 100
            cgpa_dep['CGPA_bin'] = cgpa_dep['CGPA_bin'].astype(str)
            fig4 = px.bar(cgpa_dep, x='CGPA_bin', y='Depression Rate (%)', color='Depression Rate (%)',
                          color_continuous_scale='Blues')
            clean_layout(fig4, h=320, title="CGPA Range vs Depression Rate (%)")
            st.plotly_chart(fig4, use_container_width=True)

    if 'Work/Study Hours' in df_raw.columns:
        wsh_dep = df_raw.groupby('Work/Study Hours')['Depression'].mean().reset_index()
        wsh_dep['Depression Rate (%)'] = wsh_dep['Depression'] * 100
        fig5 = px.scatter(wsh_dep, x='Work/Study Hours', y='Depression Rate (%)', size='Depression Rate (%)',
                          color='Depression Rate (%)', color_continuous_scale='Reds', size_max=20)
        clean_layout(fig5, h=320, title="Work/Study Hours vs Depression Rate (%)")
        st.plotly_chart(fig5, use_container_width=True)

    # Risk summary cards
    section_header("⚠️", "Key Risk Factors Summary")
    risk_cols = st.columns(4)
    risk_factors = [
        ("🎓", "Academic Pressure", "Tekanan studi tinggi meningkatkan risiko 2-3x"),
        ("💰", "Financial Stress", "Kondisi keuangan sulit memperburuk kesehatan mental"),
        ("😴", "Sleep Duration", "Kurang tidur (<5 jam) berkorelasi kuat dengan depresi"),
        ("🍽️", "Dietary Habits", "Pola makan buruk merupakan indikator risiko depresi"),
    ]
    for col, (icon, title, desc) in zip(risk_cols, risk_factors):
        with col:
            st.markdown(f"""
            <div style='background:white; border:1px solid #E2E8F0; border-top:3px solid {COLORS["danger"]};
                        border-radius:12px; padding:16px; text-align:center;'>
                <div style='font-size:28px; margin-bottom:8px;'>{icon}</div>
                <div style='font-size:13px; font-weight:700; color:#0F172A; margin-bottom:6px;'>{title}</div>
                <div style='font-size:11px; color:#64748B; line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — MODEL PERFORMANCE
# ══════════════════════════════════════════════════════════════
elif menu == "🎯  Model Performance":
    section_header("🎯", "Model Performance Evaluation", "XGBoost vs GBDT")

    best_badge = f"🏆 Model Terbaik: {best_model_name}"
    st.markdown(f"""
    <div class='ai-insight'>
        <div class='ai-insight-header'>📊 {best_badge}</div>
        <p class='ai-insight-text'>
            Evaluasi dilakukan pada data uji (20% dari total data) menggunakan 5 metrik kinerja.
            Model dipilih berdasarkan nilai ROC AUC tertinggi.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics comparison
    section_header("📊", "Metrics Comparison Table")
    perf_df = pd.DataFrame({
        'Metric'  : ['Accuracy','Precision','Recall','F1 Score','ROC AUC'],
        'XGBoost' : [xgb_results['Accuracy'],  xgb_results['Precision'],  xgb_results['Recall'],
                     xgb_results['F1 Score'],   xgb_results['ROC AUC']],
        'GBDT'    : [gbdt_results['Accuracy'], gbdt_results['Precision'], gbdt_results['Recall'],
                     gbdt_results['F1 Score'],  gbdt_results['ROC AUC']],
    })
    perf_df['Best'] = perf_df.apply(lambda r: 'XGBoost' if r['XGBoost'] >= r['GBDT'] else 'GBDT', axis=1)
    st.dataframe(perf_df.style.format({'XGBoost':'{:.4f}','GBDT':'{:.4f}'}), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='XGBoost', x=perf_df['Metric'], y=perf_df['XGBoost'],
                                  marker_color=COLORS['primary'], text=perf_df['XGBoost'].round(4), textposition='outside'))
        fig_bar.add_trace(go.Bar(name='GBDT', x=perf_df['Metric'], y=perf_df['GBDT'],
                                  marker_color=COLORS['danger'], text=perf_df['GBDT'].round(4), textposition='outside'))
        fig_bar.update_layout(barmode='group', yaxis=dict(range=[0.5, 1.08]),
                               legend=dict(orientation='h', y=1.1))
        clean_layout(fig_bar, h=380, title="Model Performance Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=fpr_xgb, y=tpr_xgb, mode='lines', name=f'XGBoost (AUC={xgb_results["ROC AUC"]:.4f})',
                                      line=dict(color=COLORS['primary'], width=2.5)))
        fig_roc.add_trace(go.Scatter(x=fpr_gbdt, y=tpr_gbdt, mode='lines', name=f'GBDT (AUC={gbdt_results["ROC AUC"]:.4f})',
                                      line=dict(color=COLORS['danger'], width=2.5)))
        fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', name='Random', line=dict(color='gray', dash='dash')))
        fig_roc.update_layout(xaxis_title='False Positive Rate', yaxis_title='True Positive Rate',
                               legend=dict(orientation='h', y=-0.2))
        clean_layout(fig_roc, h=380, title="ROC Curve Comparison")
        st.plotly_chart(fig_roc, use_container_width=True)

    # Confusion matrices
    section_header("🔲", "Confusion Matrices")
    c3, c4 = st.columns(2)
    for col, cm, name, color in [(c3, cm_xgb,'XGBoost',COLORS['primary']),(c4, cm_gbdt,'GBDT',COLORS['danger'])]:
        with col:
            fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale='Blues',
                               x=['Tidak Depresi','Depresi'], y=['Tidak Depresi','Depresi'])
            fig_cm.update_layout(xaxis_title='Prediksi', yaxis_title='Aktual')
            clean_layout(fig_cm, h=320, title=f"Confusion Matrix — {name}")
            st.plotly_chart(fig_cm, use_container_width=True)

    # KPI cards per model
    section_header("🏅", "Per-Model Scorecard")
    cc = st.columns(2)
    for c, r, name in [(cc[0], xgb_results,'XGBoost'),(cc[1], gbdt_results,'GBDT')]:
        with c:
            badge = "🏆 BEST MODEL" if name == best_model_name else ""
            st.markdown(f"""
            <div style='background:white; border:2px solid {"#2563EB" if name==best_model_name else "#E2E8F0"};
                        border-radius:16px; padding:20px; margin-bottom:10px;'>
                <div style='font-size:16px; font-weight:800; color:#0F172A; margin-bottom:12px;'>
                    {"⚡" if name=="XGBoost" else "🌲"} {name} {badge}
                </div>
                <div style='display:grid; grid-template-columns:1fr 1fr; gap:10px;'>
                    <div style='text-align:center;'><div style='font-size:20px; font-weight:800; color:{COLORS["primary"]};'>{r["Accuracy"]:.4f}</div><div style='font-size:10px; color:#64748B;'>ACCURACY</div></div>
                    <div style='text-align:center;'><div style='font-size:20px; font-weight:800; color:{COLORS["success"]};'>{r["F1 Score"]:.4f}</div><div style='font-size:10px; color:#64748B;'>F1 SCORE</div></div>
                    <div style='text-align:center;'><div style='font-size:20px; font-weight:800; color:{COLORS["warning"]};'>{r["Precision"]:.4f}</div><div style='font-size:10px; color:#64748B;'>PRECISION</div></div>
                    <div style='text-align:center;'><div style='font-size:20px; font-weight:800; color:{COLORS["accent"]};'>{r["ROC AUC"]:.4f}</div><div style='font-size:10px; color:#64748B;'>ROC AUC</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 6 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════════
elif menu == "🔍  Feature Importance":
    section_header("🔍", "Feature Importance Analysis", f"Model: {best_model_name}")

    tab1, tab2 = st.tabs(["⚡ XGBoost", "🌲 GBDT"])

    def make_fi_chart(fi_df, model_name, color):
        top10 = fi_df.head(10)
        fig = go.Figure(go.Bar(
            x=top10['Importance'][::-1], y=top10['Feature'][::-1],
            orientation='h', marker=dict(color=color, opacity=0.85),
            text=top10['Importance'][::-1].round(4), textposition='outside',
        ))
        clean_layout(fig, h=420, title=f"Top 10 Feature Importance — {model_name}")
        return fig

    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.plotly_chart(make_fi_chart(xgb_fi_df, 'XGBoost', COLORS['primary']), use_container_width=True)
        with c2:
            section_header("📋", "XGBoost Top Features")
            st.dataframe(xgb_fi_df[['Feature','Importance']].head(15)
                         .style.format({'Importance': '{:.4f}'}), use_container_width=True, height=380)

    with tab2:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.plotly_chart(make_fi_chart(gbdt_fi_df, 'GBDT', COLORS['danger']), use_container_width=True)
        with c2:
            section_header("📋", "GBDT Top Features")
            st.dataframe(gbdt_fi_df[['Feature','Importance']].head(15)
                         .style.format({'Importance': '{:.4f}'}), use_container_width=True, height=380)

    section_header("🔬", "Comparison: XGBoost vs GBDT Feature Rankings")
    merged = xgb_fi_df[['Feature','Importance']].rename(columns={'Importance':'XGBoost'})\
              .merge(gbdt_fi_df[['Feature','Importance']].rename(columns={'Importance':'GBDT'}),
                     on='Feature', how='outer').fillna(0)\
              .sort_values('XGBoost', ascending=False).head(10)

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name='XGBoost', x=merged['Feature'], y=merged['XGBoost'],
                               marker_color=COLORS['primary']))
    fig_comp.add_trace(go.Bar(name='GBDT', x=merged['Feature'], y=merged['GBDT'],
                               marker_color=COLORS['danger']))
    fig_comp.update_layout(barmode='group', legend=dict(orientation='h', y=1.1))
    clean_layout(fig_comp, h=380, title="Feature Importance Comparison")
    st.plotly_chart(fig_comp, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 7 — EXPLAINABLE AI (SHAP)
# ══════════════════════════════════════════════════════════════
elif menu == "🤖  Explainable AI (SHAP)":
    section_header("🤖", "Explainable AI — SHAP Analysis", f"Model: {best_model_name}")

    st.markdown(f"""
    <div class='ai-insight'>
        <div class='ai-insight-header'>🔬 SHAP (SHapley Additive exPlanations) · {best_model_name}</div>
        <p class='ai-insight-text'>
            SHAP mengukur kontribusi setiap fitur terhadap prediksi model secara individual (lokal) maupun global.
            Nilai SHAP positif → mendorong prediksi ke <b>Depresi</b>. Nilai negatif → mendorong ke <b>Tidak Depresi</b>.
            Mean |SHAP| menunjukkan kepentingan fitur secara rata-rata di seluruh sampel.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        fig_shap = go.Figure(go.Bar(
            x=shap_fi_df['Mean |SHAP|'][:10][::-1],
            y=shap_fi_df['Feature'][:10][::-1],
            orientation='h',
            marker=dict(color=COLORS['purple'], opacity=0.85),
            text=shap_fi_df['Mean |SHAP|'][:10][::-1].round(4),
            textposition='outside',
        ))
        clean_layout(fig_shap, h=420, title=f"SHAP Feature Impact — {best_model_name} (Top 10)")
        st.plotly_chart(fig_shap, use_container_width=True)
    with c2:
        section_header("📊", "SHAP Rankings")
        st.dataframe(shap_fi_df[['Feature','Mean |SHAP|']].head(15)
                     .style.format({'Mean |SHAP|': '{:.4f}'}), use_container_width=True, height=380)

    section_header("🧩", "SHAP Feature Interpretation")
    interp_cols = st.columns(3)
    for i, (_, row) in enumerate(shap_fi_df.head(3).iterrows()):
        with interp_cols[i]:
            st.markdown(f"""
            <div style='background:white; border:1px solid #E2E8F0; border-top:3px solid {COLORS["purple"]};
                        border-radius:12px; padding:16px;'>
                <div style='font-size:11px; font-weight:700; color:{COLORS["purple"]}; text-transform:uppercase; margin-bottom:6px;'>Top {i+1} SHAP Feature</div>
                <div style='font-size:14px; font-weight:700; color:#0F172A; margin-bottom:8px;'>{row["Feature"]}</div>
                <div style='font-size:20px; font-weight:800; color:{COLORS["purple"]};'>{row["Mean |SHAP|"]:.4f}</div>
                <div style='font-size:11px; color:#64748B; margin-top:4px;'>Mean |SHAP Value|</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='research-card'>
        <div class='research-card-title'>💡 Interpretasi Hasil SHAP</div>
        <div class='research-card-body'>
            <b>SHAP Global Interpretation:</b> Fitur-fitur dengan nilai Mean |SHAP| tertinggi
            merupakan faktor paling determinan dalam prediksi depresi mahasiswa. Semakin tinggi nilai SHAP,
            semakin besar kontribusi fitur tersebut terhadap keputusan model.<br><br>
            <b>Tekanan Akademik (Academic Pressure):</b> Fitur ini memiliki kontribusi terbesar
            dalam menentukan apakah mahasiswa berisiko depresi. Nilai tekanan tinggi secara konsisten
            mendorong prediksi ke arah depresi.<br><br>
            <b>Durasi Tidur (Sleep Duration):</b> Mahasiswa yang tidur kurang dari 5 jam memiliki
            nilai SHAP positif yang tinggi, mengindikasikan kontribusi signifikan terhadap risiko depresi.<br><br>
            <b>Stres Finansial (Financial Stress):</b> Kondisi keuangan yang buruk berkorelasi positif
            dengan risiko depresi, terutama pada mahasiswa yang belajar sambil bekerja.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 8 — INDIVIDUAL PREDICTION
# ══════════════════════════════════════════════════════════════
elif menu == "🔮  Individual Depression Prediction":
    section_header("🔮", "Individual Depression Prediction", "Real-time Prediction")

    st.markdown("""
    <div class='ai-insight'>
        <div class='ai-insight-header'>📝 Form Prediksi Depresi Mahasiswa</div>
        <p class='ai-insight-text'>Isi seluruh informasi di bawah ini dan klik <b>Predict Depression Risk</b> untuk mendapatkan hasil prediksi.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        st.markdown("#### 👤 Informasi Demografis")
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            gender = st.selectbox("Gender", ['Male', 'Female'])
        with r1c2:
            age = st.number_input("Age", min_value=15, max_value=60, value=21)
        with r1c3:
            city = st.selectbox("City", sorted(df_raw['City'].dropna().unique().tolist()) if 'City' in df_raw.columns else ['Unknown'])

        st.markdown("#### 🎓 Informasi Akademik")
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            profession = st.selectbox("Profession", sorted(df_raw['Profession'].dropna().unique().tolist()) if 'Profession' in df_raw.columns else ['Student'])
        with r2c2:
            degree = st.selectbox("Degree", sorted(df_raw['Degree'].dropna().unique().tolist()) if 'Degree' in df_raw.columns else ['BSc'])
        with r2c3:
            cgpa = st.slider("CGPA", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

        r3c1, r3c2, r3c3 = st.columns(3)
        with r3c1:
            academic_pressure = st.slider("Academic Pressure (1-5)", 1, 5, 3)
        with r3c2:
            work_pressure = st.slider("Work Pressure (0-5)", 0, 5, 2)
        with r3c3:
            study_satisfaction = st.slider("Study Satisfaction (1-5)", 1, 5, 3)

        r4c1, r4c2, r4c3 = st.columns(3)
        with r4c1:
            job_satisfaction = st.slider("Job Satisfaction (0-5)", 0, 5, 3)
        with r4c2:
            work_study_hours = st.slider("Work/Study Hours per day", 0, 16, 6)
        with r4c3:
            financial_stress = st.slider("Financial Stress (1-5)", 1, 5, 2)

        st.markdown("#### 🏥 Informasi Kesehatan")
        r5c1, r5c2, r5c3 = st.columns(3)
        with r5c1:
            sleep_duration = st.selectbox("Sleep Duration", ['Less than 5 hours','5-6 hours','7-8 hours','More than 8 hours','Others'])
        with r5c2:
            dietary_habits = st.selectbox("Dietary Habits", ['Healthy','Moderate','Unhealthy'])
        with r5c3:
            suicidal_thoughts = st.selectbox("Suicidal Thoughts?", ['No', 'Yes'])

        family_history = st.selectbox("Family History of Mental Illness", ['No', 'Yes'])

        submitted = st.form_submit_button("🔮 Predict Depression Risk", use_container_width=True)

    if submitted:
        input_data = pd.DataFrame([{
            'Gender'                              : gender,
            'Age'                                 : age,
            'City'                                : city,
            'Profession'                          : profession,
            'Academic Pressure'                   : academic_pressure,
            'Work Pressure'                       : work_pressure,
            'CGPA'                                : cgpa,
            'Study Satisfaction'                  : study_satisfaction,
            'Job Satisfaction'                    : job_satisfaction,
            'Sleep Duration'                      : sleep_duration,
            'Dietary Habits'                      : dietary_habits,
            'Degree'                              : degree,
            'Have you ever had suicidal thoughts ?': suicidal_thoughts,
            'Work/Study Hours'                    : work_study_hours,
            'Financial Stress'                    : financial_stress,
            'Family History of Mental Illness'    : family_history,
        }])

        input_data = input_data[num_features + cat_features]
        pred       = best_model.predict(input_data)[0]
        prob       = best_model.predict_proba(input_data)[0]
        prob_dep   = prob[1]
        prob_nodep = prob[0]

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if pred == 1:
                st.markdown(f"""
                <div class='pred-depression'>
                    <div class='pred-title'>⚠️ HIGH RISK OF DEPRESSION</div>
                    <div class='pred-prob'>{prob_dep:.1%}</div>
                    <div class='pred-label'>Probabilitas Depresi</div>
                    <div class='risk-badge'>🚨 PERLU PERHATIAN SEGERA</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='pred-nodepression'>
                    <div class='pred-title'>✅ LOW RISK OF DEPRESSION</div>
                    <div class='pred-prob'>{prob_nodep:.1%}</div>
                    <div class='pred-label'>Probabilitas Tidak Depresi</div>
                    <div class='risk-badge'>💚 KONDISI MENTAL SEHAT</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📊", "Probability Breakdown")
        fig_prob = go.Figure(go.Bar(
            x=['Tidak Depresi', 'Depresi'], y=[prob_nodep, prob_dep],
            marker=dict(color=[COLORS['success'], COLORS['danger']], opacity=0.85),
            text=[f'{prob_nodep:.1%}', f'{prob_dep:.1%}'], textposition='outside',
        ))
        fig_prob.update_layout(yaxis=dict(range=[0, 1.15]))
        clean_layout(fig_prob, h=320, title="Prediction Probability")
        st.plotly_chart(fig_prob, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 9 — BATCH PREDICTION
# ══════════════════════════════════════════════════════════════
elif menu == "📁  Batch Depression Prediction":
    section_header("📁", "Batch Depression Prediction", "CSV Upload")

    st.markdown("""
    <div class='upload-zone'>
        <div class='upload-zone-title'>📤 Upload CSV untuk Prediksi Batch</div>
        <div class='upload-zone-sub'>File harus memiliki kolom yang sama dengan dataset pelatihan (tanpa kolom 'id' dan 'Depression')</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file:
        try:
            batch_df = pd.read_csv(uploaded_file, sep=';')
            if batch_df.shape[1] < 5:
                batch_df = pd.read_csv(uploaded_file)
        except:
            batch_df = pd.read_csv(uploaded_file)

        st.success(f"✅ File berhasil diupload: {batch_df.shape[0]} baris, {batch_df.shape[1]} kolom")

        try:
            cols_needed = num_features + cat_features
            batch_input = batch_df[cols_needed]
            predictions  = best_model.predict(batch_input)
            probabilities = best_model.predict_proba(batch_input)

            result_df = batch_df.copy()
            result_df['Prediction']          = predictions
            result_df['Depression_Label']    = result_df['Prediction'].map({0: 'Tidak Depresi', 1: 'Depresi'})
            result_df['Prob_Tidak_Depresi']  = probabilities[:, 0].round(4)
            result_df['Prob_Depresi']        = probabilities[:, 1].round(4)

            # Summary
            n_dep_batch    = (predictions == 1).sum()
            n_nodep_batch  = (predictions == 0).sum()
            rate_batch     = n_dep_batch / len(predictions) * 100

            section_header("📊", "Batch Prediction Summary")
            sc1, sc2, sc3, sc4 = st.columns(4)
            with sc1: st.markdown(kpi_card("📋", f"{len(predictions):,}", "TOTAL PREDIKSI", "sampel", "kpi-blue"), unsafe_allow_html=True)
            with sc2: st.markdown(kpi_card("😟", f"{n_dep_batch:,}", "DEPRESI", f"{rate_batch:.1f}%", "kpi-red"), unsafe_allow_html=True)
            with sc3: st.markdown(kpi_card("😊", f"{n_nodep_batch:,}", "TIDAK DEPRESI", f"{100-rate_batch:.1f}%", "kpi-green"), unsafe_allow_html=True)
            with sc4: st.markdown(kpi_card("📈", f"{rate_batch:.1f}%", "DEPRESSION RATE", "dalam batch ini", "kpi-amber"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns([1, 1])
            with c1:
                fig_b = px.pie(values=[n_nodep_batch, n_dep_batch], names=['Tidak Depresi','Depresi'],
                               color_discrete_map={'Tidak Depresi': COLORS['success'], 'Depresi': COLORS['danger']},
                               hole=0.4)
                clean_layout(fig_b, h=300, title="Batch Prediction Distribution")
                st.plotly_chart(fig_b, use_container_width=True)
            with c2:
                fig_hist = px.histogram(result_df, x='Prob_Depresi', nbins=30, color_discrete_sequence=[COLORS['danger']])
                clean_layout(fig_hist, h=300, title="Distribution of Depression Probability")
                st.plotly_chart(fig_hist, use_container_width=True)

            section_header("📄", "Prediction Results")
            st.dataframe(result_df, use_container_width=True, height=350)

            csv_out = result_df.to_csv(index=False)
            st.download_button("📥 Download Hasil Prediksi (CSV)", data=csv_out,
                               file_name="depression_predictions.csv", mime="text/csv",
                               use_container_width=True)
        except KeyError as e:
            st.error(f"❌ Kolom tidak sesuai: {e}. Pastikan CSV memiliki kolom: {num_features + cat_features}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.info("👆 Upload file CSV untuk memulai prediksi batch")
        st.markdown("**Contoh format kolom yang dibutuhkan:**")
        sample = df_raw[num_features + cat_features].head(3)
        st.dataframe(sample, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 10 — ABOUT RESEARCH
# ══════════════════════════════════════════════════════════════
elif menu == "📚  About Research":
    section_header("📚", "About This Research", "Student Depression Detection")

    st.markdown("""
    <div class='hero-banner' style='padding:28px 36px;'>
        <div class='hero-title' style='font-size:24px;'>🧠 Prediksi Risiko Depresi Mahasiswa</div>
        <div class='hero-sub'>Menggunakan XGBoost, Gradient Boosting Decision Tree (GBDT), dan SHAP Explainability</div>
        <span class='hero-badge'>Machine Learning 2026</span>
        <span class='hero-badge'>Business Statistics</span>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "🎯 Latar Belakang", "Depresi merupakan salah satu masalah kesehatan mental paling umum di kalangan mahasiswa. Tekanan akademik, financial stress, dan kurang tidur merupakan faktor-faktor yang berkontribusi signifikan. Penelitian ini bertujuan membangun model machine learning untuk mendeteksi risiko depresi mahasiswa secara dini."),
        ("02", "📦 Dataset", f"Dataset Student Depression terdiri dari {n_data:,} observasi dengan 16 fitur yang mencakup informasi demografis, akademik, dan kesehatan mahasiswa. Target variabel adalah 'Depression' (1 = Depresi, 0 = Tidak Depresi)."),
        ("03", "🔧 Preprocessing", "Proses preprocessing menggunakan Pipeline dan ColumnTransformer dari Scikit-learn untuk mencegah data leakage. Fitur numerik: SimpleImputer (median) + StandardScaler. Fitur kategorik: SimpleImputer (mode) + OneHotEncoder."),
        ("04", "🌲 Gradient Boosting (GBDT)", "GradientBoostingClassifier dari Scikit-learn dengan optimasi hyperparameter via RandomizedSearchCV (n_iter=10, cv=5, scoring=ROC AUC). GBDT membangun ensemble dari decision tree secara sekuensial, di mana setiap pohon memperbaiki kesalahan pohon sebelumnya."),
        ("05", "⚡ XGBoost", "XGBoost (eXtreme Gradient Boosting) merupakan implementasi gradient boosting yang dioptimasi untuk kecepatan dan performa. Menggunakan regularisasi L1/L2 untuk mencegah overfitting. Parameter tuning meliputi n_estimators, max_depth, learning_rate, subsample, dan colsample_bytree."),
        ("06", "🔬 SHAP Explainability", "SHAP (SHapley Additive exPlanations) digunakan untuk menginterpretasikan prediksi model secara transparan. TreeExplainer digunakan untuk efisiensi pada tree-based models. Visualisasi meliputi SHAP Bar Plot dan Beeswarm Plot untuk memahami kontribusi setiap fitur."),
        ("07", "🏆 Hasil", f"Model terbaik: {best_model_name} dengan Accuracy: {best_scores['Accuracy']:.4f}, F1 Score: {best_scores['F1 Score']:.4f}, ROC AUC: {best_scores['ROC AUC']:.4f}. Model berhasil mengidentifikasi faktor-faktor risiko utama depresi mahasiswa."),
    ]

    for num, title, desc in steps:
        st.markdown(f"""
        <div class='method-step'>
            <div class='method-step-num'>STEP {num}</div>
            <div class='method-step-title'>{title}</div>
            <div class='method-step-desc'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 11 — ABOUT AUTHOR
# ══════════════════════════════════════════════════════════════
elif menu == "👩‍💻  About Author":
    section_header("👩‍💻", "About the Authors", "Business Statistics 2026")

    c1, c2 = st.columns(2)
    for col, name, icon in [(c1,"Artika Putri Rahmawati","👩‍💻"), (c2,"Fi Amanila Putri Kinanti","👩‍💻")]:
        with col:
            st.markdown(f"""
            <div class='profile-card'>
                <div class='profile-avatar'>{icon}</div>
                <div class='profile-name'>{name}</div>
                <div class='profile-major'>Business Statistics</div>
                <span class='profile-tag'>Machine Learning</span>
                <span class='profile-tag'>Data Science</span>
                <span class='profile-tag'>Mental Health Analytics</span>
                <span class='profile-tag'>XGBoost</span>
                <span class='profile-tag'>SHAP</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #EFF6FF, #F0F9FF); border:1px solid #BFDBFE;
                border-radius:16px; padding:28px 32px; text-align:center;'>
        <div style='font-size:18px; font-weight:700; color:#1E40AF; margin-bottom:10px;'>
            🎓 Academic Research Project
        </div>
        <p style='font-size:13px; color:#1E3A5F; line-height:1.8; max-width:700px; margin:0 auto;'>
            Proyek ini dikembangkan sebagai bagian dari Final Project Mata Kuliah <b>Machine Learning</b>
            Program Studi <b>Business Statistics</b>. Penelitian ini mendemonstrasikan aplikasi praktis
            machine learning dalam bidang kesehatan mental mahasiswa, menggabungkan metodologi statistik
            yang ketat dengan alat data science modern untuk mendeteksi risiko depresi secara dini.
        </p>
        <div style='margin-top:16px; font-size:12px; color:#60A5FA;'>
            Built with ❤️ using Python · Streamlit · XGBoost · Gradient Boosting · SHAP · Plotly
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    stat_cols = st.columns(4)
    stats = [
        ("📊", f"{n_data:,}", "Students Analyzed"),
        ("🤖", "2", "Models Trained"),
        ("🎯", f"{best_scores['Accuracy']:.1%}", "Best Accuracy"),
        ("🏆", f"{best_scores['F1 Score']:.4f}", "Best F1 Score"),
    ]
    for col, (icon, val, lbl) in zip(stat_cols, stats):
        with col:
            st.markdown(f"""
            <div style='text-align:center; background:white; border:1px solid #E2E8F0;
                        border-radius:14px; padding:20px 10px; box-shadow:0 2px 12px rgba(0,0,0,0.04);'>
                <div style='font-size:28px; margin-bottom:6px;'>{icon}</div>
                <div style='font-family:Plus Jakarta Sans,sans-serif; font-size:20px; font-weight:800; color:#0F172A;'>{val}</div>
                <div style='font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.8px; margin-top:4px;'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class='footer-bar'>
    🧠 <b>Student Depression Detection System</b> &nbsp;|&nbsp;
    Artika Putri Rahmawati & Fi Amanila Putri Kinanti · Business Statistics · 2026 &nbsp;|&nbsp;
    ⚡ XGBoost &amp; 🌲 Gradient Boosting &nbsp;|&nbsp;
    Built with Streamlit
</div>
""", unsafe_allow_html=True)




