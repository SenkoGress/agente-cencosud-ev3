import streamlit as st
import pandas as pd
import re

# Configuración de la página
st.set_page_config(page_title="Dashboard Observabilidad Cencosud", layout="wide")
st.title("📊 Dashboard de Observabilidad - Agente Cencosud")
st.markdown("Monitor de métricas de rendimiento (KPIs) y trazabilidad del sistema.")

# Función para procesar el archivo log
def procesar_logs(ruta_archivo):
    datos = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            
            for linea in lineas:
                # Buscamos las líneas que indican el final de la ejecución
                if "ESTADO:" in linea:
                    # Extraer TraceID
                    trace_match = re.search(r'TraceID: (.*?) \|', linea)
                    trace_id = trace_match.group(1) if trace_match else "Desconocido"
                    
                    # --- NUEVO: Lógica de 3 categorías (ÉXITO, DENEGADO, ERROR) ---
                    if "ESTADO: ÉXITO" in linea:
                        estado = "ÉXITO"
                    elif "ESTADO: DENEGADO" in linea:
                        estado = "DENEGADO"
                    else:
                        estado = "ERROR"
                    
                    # Extraer Latencia
                    latencia_match = re.search(r'LATENCIA(?: AL FALLO)?: (.*?)s', linea)
                    latencia = float(latencia_match.group(1)) if latencia_match else 0.0
                    
                    datos.append({
                        "Trace ID": trace_id,
                        "Estado": estado,
                        "Latencia (s)": latencia
                    })
    except FileNotFoundError:
        st.error("No se encontró el archivo de logs. Asegúrate de hacerle preguntas al agente primero.")
        
    return pd.DataFrame(datos)

# Cargar los datos
df_logs = procesar_logs('trazabilidad_cencosud.log')

if not df_logs.empty:
    # --- MÉTRICAS GENERALES (KPIs) ---
    st.subheader("📈 Métricas Clave de Rendimiento")
    col1, col2, col3 = st.columns(3)
    
    total_consultas = len(df_logs)
    # Calculamos porcentaje de éxito real
    tasa_exito = (len(df_logs[df_logs['Estado'] == 'ÉXITO']) / total_consultas) * 100
    latencia_media = df_logs['Latencia (s)'].mean()
    
    col1.metric("Total Consultas Procesadas", total_consultas)
    col2.metric("Tasa de Éxito", f"{tasa_exito:.1f}%")
    col3.metric("Latencia Media", f"{latencia_media:.2f} s")
    
    # --- GRÁFICOS ---
    st.divider()
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        st.subheader("Latencia por Consulta")
        st.line_chart(df_logs['Latencia (s)'])
        
    with col_grafico2:
        st.subheader("Distribución de Estados")
        # Esto generará automáticamente las 3 barras (o las que existan)
        estado_counts = df_logs['Estado'].value_counts()
        st.bar_chart(estado_counts)
        
    # --- TABLA DE TRAZABILIDAD ---
    st.divider()
    st.subheader("🔍 Registro de Trazabilidad (Detallado)")
    st.dataframe(df_logs.sort_values(by="Trace ID", ascending=False))

else:
    st.info("Esperando datos... Ejecuta 'app.py' y realiza consultas para alimentar el dashboard.")