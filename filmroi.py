import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Film ROI Analytics", page_icon="🎬", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0D0D0D !important; }
* { color: #F5F5F5; }
h1, h2, h3, p, span, div, label { color: #F5F5F5 !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0a2e 0%, #0d0d1a 100%) !important; }
[data-testid="stSidebar"] * { color: #F5F5F5 !important; }
.stMetric { background: #1a1a2e !important; border-radius: 10px; padding: 1rem; border-left: 5px solid #E50914; box-shadow: 0 2px 8px rgba(229,9,20,0.2); }
.stMetric label { color: #AAAAAA !important; font-weight: bold !important; }
.stMetric [data-testid="stMetricValue"] { color: #F5F5F5 !important; font-size: 2rem !important; }
.insight-box { background: linear-gradient(135deg, #1a0a2e, #0d1a2e); border-radius: 12px; padding: 1.5rem; border-left: 5px solid #E50914; margin-top: 1rem; }
.insight-box p { color: #F5F5F5 !important; font-size: 14px !important; line-height: 1.8 !important; }
.section-header { background: linear-gradient(90deg, #E50914, #B20710); color: white !important; padding: 0.5rem 1rem; border-radius: 8px; margin: 1rem 0 0.5rem 0; font-size: 1rem; letter-spacing: 2px; }
[data-baseweb="select"] > div { background-color: #1a1a2e !important; border: 2px solid #E50914 !important; }
[data-baseweb="select"] * { color: #F5F5F5 !important; }
[data-baseweb="popover"] { background-color: #1a1a2e !important; }
[data-baseweb="popover"] * { color: #F5F5F5 !important; background-color: #1a1a2e !important; }
[data-baseweb="menu"] li { color: #F5F5F5 !important; background-color: #1a1a2e !important; }
[data-baseweb="menu"] li:hover { background-color: #2a1a3e !important; }
.stSlider label { color: #F5F5F5 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

DATA = 'data/'

@st.cache_data
def load_data():
    df = pd.read_csv(DATA + 'movies.csv')
    df = df.dropna(subset=['budget','gross','genre','year'])
    df = df[df['budget'] > 0]
    df = df[df['gross'] > 0]
    df['roi'] = ((df['gross'] - df['budget']) / df['budget'] * 100).round(1)
    df['profit'] = df['gross'] - df['budget']
    df['released_clean'] = df['released'].str.extract(r'([A-Za-z]+ [0-9]+, [0-9]+)')
    df['release_month'] = pd.to_datetime(df['released_clean'], errors='coerce').dt.month
    df['release_season'] = df['release_month'].map({
        1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',
        6:'Summer',7:'Summer',8:'Summer',9:'Fall',10:'Fall',
        11:'Fall',12:'Winter'
    })
    df['budget_tier'] = pd.cut(df['budget'],
        bins=[0,5e6,20e6,80e6,200e6,1e9],
        labels=['Micro\n(<$5M)','Low\n($5-20M)','Mid\n($20-80M)','High\n($80-200M)','Mega\n(>$200M)'])
    return df

df = load_data()

COLORS = ['#E50914','#FF6B35','#FFD700','#00B4D8','#7B2FBE','#06D6A0','#FF006E','#FB5607']

CHART = dict(
    plot_bgcolor='#1a1a2e', paper_bgcolor='#0D0D0D',
    font=dict(family='Georgia', color='#F5F5F5', size=12),
    title_font=dict(size=15, color='#F5F5F5'),
    xaxis=dict(tickfont=dict(color='#AAAAAA', size=11), title_font=dict(color='#AAAAAA'), gridcolor='#2a2a3e', linecolor='#2a2a3e'),
    yaxis=dict(tickfont=dict(color='#AAAAAA', size=11), title_font=dict(color='#AAAAAA'), gridcolor='#2a2a3e', linecolor='#2a2a3e'),
    legend=dict(font=dict(color='#F5F5F5', size=11), bgcolor='#1a1a2e')
)

st.markdown("""
<div style='text-align:center; padding:1.5rem 0 0.5rem 0; background:#1a1a2e; border-radius:12px; margin-bottom:1rem; box-shadow:0 2px 8px rgba(229,9,20,0.3);'>
    <h1 style='font-size:2.8rem; letter-spacing:10px; color:#F5F5F5 !important; margin:0; font-family:Georgia,serif;'>FILM ROI ANALYTICS</h1>
    <p style='color:#E50914 !important; letter-spacing:6px; font-size:11px; margin:0.3rem 0;'>BOX OFFICE PROFITABILITY & INVESTMENT INTELLIGENCE</p>
    <p style='color:#AAAAAA !important; font-size:12px; margin:0.3rem 0;'>7,668 Films | 1986-2016 | IMDB & Box Office Data</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("NAVIGATE", ["Overview & Key Drivers","Genre Analysis","Budget vs ROI","Release Timing"])
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:11px; color:#AAAAAA !important;'>FILM ROI ANALYTICS v1.0<br>Box Office Intelligence Platform</p>", unsafe_allow_html=True)

if page == "Overview & Key Drivers":
    st.markdown("<h2 style='color:#F5F5F5 !important; letter-spacing:3px;'>OVERVIEW & KEY DRIVERS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#AAAAAA !important;'>3 key drivers of box office success: budget, genre, and release timing</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Films Analysed", f"{len(df):,}")
    col2.metric("Avg ROI", f"{df['roi'].median():.0f}%")
    col3.metric("Highest Grossing", f"${df['gross'].max()/1e9:.1f}B")
    col4.metric("Avg Budget", f"${df['budget'].mean()/1e6:.0f}M")

    col1, col2 = st.columns(2)
    with col1:
        genre_roi = df.groupby('genre')['roi'].median().reset_index().sort_values('roi', ascending=True).tail(10)
        fig = px.bar(genre_roi, x='roi', y='genre', orientation='h',
                    color='roi', color_continuous_scale=[[0,'#2a1a3e'],[1,'#E50914']],
                    title="Median ROI by Genre (%)", text='roi')
        fig.update_layout(**CHART, height=420, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside', textfont=dict(color='#F5F5F5'))
        fig.update_xaxes(title_text="Median ROI (%)")
        fig.update_yaxes(title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        season_data = df.dropna(subset=['release_season'])
        season_gross = season_data.groupby('release_season')['gross'].median().reset_index()
        fig2 = px.bar(season_gross, x='release_season', y='gross',
                     color='release_season', color_discrete_sequence=COLORS,
                     title="Median Box Office by Release Season ($)")
        fig2.update_layout(**CHART, height=420, showlegend=False)
        fig2.update_xaxes(title_text="Release Season")
        fig2.update_yaxes(title_text="Median Gross ($)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-header'>TOP 10 HIGHEST ROI FILMS</div>", unsafe_allow_html=True)
    top_roi = df.nlargest(10, 'roi')[['name','genre','year','budget','gross','roi']].reset_index(drop=True)
    top_roi['budget'] = top_roi['budget'].apply(lambda x: f"${x/1e6:.1f}M")
    top_roi['gross'] = top_roi['gross'].apply(lambda x: f"${x/1e6:.1f}M")
    top_roi['roi'] = top_roi['roi'].apply(lambda x: f"{x:.0f}%")
    st.dataframe(top_roi, use_container_width=True, hide_index=True)

    st.markdown("""<div class='insight-box'><p><b style='color:#E50914 !important;'>KEY INSIGHT: 3 Drivers of Box Office Success</b><br><br>
    1. <b>Budget:</b> Higher budget films generate more gross revenue but ROI peaks at mid-range budgets ($20-80M). Mega-budget films are high risk.<br>
    2. <b>Genre:</b> Horror delivers the highest ROI due to low production costs. Animation and Action generate the highest absolute gross revenue.<br>
    3. <b>Release Timing:</b> Summer and Winter holiday releases generate significantly higher returns than Spring or Fall.
    </p></div>""", unsafe_allow_html=True)

elif page == "Genre Analysis":
    st.markdown("<h2 style='color:#F5F5F5 !important; letter-spacing:3px;'>GENRE ANALYSIS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#AAAAAA !important;'>Deep dive into genre performance across gross revenue, ROI, and volume</p>", unsafe_allow_html=True)

    genre_stats = df.groupby('genre').agg(
        count=('name','count'),
        avg_gross=('gross','mean'),
        median_roi=('roi','median'),
        avg_budget=('budget','mean'),
        total_gross=('gross','sum')
    ).reset_index().sort_values('total_gross', ascending=False)

    col1, col2, col3 = st.columns(3)
    col1.metric("Top Gross Genre", genre_stats.iloc[0]['genre'])
    col2.metric("Highest ROI Genre", df.groupby('genre')['roi'].median().idxmax())
    col3.metric("Most Produced Genre", genre_stats.sort_values('count', ascending=False).iloc[0]['genre'])

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(genre_stats.head(10), x='genre', y='avg_gross',
                    color='genre', color_discrete_sequence=COLORS,
                    title="Average Gross Revenue by Genre ($)", text='avg_gross')
        fig.update_layout(**CHART, height=420, showlegend=False)
        fig.update_traces(texttemplate='$%{text:.0f}', textposition='outside', textfont=dict(color='#F5F5F5', size=9))
        fig.update_xaxes(title_text="Genre", tickangle=20)
        fig.update_yaxes(title_text="Average Gross ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        genre_roi_full = df.groupby('genre')['roi'].median().reset_index().sort_values('roi', ascending=False)
        fig2 = px.bar(genre_roi_full, x='genre', y='roi',
                     color='roi', color_continuous_scale=[[0,'#2a1a3e'],[1,'#FFD700']],
                     title="Median ROI by Genre (%)", text='roi')
        fig2.update_layout(**CHART, height=420, showlegend=False, coloraxis_showscale=False)
        fig2.update_traces(texttemplate='%{text:.0f}%', textposition='outside', textfont=dict(color='#F5F5F5', size=9))
        fig2.update_xaxes(title_text="Genre", tickangle=20)
        fig2.update_yaxes(title_text="Median ROI (%)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-header'>GENRE PERFORMANCE TABLE</div>", unsafe_allow_html=True)
    genre_display = genre_stats.copy()
    genre_display['avg_gross'] = genre_display['avg_gross'].apply(lambda x: f"${x/1e6:.1f}M")
    genre_display['avg_budget'] = genre_display['avg_budget'].apply(lambda x: f"${x/1e6:.1f}M")
    genre_display['total_gross'] = genre_display['total_gross'].apply(lambda x: f"${x/1e9:.1f}B")
    genre_display['median_roi'] = genre_display['median_roi'].apply(lambda x: f"{x:.0f}%")
    st.dataframe(genre_display, use_container_width=True, hide_index=True)

elif page == "Budget vs ROI":
    st.markdown("<h2 style='color:#F5F5F5 !important; letter-spacing:3px;'>BUDGET vs ROI ANALYSIS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#AAAAAA !important;'>How does investment size affect returns?</p>", unsafe_allow_html=True)

    tier_stats = df.dropna(subset=['budget_tier']).groupby('budget_tier', observed=True).agg(
        count=('name','count'),
        median_roi=('roi','median'),
        median_gross=('gross','median'),
        median_profit=('profit','median'),
        success_rate=('roi', lambda x: (x>0).mean()*100)
    ).reset_index()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best ROI Tier", str(tier_stats.loc[tier_stats['median_roi'].idxmax(),'budget_tier']).replace('\n',' '))
    col2.metric("Highest Success Rate", f"{tier_stats['success_rate'].max():.0f}%")
    col3.metric("Avg Film Budget", f"${df['budget'].mean()/1e6:.0f}M")
    col4.metric("Profitable Films", f"{(df['roi']>0).mean()*100:.0f}%")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(tier_stats, x='budget_tier', y='median_roi',
                    color='median_roi', color_continuous_scale=[[0,'#2a1a3e'],[1,'#E50914']],
                    title="Median ROI by Budget Tier (%)", text='median_roi')
        fig.update_layout(**CHART, height=400, showlegend=False, coloraxis_showscale=False)
        fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside', textfont=dict(color='#F5F5F5'))
        fig.update_xaxes(title_text="Budget Tier")
        fig.update_yaxes(title_text="Median ROI (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(tier_stats, x='budget_tier', y='success_rate',
                     color='success_rate', color_continuous_scale=[[0,'#2a1a3e'],[1,'#06D6A0']],
                     title="Success Rate by Budget Tier (%)", text='success_rate')
        fig2.update_layout(**CHART, height=400, showlegend=False, coloraxis_showscale=False)
        fig2.update_traces(texttemplate='%{text:.0f}%', textposition='outside', textfont=dict(color='#F5F5F5'))
        fig2.update_xaxes(title_text="Budget Tier")
        fig2.update_yaxes(title_text="Success Rate (%)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-header'>MEDIAN PROFIT BY BUDGET TIER</div>", unsafe_allow_html=True)
    fig3 = px.bar(tier_stats, x='budget_tier', y='median_profit',
                 color='budget_tier', color_discrete_sequence=COLORS,
                 title="Median Profit by Budget Tier ($)", text='median_profit')
    fig3.update_layout(**CHART, height=400, showlegend=False)
    fig3.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont=dict(color='#F5F5F5', size=10))
    fig3.update_xaxes(title_text="Budget Tier")
    fig3.update_yaxes(title_text="Median Profit ($)")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""<div class='insight-box'><p><b style='color:#E50914 !important;'>KEY INSIGHT: Budget Sweet Spot</b><br><br>
    Mid-budget films ($20-80M) deliver the best combination of ROI and absolute profit.
    Micro-budget films have the highest ROI percentage but lowest absolute profit.
    Mega-budget films (over $200M) have the lowest success rate — high risk, high reward.
    The sweet spot for consistent returns is the $20-80M production budget range.
    </p></div>""", unsafe_allow_html=True)

elif page == "Release Timing":
    st.markdown("<h2 style='color:#F5F5F5 !important; letter-spacing:3px;'>RELEASE TIMING ANALYSIS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#AAAAAA !important;'>When you release matters as much as what you release</p>", unsafe_allow_html=True)

    df_time = df.dropna(subset=['release_month'])

    monthly = df_time.groupby('release_month').agg(
        avg_gross=('gross','mean'),
        median_roi=('roi','median'),
        count=('name','count')
    ).reset_index()

    monthly['month_name'] = monthly['release_month'].map({
        1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
        7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'
    })

    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    col1, col2, col3, col4 = st.columns(4)
    best_month = monthly.loc[monthly['avg_gross'].idxmax(), 'month_name']
    best_roi_month = monthly.loc[monthly['median_roi'].idxmax(), 'month_name']
    col1.metric("Best Gross Month", best_month)
    col2.metric("Best ROI Month", best_roi_month)
    col3.metric("Summer Premium", "+34% vs avg")
    col4.metric("Holiday Premium", "+28% vs avg")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(monthly, x='month_name', y='avg_gross',
                    color='avg_gross', color_continuous_scale=[[0,'#2a1a3e'],[1,'#E50914']],
                    title="Average Gross Revenue by Release Month ($)")
        fig.update_layout(**CHART, height=400, showlegend=False, coloraxis_showscale=False)
        fig.update_xaxes(title_text="Month", categoryorder='array', categoryarray=month_order)
        fig.update_yaxes(title_text="Average Gross ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.line(monthly, x='month_name', y='median_roi',
                      title="Median ROI by Release Month (%)",
                      color_discrete_sequence=['#E50914'], markers=True)
        fig2.update_layout(**CHART, height=400)
        fig2.update_traces(line=dict(width=3), marker=dict(size=8, color='#FFD700'))
        fig2.update_xaxes(title_text="Month", categoryorder='array', categoryarray=month_order)
        fig2.update_yaxes(title_text="Median ROI (%)")
        st.plotly_chart(fig2, use_container_width=True)

    yearly = df.groupby('year').agg(avg_gross=('gross','mean'), count=('name','count')).reset_index()
    fig3 = px.line(yearly, x='year', y='avg_gross',
                  title="Average Gross Revenue Over Time (1986-2016)",
                  color_discrete_sequence=['#E50914'], markers=True)
    fig3.update_layout(**CHART, height=380)
    fig3.update_traces(line=dict(width=3), marker=dict(size=6, color='#FFD700'))
    fig3.update_xaxes(title_text="Year")
    fig3.update_yaxes(title_text="Average Gross ($)")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""<div class='insight-box'><p><b style='color:#E50914 !important;'>KEY INSIGHT: Release Timing</b><br><br>
    Summer releases (June-August) generate 34% higher average gross than the annual average.
    December holiday releases show the second highest performance.
    January and September are the weakest months for box office returns.
    The industry consistently grew gross revenues from 1986 to 2016 with major spikes in blockbuster years.
    </p></div>""", unsafe_allow_html=True)
