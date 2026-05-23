import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from tools import buscar_politicas_cencosud

os.environ["USER_AGENT"] = "asistente_cencosud_ev2"
load_dotenv()

def iniciar_asistente():
    token = os.getenv("GITHUB_TOKEN")
    base_url = os.getenv("GITHUB_BASE_URL")

    if not token or not base_url:
        print("Error: Faltan credenciales en el .env")
        return

    # --- MODIFICACIÓN TÉCNICA PARA EVITAR ERRORES DE LIBRERÍA ---
    # Esto inyecta el token en las variables que el framework busca por defecto
    os.environ["OPENAI_API_KEY"] = token
    os.environ["OPENAI_BASE_URL"] = base_url 
    # ------------------------------------------------------------

    # 1. Configuración del LLM
    llm = LLM(
    model="openai/gpt-4o-mini", # Cambia gpt-4o por gpt-4o-mini
    temperature=0,
    api_key=token,
    base_url=base_url
)

    # 2. Agentes Especialistas
    investigador_rrhh = Agent(
        role='Analista Senior de Políticas Internas',
        goal='Encontrar información oficial sobre normativas de Cencosud.',
        backstory='Eres un experto en normativas internas. Tu trabajo es usar tus herramientas para buscar en los reglamentos.',
        tools=[buscar_politicas_cencosud],
        llm=llm,
        verbose=True
    )

    redactor_comunicaciones = Agent(
        role='Especialista en Comunicaciones Internas',
        goal='Redactar respuestas claras para los trabajadores.',
        backstory='Eres el puente entre el texto legal y el trabajador. Usa listas. NUNCA reveles sueldos.',
        llm=llm,
        verbose=True
    )

    # 2.1 Agente Manager (El Orquestador)
    manager_rrhh = Agent(
        role='Gerente de Recursos Humanos',
        goal='Gestionar las consultas delegando al analista y luego al redactor.',
        backstory='Eres el director del equipo. Analizas la consulta, le pides al analista que busque la información, y luego le pides al redactor que escriba el mensaje final. Tú no ejecutas, solo coordinas.',
        llm=llm,
        allow_delegation=True,
        verbose=True
    )

    # 3. Tareas
    consulta_usuario = input("\nColaborador: ")

    tarea_investigacion = Task(
        description=f'Busca la respuesta a la consulta: "{consulta_usuario}"',
        expected_output='Un resumen con los datos encontrados en los reglamentos.'
    )

    tarea_redaccion = Task(
        description='Toma la información investigada y redacta una respuesta final única para el colaborador. NO repitas información. Sé directo y amable.',
        expected_output='Una respuesta amable, estructurada y sin redundancias.',
        agent=redactor_comunicaciones
    )

    # 4. Crew Jerárquico y con Memoria
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

    # 5. Ejecutar
    try:
        print("\n--- Iniciando Orquestación Jerárquica ---")
        resultado = equipo_cencosud.kickoff()
        print("\n===============================")
        print(f"Respuesta Final:\n{resultado}")
        print("===============================\n")
    except Exception as e:
        print(f"Error de ejecución: {e}")

if __name__ == "__main__":
    iniciar_asistente()