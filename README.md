Sistema de Orquestación y Soporte Corporativo - Cencosud (EV3)
Este repositorio contiene la implementación de un sistema de orquestación jerárquica diseñado para automatizar y gestionar las consultas de los colaboradores sobre las normativas y reglamentos internos de Cencosud.

El sistema utiliza una arquitectura basada en agentes de software especializados y procesamiento de lenguaje natural para recuperar información documental y asegurar respuestas precisas y apegadas a la legalidad de la empresa. Además, cuenta con métricas de rendimiento, observabilidad y trazabilidad integradas.

Arquitectura del Sistema
La solución está construida sobre el framework CrewAI, implementando un flujo de tipo Process.hierarchical para garantizar la correcta toma de decisiones y delegación de tareas automatizadas.

Gerente de Recursos Humanos (Manager): Actúa como orquestador del sistema. Recibe la consulta del usuario, evalúa los requerimientos y delega las tareas de búsqueda y redacción a los subprocesos correspondientes.

Analista Senior de Políticas Internas: Módulo técnico encargado de la recuperación de información. Utiliza herramientas de búsqueda semántica (FAISS) para extraer fragmentos exactos de los reglamentos internos preprocesados.

Especialista en Comunicaciones Internas: Módulo responsable del formato de salida. Genera respuestas estructuradas, claras y que cumplen con las directrices de comunicación corporativa.

Requisitos Previos
Python 3.10 o superior.

Git.

Token de acceso (Fine-grained) con permisos de ejecución en repositorios y modelos.

Instalación y Configuración
Clonar el repositorio:
git clone https://github.com/SenkoGress/agente-cencosud-ev3.git
cd agente-cencosud-ev3

Configurar el entorno:
Para Windows, crea el entorno con: python -m venv venv y actívalo con: venv\Scripts\activate.
Para Linux o Mac, crea el entorno con: python3 -m venv venv y actívalo con: source venv/bin/activate.

Instalar dependencias:
pip install -r requirements.txt

Configurar credenciales:
Crea el archivo de configuración a partir de la plantilla. En Windows usa: copy .env.example .env y en Linux o Mac usa: cp .env.example .env. Luego abre el archivo .env y completa las credenciales requeridas.

Ejecución
Para iniciar el asistente: python app.py (Escribe 'salir' en la terminal para terminar).

Para visualizar el dashboard de observabilidad: streamlit run dashboard.py
