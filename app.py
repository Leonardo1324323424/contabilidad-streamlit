import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Contabilidad - MVP", layout="wide")

st.title("CONTABILIDAD - MVP")
st.success("✅ VS Code + .venv + Streamlit funcionando")

# --- Estado (memoria) ---
if "movs" not in st.session_state:
    st.session_state.movs = pd.DataFrame(
        columns=["Fecha", "Tipo", "Concepto", "Monto"]
    )

# --- Formulario ---
st.subheader("Registrar movimiento")

with st.form("form_mov", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([1, 1, 3, 1])

    fecha = col1.date_input("Fecha", value=date.today())
    tipo = col2.selectbox("Tipo", ["Ingreso", "Gasto"])
    concepto = col3.text_input("Concepto", placeholder="Ej: Sueldo, Pasajes, Comida…")
    monto = col4.number_input("Monto", min_value=0.0, step=1.0)

    submitted = st.form_submit_button("➕ Agregar")

if submitted:
    if concepto.strip() == "":
        st.error("⚠️ Escribe un concepto.")
    elif monto <= 0:
        st.error("⚠️ El monto debe ser mayor a 0.")
    else:
        nuevo = pd.DataFrame([{
            "Fecha": fecha,
            "Tipo": tipo,
            "Concepto": concepto.strip(),
            "Monto": float(monto),
        }])
        st.session_state.movs = pd.concat([st.session_state.movs, nuevo], ignore_index=True)
        st.success("✅ Movimiento agregado.")

# --- Resumen ---
df = st.session_state.movs.copy()

st.subheader("Resumen")
colA, colB, colC = st.columns(3)

total_ing = df.loc[df["Tipo"] == "Ingreso", "Monto"].sum()
total_gas = df.loc[df["Tipo"] == "Gasto", "Monto"].sum()
balance = total_ing - total_gas

colA.metric("Ingresos", f"S/ {total_ing:,.2f}")
colB.metric("Gastos", f"S/ {total_gas:,.2f}")
colC.metric("Balance", f"S/ {balance:,.2f}")

# --- Tabla ---
st.subheader("Movimientos")
st.dataframe(df, width="stretch", hide_index=True)

# --- Descargar ---
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Descargar CSV",
    data=csv,
    file_name="movimientos.csv",
    mime="text/csv"
)

# --- Botón limpiar ---
if st.button("🗑️ Borrar todo"):
    st.session_state.movs = df.iloc[0:0].copy()
    st.warning("Se borraron los movimientos.")
