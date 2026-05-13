
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Explorador de soluciones IA para Intercom", page_icon="🧭", layout="wide")

SOLUTIONS = [
    {
        "id": "openai_custom_api",
        "nombre": "OpenAI / Azure OpenAI + Intercom API + Webhooks",
        "categoria": "Código / Backend propio",
        "nivel": "Avanzado",
        "costo": "Medio-Alto",
        "tiempo": "2 a 8 semanas",
        "mejor_para": "Cliente que no quiere Fin y necesita control total del bot, reglas, prompts, base de conocimiento y escalamiento.",
        "descripcion": "Crear un backend propio en Python/FastAPI que reciba eventos de Intercom por Webhook, consulte una base de conocimiento, llame a OpenAI/Azure OpenAI y responda o escale a un agente.",
        "arquitectura": "Intercom Messenger -> Webhook Intercom -> Backend Python -> Base de conocimiento/RAG -> OpenAI/Azure OpenAI -> Respuesta en Intercom o asignación a agente",
        "pros": ["Máximo control", "Permite preguntas abiertas", "Se conecta con CRM/ERP/BD", "Reglas personalizadas de espera y escalamiento", "Puede usar modelos distintos a Fin"],
        "contras": ["Requiere desarrollo", "Debe manejar seguridad, tokens, logs, límites API y errores", "Necesita mantenimiento"],
        "pasos": [
            "Crear una app privada en Intercom Developer Hub y obtener token.",
            "Configurar Webhooks de Intercom para eventos de conversación/mensaje.",
            "Crear backend en Python con FastAPI o Flask.",
            "Construir base de conocimiento: FAQs, horarios, políticas, sedes, pagos, garantías.",
            "Agregar búsqueda semántica/RAG si hay documentos extensos.",
            "Llamar a OpenAI/Azure OpenAI con prompt seguro y contexto recuperado.",
            "Si la respuesta tiene baja confianza, contiene palabras sensibles o el cliente pide humano, asignar a equipo/agente.",
            "Si cola alta o espera > 60 segundos, enviar mensaje de alta demanda.",
            "Guardar métricas: resuelto por bot, escalado, tiempo de respuesta, temas frecuentes.",
            "Probar con conversaciones reales antes de producción."
        ],
        "ejemplo": "Cliente: ¿Cuál es el horario?\nBot: Nuestro horario es lunes a viernes de 8:00 a.m. a 6:00 p.m.\n\nCliente: Quiero poner una queja por facturación\nBot: Voy a transferirte con un agente para revisar tu caso con seguridad.",
        "recomendacion": "La mejor opción si el cliente quiere una alternativa robusta a Fin y tiene equipo técnico o presupuesto para desarrollo."
    },
    {
        "id": "zapier_openai",
        "nombre": "Zapier + Intercom + ChatGPT/OpenAI",
        "categoria": "No-code / Low-code",
        "nivel": "Básico-Medio",
        "costo": "Medio",
        "tiempo": "1 a 5 días",
        "mejor_para": "Prototipo rápido o automatizaciones simples sin desarrollar backend completo.",
        "descripcion": "Crear Zaps donde un evento de Intercom dispara una acción en ChatGPT/OpenAI y luego se usa Intercom o Webhooks para registrar nota, sugerir respuesta o actualizar ticket/conversación.",
        "arquitectura": "Intercom Trigger -> Zapier -> ChatGPT/OpenAI Action -> Intercom Action/Webhook -> Nota, respuesta o escalamiento",
        "pros": ["Rápido", "No requiere mucho código", "Fácil de demostrar", "Conecta muchas apps"],
        "contras": ["Puede quedarse corto para lógica compleja", "Costos por tareas", "Menor control de seguridad y reintentos", "Responder directamente en conversaciones puede requerir acciones/API avanzadas"],
        "pasos": [
            "Crear cuenta en Zapier y conectar Intercom.",
            "Crear Zap con trigger de Intercom: nueva conversación, ticket o evento disponible.",
            "Agregar acción ChatGPT/OpenAI para clasificar intención o generar respuesta.",
            "Agregar filtros: si es FAQ responder/sugerir; si es reclamo/factura/cancelación escalar.",
            "Agregar acción Intercom: crear nota, actualizar ticket, aplicar tag o usar Webhook/API para responder.",
            "Agregar paso de alta demanda: si hay tag/cola/condición, enviar mensaje de espera.",
            "Probar con 20-50 preguntas reales y ajustar prompts.",
            "Publicar Zap y monitorear errores."
        ],
        "ejemplo": "Trigger: Nueva conversación en Intercom\nAction 1: ChatGPT clasifica intención\nAction 2: Si intención = horario, generar respuesta\nAction 3: Intercom aplica tag 'respondido_bot' o envía respuesta vía API/Webhook",
        "recomendacion": "Muy buena opción para una demo rápida, pero no la dejaría como solución crítica si el volumen es alto o hay reglas complejas."
    },
    {
        "id": "make_openai",
        "nombre": "Make.com + Intercom + OpenAI",
        "categoria": "No-code / Automatización visual",
        "nivel": "Medio",
        "costo": "Medio",
        "tiempo": "2 a 10 días",
        "mejor_para": "Flujos visuales más flexibles que Zapier, con routers, filtros, escenarios y HTTP/API personalizados.",
        "descripcion": "Diseñar escenarios en Make que reciban eventos de Intercom, llamen a OpenAI, consulten Google Sheets/Notion/Airtable como base de conocimiento y actualicen Intercom.",
        "arquitectura": "Intercom/Webhook -> Make Scenario -> Router de intención -> OpenAI + Knowledge Base -> Intercom API",
        "pros": ["Muy visual", "Más flexible para escenarios complejos", "Buen manejo de routers/filtros", "Puede usar HTTP para endpoints no soportados"],
        "contras": ["Requiere buena configuración", "Puede ser frágil si cambian campos/API", "Costos por operaciones", "No reemplaza totalmente un backend robusto"],
        "pasos": [
            "Crear escenario en Make.",
            "Configurar módulo Intercom o Webhook personalizado.",
            "Agregar router: FAQ, alta demanda, escalar, pregunta abierta.",
            "Conectar base de conocimiento en Google Sheets/Notion/Airtable o HTTP.",
            "Agregar módulo OpenAI para generar respuesta controlada.",
            "Responder, etiquetar o asignar conversación usando Intercom/API.",
            "Crear manejo de errores y reintentos.",
            "Activar escenario y monitorear operaciones."
        ],
        "ejemplo": "Router 1: pregunta contiene 'horario' -> respuesta fija\nRouter 2: contiene 'factura' -> asignar a agente\nRouter 3: otra pregunta -> OpenAI + base de conocimiento",
        "recomendacion": "Buena alternativa si el cliente quiere no-code pero con más control visual que Zapier."
    },
    {
        "id": "n8n_openai",
        "nombre": "n8n + Intercom + OpenAI",
        "categoria": "Low-code / Self-hosted opcional",
        "nivel": "Medio-Avanzado",
        "costo": "Bajo-Medio",
        "tiempo": "1 a 3 semanas",
        "mejor_para": "Equipos que quieren automatización visual pero con opción de self-hosting, control técnico y nodos HTTP/API.",
        "descripcion": "Usar n8n para recibir eventos, consultar OpenAI, ejecutar lógica, llamar REST APIs y mantener más control que Zapier/Make.",
        "arquitectura": "Intercom Trigger/Webhook -> n8n Workflow -> OpenAI Node/HTTP -> Reglas -> Intercom Node/API",
        "pros": ["Puede ser self-hosted", "Flexible", "Bueno para integraciones API", "Menor dependencia de plataformas cerradas"],
        "contras": ["Requiere administración si se autohospeda", "Necesita conocimiento técnico", "Hay que cuidar seguridad y disponibilidad"],
        "pasos": [
            "Crear workflow en n8n.",
            "Agregar trigger de Intercom o Webhook.",
            "Agregar nodo OpenAI para clasificar/generar respuesta.",
            "Agregar IF/Switch para FAQ, alta demanda y escalamiento.",
            "Usar nodo Intercom o HTTP Request para responder/asignar/taggear.",
            "Guardar logs en Google Sheets/DB.",
            "Probar y activar."
        ],
        "ejemplo": "Webhook recibe mensaje -> OpenAI clasifica -> IF horario responde -> IF baja confianza asigna a soporte humano",
        "recomendacion": "Muy buena opción si quieren evitar Fin y tener una solución flexible con menor código que backend propio."
    },
    {
        "id": "botpress_custom",
        "nombre": "Botpress / Voiceflow / plataforma chatbot + Intercom",
        "categoria": "Plataforma chatbot",
        "nivel": "Medio",
        "costo": "Medio-Alto",
        "tiempo": "1 a 4 semanas",
        "mejor_para": "Equipos que prefieren diseñar flujos conversacionales visuales con IA y luego conectar Intercom.",
        "descripcion": "Construir el bot en una plataforma especializada de chatbot/IA y conectarlo a Intercom con API, Webhook o integración disponible.",
        "arquitectura": "Intercom -> Webhook/API -> Plataforma chatbot -> Knowledge Base/LLM -> Intercom handoff",
        "pros": ["Diseño visual de conversaciones", "Manejo de intenciones", "Puede tener analítica", "Menos código que backend propio"],
        "contras": ["Costo adicional", "Dependencia del proveedor", "Integración con Intercom puede requerir API custom"],
        "pasos": [
            "Elegir plataforma chatbot.",
            "Crear intents: horarios, pagos, precios, sedes, soporte, agente humano.",
            "Cargar base de conocimiento.",
            "Configurar webhook/API con Intercom.",
            "Definir fallback y handoff a agente.",
            "Probar conversaciones y publicar."
        ],
        "ejemplo": "Flujo visual: saludo -> pregunta abierta -> intent detection -> respuesta FAQ o handoff",
        "recomendacion": "Buena si el cliente quiere administrar flujos sin depender siempre de desarrollo."
    },
    {
        "id": "rag_assistant",
        "nombre": "Asistente RAG con documentos internos + Intercom",
        "categoria": "IA documental",
        "nivel": "Avanzado",
        "costo": "Medio-Alto",
        "tiempo": "3 a 8 semanas",
        "mejor_para": "Empresas con muchos documentos, políticas, manuales o preguntas abiertas que no caben en un FAQ simple.",
        "descripcion": "Crear un sistema RAG: indexar documentos, buscar fragmentos relevantes y generar respuesta con citas internas. Si no encuentra evidencia, escala a agente.",
        "arquitectura": "Intercom -> Backend -> Vector DB/Buscador -> LLM -> Respuesta con fuente o handoff",
        "pros": ["Mejor para preguntas abiertas", "Reduce alucinaciones si se exige evidencia", "Escalable a muchos documentos"],
        "contras": ["Más desarrollo", "Hay que limpiar documentos", "Requiere evaluación continua"],
        "pasos": [
            "Recolectar documentos oficiales.",
            "Limpiar y dividir documentos en fragmentos.",
            "Crear embeddings y almacenarlos en vector DB o buscador.",
            "Recibir mensaje de Intercom vía Webhook.",
            "Buscar contexto relevante.",
            "Generar respuesta solo con información encontrada.",
            "Si no hay evidencia suficiente, escalar a agente.",
            "Medir precisión y actualizar base."
        ],
        "ejemplo": "Cliente pregunta política de garantía -> Bot busca política oficial -> responde y si no encuentra el producto exacto escala.",
        "recomendacion": "Ideal si las respuestas deben ser confiables y basadas en documentos internos."
    }
]

