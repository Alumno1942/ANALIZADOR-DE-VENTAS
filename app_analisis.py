"""
App web de análisis de ventas con Streamlit.
El usuario sube un CSV y la app genera resumen + gráficas automáticamente.
Autor: Gadiel
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analizador de Ventas", page_icon="📊")

st.title("📊 Analizador de Ventas")
st.write("Sube tu archivo CSV de ventas y obtén un reporte automático.")

# El usuario sube su archivo desde el navegador
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)

    # Validamos que tenga las columnas que esperamos
    columnas_necesarias = {"fecha", "producto", "categoria", "cantidad", "precio_unitario"}
    if not columnas_necesarias.issubset(df.columns):
        st.error(
            f"Tu CSV debe tener estas columnas: {', '.join(columnas_necesarias)}"
        )
    else:
        df["total"] = df["cantidad"] * df["precio_unitario"]

        st.subheader("Resumen general")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de ventas", f"${df['total'].sum():,.2f}")
        col2.metric("Transacciones", len(df))
        col3.metric("Producto top", df.groupby("producto")["cantidad"].sum().idxmax())

        st.subheader("Ventas por categoría")
        resumen_categoria = df.groupby("categoria")["total"].sum().sort_values(ascending=False)
        st.bar_chart(resumen_categoria)

        st.subheader("Ventas por día")
        resumen_dia = df.groupby("fecha")["total"].sum()
        st.line_chart(resumen_dia)

        st.subheader("Datos completos")
        st.dataframe(df)
else:
    st.info("👆 Sube un archivo CSV para comenzar. Debe tener las columnas: fecha, producto, categoria, cantidad, precio_unitario")
