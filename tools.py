import os
from crewai.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

@tool("Buscador de Politicas Cencosud")
def buscar_politicas_cencosud(consulta: str) -> str:
    """
    Busca información oficial en el reglamento interno, guía de beneficios 
    y políticas de vacaciones de Cencosud. 
    Usa esta herramienta siempre que necesites responder dudas sobre beneficios o normativas internas.
    """
    token = os.getenv("GITHUB_TOKEN")
    base_url = os.getenv("GITHUB_BASE_URL")
    
    if not token:
        return "Error: Credenciales no configuradas. Falla en el sistema."

    # 1. Inicializar el mismo modelo de embeddings que se usó en la ingesta
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=token,
        base_url=base_url
    )

    # 2. Conectar con la base de datos vectorial FAISS
    try:
        db = FAISS.load_local(
            "faiss_index_cencosud", 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        # 3. Realizar la búsqueda semántica (Retriever manual)
        resultados = db.similarity_search(consulta, k=3)
        
        # 4. Extraer el texto limpio para el Agente
        texto_recuperado = "\n\n---\n\n".join([doc.page_content for doc in resultados])
        
        return texto_recuperado

    except Exception as e:
        return f"Error crítico al acceder a la base de datos: {str(e)}. Verifica que faiss_index_cencosud exista."

# --- NUEVAS HERRAMIENTAS PARA CUMPLIR CON EL IE1 ---

@tool("evaluar_normativa")
def evaluar_normativa(consulta_usuario: str) -> str:
    """
    Evalúa si la consulta del empleado cumple o viola la normativa de privacidad de Cencosud.
    Útil para que el analista senior razone y valide la viabilidad de la pregunta antes de investigar.
    """
    consulta_lower = consulta_usuario.lower()
    # Validación lógica para proteger datos sensibles (Ley 19.628)
    if "sueldo" in consulta_lower or "liquidación" in consulta_lower or "remuneración" in consulta_lower or "bono" in consulta_lower:
        return "Evaluación de Riesgo: Alerta de Privacidad. La consulta involucra datos sensibles de remuneración. El agente debe indicar que por políticas de seguridad debe consultar el portal 'Mi Cencosud'."
    else:
        return "Evaluación de Riesgo: Aprobada. La consulta es viable y no viola leyes de privacidad. Procede a buscar en las políticas."

@tool("generar_comunicado")
def generar_comunicado(informacion_procesada: str) -> str:
    """
    Formatea la información investigada en un comunicado corporativo oficial de RRHH.
    Útil para el especialista en comunicaciones al redactar la respuesta final.
    """
    comunicado_oficial = (
        "Estimado colaborador de Cencosud,\n\n"
        "Junto con saludar, y en respuesta a su consulta, le informamos lo siguiente:\n\n"
        f"{informacion_procesada}\n\n"
        "Ante cualquier duda adicional, le recordamos que puede consultar directamente a su jefe de local o mediante el portal oficial 'Mi Cencosud'.\n\n"
        "Atentamente,\n"
        "Gerencia de Recursos Humanos."
    )
    return comunicado_oficial