
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Explorador de inversión IA para Intercom", page_icon="💸", layout="wide")

# -------------------- ESTILOS COMPACTOS --------------------
st.markdown("""
<style>
/* Layout general */
.block-container {padding-top: 1.2rem !important; padding-left: 2rem !important; padding-right: 2rem !important;}
html, body, [class*="css"] {font-size: 14.5px;}

/* Títulos más compactos */
h1 {font-size: 1.55rem !important; line-height: 1.18 !important; margin-bottom: .6rem !important;}
h2 {font-size: 1.20rem !important; line-height: 1.2 !important;}
h3 {font-size: 1.05rem !important; line-height: 1.22 !important; margin-top: .8rem !important;}
h4 {font-size: .95rem !important; line-height: 1.2 !important;}

/* Texto */
.stMarkdown p, .stMarkdown li {font-size: .90rem !important; line-height: 1.38 !important;}
.stCaptionContainer, .stCaptionContainer p {font-size: .78rem !important;}

/* Métricas: más pequeñas y con salto de línea para no cortar precios */
div[data-testid="stMetric"] {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 8px 10px;
    min-height: 70px;
    overflow: visible;
}
div[data-testid="stMetricLabel"] p {
    font-size: .72rem !important;
    line-height: 1.05 !important;
    white-space: normal !important;
}
div[data-testid="stMetricValue"] {
    font-size: .88rem !important;
    line-height: 1.12 !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

/* Código compacto */
pre, code {font-size: .78rem !important; line-height: 1.28 !important;}

/* Radio y textos de sidebar */
label, .stRadio label, .stSelectbox label, .stNumberInput label, .stTextInput label {font-size: .84rem !important;}

/* Separadores menos altos */
hr {margin: .75rem 0 !important;}
</style>
""", unsafe_allow_html=True)

USD_TO_COP_DEFAULT = 3900

