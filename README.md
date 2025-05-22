# 💊 Sistema de Gestión Inteligente de Medicinas

¡Bienvenido a mi proyecto de **asistente multiagente para gestión de medicinas**! 🧠💬  
Este sistema combina IA conversacional, recuperación de información y almacenamiento vectorial para facilitar el seguimiento de tratamientos médicos.

---

## 🌐 ¿Qué es este proyecto?

Un **asistente inteligente** que permite a los usuarios:

- Registrar pacientes, medicamentos y pastilleros semanales.
- Consultar qué medicina toma alguien un día y momento específico.
- Realizar preguntas generales sobre fármacos.

Todo con respuestas naturales y contextualizadas gracias a un modelo LLM y almacenamiento en **ChromaDB**.

---

## 🧠 Tecnología detrás del proyecto

### 🚀 Modelo de Lenguaje (LLM)

Este asistente utiliza **Gemini 2.0 Flash** a través de Gemini API, lo cual permite:

- ✅ Comprensión contextual de instrucciones médicas.
- ✅ Razonamiento lógico para respuestas clínicas simples.
- ✅ Generación de lenguaje natural explicativo.
- ✅ Gestión de múltiples tipos de interacción (registro, consulta, explicación).

---

### 🧠 Backend con FastAPI

La lógica del sistema está desarrollada con **[FastAPI](https://fastapi.tiangolo.com/)**.  
Permite:

- ⚙️ Endpoints REST eficientes y claros.
- 🔄 Procesamiento de entradas según intención (guardar, consultar, explicar).
- 💾 Interacción directa con ChromaDB para almacenar y recuperar datos médicos.

---

### 💾 Almacenamiento en ChromaDB

Utiliza **ChromaDB** como base de datos vectorial para:

- 📚 Almacenar registros de medicamentos por paciente.
- 🗂️ Guardar estructuras de pastillero (día y momento del día).
- 🔍 Recuperar información precisa y relevante en consultas.

---

### 💻 Interfaz en React

Interfaz moderna y conectada al backend con:

- 🧑‍⚕️ Panel para múltiples conversaciones.
- 💬 Registro de interacciones y seguimiento.
- ✅ UX intuitiva para usuarios sin experiencia técnica.

---

##  🧰 Stack Tecnológico

- FastAPI	        Backend REST para el sistema  
- ChromaDB	        Almacenamiento vectorial de datos médicos  
- Gemini           Conversacional avanzada  
- React.js	        Interfaz de usuario web  
- Python 🐍	        Lógica central del sistema  
- UUID	            Identificación única de conversaciones  

---

## 🧪 Ejemplo de uso

👤 Usuario:  
> Pilar toma amoxicilina los lunes por la tarde y paracetamol los miércoles por la mañana.  
> Juan toma ibuprofeno los martes por la noche y loratadina los jueves por la mañana.

🤖 Asistente:  
> Información guardada correctamente.

👤 Usuario:  
> ¿Qué toma Juan los jueves por la mañana?

🤖 Asistente:  
> Juan toma loratadina y naproxeno los jueves por la mañana.

---

## 🔐 Requisitos previos

- Python 3.9+
- API Key válida de Gemini

---

## ✨ Características destacadas

- ✅ Registro de pacientes y tratamientos con estructura tipo pastillero  
- ✅ Consultas por día y momento con precisión  
- ✅ Preguntas generales respondidas con contexto  
- ✅ Multi-agente y multi-conversación  
- ✅ Código limpio y modular, fácil de extender  

---

## 📌 Próximas mejoras

- Visualización gráfica del pastillero en React  
- Control de acceso por paciente o familiar  
- Soporte para múltiples idiomas  
- Recordatorios automáticos vía notificación  

---

## 📫 Contacto

¿Tienes dudas o sugerencias?  
Puedes escribirme por [LinkedIn](https://www.linkedin.com/in/daniel-foronda-melchor).

---

## ⭐ ¡Dale una estrella si te gustó el proyecto!