FAQ = {
    "horario": "Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.",
    "horarios": "Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.",
    "precio": "Para darte precios exactos necesito saber el producto o servicio. Si quieres, te conecto con un agente comercial.",
    "ubicacion": "Compártenos tu ciudad y te indicamos la sede o canal más cercano.",
    "ubicación": "Compártenos tu ciudad y te indicamos la sede o canal más cercano.",
    "pago": "Aceptamos los métodos de pago definidos por la empresa. Un agente puede confirmar el detalle según tu caso."
}
ESCALATION_KEYWORDS = ["reclamo", "queja", "cancelar", "devolución", "devolucion", "factura", "garantía", "garantia", "asesor", "humano", "agente"]

st.title("🧭 Explorador de soluciones IA para Intercom sin usar Fin")
st.caption("Prototipo investigativo para comparar OpenAI, Zapier, Make, n8n, plataformas chatbot y backend propio.")

with st.sidebar:
    st.header("🔎 Filtros de investigación")
    texto = st.text_input("Buscar opción", placeholder="Ej: OpenAI, Zapier, Make, n8n, RAG")
    categorias = sorted(set(s["categoria"] for s in SOLUTIONS))
    categoria = st.selectbox("Categoría", ["Todas"] + categorias)
    nivel = st.selectbox("Nivel técnico", ["Todos", "Básico-Medio", "Medio", "Medio-Avanzado", "Avanzado"])
    st.divider()
    st.header("⚙️ Simulación")
    company_name = st.text_input("Empresa", value="Mi Empresa")
    queue_size = st.number_input("Personas en espera", min_value=0, value=12)
    high_demand_threshold = st.number_input("Umbral alta demanda", min_value=1, value=10)