SOLUTIONS = [
    {
        "nombre": "Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI",
        "categoria": "Código / Backend propio", "nivel": "Avanzado", "tiempo": "2 a 8 semanas", "costo": "Medio-Alto",
        "mejor_para": "Cliente que no quiere Fin y necesita control total del bot, reglas, prompts, base de conocimiento, alta demanda y escalamiento.",
        "descripcion": "Desarrollar un backend propio en Python/FastAPI que reciba eventos de Intercom, consulte FAQs/documentos, use OpenAI o Azure OpenAI y responda o escale a agente.",
        "arquitectura": "Intercom Messenger -> Webhook Intercom -> Backend Python/FastAPI -> FAQ/RAG -> OpenAI/Azure OpenAI -> Respuesta o asignación a agente",
        "pros": ["Máximo control", "Preguntas abiertas", "Reglas de espera y alta demanda", "Integración con CRM/ERP/BD", "Escalamiento humano personalizado"],
        "contras": ["Requiere desarrollo", "Mantenimiento técnico", "Seguridad y monitoreo", "Costos de hosting y API"],
        "necesitas": ["Cuenta activa de Intercom con Developer Hub/API/Webhooks", "Token privado de Intercom", "Cuenta OpenAI o Azure OpenAI", "Servidor público para webhooks", "Base de conocimiento", "Logs y base de datos", "Equipo técnico Python", "Políticas de seguridad y manejo de datos"],
        "inicial": (1500, 8000), "mensual": (80, 600),
        "variable": "Tokens IA + hosting + monitoreo. Puede empezar bajo, pero crece con volumen.",
        "rubros": [("Desarrollo inicial", "USD 1.500 - 8.000", "Backend, webhooks, lógica, pruebas."), ("Hosting/API", "USD 20 - 200/mes", "Servidor o serverless."), ("OpenAI/Azure OpenAI", "Según tokens", "Costo por uso."), ("Vector DB/RAG opcional", "USD 0 - 150/mes", "Para documentos extensos."), ("Mantenimiento", "USD 100 - 500/mes", "Ajustes y monitoreo.")],
        "pasos": ["Crear app privada en Intercom Developer Hub", "Configurar webhooks", "Crear backend Python con FastAPI", "Construir base de conocimiento", "Integrar OpenAI/Azure OpenAI", "Clasificar FAQ/pregunta abierta/alta demanda/escalar", "Responder o asignar en Intercom", "Registrar métricas", "Probar y publicar"],
        "ejemplo": "Cliente: ¿Cuál es el horario?\nBot: Nuestro horario es lunes a viernes de 8:00 a.m. a 6:00 p.m.\n\nCliente: Tengo una queja por facturación\nBot: Voy a transferirte con un agente para revisar tu caso con seguridad.",
        "recomendacion": "La opción más completa para producción si el cliente quiere evitar Fin y mantener control total."
    },
    {
        "nombre": "Zapier + Intercom + ChatGPT/OpenAI",
        "categoria": "No-code / Low-code", "nivel": "Básico-Medio", "tiempo": "1 a 5 días", "costo": "Medio",
        "mejor_para": "Demo rápida o automatizaciones simples sin backend propio.",
        "descripcion": "Crear Zaps donde Intercom dispara una acción en ChatGPT/OpenAI y luego se registra nota, tag, ticket, respuesta o escalamiento.",
        "arquitectura": "Intercom Trigger -> Zapier -> ChatGPT/OpenAI -> Filtros/Paths -> Intercom Action/Webhook",
        "pros": ["Muy rápido", "No-code", "Buen prototipo", "Conecta muchas apps"],
        "contras": ["Costos por tareas", "Menor control", "Puede ser limitado para responder directo", "Dependencia de Zapier"],
        "necesitas": ["Cuenta Zapier", "Cuenta Intercom conectada", "Cuenta OpenAI", "Triggers definidos", "Prompts", "Filtros/Paths", "Pruebas de consumo de tareas"],
        "inicial": (100, 800), "mensual": (20, 150),
        "variable": "Tareas Zapier + tokens OpenAI. En flujos multi-step, cada acción consume tareas.",
        "rubros": [("Configuración", "USD 100 - 800", "Zaps, prompts y pruebas."), ("Zapier", "Desde USD 19,99/mes aprox.", "Según tareas."), ("OpenAI", "Según tokens", "Generación y clasificación."), ("Mantenimiento", "USD 50 - 200/mes", "Ajustes a Zaps.")],
        "pasos": ["Crear Zap con trigger de Intercom", "Agregar ChatGPT/OpenAI", "Crear filtros/paths", "Agregar acción Intercom o webhook", "Probar", "Publicar"],
        "ejemplo": "Nueva conversación -> ChatGPT clasifica -> Si es horario responde/sugiere -> Si es reclamo aplica tag y escala.",
        "recomendacion": "Ideal para validar rápido, no necesariamente para alto volumen crítico."
    },
    {
        "nombre": "Make.com + Intercom + OpenAI",
        "categoria": "No-code / Automatización visual", "nivel": "Medio", "tiempo": "2 a 10 días", "costo": "Medio",
        "mejor_para": "Flujos visuales con routers, filtros y llamadas HTTP/API más flexibles.",
        "descripcion": "Diseñar escenarios en Make que reciben Intercom, consultan OpenAI y actualizan Intercom con reglas visuales.",
        "arquitectura": "Intercom/Webhook -> Make Scenario -> Router -> OpenAI + Knowledge Base -> Intercom API",
        "pros": ["Visual", "Routers/filtros potentes", "HTTP flexible", "Buen costo para prototipos"],
        "contras": ["Requiere configuración", "Costos por créditos", "Fragilidad si cambian campos", "Dependencia de Make"],
        "necesitas": ["Cuenta Make", "Módulo Intercom o webhook", "Cuenta OpenAI", "Base de conocimiento", "Routers", "Manejo de errores"],
        "inicial": (200, 1200), "mensual": (12, 120),
        "variable": "Créditos Make + tokens OpenAI + posibles conectores externos.",
        "rubros": [("Configuración", "USD 200 - 1.200", "Escenarios y routers."), ("Make", "Desde USD 12/mes aprox.", "Según créditos."), ("OpenAI", "Según tokens", "Costo por conversación."), ("Mantenimiento", "USD 50 - 250/mes", "Ajustes.")],
        "pasos": ["Crear escenario", "Recibir evento Intercom", "Agregar router", "Consultar FAQ", "Llamar OpenAI", "Responder/asignar vía Intercom", "Monitorear"],
        "ejemplo": "Router 1: horario -> respuesta fija. Router 2: factura -> agente. Router 3: pregunta abierta -> OpenAI.",
        "recomendacion": "Muy buena alternativa no-code si Zapier se queda corto."
    },
    {
        "nombre": "n8n + Intercom + OpenAI",
        "categoria": "Low-code / Self-hosted opcional", "nivel": "Medio-Avanzado", "tiempo": "1 a 3 semanas", "costo": "Bajo-Medio",
        "mejor_para": "Automatización visual con opción self-hosted y más control técnico.",
        "descripcion": "Usar n8n para workflows con Intercom, OpenAI, reglas, HTTP y logs; puede ser cloud o self-hosted.",
        "arquitectura": "Intercom Webhook -> n8n Workflow -> OpenAI Node/HTTP -> IF/Switch -> Intercom API",
        "pros": ["Self-host opcional", "Flexible", "Bueno para APIs", "Económico en flujos complejos"],
        "contras": ["Curva técnica", "Self-host requiere mantenimiento", "Hay que asegurar disponibilidad"],
        "necesitas": ["n8n Cloud o servidor", "Credenciales Intercom", "Cuenta OpenAI", "Dominio/SSL si self-hosted", "Base de conocimiento", "Monitoreo"],
        "inicial": (300, 2000), "mensual": (0, 800),
        "variable": "n8n Cloud por ejecuciones o servidor self-hosted + tokens IA.",
        "rubros": [("Configuración", "USD 300 - 2.000", "Workflows y pruebas."), ("n8n Cloud", "Desde ~20€/mes anual", "Según ejecuciones."), ("Self-hosting", "USD 5 - 50/mes", "Servidor y backups."), ("OpenAI", "Según tokens", "Costo por uso."), ("Mantenimiento", "USD 50 - 300/mes", "Soporte.")],
        "pasos": ["Crear workflow", "Configurar webhook/Intercom", "Agregar OpenAI", "Crear IF/Switch", "Llamar Intercom API", "Guardar logs", "Activar"],
        "ejemplo": "Webhook recibe mensaje -> OpenAI clasifica -> IF horario responde -> IF baja confianza asigna a agente.",
        "recomendacion": "Buena para balance entre control y costo; más técnica que Make/Zapier."
    },
    {
        "nombre": "Asistente RAG documental + Intercom",
        "categoria": "IA documental", "nivel": "Avanzado", "tiempo": "3 a 8 semanas", "costo": "Medio-Alto",
        "mejor_para": "Empresas con manuales, políticas o documentación extensa.",
        "descripcion": "Indexar documentos, buscar fragmentos relevantes y generar respuestas con evidencia. Si no encuentra contexto, escala.",
        "arquitectura": "Intercom -> Backend Python -> Vector DB/Azure AI Search/Pinecone -> LLM -> Intercom",
        "pros": ["Respuestas basadas en documentos", "Mejor para preguntas abiertas", "Reduce respuestas inventadas", "Escalable"],
        "contras": ["Mayor desarrollo", "Hay que limpiar documentos", "Evaluación continua", "Costo de búsqueda/vector DB"],
        "necesitas": ["Todo lo de Python propio", "Documentos limpios", "Embeddings", "Vector DB/buscador", "Proceso de actualización", "Evaluación de precisión"],
        "inicial": (2500, 12000), "mensual": (150, 1000),
        "variable": "Tokens + embeddings + almacenamiento/buscador + mantenimiento documental.",
        "rubros": [("Desarrollo", "USD 2.500 - 12.000", "RAG y backend."), ("Vector DB", "USD 0 - 500/mes", "Según volumen."), ("OpenAI/Azure", "Según tokens", "Embeddings + respuestas."), ("Mantenimiento", "USD 100 - 500/mes", "Actualizar contenido.")],
        "pasos": ["Recolectar documentos", "Limpiar y fragmentar", "Crear embeddings", "Integrar Intercom", "Recuperar contexto", "Responder con evidencia", "Escalar si no hay confianza", "Medir precisión"],
        "ejemplo": "Cliente pregunta garantía -> Bot busca política oficial -> responde -> si no hay claridad, escala.",
        "recomendacion": "La mejor opción si el cliente tiene mucha documentación y requiere respuestas confiables."
    },
    {
        "nombre": "Botpress / Voiceflow / plataforma chatbot + Intercom",
        "categoria": "Plataforma chatbot", "nivel": "Medio", "tiempo": "1 a 4 semanas", "costo": "Medio-Alto",
        "mejor_para": "Equipos que prefieren flujos visuales administrables por negocio.",
        "descripcion": "Crear bot en una plataforma especializada y conectarlo a Intercom mediante integración, webhook o API.",
        "arquitectura": "Intercom -> Webhook/API -> Plataforma chatbot -> LLM/KB -> Handoff Intercom",
        "pros": ["Flujos visuales", "Menos código", "Administrable por negocio", "Analítica"],
        "contras": ["Costo proveedor", "Lock-in", "Integración custom", "Limitaciones por plataforma"],
        "necesitas": ["Cuenta plataforma chatbot", "Licencia", "Conector/API con Intercom", "Diseño de intents", "Base de conocimiento", "Reglas de handoff"],
        "inicial": (500, 3000), "mensual": (50, 1000),
        "variable": "Mensajes/conversaciones de la plataforma + IA + add-ons.",
        "rubros": [("Diseño/configuración", "USD 500 - 3.000", "Flujos e intents."), ("Licencia", "USD 50 - 1.000+/mes", "Según proveedor."), ("OpenAI/LLM", "Incluido o separado", "Según plataforma."), ("Mantenimiento", "USD 100 - 400/mes", "Ajustes.")],
        "pasos": ["Elegir plataforma", "Crear intents", "Cargar conocimiento", "Conectar Intercom", "Definir fallback", "Probar y publicar"],
        "ejemplo": "Saludo -> pregunta abierta -> intención -> respuesta FAQ o handoff.",
        "recomendacion": "Buena si negocio quiere gestionar conversaciones sin depender siempre de desarrollo."
    },
]

