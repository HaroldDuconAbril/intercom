
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Intercom AI Options Lab", page_icon="🤖", layout="wide")

st.markdown("""
<style>
:root {--bg:#f8fafc; --card:#ffffff; --line:#e5e7eb; --text:#0f172a; --muted:#64748b; --brand:#2563eb; --brand2:#7c3aed; --good:#16a34a; --warn:#d97706;}
.block-container {padding-top:1.1rem!important; padding-left:2rem!important; padding-right:2rem!important; max-width:1400px;}
html, body, [class*="css"] {font-size:14.3px; color:var(--text);} 
h1 {font-size:1.55rem!important; line-height:1.15!important; margin-bottom:.35rem!important;}
h2 {font-size:1.18rem!important;} h3 {font-size:1.02rem!important; margin-top:.6rem!important;} h4 {font-size:.92rem!important;}
.stMarkdown p, .stMarkdown li {font-size:.89rem!important; line-height:1.38!important;}
.hero {background:linear-gradient(135deg,#0f172a 0%,#1d4ed8 58%,#7c3aed 100%); padding:18px 22px; border-radius:18px; color:white; margin-bottom:14px; box-shadow:0 12px 30px rgba(15,23,42,.18);} 
.hero h1 {color:white!important; margin:0!important;} .hero p {color:#e0e7ff!important; margin:.35rem 0 0 0!important;}
.card {background:var(--card); border:1px solid var(--line); border-radius:16px; padding:14px 16px; box-shadow:0 4px 16px rgba(15,23,42,.045); margin-bottom:10px;}
.small-muted {color:var(--muted); font-size:.78rem;}
.badge {display:inline-block; padding:3px 8px; border-radius:999px; background:#eff6ff; color:#1d4ed8; font-size:.72rem; font-weight:700; margin-right:5px; margin-bottom:4px;}
.badge-purple {background:#f3e8ff; color:#6d28d9;} .badge-green {background:#dcfce7; color:#15803d;} .badge-orange {background:#ffedd5; color:#c2410c;}
div[data-testid="stMetric"] {background:#fff; border:1px solid var(--line); border-radius:14px; padding:9px 10px; box-shadow:0 3px 12px rgba(15,23,42,.04); min-height:70px;}
div[data-testid="stMetricLabel"] p {font-size:.70rem!important; color:var(--muted)!important; line-height:1.05!important; white-space:normal!important;}
div[data-testid="stMetricValue"] {font-size:.88rem!important; line-height:1.12!important; white-space:normal!important; overflow-wrap:anywhere!important; word-break:break-word!important;}
pre, code {font-size:.76rem!important; line-height:1.28!important; border-radius:12px!important;}
hr {margin:.75rem 0!important;} label {font-size:.83rem!important;} .stButton>button {border-radius:10px;}
</style>
""", unsafe_allow_html=True)

USD_TO_COP_DEFAULT = 3900

