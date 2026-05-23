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