FAQ = {"horario": "Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.", "horarios": "Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.", "precio": "Para darte precios exactos necesito saber el producto o servicio. Si quieres, te conecto con un agente comercial.", "ubicacion": "Compártenos tu ciudad y te indicamos la sede o canal más cercano.", "ubicación": "Compártenos tu ciudad y te indicamos la sede o canal más cercano.", "pago": "Aceptamos los métodos de pago definidos por la empresa. Un agente puede confirmar el detalle según tu caso."}
ESCALATION_KEYWORDS = ["reclamo", "queja", "cancelar", "devolución", "devolucion", "factura", "garantía", "garantia", "asesor", "humano", "agente"]

st.title("💸 Explorador de soluciones IA para Intercom sin Fin")
st.caption("Comparador investigativo con opciones, requisitos, inversión estimada, paso a paso y simulador.")

with st.sidebar:
    st.header("🔎 Filtros")
    texto = st.text_input("Buscar opción", placeholder="Python, OpenAI, Zapier, Make, n8n, RAG")
    categorias = sorted(set(s["categoria"] for s in SOLUTIONS))
    categoria = st.selectbox("Categoría", ["Todas"] + categorias)
    nivel = st.selectbox("Nivel técnico", ["Todos", "Básico-Medio", "Medio", "Medio-Avanzado", "Avanzado"])
    st.divider()
    st.header("🧮 Supuestos")
    usd_to_cop = st.number_input("TRM COP/USD", min_value=3000, max_value=6000, value=USD_TO_COP_DEFAULT, step=50)
    conversaciones_mes = st.number_input("Conversaciones al mes", min_value=100, max_value=200000, value=5000, step=100)
    pct_ia = st.slider("% que procesa IA", 10, 100, 60, 5)
    tokens_in = st.number_input("Tokens entrada prom.", min_value=100, max_value=10000, value=1200, step=100)
    tokens_out = st.number_input("Tokens salida prom.", min_value=50, max_value=5000, value=350, step=50)
    input_price = st.number_input("USD / 1M tokens entrada", min_value=0.01, max_value=50.0, value=0.75, step=0.05)
    output_price = st.number_input("USD / 1M tokens salida", min_value=0.01, max_value=100.0, value=4.50, step=0.10)
    st.divider()
    st.header("⚙️ Simulación")
    company_name = st.text_input("Empresa", value="Mi Empresa")
    queue_size = st.number_input("Personas en espera", min_value=0, value=12)
    high_demand_threshold = st.number_input("Umbral alta demanda", min_value=1, value=10)

