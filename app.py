import os
import time
import uuid      # NUEVO: Para crear un Trace ID único como pide la materia
import logging   # NUEVO: Para guardar el registro de operaciones y errores
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools import buscar_politicas_cencosud, evaluar_normativa, generar_comunicado

# 1. (IE3 e IE4) CONFIGURACIÓN DE OBSERVABILIDAD Y LOGS LOCALES
# Esto creará un archivo .log donde se guardará todo lo que pasa "por debajo"
logging.basicConfig(
    filename='trazabilidad_cencosud.log',
    level=logging.INFO,
    format='%(asctime)s | TraceID: %(name)s | Nivel: %(levelname)s | %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger('Asistente_Cencosud')

os.environ["USER_AGENT"] = "asistente_cencosud_ev3"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

load_dotenv()

def iniciar_asistente():
    token = os.getenv("GITHUB_TOKEN")
    base_url = os.getenv("GITHUB_BASE_URL")

    if not token or not base_url:
        print("Error: Faltan credenciales en el .env")
        logger.error("Fallo de inicio: Faltan credenciales GITHUB_TOKEN o BASE_URL")
        return

    # (IE1, IE2) INTEGRACIÓN CON LANGSMITH (Opcional - Nube)
    # Si habilitamos esto y ponemos un LANGCHAIN_API_KEY en el .env, rastreará uso de tokens y costos.
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Cencosud_Agent_PRD"

    os.environ["OPENAI_API_KEY"] = token
    os.environ["OPENAI_BASE_URL"] = base_url 

    # Configuración del LLM
    llm = LLM(
        model="openai/gpt-4o-mini", 
        temperature=0,
        api_key=token,
        base_url=base_url
    )

    # Asignamos las herramientas a los Agentes
    investigador_rrhh = Agent(
        role='Analista Senior de Políticas Internas',
        goal='Encontrar información oficial sobre normativas de Cencosud.',
        backstory='Eres un experto en normativas internas. Tu trabajo es usar tus herramientas para buscar en los reglamentos.',
        tools=[buscar_politicas_cencosud, evaluar_normativa],
        llm=llm,
        verbose=True
    )

    redactor_comunicaciones = Agent(
        role='Especialista en Comunicaciones Internas',
        goal='Redactar respuestas claras para los trabajadores.',
        backstory='Eres el puente entre el texto legal y el trabajador. Usa listas. NUNCA reveles sueldos.',
        tools=[generar_comunicado],
        llm=llm,
        verbose=True
    )

    manager_rrhh = Agent(
        role='Gerente de Recursos Humanos',
        goal='Gestionar las consultas delegando al analista y luego al redactor.',
        backstory='Eres el director del equipo. Analizas la consulta, le pides al analista que busque la información, y luego le pides al redactor que escriba el mensaje final. Tú no ejecutas, solo coordinas.',
        llm=llm,
        allow_delegation=True,
        verbose=True
    )

    historial_conversacion = ""

    print("\n[Sistema]: Asistente Cencosud iniciado con Trazabilidad (Logs). Escribe 'salir' para terminar.")
    
    while True:
        consulta_usuario = input("\nColaborador: ")
        
        if consulta_usuario.lower() == 'salir':
            logger.info("Sesión finalizada por el usuario.")
            print("Cerrando asistente...")
            break

        # 2. (IE3) CREACIÓN DE IDENTIFICADOR ÚNICO (Trace ID)
        trace_id = str(uuid.uuid4())[:8] # Un código único para esta pregunta
        logger.name = trace_id
        
        logger.info(f"CONSULTA ENTRANTE: {consulta_usuario}")
        
        # 3. (IE2) MEDICIÓN DE LATENCIA (Cronómetro)
        tiempo_inicio = time.time()

        tarea_investigacion = Task(
            description=(
                f"Historial de conversación previo:\n{historial_conversacion if historial_conversacion else 'Ninguno todavía.'}\n\n"
                f"Nueva consulta del colaborador: '{consulta_usuario}'\n\n"
                "Instrucciones: Evalúa si la consulta cumple la normativa y luego busca la respuesta en los documentos oficiales."
            ),
            expected_output='Un resumen con los datos encontrados en los reglamentos.',
            agent=investigador_rrhh 
        )

        tarea_redaccion = Task(
            description='Toma la información investigada y usa tu herramienta de comunicado para redactar la respuesta final al colaborador. NO repitas información.',
            expected_output='Un comunicado oficial estructurado.',
            agent=redactor_comunicaciones
        )

        equipo_cencosud = Crew(
            agents=[investigador_rrhh, redactor_comunicaciones],
            tasks=[tarea_investigacion, tarea_redaccion],
            manager_agent=manager_rrhh,      
            process=Process.hierarchical,    
            memory=False,                    
            embedder={                       
                "provider": "openai",
                "config": {
                    "api_key": token,
                    "base_url": base_url,
                    "model": "text-embedding-3-small"
                }
            },
            verbose=True
        )

        try:
            print("\n--- Iniciando orquestación jerárquica ---")
            resultado = equipo_cencosud.kickoff()
            
            tiempo_fin = time.time()
            latencia = round(tiempo_fin - tiempo_inicio, 2)
            
           # --- CLASIFICADOR INTELIGENTE DE ESTADOS PARA EL DASHBOARD ---
            texto_resultado = str(resultado).lower()
            
            # Si la respuesta contiene palabras del filtro ético, se registra como DENEGADO
            if "privacidad" in texto_resultado or "seguridad" in texto_resultado or "no puedo" in texto_resultado:
                logger.warning(f"ESTADO: DENEGADO | LATENCIA: {latencia}s | RESPUESTA: {resultado}")
            else:
                logger.info(f"ESTADO: ÉXITO | LATENCIA: {latencia}s | RESPUESTA: {resultado}")
            # --------------------------------------------------------------------
            # --------------------------------------------------------------------
            
            historial_conversacion += f"Colaborador: {consulta_usuario}\nAsistente Cencosud: {resultado}\n\n"
            
            print("\n===============================")
            print(f"Respuesta final:\n{resultado}")
            print("===============================\n")
            
            time.sleep(1) 
            
        except Exception as e:
            tiempo_fin = time.time()
            latencia = round(tiempo_fin - tiempo_inicio, 2)
            logger.error(f"ESTADO: ERROR_SISTEMA | LATENCIA AL FALLO: {latencia}s | DETALLE: {str(e)}")
            print(f"Error de ejecución: {e}")

if __name__ == "__main__":
    iniciar_asistente()