SOLUTIONS = [
    {
        "nombre":"Fin AI Agent nativo de Intercom",
        "categoria":"Nativo Intercom", "nivel":"Básico-Medio", "tiempo":"Horas a pocos días", "costo":"Variable por outcome",
        "tag":"Nativo", "color":"green",
        "mejor_para":"Comparar contra alternativas externas; ideal si se quiere activar rápido y reducir desarrollo.",
        "descripcion":"Usar Fin AI Agent dentro de Intercom o como Fin standalone. Responde con conocimiento configurado, escala a agente y cobra por outcome/resolución.",
        "arquitectura":"Intercom/Fin -> Knowledge Hub/Procedures -> Respuesta automática -> Handoff a Inbox/agente",
        "pros":["Implementación rápida", "Menos desarrollo", "Escalamiento nativo", "Reportes y monitoreo integrados", "Puede salir más barato si evita desarrollo"],
        "contras":["El cliente no lo prefiere inicialmente", "Costo variable por outcome", "Menos control que Python propio", "Dependencia del ecosistema Intercom"],
        "necesitas":["Plan Intercom o Fin standalone", "Contenido/Knowledge Hub organizado", "Reglas de handoff", "Equipo/agentes configurados", "Validar outcomes mensuales"],
        "inicial":(0,500), "mensual":(29,800), "fin":True,
        "variable":"Fin cobra desde USD 0,99 por outcome; si se usa con Intercom también hay costo por seat. Hay mínimo de outcomes en standalone.",
        "rubros":[("Fin AI Agent", "Desde USD 0,99/outcome", "Costo por resultado/resolución."), ("Intercom seat", "Desde USD 29/seat/mes anual", "Si se usa con Intercom Helpdesk."), ("Configuración", "USD 0 - 500", "Carga de conocimiento y pruebas."), ("Add-ons opcionales", "USD 99+/mes", "Pro, Copilot u otros módulos.")],
        "pasos":["Activar Fin o trial", "Cargar Knowledge Hub/FAQs", "Definir tono y reglas", "Configurar handoff a Inbox/equipo", "Probar simulaciones", "Publicar por segmento", "Medir outcomes y costo real"],
        "ejemplo":"Cliente: ¿Cuál es el horario?\nFin: Responde usando Knowledge Hub.\n\nCliente: Tengo un reclamo de factura\nFin: Solicita datos mínimos y deriva al equipo configurado.",
        "recomendacion":"Aunque el cliente no quiera Fin, conviene dejarlo en comparación porque puede ser competitivo si se valora velocidad, bajo desarrollo y soporte nativo."
    },
    {
        "nombre":"Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI",
        "categoria":"Código / Backend propio", "nivel":"Avanzado", "tiempo":"2 a 8 semanas", "costo":"Medio-Alto", "tag":"Producción", "color":"purple",
        "mejor_para":"Cliente que no quiere Fin y necesita control total del bot, reglas, prompts, base de conocimiento, alta demanda y escalamiento.",
        "descripcion":"Backend propio en Python/FastAPI que recibe eventos de Intercom, consulta FAQs/documentos, usa OpenAI o Azure OpenAI y responde o escala a agente.",
        "arquitectura":"Intercom Messenger -> Webhook Intercom -> Backend Python/FastAPI -> FAQ/RAG -> OpenAI/Azure OpenAI -> Respuesta o asignación a agente",
        "pros":["Máximo control", "Preguntas abiertas", "Reglas de espera y alta demanda", "Integración CRM/ERP/BD", "Escalamiento personalizado"],
        "contras":["Requiere desarrollo", "Mantenimiento técnico", "Seguridad y monitoreo", "Costos de hosting y API"],
        "necesitas":["Developer Hub/API/Webhooks de Intercom", "Token privado Intercom", "OpenAI o Azure OpenAI", "Servidor público", "Base de conocimiento", "Logs/BD", "Equipo técnico Python", "Políticas de seguridad"],
        "inicial":(1500,8000), "mensual":(80,600), "fin":False,
        "variable":"Tokens IA + hosting + monitoreo. Crece con volumen y complejidad.",
        "rubros":[("Desarrollo inicial", "USD 1.500 - 8.000", "Backend, webhooks, lógica, pruebas."), ("Hosting/API", "USD 20 - 200/mes", "Servidor o serverless."), ("OpenAI/Azure OpenAI", "Según tokens", "Costo por uso."), ("Vector DB/RAG opcional", "USD 0 - 150/mes", "Para documentos extensos."), ("Mantenimiento", "USD 100 - 500/mes", "Ajustes y monitoreo.")],
        "pasos":["Crear app privada en Intercom", "Configurar webhooks", "Crear backend Python/FastAPI", "Construir base de conocimiento", "Integrar OpenAI/Azure OpenAI", "Clasificar intención", "Responder/asignar en Intercom", "Registrar métricas", "Probar y publicar"],
        "ejemplo":"Cliente: ¿Cuál es el horario?\nBot Python: Consulta FAQ y responde.\n\nCliente: Tengo una queja por facturación\nBot Python: Detecta caso sensible y asigna a agente.",
        "recomendacion":"La opción más completa para producción si se quiere evitar Fin y mantener control total."
    },
    {
        "nombre":"Zapier + Intercom + ChatGPT/OpenAI",
        "categoria":"No-code / Low-code", "nivel":"Básico-Medio", "tiempo":"1 a 5 días", "costo":"Medio", "tag":"Demo rápida", "color":"orange",
        "mejor_para":"Demo rápida o automatizaciones simples sin backend propio.",
        "descripcion":"Zaps donde Intercom dispara una acción en ChatGPT/OpenAI y luego registra nota, tag, ticket, respuesta o escalamiento.",
        "arquitectura":"Intercom Trigger -> Zapier -> ChatGPT/OpenAI -> Filtros/Paths -> Intercom Action/Webhook",
        "pros":["Muy rápido", "No-code", "Buen prototipo", "Conecta muchas apps"],
        "contras":["Costos por tareas", "Menor control", "Responder directo puede requerir API", "Dependencia de Zapier"],
        "necesitas":["Cuenta Zapier", "Intercom conectado", "OpenAI conectado", "Triggers", "Prompts", "Paths/Filtros", "Pruebas de tareas"],
        "inicial":(100,800), "mensual":(20,150), "fin":False,
        "variable":"Tareas Zapier + tokens OpenAI. En multi-step, cada acción consume tareas.",
        "rubros":[("Configuración", "USD 100 - 800", "Zaps, prompts y pruebas."), ("Zapier", "Desde USD 19,99/mes aprox.", "Según tareas."), ("OpenAI", "Según tokens", "Generación y clasificación."), ("Mantenimiento", "USD 50 - 200/mes", "Ajustes a Zaps.")],
        "pasos":["Crear Zap con trigger", "Agregar ChatGPT/OpenAI", "Crear filtros/paths", "Agregar acción Intercom/webhook", "Probar", "Publicar"],
        "ejemplo":"Nueva conversación -> ChatGPT clasifica -> si es FAQ responde/sugiere -> si es reclamo tag y escala.",
        "recomendacion":"Ideal para validar rápido, no para alto volumen crítico."
    },
    {
        "nombre":"Make.com + Intercom + OpenAI",
        "categoria":"No-code / Automatización visual", "nivel":"Medio", "tiempo":"2 a 10 días", "costo":"Medio", "tag":"Visual", "color":"orange",
        "mejor_para":"Flujos visuales con routers, filtros y llamadas HTTP/API más flexibles.",
        "descripcion":"Escenarios en Make que reciben eventos de Intercom, consultan OpenAI y actualizan Intercom con reglas visuales.",
        "arquitectura":"Intercom/Webhook -> Make Scenario -> Router -> OpenAI + Knowledge Base -> Intercom API",
        "pros":["Visual", "Routers/filtros potentes", "HTTP flexible", "Buen costo para prototipos"],
        "contras":["Requiere configuración", "Costos por créditos", "Fragilidad si cambian campos", "Dependencia de Make"],
        "necesitas":["Cuenta Make", "Módulo Intercom o webhook", "OpenAI", "Base de conocimiento", "Routers", "Manejo de errores"],
        "inicial":(200,1200), "mensual":(12,120), "fin":False,
        "variable":"Créditos Make + tokens OpenAI + posibles conectores externos.",
        "rubros":[("Configuración", "USD 200 - 1.200", "Escenarios y routers."), ("Make", "Desde USD 12/mes aprox.", "Según créditos."), ("OpenAI", "Según tokens", "Costo por conversación."), ("Mantenimiento", "USD 50 - 250/mes", "Ajustes.")],
        "pasos":["Crear escenario", "Recibir evento Intercom", "Agregar router", "Consultar FAQ", "Llamar OpenAI", "Responder/asignar vía Intercom", "Monitorear"],
        "ejemplo":"Router horario -> respuesta fija. Router factura -> agente. Router abierta -> OpenAI + contexto.",
        "recomendacion":"Muy buena alternativa no-code si Zapier se queda corto."
    },
    {
        "nombre":"n8n + Intercom + OpenAI",
        "categoria":"Low-code / Self-hosted opcional", "nivel":"Medio-Avanzado", "tiempo":"1 a 3 semanas", "costo":"Bajo-Medio", "tag":"Flexible", "color":"purple",
        "mejor_para":"Automatización visual con opción self-hosted y más control técnico.",
        "descripcion":"Workflows con Intercom, OpenAI, reglas, HTTP y logs; puede ser cloud o self-hosted.",
        "arquitectura":"Intercom Webhook -> n8n Workflow -> OpenAI Node/HTTP -> IF/Switch -> Intercom API",
        "pros":["Self-host opcional", "Flexible", "Bueno para APIs", "Económico en flujos complejos"],
        "contras":["Curva técnica", "Self-host requiere mantenimiento", "Hay que asegurar disponibilidad"],
        "necesitas":["n8n Cloud o servidor", "Credenciales Intercom", "OpenAI", "Dominio/SSL si self-hosted", "Base de conocimiento", "Monitoreo"],
        "inicial":(300,2000), "mensual":(0,800), "fin":False,
        "variable":"n8n Cloud por ejecuciones o servidor self-hosted + tokens IA.",
        "rubros":[("Configuración", "USD 300 - 2.000", "Workflows y pruebas."), ("n8n Cloud", "Desde ~20€/mes anual", "Según ejecuciones."), ("Self-hosting", "USD 5 - 50/mes", "Servidor y backups."), ("OpenAI", "Según tokens", "Costo por uso."), ("Mantenimiento", "USD 50 - 300/mes", "Soporte.")],
        "pasos":["Crear workflow", "Configurar webhook/Intercom", "Agregar OpenAI", "Crear IF/Switch", "Llamar Intercom API", "Guardar logs", "Activar"],
        "ejemplo":"Webhook recibe mensaje -> OpenAI clasifica -> IF horario responde -> IF baja confianza asigna a agente.",
        "recomendacion":"Buena para balance entre control y costo; más técnica que Make/Zapier."
    },
    {
        "nombre":"Asistente RAG documental + Intercom",
        "categoria":"IA documental", "nivel":"Avanzado", "tiempo":"3 a 8 semanas", "costo":"Medio-Alto", "tag":"Documentos", "color":"purple",
        "mejor_para":"Empresas con manuales, políticas o documentación extensa.",
        "descripcion":"Indexar documentos, buscar fragmentos relevantes y generar respuestas con evidencia. Si no encuentra contexto, escala.",
        "arquitectura":"Intercom -> Backend Python -> Vector DB/Azure AI Search/Pinecone -> LLM -> Intercom",
        "pros":["Respuestas basadas en documentos", "Mejor para preguntas abiertas", "Reduce respuestas inventadas", "Escalable"],
        "contras":["Mayor desarrollo", "Hay que limpiar documentos", "Evaluación continua", "Costo de búsqueda/vector DB"],
        "necesitas":["Todo lo de Python propio", "Documentos limpios", "Embeddings", "Vector DB/buscador", "Proceso de actualización", "Evaluación de precisión"],
        "inicial":(2500,12000), "mensual":(150,1000), "fin":False,
        "variable":"Tokens + embeddings + almacenamiento/buscador + mantenimiento documental.",
        "rubros":[("Desarrollo", "USD 2.500 - 12.000", "RAG y backend."), ("Vector DB", "USD 0 - 500/mes", "Según volumen."), ("OpenAI/Azure", "Según tokens", "Embeddings + respuestas."), ("Mantenimiento", "USD 100 - 500/mes", "Actualizar contenido.")],
        "pasos":["Recolectar documentos", "Limpiar y fragmentar", "Crear embeddings", "Integrar Intercom", "Recuperar contexto", "Responder con evidencia", "Escalar si no hay confianza", "Medir precisión"],
        "ejemplo":"Cliente pregunta garantía -> Bot busca política oficial -> responde -> si no hay claridad, escala.",
        "recomendacion":"La mejor opción si hay mucha documentación y se requieren respuestas confiables."
    },
    {
        "nombre":"Botpress / Voiceflow / plataforma chatbot + Intercom",
        "categoria":"Plataforma chatbot", "nivel":"Medio", "tiempo":"1 a 4 semanas", "costo":"Medio-Alto", "tag":"Chatbot visual", "color":"green",
        "mejor_para":"Equipos que prefieren flujos visuales administrables por negocio.",
        "descripcion":"Crear bot en una plataforma especializada y conectarlo a Intercom mediante integración, webhook o API.",
        "arquitectura":"Intercom -> Webhook/API -> Plataforma chatbot -> LLM/KB -> Handoff Intercom",
        "pros":["Flujos visuales", "Menos código", "Administrable por negocio", "Analítica"],
        "contras":["Costo proveedor", "Lock-in", "Integración custom", "Limitaciones por plataforma"],
        "necesitas":["Cuenta plataforma chatbot", "Licencia", "Conector/API con Intercom", "Diseño de intents", "Base de conocimiento", "Reglas de handoff"],
        "inicial":(500,3000), "mensual":(50,1000), "fin":False,
        "variable":"Mensajes/conversaciones de la plataforma + IA + add-ons.",
        "rubros":[("Diseño/configuración", "USD 500 - 3.000", "Flujos e intents."), ("Licencia", "USD 50 - 1.000+/mes", "Según proveedor."), ("OpenAI/LLM", "Incluido o separado", "Según plataforma."), ("Mantenimiento", "USD 100 - 400/mes", "Ajustes.")],
        "pasos":["Elegir plataforma", "Crear intents", "Cargar conocimiento", "Conectar Intercom", "Definir fallback", "Probar y publicar"],
        "ejemplo":"Saludo -> pregunta abierta -> intención -> respuesta FAQ o handoff.",
        "recomendacion":"Buena si negocio quiere gestionar conversaciones sin depender siempre de desarrollo."
    },
]

