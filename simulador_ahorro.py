import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Simulador de Ahorro con Capitalización", layout="centered")

# Título de la aplicación
st.title("Simulador de Ahorro con Capitalización")

# Contenedor principal con bordes y padding
with st.container():
    # Formulario para ingresar los datos
    col1, col2 = st.columns(2)
    
    with col1:
        monto_objetivo = st.number_input("¿Cuánto querés ahorrar? ($):", min_value=0.0, step=1000.0, format="%.2f")
    
    with col2:
        plazo_anios = st.number_input("¿En cuántos años?", min_value=1, max_value=50, step=1)
    
    # Frecuencia de aportes
    frecuencia_aporte = st.selectbox(
        "¿Cada cuánto aportás cuotas?",
        options=["Mensual", "Trimestral", "Semestral", "Anual"],
        index=0
    )
    
    # Tasa anual de inversión
    tasa_anual = st.number_input("Tasa anual de inversión (%):", min_value=0.0, max_value=100.0, value=5.0, step=0.5, format="%.2f")
    
    # Frecuencia de capitalización
    frecuencia_capitalizacion = st.selectbox(
        "¿Cada cuánto se capitaliza la tasa?",
        options=["Mensual", "Trimestral", "Semestral", "Anual"],
        index=2
    )
    
    # Diccionario de periodos por año según la frecuencia
    periodos = {
        "Mensual": 12,
        "Trimestral": 4,
        "Semestral": 2,
        "Anual": 1
    }
    
    # Botón de cálculo
    if st.button("Calcular"):
        if monto_objetivo > 0 and plazo_anios > 0:
            # Convertir tasa anual a decimal
            tasa_decimal = tasa_anual / 100
            
            # Calcular periodos totales y por capitalización
            periodos_aporte = periodos[frecuencia_aporte] * plazo_anios
            periodos_capitalizacion = periodos[frecuencia_capitalizacion]
            
            # Calcular tasa por periodo de capitalización
            tasa_periodo = (1 + tasa_decimal) ** (1 / periodos_capitalizacion) - 1
            
            # Calcular cuota periódica para alcanzar el monto objetivo
            # Usando la fórmula de valor futuro de una anualidad con capitalización compuesta
            periodos_totales = plazo_anios * periodos_capitalizacion
            periodos_por_aporte = periodos_capitalizacion / periodos[frecuencia_aporte]
            
            # Ajustar si los aportes son más frecuentes que la capitalización
            if periodos_por_aporte < 1:
                # En este caso, hay varios aportes antes de cada capitalización
                aportes_por_capitalizacion = periodos[frecuencia_aporte] / periodos_capitalizacion
                
                # Calcular la cuota considerando varios aportes por periodo de capitalización
                cuota = monto_objetivo / ((1 + tasa_periodo) ** periodos_totales - 1) * tasa_periodo / (1 - (1 + tasa_periodo) ** (-1))
                cuota = cuota / aportes_por_capitalizacion
            else:
                # Cuando la capitalización es más frecuente que los aportes
                factor = (1 + tasa_periodo) ** periodos_totales
                cuota = monto_objetivo * tasa_periodo / (factor - 1)
                # Ajustar la cuota si hay varias capitalizaciones entre aportes
                cuota = cuota * (1 + tasa_periodo) ** (periodos_por_aporte - 1)
            
            # Mostrar resultados
            st.success(f"Para alcanzar ${monto_objetivo:.2f} en {plazo_anios} años:")
            st.info(f"Debes aportar ${cuota:.2f} por {frecuencia_aporte.lower()}")
            
            # Calcular y mostrar detalles de la inversión
            total_aportado = cuota * periodos_aporte
            intereses_ganados = monto_objetivo - total_aportado
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total aportado", f"${total_aportado:.2f}")
            col2.metric("Intereses ganados", f"${intereses_ganados:.2f}")
            col3.metric("Monto final", f"${monto_objetivo:.2f}")
            
            # Crear tabla de evolución del ahorro
            st.subheader("Evolución del ahorro")
            
            # Inicializar variables para la simulación
            saldo = 0
            aportes_acumulados = 0
            intereses_acumulados = 0
            
            # Crear DataFrame para la tabla y gráfico
            data = []
            
            # Número de aportes por periodo de capitalización
            aportes_por_periodo = periodos[frecuencia_aporte] / periodos_capitalizacion
            
            # Simular la evolución del ahorro
            for periodo in range(1, periodos_totales + 1):
                # Aporte del periodo
                aporte_periodo = cuota * aportes_por_periodo
                aportes_acumulados += aporte_periodo
                
                # Aplicar interés al saldo anterior
                interes_periodo = saldo * tasa_periodo
                intereses_acumulados += interes_periodo
                
                # Actualizar saldo
                saldo = saldo + interes_periodo + aporte_periodo
                
                # Agregar datos al periodo correspondiente
                if periodo % (periodos_capitalizacion / periodos_capitalizacion) == 0:  # Para cada periodo de capitalización
                    data.append({
                        "Periodo": periodo,
                        "Tiempo": f"{periodo/periodos_capitalizacion:.1f} años",
                        "Aportes": aportes_acumulados,
                        "Intereses": intereses_acumulados,
                        "Saldo": saldo
                    })
            
            # Crear DataFrame y mostrar tabla
            df = pd.DataFrame(data)
            st.dataframe(df[["Periodo", "Tiempo", "Aportes", "Intereses", "Saldo"]].style.format({
                "Aportes": "${:.2f}",
                "Intereses": "${:.2f}",
                "Saldo": "${:.2f}"
            }))
            
            # Crear gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df["Periodo"], df["Saldo"], marker='o', linewidth=2, label="Saldo Total")
            ax.plot(df["Periodo"], df["Aportes"], marker='s', linewidth=2, label="Aportes")
            ax.plot(df["Periodo"], df["Intereses"], marker='^', linewidth=2, label="Intereses")
            
            ax.set_xlabel("Periodo")
            ax.set_ylabel("Monto ($)")
            ax.set_title("Evolución del Ahorro")
            ax.legend()
            ax.grid(True)
            
            # Mostrar gráfico
            st.pyplot(fig)
            
        else:
            st.error("Por favor, ingresa valores válidos para el monto objetivo y el plazo.")

# Información adicional
with st.expander("Acerca de este simulador"):
    st.write("""
    Este simulador te permite calcular cuánto necesitas ahorrar periódicamente para alcanzar un monto objetivo en un plazo determinado,
    considerando una tasa de interés y diferentes frecuencias de aporte y capitalización.
    
    - **Monto objetivo**: Es la cantidad total que deseas alcanzar.
    - **Plazo**: El tiempo en años para alcanzar el objetivo.
    - **Frecuencia de aporte**: Cada cuánto realizarás aportes.
    - **Tasa anual**: La tasa de interés anual que se aplicará a tu ahorro.
    - **Frecuencia de capitalización**: Cada cuánto se calculan y añaden los intereses al capital.
    
    La fórmula utilizada corresponde al cálculo de valor futuro de una anualidad con capitalización compuesta.
    """)