filtered = SOLUTIONS
if texto:
    t = texto.lower()
    filtered = [s for s in filtered if t in (s["nombre"] + s["descripcion"] + s["categoria"]).lower()]
if categoria != "Todas":
    filtered = [s for s in filtered if s["categoria"] == categoria]
if nivel != "Todos":
    filtered = [s for s in filtered if s["nivel"] == nivel]

left, right = st.columns([1.05, 1.45], gap="large")

with left:
    st.subheader("📚 Opciones encontradas")
    if not filtered:
        st.warning("No hay resultados con esos filtros.")
        selected_name = None
    else:
        names = [s["nombre"] for s in filtered]
        selected_name = st.radio("Elige una opción para ver el paso a paso", names, label_visibility="collapsed")
        st.info("Tip: si el cliente no quiere Fin, las rutas más fuertes son: OpenAI custom, Make, Zapier, n8n o RAG documental.")
        st.markdown("### Comparador rápido")
        for s in filtered:
            st.markdown(f"**{s['nombre']}**  \n{s['categoria']} · {s['nivel']} · {s['tiempo']}")

with right:
    st.subheader("🧩 Detalle y paso a paso")
    if selected_name:
        s = next(x for x in filtered if x["nombre"] == selected_name)
        m1, m2, m3 = st.columns(3)
        m1.metric("Nivel", s["nivel"])
        m2.metric("Tiempo", s["tiempo"])
        m3.metric("Costo", s["costo"])
        st.markdown(f"### {s['nombre']}")
        st.write("**Mejor para:**", s["mejor_para"])
        st.write(s["descripcion"])
        st.markdown("#### Arquitectura")
        st.code(s["arquitectura"], language="text")
        a, b = st.columns(2)
        with a:
            st.markdown("#### Pros")
            for p in s["pros"]:
                st.write(f"✅ {p}")
        with b:
            st.markdown("#### Contras")
            for c in s["contras"]:
                st.write(f"⚠️ {c}")
        st.markdown("#### Paso a paso")
        for i, step in enumerate(s["pasos"], 1):
            st.write(f"**{i}.** {step}")
        st.markdown("#### Ejemplo")
        st.code(s["ejemplo"], language="text")
        st.success(s["recomendacion"])