filtered = SOLUTIONS
if texto:
    t = texto.lower()
    filtered = [s for s in filtered if t in (s["nombre"] + s["descripcion"] + s["categoria"]).lower()]
if categoria != "Todas": filtered = [s for s in filtered if s["categoria"] == categoria]
if nivel != "Todos": filtered = [s for s in filtered if s["nivel"] == nivel]

ia_conversations = conversaciones_mes * pct_ia / 100
ai_monthly = (ia_conversations * tokens_in / 1_000_000 * input_price) + (ia_conversations * tokens_out / 1_000_000 * output_price)

def usd(x): return f"USD {x:,.0f}".replace(",", ".")
def cop(x): return f"COP {x*usd_to_cop:,.0f}".replace(",", ".")

left, right = st.columns([1.0, 1.55], gap="large")

with left:
    st.subheader("📚 Opciones")
    if not filtered:
        st.warning("No hay resultados con esos filtros.")
        selected_name = None
    else:
        selected_name = st.radio("Elige una opción", [s["nombre"] for s in filtered], label_visibility="collapsed")
        st.info("La opción propia con Python queda incluida como alternativa principal de producción.")
        st.markdown("### Comparador rápido")
        for s in filtered:
            ini, mon = s["inicial"], s["mensual"]
            st.markdown(f"**{s['nombre']}**  \n{s['categoria']} · {s['nivel']}  \nInicial {usd(ini[0])}-{usd(ini[1])} · Mensual fijo {usd(mon[0])}-{usd(mon[1])}")