FAQ = {"horario":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.", "horarios":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.", "precio":"Para darte precios exactos necesito saber el producto o servicio. Si quieres, te conecto con un agente comercial.", "ubicacion":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.", "ubicación":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.", "pago":"Aceptamos los métodos de pago definidos por la empresa. Un agente puede confirmar el detalle según tu caso."}
ESCALATION_KEYWORDS = ["reclamo", "queja", "cancelar", "devolución", "devolucion", "factura", "garantía", "garantia", "asesor", "humano", "agente"]

def usd(x): return f"USD {x:,.0f}".replace(",", ".")
def cop(x, rate): return f"COP {x*rate:,.0f}".replace(",", ".")
def badge_class(color): return {"green":"badge badge-green", "purple":"badge badge-purple", "orange":"badge badge-orange"}.get(color, "badge")

def simular_respuesta(solution, question, queue_size, threshold, company_name):
    q = question.lower()
    response = next((ans for key, ans in FAQ.items() if key in q), None)
    needs_agent = any(k in q for k in ESCALATION_KEYWORDS)
    demand = queue_size >= threshold
    demand_msg = " Tenemos alta demanda; el sistema avisaría al cliente y mantendría la conversación en espera controlada." if demand else ""
    tech = solution["nombre"]
    if solution.get("fin"):
        channel = "Fin buscaría la respuesta en Knowledge Hub/Procedures y haría handoff nativo en Intercom."
    elif "Python" in tech:
        channel = "El backend Python recibiría el webhook, clasificaría la intención y respondería/asignaría usando la API de Intercom."
    elif "Zapier" in tech:
        channel = "Zapier ejecutaría el Zap: trigger de Intercom, paso ChatGPT/OpenAI, filtro y acción de Intercom/Webhook."
    elif "Make" in tech:
        channel = "Make ejecutaría el escenario visual con routers: FAQ, OpenAI o escalamiento a agente."
    elif "n8n" in tech:
        channel = "n8n ejecutaría el workflow con IF/Switch, nodo OpenAI y llamada HTTP/API a Intercom."
    elif "RAG" in tech:
        channel = "El asistente RAG buscaría evidencia en documentos antes de responder; sin evidencia escalaría."
    else:
        channel = "La plataforma chatbot detectaría intención y enviaría respuesta o handoff hacia Intercom."
    if response and not needs_agent:
        decision = response
    elif needs_agent:
        decision = f"Voy a transferir tu solicitud a un agente de {company_name}."
    else:
        decision = f"Para responder con seguridad voy a pasar tu caso a un agente de {company_name}."
    return f"**Tecnología seleccionada:** {tech}\n\n**Cómo actuaría:** {channel}\n\n**Respuesta al cliente:** {decision}{demand_msg}"

