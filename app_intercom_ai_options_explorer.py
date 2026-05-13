
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Explorador de inversión IA para Intercom", page_icon="💸", layout="wide")

USD_TO_COP_DEFAULT = 3900

SOLUTIONS = [
    {
        "id": "python_custom_api",
        "nombre": "Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI",
        "categoria": "Código / Backend propio",
        "nivel": "Avanzado",
        "costo": "Medio-Alto",
        "tiempo": "2 a 8 semanas",
        "mejor_para": "Cliente que no quiere Fin y necesita control total del bot, reglas, prompts, base de conocimiento, alta demanda y escalamiento.",
        "descripcion": "Desarrollar un backend propio en Python/FastAPI que reciba eventos de Intercom, consulte FAQs/documentos, use OpenAI o Azure OpenAI y responda o escale a agente.",
        "arquitectura": "Intercom Messenger -> Webhook Intercom -> Backend Python/FastAPI -> FAQ/RAG -> OpenAI/Azure OpenAI -> Respuesta o asignación a agente",
        "pros": ["Máximo control", "Preguntas abiertas", "Reglas de espera y alta demanda", "Integración con CRM/ERP/BD", "Escalamiento humano personalizado"],
        "contras": ["Requiere desarrollo", "Mantenimiento técnico", "Seguridad y monitoreo", "Costos de hosting y API"],
        "necesitas": [
            "Cuenta activa de Intercom con permisos de Developer Hub/API/Webhooks.",
            "Token privado de Intercom y configuración de webhooks.",
            "Cuenta de OpenAI o Azure OpenAI.",
            "Servidor/API pública: Render, Railway, Azure App Service, AWS, GCP o VPS.",
            "Base de conocimiento: FAQs, documentos, políticas, horarios, pagos, garantías.",
            "Base de datos o storage para logs y trazabilidad.",
            "Equipo técnico: backend Python, QA y alguien de soporte que valide respuestas.",
            "Políticas de seguridad: manejo de datos personales, secretos y logs."
        ],
        "inversion_inicial_usd": (1500, 8000),
        "mensual_fijo_usd": (80, 600),
        "mensual_variable": "Tokens IA + hosting + monitoreo. Puede empezar bajo, pero crece con volumen.",
        "rubros": [
            ("Desarrollo inicial", "USD 1.500 - 8.000", "Backend, webhooks, lógica de escalamiento, pruebas."),
            ("Hosting/API", "USD 20 - 200/mes", "Servidor o serverless para recibir webhooks."),
            ("OpenAI/Azure OpenAI", "Según tokens", "Costo por tokens de entrada/salida."),
            ("Vector DB/RAG opcional", "USD 0 - 150/mes", "Solo si se usan documentos extensos."),
            ("Mantenimiento", "USD 100 - 500/mes", "Ajustes, monitoreo, prompts y errores.")
        ],
        "pasos": [
            "Crear app privada en Intercom Developer Hub y obtener token.",
            "Configurar webhooks para eventos de conversación/mensaje.",
            "Crear backend Python con FastAPI o Flask.",
            "Construir base de conocimiento y reglas de negocio.",
            "Integrar OpenAI/Azure OpenAI con prompt controlado.",
            "Implementar clasificación: FAQ, pregunta abierta, alta demanda, escalar.",
            "Responder o asignar conversación a agente/equipo en Intercom.",
            "Registrar métricas y logs.",
            "Probar con conversaciones reales y publicar."
        ],
        "ejemplo": "Cliente: ¿Cuál es el horario?\nBot: Nuestro horario es lunes a viernes de 8:00 a.m. a 6:00 p.m.\n\nCliente: Tengo una queja por facturación\nBot: Voy a transferirte con un agente para revisar tu caso con seguridad.",
        "recomendacion": "La opción más completa para producción si el cliente quiere evitar Fin y mantener control total."
    },
    {
        "id": "zapier_openai",
        "nombre": "Zapier + Intercom + ChatGPT/OpenAI",
        "categoria": "No-code / Low-code",
        "nivel": "Básico-Medio",
        "costo": "Medio",
        "tiempo": "1 a 5 días",
        "mejor_para": "Demo rápida o automatizaciones simples sin backend propio.",
        "descripcion": "Crear Zaps donde Intercom dispara una acción en ChatGPT/OpenAI y luego se registra nota, tag, ticket, respuesta o escalamiento.",
        "arquitectura": "Intercom Trigger -> Zapier -> ChatGPT/OpenAI -> Filtros/Paths -> Intercom Action/Webhook",
        "pros": ["Muy rápido", "No-code", "Buen prototipo", "Conecta muchas apps"],
        "contras": ["Costos por tareas", "Menor control", "Puede ser limitado para responder directo", "Dependencia de Zapier"],
        "necesitas": [
            "Cuenta de Zapier con plan que permita multi-step, webhooks o apps premium si aplica.",
            "Cuenta de Intercom conectada a Zapier.",
            "Cuenta de OpenAI/ChatGPT conectada a Zapier.",
            "Definir triggers: nueva conversación, ticket, tag o evento disponible.",
            "Prompts de clasificación y respuesta.",
            "Filtros/Paths para FAQ, alta demanda y escalamiento.",
            "Pruebas para validar consumo de tareas."
        ],
        "inversion_inicial_usd": (100, 800),
        "mensual_fijo_usd": (20, 150),
        "mensual_variable": "Tareas Zapier + tokens OpenAI. En flujos multi-step, cada acción consume tareas.",
        "rubros": [
            ("Configuración inicial", "USD 100 - 800", "Zaps, prompts, pruebas."),
            ("Zapier", "Desde USD 19,99/mes aprox.", "Depende de tareas y plan."),
            ("OpenAI", "Según tokens", "Costo de generación/clasificación."),
            ("Mantenimiento", "USD 50 - 200/mes", "Ajustes a Zaps y prompts.")
        ],
        "pasos": [
            "Crear Zap con trigger de Intercom.",
            "Agregar acción ChatGPT/OpenAI para clasificar intención.",
            "Crear Paths/Filtros: FAQ, agente, alta demanda.",
            "Agregar acción Intercom: tag, nota, ticket o webhook/API.",
            "Probar con preguntas reales.",
            "Publicar y monitorear tareas consumidas."
        ],
        "ejemplo": "Trigger: Nueva conversación -> ChatGPT clasifica -> Si es horario responde/sugiere -> Si es reclamo aplica tag y escala.",
        "recomendacion": "Ideal para validar rápido, no necesariamente para alto volumen crítico."
    },
    {
        "id": "make_openai",
        "nombre": "Make.com + Intercom + OpenAI",
        "categoria": "No-code / Automatización visual",
        "nivel": "Medio",
        "costo": "Medio",
        "tiempo": "2 a 10 días",
        "mejor_para": "Flujos visuales con routers, filtros y llamadas HTTP/API más flexibles.",
        "descripcion": "Diseñar escenarios en Make que reciben Intercom, consultan OpenAI y actualizan Intercom con reglas visuales.",
        "arquitectura": "Intercom/Webhook -> Make Scenario -> Router -> OpenAI + Knowledge Base -> Intercom API",
        "pros": ["Visual", "Routers/filtros potentes", "HTTP flexible", "Buen costo para prototipos"],
        "contras": ["Requiere buena configuración", "Costos por créditos", "Puede ser frágil si cambian campos", "Dependencia de Make"],
        "necesitas": [
            "Cuenta de Make.",
            "Módulo Intercom o webhook personalizado.",
            "Cuenta OpenAI.",
            "Base de conocimiento en Sheets/Notion/Airtable/BD o documento estructurado.",
            "Routers para FAQ, escalamiento y alta demanda.",
            "Manejo de errores y reintentos."
        ],
        "inversion_inicial_usd": (200, 1200),
        "mensual_fijo_usd": (12, 120),
        "mensual_variable": "Créditos Make + tokens OpenAI + posibles conectores externos.",
        "rubros": [
            ("Configuración inicial", "USD 200 - 1.200", "Escenarios, routers, pruebas."),
            ("Make", "Desde USD 12/mes aprox.", "Depende de créditos."),
            ("OpenAI", "Según tokens", "Costo por conversación."),
            ("Mantenimiento", "USD 50 - 250/mes", "Ajustes y monitoreo.")
        ],
        "pasos": [
            "Crear escenario en Make.",
            "Recibir evento Intercom por módulo o webhook.",
            "Agregar router de intención.",
            "Consultar FAQ/base de conocimiento.",
            "Llamar OpenAI si la pregunta es abierta.",
            "Responder, taggear o asignar vía Intercom/API.",
            "Activar y monitorear operaciones."
        ],
        "ejemplo": "Router 1: horario -> respuesta fija. Router 2: factura -> agente. Router 3: pregunta abierta -> OpenAI + contexto.",
        "recomendacion": "Muy buena alternativa no-code si Zapier se queda corto."
    },
    {
        "id": "n8n_openai",
        "nombre": "n8n + Intercom + OpenAI",
        "categoria": "Low-code / Self-hosted opcional",
        "nivel": "Medio-Avanzado",
        "costo": "Bajo-Medio",
        "tiempo": "1 a 3 semanas",
        "mejor_para": "Equipos que quieren automatización visual con opción self-hosted y más control técnico.",
        "descripcion": "Usar n8n para workflows con Intercom, OpenAI, reglas, HTTP y logs; puede ser cloud o self-hosted.",
        "arquitectura": "Intercom Webhook -> n8n Workflow -> OpenAI Node/HTTP -> IF/Switch -> Intercom API",
        "pros": ["Self-host opcional", "Flexible", "Bueno para APIs", "Puede ser económico en flujos complejos"],
        "contras": ["Curva técnica", "Si es self-hosted requiere mantenimiento", "Hay que asegurar disponibilidad"],
        "necesitas": [
            "Cuenta n8n Cloud o servidor para self-hosted.",
            "Credenciales Intercom/API o webhook.",
            "Cuenta OpenAI.",
            "Dominio/SSL si es self-hosted.",
            "Base de conocimiento o conexión a Sheets/DB.",
            "Monitoreo de ejecuciones y errores."
        ],
        "inversion_inicial_usd": (300, 2000),
        "mensual_fijo_usd": (0, 800),
        "mensual_variable": "n8n Cloud por ejecuciones o costo de servidor self-hosted + tokens IA.",
        "rubros": [
            ("Configuración inicial", "USD 300 - 2.000", "Workflows, API, pruebas."),
            ("n8n Cloud", "Desde ~20€/mes anual", "Depende de ejecuciones."),
            ("Self-hosting", "USD 5 - 50/mes", "Servidor, backups, SSL; más mantenimiento."),
            ("OpenAI", "Según tokens", "Costo por uso."),
            ("Mantenimiento", "USD 50 - 300/mes", "Actualizaciones y soporte.")
        ],
        "pasos": [
            "Crear workflow en n8n.",
            "Configurar webhook o nodo Intercom.",
            "Agregar OpenAI para clasificar/generar.",
            "Crear IF/Switch para FAQ, alta demanda y escalamiento.",
            "Llamar Intercom API para responder/taggear/asignar.",
            "Guardar logs y activar workflow."
        ],
        "ejemplo": "Webhook recibe mensaje -> OpenAI clasifica -> IF horario responde -> IF baja confianza asigna a agente.",
        "recomendacion": "Buena para balance entre control y costo; más técnica que Make/Zapier."
    },
    {
        "id": "rag_assistant",
        "nombre": "Asistente RAG documental + Intercom",
        "categoria": "IA documental",
        "nivel": "Avanzado",
        "costo": "Medio-Alto",
        "tiempo": "3 a 8 semanas",
        "mejor_para": "Empresas con manuales, políticas o documentación extensa que necesitan respuestas con base en fuentes.",
        "descripcion": "Indexar documentos, buscar fragmentos relevantes y generar respuestas con evidencia. Si no encuentra contexto, escala.",
        "arquitectura": "Intercom -> Backend Python -> Vector DB/Azure AI Search/Pinecone -> LLM -> Intercom",
        "pros": ["Respuestas basadas en documentos", "Mejor para preguntas abiertas", "Reduce respuestas inventadas", "Escalable"],
        "contras": ["Mayor desarrollo", "Hay que limpiar documentos", "Requiere evaluación continua", "Costo de búsqueda/vector DB"],
        "necesitas": [
            "Todo lo de solución Python propia.",
            "Documentos oficiales en formato limpio.",
            "Embeddings y base vectorial o buscador: Azure AI Search, Pinecone, Chroma, pgvector, etc.",
            "Proceso de actualización de documentos.",
            "Evaluación de precisión y fuentes."
        ],
        "inversion_inicial_usd": (2500, 12000),
        "mensual_fijo_usd": (150, 1000),
        "mensual_variable": "Tokens + embeddings + almacenamiento/buscador + mantenimiento documental.",
        "rubros": [
            ("Desarrollo inicial", "USD 2.500 - 12.000", "RAG, documentos, backend, pruebas."),
            ("Vector DB/buscador", "USD 0 - 500/mes", "Depende de volumen y proveedor."),
            ("OpenAI/Azure OpenAI", "Según tokens", "Embeddings + respuestas."),
            ("Mantenimiento documental", "USD 100 - 500/mes", "Actualizar y validar contenido.")
        ],
        "pasos": [
            "Recolectar documentos oficiales.",
            "Limpiar y fragmentar documentos.",
            "Crear embeddings y cargarlos a vector DB/buscador.",
            "Integrar Intercom con backend.",
            "Recuperar contexto relevante por pregunta.",
            "Responder solo con evidencia suficiente.",
            "Escalar si no hay confianza.",
            "Medir precisión y actualizar documentos."
        ],
        "ejemplo": "Cliente pregunta garantía -> Bot busca política oficial -> responde con base en el documento -> si no hay claridad, escala.",
        "recomendacion": "La mejor opción si el cliente tiene mucha documentación y requiere respuestas confiables."
    },
    {
        "id": "chatbot_platform",
        "nombre": "Botpress / Voiceflow / plataforma chatbot + Intercom",
        "categoria": "Plataforma chatbot",
        "nivel": "Medio",
        "costo": "Medio-Alto",
        "tiempo": "1 a 4 semanas",
        "mejor_para": "Equipos que prefieren construir flujos visuales y que negocio pueda administrarlos.",
        "descripcion": "Crear bot en una plataforma especializada y conectarlo a Intercom mediante integración, webhook o API.",
        "arquitectura": "Intercom -> Webhook/API -> Plataforma chatbot -> LLM/KB -> Handoff Intercom",
        "pros": ["Flujos visuales", "Menos código", "Administrable por negocio", "Analítica conversacional"],
        "contras": ["Costo proveedor", "Lock-in", "Integración puede requerir custom", "Limitaciones según plataforma"],
        "necesitas": [
            "Cuenta en plataforma chatbot.",
            "Licencia según volumen de conversaciones/mensajes.",
            "Conector o webhook/API con Intercom.",
            "Diseño de intents y flujos.",
            "Base de conocimiento.",
            "Reglas de handoff a agentes."
        ],
        "inversion_inicial_usd": (500, 3000),
        "mensual_fijo_usd": (50, 1000),
        "mensual_variable": "Mensajes/conversaciones de la plataforma + IA + posibles add-ons.",
        "rubros": [
            ("Diseño/configuración", "USD 500 - 3.000", "Flujos, intents, pruebas."),
            ("Licencia plataforma", "USD 50 - 1.000+/mes", "Depende del proveedor y volumen."),
            ("OpenAI/LLM", "Incluido o separado", "Según plataforma."),
            ("Mantenimiento", "USD 100 - 400/mes", "Ajuste de flujos y respuestas.")
        ],
        "pasos": [
            "Elegir plataforma chatbot.",
            "Crear intents: horarios, pagos, precios, soporte, humano.",
            "Cargar base de conocimiento.",
            "Configurar webhook/API con Intercom.",
            "Definir fallback y handoff.",
            "Probar y publicar."
        ],
        "ejemplo": "Flujo visual: saludo -> pregunta abierta -> intención -> respuesta FAQ o handoff.",
        "recomendacion": "Buena si el equipo de negocio quiere gestionar conversaciones sin depender siempre de desarrollo."
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

st.title("💸 Explorador de soluciones IA para Intercom sin Fin: opciones + inversión")
st.caption("Comparador investigativo para estimar qué se necesita, cuánto podría costar y cómo implementar cada alternativa.")

with st.sidebar:
    st.header("🔎 Filtros")
    texto = st.text_input("Buscar opción", placeholder="Python, OpenAI, Zapier, Make, n8n, RAG")
    categorias = sorted(set(s["categoria"] for s in SOLUTIONS))
    categoria = st.selectbox("Categoría", ["Todas"] + categorias)
    nivel = st.selectbox("Nivel técnico", ["Todos", "Básico-Medio", "Medio", "Medio-Avanzado", "Avanzado"])
    st.divider()
    st.header("🧮 Supuestos de costos")
    usd_to_cop = st.number_input("TRM estimada COP por USD", min_value=3000, max_value=6000, value=USD_TO_COP_DEFAULT, step=50)
    conversaciones_mes = st.number_input("Conversaciones al mes", min_value=100, max_value=200000, value=5000, step=100)
    pct_ia = st.slider("% conversaciones que procesa IA", 10, 100, 60, 5)
    tokens_in = st.number_input("Tokens entrada promedio", min_value=100, max_value=10000, value=1200, step=100)
    tokens_out = st.number_input("Tokens salida promedio", min_value=50, max_value=5000, value=350, step=50)
    input_price = st.number_input("USD / 1M tokens entrada", min_value=0.01, max_value=50.0, value=0.75, step=0.05)
    output_price = st.number_input("USD / 1M tokens salida", min_value=0.01, max_value=100.0, value=4.50, step=0.10)
    st.caption("Valores por defecto orientativos para un modelo económico/mini. Ajusta con el precio real del proveedor.")
    st.divider()
    st.header("⚙️ Simulación bot")
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

ia_conversations = conversaciones_mes * pct_ia / 100
ai_monthly = (ia_conversations * tokens_in / 1_000_000 * input_price) + (ia_conversations * tokens_out / 1_000_000 * output_price)

def usd(x):
    return f"USD {x:,.0f}".replace(",", ".")

def cop(x):
    return f"COP {x*usd_to_cop:,.0f}".replace(",", ".")

left, right = st.columns([1.0, 1.55], gap="large")

with left:
    st.subheader("📚 Opciones encontradas")
    if not filtered:
        st.warning("No hay resultados con esos filtros.")
        selected_name = None
    else:
        names = [s["nombre"] for s in filtered]
        selected_name = st.radio("Elige una opción", names, label_visibility="collapsed")
        st.info("La opción propia con Python queda incluida como alternativa principal de producción.")
        st.markdown("### Comparador rápido")
        for s in filtered:
            ini = s["inversion_inicial_usd"]
            mon = s["mensual_fijo_usd"]
            st.markdown(f"**{s['nombre']}**  \n{s['categoria']} · {s['nivel']} · Inicial {usd(ini[0])}-{usd(ini[1])} · Mensual fijo {usd(mon[0])}-{usd(mon[1])}")

with right:
    st.subheader("🧩 Detalle, inversión y paso a paso")
    if selected_name:
        s = next(x for x in filtered if x["nombre"] == selected_name)
        ini_low, ini_high = s["inversion_inicial_usd"]
        mon_low, mon_high = s["mensual_fijo_usd"]
        total_low = mon_low + ai_monthly
        total_high = mon_high + ai_monthly

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Nivel", s["nivel"])
        m2.metric("Tiempo", s["tiempo"])
        m3.metric("Inicial estimado", f"{usd(ini_low)}-{usd(ini_high)}")
        m4.metric("Mensual + IA", f"{usd(total_low)}-{usd(total_high)}")

        st.markdown(f"### {s['nombre']}")
        st.write("**Mejor para:**", s["mejor_para"])
        st.write(s["descripcion"])

        st.markdown("#### 💰 Inversión estimada")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Inicial en COP", f"{cop(ini_low)} - {cop(ini_high)}")
            st.metric("Costo IA estimado/mes", f"{usd(ai_monthly)} / {cop(ai_monthly)}")
        with c2:
            st.metric("Mensual total estimado USD", f"{usd(total_low)} - {usd(total_high)}")
            st.metric("Mensual total estimado COP", f"{cop(total_low)} - {cop(total_high)}")
        st.caption("Estimación referencial. Cambia mucho por volumen, modelo IA, plan contratado, tareas/operaciones y alcance de desarrollo.")

        st.markdown("#### 🧾 Rubros de inversión")
        for name, amount, note in s["rubros"]:
            st.write(f"**{name}:** {amount}. {note}")
        st.write("**Variable principal:**", s["mensual_variable"])

        st.markdown("#### ✅ Qué habría que tener para usar esta opción")
        for req in s["necesitas"]:
            st.write(f"- {req}")

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
st.subheader("✅ Lectura ejecutiva")
st.markdown("""
- **Más rápida para demo:** Zapier + OpenAI.
- **Más visual y flexible no-code:** Make + OpenAI.
- **Más balance entre control y costo:** n8n + OpenAI.
- **Más robusta para producción:** Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI.
- **Más confiable con documentos:** RAG documental + Intercom.
""")
st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
