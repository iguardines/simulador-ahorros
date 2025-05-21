import streamlit as st
from math import pow

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Ahorro con Capitalización",
    layout="centered"
)

# Título principal
st.title("Simulador de Ahorro con Capitalización")

# Interfaz de usuario
monto_objetivo = st.number_input("¿Cuánto querés ahorrar? ($):", min_value=0.0, step=1000.0)
anios = st.number_input("¿En cuántos años?", min_value=1, step=1)
frec_aporte = st.selectbox("¿Cada cuánto aportás cuotas?", 
                         ["Mensual", "Trimestral", "Semestral", "Anual"])
tasa_anual = st.number_input("Tasa anual de inversión (%):", min_value=0.0, step=0.5)
capitalizacion = st.selectbox("¿Cada cuánto se capitaliza la tasa?", 
                            ["Mensual", "Trimestral", "Semestral", "Anual"])

# Botón para calcular
if st.button("Calcular cuota"):
    try:
        # Convertir tasa a decimal
        tasa_anual = tasa_anual / 100
        
        # Diccionario para convertir frecuencia a número
        frec_dict = {"mensual": 12, "trimestral": 4, "semestral": 2, "anual": 1}
        
        # Obtener valores numéricos
        pagos_anuales = frec_dict.get(frec_aporte.lower())
        cap_anual = frec_dict.get(capitalizacion.lower())
        
        # Calcular la tasa efectiva por período
        tasa_efectiva = pow(1 + tasa_anual / cap_anual, cap_anual / pagos_anuales) - 1
        
        # Calcular el total de pagos
        total_pagos = pagos_anuales * anios
        
        # Calcular la cuota
        factor = pow(1 + tasa_efectiva, total_pagos) - 1
        cuota = monto_objetivo * tasa_efectiva / factor
        
        # Mostrar el resultado
        st.success(f"Necesitás aportar: ${cuota:,.2f} por período")
        
        # Información adicional
        st.info(f"""
        **Detalles del cálculo:**
        - Monto objetivo: ${monto_objetivo:,.2f}
        - Plazo: {anios} años ({total_pagos} aportes {frec_aporte.lower()}s)
        - Tasa anual: {tasa_anual*100:.2f}% (capitalización {capitalizacion.lower()})
        - Tasa efectiva por período: {tasa_efectiva*100:.4f}%
        """)
        
    except Exception as e:
        st.error(f"Error en el cálculo: {str(e)}")
        st.info("Por favor, verifica los valores ingresados.")
