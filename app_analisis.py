"""
App web de análisis de ventas con Streamlit.
Autor: Gadiel
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mis Ventas", page_icon="🧡", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2.5rem; }
    h1 { font-weight: 800; }
    [data-testid="stMetric"] {
        background-color: #FDE9D0;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #F3C98B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Mis Ventas")
st.write("Sube tu archivo de ventas y mira cómo te fue, sin fórmulas ni vueltas.")

archivo = st.file_uploader("Arrastra tu CSV aquí", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)

    columnas_necesarias = {"fecha", "producto", "categoria", "cantidad", "precio_unitario"}
    if not columnas_necesarias.issubset(df.columns):
        st.error(f"Tu archivo debe tener estas columnas: {', '.join(columnas_necesarias)}")
    else:
        df["total"] = df["cantidad"] * df["precio_unitario"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total vendido", f"${df['total'].sum():,.2f}")
        col2.metric("Ventas registradas", len(df))
        col3.metric("Lo que más se vende", df.groupby("producto")["cantidad"].sum().idxmax())

        st.write("")

        tab1, tab2, tab3 = st.tabs(["Por categoría", "Por día", "Tabla completa"])

        with tab1:
            resumen_categoria = df.groupby("categoria")["total"].sum().sort_values(ascending=False)
            st.bar_chart(resumen_categoria, color="#D97706")

        with tab2:
            resumen_dia = df.groupby("fecha")["total"].sum()
            st.line_chart(resumen_dia, color="#D97706")

        with tab3:
            st.dataframe(df, use_container_width=True)
else:
    st.caption("Tu archivo debe tener las columnas: fecha, producto, categoria, cantidad, precio_unitario")