st.markdown("""
<div class="hero">
<h1>🤖 Intercom AI Options Lab</h1>
<p>Comparador profesional de alternativas para atención al cliente: Fin, Python propio, OpenAI, Zapier, Make, n8n, RAG y plataformas chatbot.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎛️ Panel")
    categorias = sorted(set(s["categoria"] for s in SOLUTIONS))
    categoria = st.selectbox("Categoría", ["Todas"] + categorias)
    nivel = st.selectbox("Nivel técnico", ["Todos", "Básico-Medio", "Medio", "Medio-Avanzado", "Avanzado"])
    modo = st.radio("Vista", ["Todas las opciones", "Solo recomendadas para demo", "Solo producción"], horizontal=False)
    st.divider()
    st.header("🧮 Costos")
    usd_to_cop = st.number_input("TRM COP/USD", min_value=3000, max_value=6000, value=USD_TO_COP_DEFAULT, step=50)
    conversaciones_mes = st.number_input("Conversaciones/mes", min_value=100, max_value=200000, value=5000, step=100)
    pct_ia = st.slider("% procesado por IA", 10, 100, 60, 5)
    tokens_in = st.number_input("Tokens entrada prom.", min_value=100, max_value=10000, value=1200, step=100)
    tokens_out = st.number_input("Tokens salida prom.", min_value=50, max_value=5000, value=350, step=50)
    input_price = st.number_input("USD / 1M tokens entrada", min_value=0.01, max_value=50.0, value=0.75, step=0.05)
    output_price = st.number_input("USD / 1M tokens salida", min_value=0.01, max_value=100.0, value=4.50, step=0.10)
    fin_outcome_price = st.number_input("Fin: USD por outcome", min_value=0.1, max_value=5.0, value=0.99, step=0.01)
    fin_seats = st.number_input("Fin/Intercom seats", min_value=0, max_value=500, value=3, step=1)
    fin_seat_price = st.number_input("USD por seat Intercom", min_value=0, max_value=300, value=29, step=1)
    st.divider()
    st.header("⚙️ Simulador")
    company_name = st.text_input("Empresa", value="Mi Empresa")
    queue_size = st.number_input("Personas en espera", min_value=0, value=12)
    high_demand_threshold = st.number_input("Umbral alta demanda", min_value=1, value=10)

filtered = SOLUTIONS
if categoria != "Todas": filtered = [s for s in filtered if s["categoria"] == categoria]
if nivel != "Todos": filtered = [s for s in filtered if s["nivel"] == nivel]
if modo == "Solo recomendadas para demo": filtered = [s for s in filtered if any(k in s["nombre"] for k in ["Zapier", "Make", "Fin"])]
if modo == "Solo producción": filtered = [s for s in filtered if any(k in s["nombre"] for k in ["Python", "RAG", "Fin"])]

ia_conversations = conversaciones_mes * pct_ia / 100
ai_monthly = (ia_conversations * tokens_in / 1_000_000 * input_price) + (ia_conversations * tokens_out / 1_000_000 * output_price)
fin_monthly = (ia_conversations * fin_outcome_price) + (fin_seats * fin_seat_price)

left, right = st.columns([1.02, 1.58], gap="large")
with left:
    st.markdown('<div class="card"><h3>📚 Opciones disponibles</h3><p class="small-muted">Selecciona una tecnología para ver inversión, requisitos y simulador adaptado.</p></div>', unsafe_allow_html=True)
    if not filtered:
        st.warning("No hay opciones con esos filtros.")
        selected_name = None
    else:
        selected_name = st.radio("Selecciona", [s["nombre"] for s in filtered], label_visibility="collapsed")
        st.markdown("### Resumen rápido")
        for s in filtered:
            ini, mon = s["inicial"], s["mensual"]
            extra = fin_monthly if s.get("fin") else ai_monthly
            total_low, total_high = mon[0] + extra, mon[1] + extra
            st.markdown(f"""
<div class="card">
<span class="{badge_class(s['color'])}">{s['tag']}</span><span class="badge">{s['nivel']}</span>
<b>{s['nombre']}</b><br>
<span class="small-muted">Inicial: {usd(ini[0])}-{usd(ini[1])} · Mensual estimado: {usd(total_low)}-{usd(total_high)}</span>
</div>
""", unsafe_allow_html=True)

with right:
    if selected_name:
        s = next(x for x in filtered if x["nombre"] == selected_name)
        ini_low, ini_high = s["inicial"]
        mon_low, mon_high = s["mensual"]
        variable_cost = fin_monthly if s.get("fin") else ai_monthly
        total_low, total_high = mon_low + variable_cost, mon_high + variable_cost

        st.markdown(f"""
<div class="card">
<span class="{badge_class(s['color'])}">{s['tag']}</span><span class="badge badge-purple">{s['categoria']}</span>
<h3>{s['nombre']}</h3>
<p><b>Mejor para:</b> {s['mejor_para']}</p>
<p>{s['descripcion']}</p>
</div>
""", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        m1.metric("Nivel / tiempo", f"{s['nivel']} · {s['tiempo']}")
        m2.metric("Costo variable IA/mes", f"{usd(variable_cost)} / {cop(variable_cost, usd_to_cop)}")
        m3, m4 = st.columns(2)
        m3.metric("Inicial estimado", f"{usd(ini_low)} - {usd(ini_high)}")
        m4.metric("Mensual total estimado", f"{usd(total_low)} - {usd(total_high)}")

        tab1, tab2, tab3, tab4 = st.tabs(["💰 Inversión", "✅ Requisitos", "🧭 Paso a paso", "💬 Simulador"])
        with tab1:
            c1, c2 = st.columns(2)
            c1.metric("Inicial COP", f"{cop(ini_low, usd_to_cop)} - {cop(ini_high, usd_to_cop)}")
            c2.metric("Mensual COP", f"{cop(total_low, usd_to_cop)} - {cop(total_high, usd_to_cop)}")
            st.markdown("#### Rubros")
            for name, amount, note in s["rubros"]:
                st.write(f"**{name}:** {amount}. {note}")
            st.info(f"Variable principal: {s['variable']}", icon="ℹ️")
        with tab2:
            for req in s["necesitas"]: st.write(f"- {req}")
            st.markdown("#### Arquitectura")
            st.code(s["arquitectura"], language="text")
            a,b = st.columns(2)
            with a:
                st.markdown("#### Pros")
                for p in s["pros"]: st.write(f"✅ {p}")
            with b:
                st.markdown("#### Contras")
                for c in s["contras"]: st.write(f"⚠️ {c}")
        with tab3:
            for i, step in enumerate(s["pasos"], 1): st.write(f"**{i}.** {step}")
            st.markdown("#### Ejemplo")
            st.code(s["ejemplo"], language="text")
            st.success(s["recomendacion"])
        with tab4:
            st.write("El simulador cambia la explicación según la tecnología seleccionada.")
            examples = ["¿Cuál es el horario?", "Quiero hablar con un asesor", "Tengo una queja por facturación", "¿Dónde están ubicados?"]
            q_demo = st.selectbox("Pregunta de ejemplo", examples)
            custom_q = st.text_input("O escribe una pregunta", placeholder="Ej: necesito ayuda con mi factura")
            q_final = custom_q if custom_q.strip() else q_demo
            st.markdown(simular_respuesta(s, q_final, queue_size, high_demand_threshold, company_name))

st.divider()
st.markdown("""
<div class="card">
<h3>✅ Lectura ejecutiva</h3>
<ul>
<li><b>Comparar siempre Fin:</b> aunque el cliente no lo prefiera, puede competir por rapidez y menor desarrollo.</li>
<li><b>Demo rápida:</b> Zapier + OpenAI o Make + OpenAI.</li>
<li><b>Balance control/costo:</b> n8n + OpenAI.</li>
<li><b>Producción robusta:</b> Python + Intercom API/Webhooks + OpenAI/Azure OpenAI.</li>
<li><b>Documentos extensos:</b> RAG documental + Intercom.</li>
</ul>
</div>
""", unsafe_allow_html=True)
st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
