# Sistema de Orquestación y Soporte Corporativo - Cencosud (EV3)

Este repositorio contiene la implementación de un sistema de **orquestación jerárquica** diseñado para automatizar y gestionar las consultas de los colaboradores sobre las normativas y reglamentos internos de **Cencosud**.

El sistema utiliza una arquitectura basada en **agentes de software especializados** y **procesamiento de lenguaje natural** para recuperar información documental y asegurar respuestas precisas y apegadas a la legalidad de la empresa.

Además, cuenta con **métricas de rendimiento**, **observabilidad** y **trazabilidad** integradas.

---

# Arquitectura del Sistema

La solución está construida sobre el framework **CrewAI**, implementando un flujo de tipo **`Process.hierarchical`** para garantizar la correcta toma de decisiones y la delegación automática de tareas.

### 1. Gerente de Recursos Humanos (Manager)

Actúa como **orquestador del sistema**.

- Recibe la consulta del usuario.
- Evalúa los requerimientos.
- Delega las tareas de búsqueda y redacción a los subprocesos correspondientes.

### 2. Analista Senior de Políticas Internas

Módulo técnico encargado de la recuperación de información.

Funciones:

- Utiliza búsqueda semántica mediante **FAISS**.
- Extrae fragmentos exactos de los reglamentos internos preprocesados.
- Entrega la información relevante al agente encargado de redactar la respuesta.

### 3. Especialista en Comunicaciones Internas

Módulo responsable del formato de salida.

Se encarga de:

- Generar respuestas estructuradas.
- Mantener claridad en la comunicación.
- Cumplir con las directrices corporativas de Cencosud.

---

# Requisitos Previos

Antes de ejecutar el proyecto asegúrate de contar con:

- **Python 3.10** o superior.
- **Git**.
- Un **Token de acceso Fine-grained** con permisos de ejecución en repositorios y modelos.

---

# Instalación y Configuración

## 1. Clonar el repositorio

```bash
git clone https://github.com/SenkoGress/agente-cencosud-ev3.git
cd agente-cencosud-ev3
```

---

## 2. Crear un entorno virtual

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

## 3. Activar el entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Configurar credenciales

Crear el archivo **`.env`** a partir de la plantilla.

### Windows

```bash
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Luego abre el archivo **`.env`** y completa las credenciales necesarias, por ejemplo:

- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- Otras variables requeridas por el proyecto.

---

# Ejecución

## Iniciar el asistente

```bash
python app.py
```

> Escribe **`salir`** en la terminal para finalizar la sesión.

---

## Dashboard de observabilidad

```bash
streamlit run dashboard.py
```

---

# Tecnologías Utilizadas

- **Python**
- **CrewAI**
- **FAISS**
- **Streamlit**
- **OpenAI**
- **GitHub API**

---

# Características

- Orquestación jerárquica mediante CrewAI.
- Recuperación de información utilizando FAISS.
- Procesamiento de lenguaje natural.
- Respuestas estructuradas y alineadas con las políticas internas.
- Dashboard de observabilidad.
- Métricas de rendimiento y trazabilidad.