with right:
    st.subheader("🧩 Detalle")
    if selected_name:
        s = next(x for x in filtered if x["nombre"] == selected_name)
        ini_low, ini_high = s["inicial"]
        mon_low, mon_high = s["mensual"]
        total_low, total_high = mon_low + ai_monthly, mon_high + ai_monthly

        # Métricas compactas en dos filas para que no se corten
        r1c1, r1c2 = st.columns(2)
        r1c1.metric("Nivel", s["nivel"])
        r1c2.metric("Tiempo", s["tiempo"])
        r2c1, r2c2 = st.columns(2)
        r2c1.metric("Inicial USD", f"{usd(ini_low)} - {usd(ini_high)}")
        r2c2.metric("Mensual + IA USD", f"{usd(total_low)} - {usd(total_high)}")

        st.markdown(f"### {s['nombre']}")
        st.write("**Mejor para:**", s["mejor_para"])
        st.write(s["descripcion"])

        st.markdown("#### 💰 Inversión estimada")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Inicial COP", f"{cop(ini_low)} - {cop(ini_high)}")
            st.metric("Mensual COP", f"{cop(total_low)} - {cop(total_high)}")
        with c2:
            st.metric("Inicial USD", f"{usd(ini_low)} - {usd(ini_high)}")
            st.metric("Costo IA/mes", f"{usd(ai_monthly)} / {cop(ai_monthly)}")
        st.caption("Estimación referencial. Ajusta volumen, modelo, plan y TRM para afinar el cálculo.")

        st.markdown("#### 🧾 Rubros")
        for name, amount, note in s["rubros"]:
            st.write(f"**{name}:** {amount}. {note}")
        st.write("**Variable principal:**", s["variable"])

        st.markdown("#### ✅ Qué habría que tener")
        for req in s["necesitas"]: st.write(f"- {req}")

        st.markdown("#### Arquitectura")
        st.code(s["arquitectura"], language="text")

        a, b = st.columns(2)
        with a:
            st.markdown("#### Pros")
            for p in s["pros"]: st.write(f"✅ {p}")
        with b:
            st.markdown("#### Contras")
            for c in s["contras"]: st.write(f"⚠️ {c}")

        st.markdown("#### Paso a paso")
        for i, step in enumerate(s["pasos"], 1): st.write(f"**{i}.** {step}")
        st.markdown("#### Ejemplo")
        st.code(s["ejemplo"], language="text")
        st.success(s["recomendacion"])

st.divider()
st.subheader("💬 Simulador simple")
question = st.chat_input("Escribe una pregunta del cliente: ¿Cuál es el horario?, quiero hablar con asesor, tengo una queja...")
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"): st.write(question)
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
    with st.chat_message("assistant"): st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

st.divider()
st.subheader("✅ Lectura ejecutiva")
st.markdown("""
- **Demo rápida:** Zapier + OpenAI.
- **Visual y flexible no-code:** Make + OpenAI.
- **Balance control/costo:** n8n + OpenAI.
- **Producción robusta:** Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI.
- **Documentos extensos:** RAG documental + Intercom.
""")
st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