st.divider()
st.subheader("💬 Simulador simple del comportamiento del bot")
question = st.chat_input("Escribe una pregunta del cliente: ¿Cuál es el horario?, quiero hablar con asesor, tengo una queja...")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    q = question.lower()
    response = next((ans for key, ans in FAQ.items() if key in q), None)
    needs_agent = any(k in q for k in ESCALATION_KEYWORDS)
    demand_msg = "En este momento tenemos alta demanda. Si necesitas agente, por favor espera; te atenderemos lo antes posible." if queue_size >= high_demand_threshold else ""
    if response and not needs_agent:
        bot_response = f"{response}\n\n{demand_msg}".strip()
    elif needs_agent:
        bot_response = f"Voy a transferir tu solicitud a un agente de {company_name}. {demand_msg}".strip()
    else:
        bot_response = f"Puedo intentar ayudarte con preguntas generales, pero para responder con seguridad voy a pasar tu caso a un agente de {company_name}. {demand_msg}".strip()
    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

st.divider()
st.subheader("✅ Recomendación ejecutiva")
st.markdown("""
Si el cliente **no quiere usar Fin**, la decisión puede ir así:

1. **Demo rápida:** Zapier + OpenAI o Make + OpenAI.  
2. **Automatización visual más controlada:** n8n o Make.  
3. **Producción robusta:** Backend Python + Intercom API/Webhooks + OpenAI/Azure OpenAI.  
4. **Muchos documentos internos:** RAG documental + Intercom.  
5. **Equipo no técnico que diseña flujos:** Botpress/Voiceflow/plataforma chatbot + Intercom.
""")

st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
