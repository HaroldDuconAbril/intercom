
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Intercom AI Options Lab", page_icon="🤖", layout="wide")

st.markdown("""
<style>
:root{--card:#fff;--line:#e5e7eb;--muted:#64748b;--dark:#0f172a;--blue:#2563eb;--purple:#7c3aed;--green:#16a34a;--orange:#ea580c;--soft:#f8fafc;}
.block-container{padding-top:1.1rem!important;padding-left:2rem!important;padding-right:2rem!important;max-width:1420px;}
html,body,[class*="css"]{font-size:14.2px;color:var(--dark)}
h1{font-size:1.55rem!important;line-height:1.15!important;margin-bottom:.25rem!important} h2{font-size:1.15rem!important} h3{font-size:1.02rem!important;margin-top:.55rem!important} h4{font-size:.92rem!important}
.stMarkdown p,.stMarkdown li{font-size:.89rem!important;line-height:1.38!important}.small{font-size:.78rem;color:var(--muted)}
.hero{background:linear-gradient(135deg,#0f172a 0%,#1d4ed8 58%,#7c3aed 100%);padding:18px 22px;border-radius:18px;color:#fff;margin-bottom:14px;box-shadow:0 14px 34px rgba(15,23,42,.18)}
.hero h1{color:white!important;margin:0!important}.hero p{color:#e0e7ff!important;margin:.35rem 0 0 0!important}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px;box-shadow:0 4px 16px rgba(15,23,42,.045);margin-bottom:10px}.soft{background:#f8fafc}.explain{background:#f8fafc;border-left:4px solid #2563eb;border-radius:12px;padding:10px 12px;margin:8px 0 12px 0;color:#334155;font-size:.86rem;line-height:1.38}
.badge{display:inline-block;padding:3px 8px;border-radius:999px;background:#eff6ff;color:#1d4ed8;font-size:.70rem;font-weight:700;margin-right:5px;margin-bottom:4px}.green{background:#dcfce7;color:#15803d}.purple{background:#f3e8ff;color:#6d28d9}.orange{background:#ffedd5;color:#c2410c}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:14px;padding:9px 10px;box-shadow:0 3px 12px rgba(15,23,42,.04);min-height:68px}div[data-testid="stMetricLabel"] p{font-size:.70rem!important;color:var(--muted)!important;white-space:normal!important}div[data-testid="stMetricValue"]{font-size:.88rem!important;line-height:1.12!important;white-space:normal!important;overflow-wrap:anywhere!important;word-break:break-word!important}
pre,code{font-size:.76rem!important;line-height:1.28!important;border-radius:12px!important}hr{margin:.75rem 0!important}label{font-size:.83rem!important}.stButton>button{border-radius:10px}
</style>
""", unsafe_allow_html=True)

# Supuestos internos simples: se ocultan al cliente para no saturar la vista.
USD_TO_COP = 4000
CONVERSACIONES_MES = 5000
PCT_IA = 60
TOKENS_IN = 1200
TOKENS_OUT = 350
INPUT_PRICE = 0.75
OUTPUT_PRICE = 4.50
FIN_OUTCOME_PRICE = 0.99
FIN_SEATS = 3
FIN_SEAT_PRICE = 29

SOLUTIONS = [
    dict(nombre="Fin AI Agent nativo de Intercom", categoria="Nativo Intercom", nivel="Básico-Medio", tiempo="Horas a pocos días", tag="Nativo", color="green", inicial=(0,500), mensual=(29,800), fin=True,
         mejor="Comparar contra alternativas externas; ideal si se quiere activar rápido y reducir desarrollo.",
         desc="Usa Fin dentro de Intercom o como Fin standalone. Responde con conocimiento configurado, escala a agente y cobra por outcome/resolución.",
         arq="Intercom/Fin -> Knowledge Hub/Procedures -> Respuesta automática -> Handoff a Inbox/agente",
         pros=["Implementación rápida", "Menos desarrollo", "Escalamiento nativo", "Reportes integrados", "Puede salir mejor si se valora velocidad"],
         cons=["Menos control que una solución propia", "Costo variable por outcome", "Dependencia del ecosistema Intercom"],
         req=["Plan Intercom o Fin standalone", "Knowledge Hub/FAQs organizado", "Reglas de handoff", "Agentes/equipos configurados", "Medir outcomes mensuales"],
         rubros=[("Fin AI Agent", "USD 0,99/outcome aprox.", "Se cobra cuando Fin logra resolver o completar un resultado medible. Si el volumen de conversaciones sube, este valor puede crecer."), ("Intercom seat", "Desde USD 29/seat/mes aprox.", "Corresponde a usuarios/agentes con acceso al helpdesk de Intercom, si se usa Fin junto con Intercom."), ("Configuración", "USD 0 - 500", "Trabajo inicial para cargar conocimiento, ajustar tono, probar handoff y validar respuestas.")],
         pasos=["Activar Fin o trial", "Cargar FAQs/Knowledge Hub", "Definir tono y reglas", "Configurar handoff", "Probar simulaciones", "Publicar y medir outcomes"],
         ejemplo="Cliente: ¿Cuál es el horario?\nFin: Responde con Knowledge Hub.\n\nCliente: Tengo un reclamo de factura\nFin: deriva al equipo configurado."),
    dict(nombre="Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI", categoria="Código / Backend propio", nivel="Avanzado", tiempo="2 a 8 semanas", tag="Producción", color="purple", inicial=(1500,8000), mensual=(80,600), fin=False,
         mejor="Cliente que no quiere Fin y necesita control total del bot, reglas, base de conocimiento, alta demanda y escalamiento.",
         desc="Backend propio en Python/FastAPI que recibe eventos de Intercom, consulta FAQs/documentos, usa OpenAI o Azure OpenAI y responde o escala a agente.",
         arq="Intercom Messenger -> Webhook Intercom -> Backend Python/FastAPI -> FAQ/RAG -> OpenAI/Azure OpenAI -> Respuesta o asignación a agente",
         pros=["Máximo control", "Preguntas abiertas", "Reglas de espera y alta demanda", "Integración con CRM/ERP/BD", "Escalamiento personalizado"],
         cons=["Requiere desarrollo", "Mantenimiento técnico", "Seguridad y monitoreo", "Costos de hosting y API"],
         req=["Intercom Developer Hub/API/Webhooks", "Token Intercom", "OpenAI o Azure OpenAI", "Servidor público", "Base de conocimiento", "Logs/BD", "Equipo técnico Python"],
         rubros=[("Desarrollo inicial", "USD 1.500 - 8.000", "Construcción del backend, integración con Intercom, lógica de decisión, pruebas y despliegue."), ("Hosting/API", "USD 20 - 200/mes", "Servidor o servicio cloud que recibe los webhooks y mantiene el bot disponible."), ("OpenAI/Azure OpenAI", "Según uso", "Costo por consumo del modelo IA. Depende de cuántas preguntas procese y qué tan largas sean las respuestas."), ("Mantenimiento", "USD 100 - 500/mes", "Ajuste de prompts, monitoreo, corrección de errores y actualización de reglas/FAQs.")],
         pasos=["Crear app privada Intercom", "Configurar webhooks", "Crear backend Python", "Construir conocimiento", "Integrar OpenAI/Azure", "Clasificar intención", "Responder/asignar", "Medir y publicar"],
         ejemplo="Cliente: ¿Cuál es el horario?\nBot Python: consulta FAQ y responde.\n\nCliente: Tengo queja por facturación\nBot Python: detecta caso sensible y asigna agente."),
    dict(nombre="Zapier + Intercom + ChatGPT/OpenAI", categoria="No-code / Low-code", nivel="Básico-Medio", tiempo="1 a 5 días", tag="Demo rápida", color="orange", inicial=(100,800), mensual=(20,150), fin=False,
         mejor="Demo rápida o automatizaciones simples sin backend propio.", desc="Zaps donde Intercom dispara una acción en ChatGPT/OpenAI y luego registra nota, tag, ticket, respuesta o escalamiento.", arq="Intercom Trigger -> Zapier -> ChatGPT/OpenAI -> Filtros/Paths -> Intercom Action/Webhook",
         pros=["Muy rápido", "No-code", "Buen prototipo", "Conecta muchas apps"], cons=["Costos por tareas", "Menor control", "Responder directo puede requerir API", "Dependencia de Zapier"],
         req=["Cuenta Zapier", "Intercom conectado", "OpenAI conectado", "Triggers", "Prompts", "Paths/Filtros"], rubros=[("Configuración", "USD 100 - 800", "Armado de Zaps, filtros, prompts y pruebas con casos reales."), ("Zapier", "Desde USD 19,99/mes aprox.", "Se paga por plan y tareas. Cada acción automatizada puede consumir tareas."), ("OpenAI", "Según uso", "Costo por las respuestas o clasificaciones generadas por IA.")],
         pasos=["Crear Zap", "Agregar OpenAI", "Crear filtros", "Acción Intercom/Webhook", "Probar", "Publicar"], ejemplo="Nueva conversación -> ChatGPT clasifica -> FAQ responde/sugiere -> reclamo escala."),
    dict(nombre="Make.com + Intercom + OpenAI", categoria="No-code / Automatización visual", nivel="Medio", tiempo="2 a 10 días", tag="Visual", color="orange", inicial=(200,1200), mensual=(12,120), fin=False,
         mejor="Flujos visuales con routers, filtros y llamadas HTTP/API más flexibles.", desc="Escenarios visuales en Make que reciben eventos de Intercom, consultan OpenAI y actualizan Intercom con reglas.", arq="Intercom/Webhook -> Make Scenario -> Router -> OpenAI + Knowledge Base -> Intercom API",
         pros=["Visual", "Routers potentes", "HTTP flexible", "Buen costo para prototipos"], cons=["Requiere configuración", "Costos por créditos", "Dependencia de Make"], req=["Cuenta Make", "Módulo Intercom o webhook", "OpenAI", "Base de conocimiento", "Routers", "Errores/reintentos"],
         rubros=[("Configuración", "USD 200 - 1.200", "Diseño de escenarios, routers, reglas de escalamiento y pruebas."), ("Make", "Desde USD 12/mes aprox.", "Se cobra por créditos/operaciones ejecutadas en los escenarios."), ("OpenAI", "Según uso", "Costo por las consultas enviadas al modelo IA.")], pasos=["Crear escenario", "Recibir evento", "Agregar router", "Consultar FAQ", "Llamar OpenAI", "Responder/asignar"], ejemplo="Router horario -> respuesta fija. Router factura -> agente. Router abierta -> OpenAI."),
    dict(nombre="n8n + Intercom + OpenAI", categoria="Low-code / Self-hosted opcional", nivel="Medio-Avanzado", tiempo="1 a 3 semanas", tag="Flexible", color="purple", inicial=(300,2000), mensual=(0,800), fin=False,
         mejor="Automatización visual con opción self-hosted y más control técnico.", desc="Workflows con Intercom, OpenAI, reglas, HTTP y logs; puede ser cloud o self-hosted.", arq="Intercom Webhook -> n8n Workflow -> OpenAI Node/HTTP -> IF/Switch -> Intercom API",
         pros=["Self-host opcional", "Flexible", "Bueno para APIs", "Económico en flujos complejos"], cons=["Curva técnica", "Self-host requiere mantenimiento", "Hay que asegurar disponibilidad"], req=["n8n Cloud o servidor", "Credenciales Intercom", "OpenAI", "Dominio/SSL si self-hosted", "Base de conocimiento"],
         rubros=[("Configuración", "USD 300 - 2.000", "Construcción de workflows, nodos, reglas, APIs y pruebas."), ("n8n Cloud/self-host", "USD 0 - 800/mes", "Cloud cobra por ejecuciones; self-host puede bajar costo pero exige administración técnica."), ("OpenAI", "Según uso", "Costo de llamadas al modelo IA.")], pasos=["Crear workflow", "Webhook/Intercom", "OpenAI", "IF/Switch", "Intercom API", "Logs", "Activar"], ejemplo="Webhook -> OpenAI clasifica -> IF horario responde -> baja confianza asigna agente."),
    dict(nombre="Asistente RAG documental + Intercom", categoria="IA documental", nivel="Avanzado", tiempo="3 a 8 semanas", tag="Documentos", color="purple", inicial=(2500,12000), mensual=(150,1000), fin=False,
         mejor="Empresas con manuales, políticas o documentación extensa.", desc="Indexa documentos, busca fragmentos relevantes y genera respuestas con evidencia; si no encuentra contexto, escala.", arq="Intercom -> Backend Python -> Vector DB/Azure AI Search/Pinecone -> LLM -> Intercom",
         pros=["Basado en documentos", "Mejor para preguntas abiertas", "Reduce respuestas inventadas", "Escalable"], cons=["Mayor desarrollo", "Limpiar documentos", "Evaluación continua", "Costo de búsqueda/vector DB"], req=["Todo lo de Python propio", "Documentos limpios", "Embeddings", "Vector DB/buscador", "Actualización documental"],
         rubros=[("Desarrollo", "USD 2.500 - 12.000", "Construcción del sistema que lee documentos y responde con base en evidencia."), ("Vector DB", "USD 0 - 500/mes", "Base para buscar documentos relevantes. Puede ser local o servicio cloud."), ("OpenAI/Azure", "Según uso", "Costo por embeddings y respuestas generadas.")], pasos=["Recolectar documentos", "Limpiar/fragmentar", "Embeddings", "Integrar Intercom", "Recuperar contexto", "Responder con evidencia", "Escalar si no hay confianza"], ejemplo="Cliente pregunta garantía -> busca política oficial -> responde o escala."),
    dict(nombre="Botpress / Voiceflow / plataforma chatbot + Intercom", categoria="Plataforma chatbot", nivel="Medio", tiempo="1 a 4 semanas", tag="Chatbot visual", color="green", inicial=(500,3000), mensual=(50,1000), fin=False,
         mejor="Equipos que prefieren flujos visuales administrables por negocio.", desc="Bot en plataforma especializada conectado a Intercom mediante integración, webhook o API.", arq="Intercom -> Webhook/API -> Plataforma chatbot -> LLM/KB -> Handoff Intercom",
         pros=["Flujos visuales", "Menos código", "Administrable por negocio", "Analítica"], cons=["Costo proveedor", "Lock-in", "Integración custom", "Limitaciones por plataforma"], req=["Cuenta plataforma", "Licencia", "Conector/API Intercom", "Intents", "Base de conocimiento", "Handoff"], rubros=[("Diseño/configuración", "USD 500 - 3.000", "Diseño de flujos, intents, mensajes y pruebas."), ("Licencia", "USD 50 - 1.000+/mes", "Depende de proveedor, usuarios y volumen."), ("OpenAI/LLM", "Incluido o separado", "Algunas plataformas lo incluyen y otras lo cobran aparte.")], pasos=["Elegir plataforma", "Crear intents", "Cargar conocimiento", "Conectar Intercom", "Fallback", "Probar"], ejemplo="Saludo -> pregunta abierta -> intención -> FAQ o handoff."),
]
FAQ = {"horario":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.", "horarios":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.", "precio":"Para darte precios exactos necesito saber el producto o servicio. Si quieres, te conecto con un agente comercial.", "ubicacion":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.", "ubicación":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.", "pago":"Aceptamos los métodos de pago definidos por la empresa. Un agente puede confirmar el detalle según tu caso."}
ESCALATION_KEYWORDS=["reclamo","queja","cancelar","devolución","devolucion","factura","garantía","garantia","asesor","humano","agente"]

def usd(x): return f"USD {x:,.0f}".replace(",",".")
def cop(x): return f"COP {x*USD_TO_COP:,.0f}".replace(",",".")
def badge(color): return {"green":"badge green","purple":"badge purple","orange":"badge orange"}.get(color,"badge")

def simular(s,q,queue,threshold,company):
    low=q.lower(); resp=next((a for k,a in FAQ.items() if k in low),None); agent=any(k in low for k in ESCALATION_KEYWORDS); demand=queue>=threshold
    if s.get("fin"): flow="Fin usaría Knowledge Hub/Procedures y handoff nativo en Intercom."
    elif "Python" in s["nombre"]: flow="El backend Python recibiría el webhook, clasificaría la intención y respondería/asignaría con API de Intercom."
    elif "Zapier" in s["nombre"]: flow="Zapier ejecutaría trigger de Intercom, OpenAI, filtros y acción Intercom/Webhook."
    elif "Make" in s["nombre"]: flow="Make usaría routers visuales para FAQ, OpenAI o escalamiento."
    elif "n8n" in s["nombre"]: flow="n8n ejecutaría IF/Switch, nodo OpenAI y llamada HTTP/API a Intercom."
    elif "RAG" in s["nombre"]: flow="RAG buscaría evidencia documental antes de responder; sin evidencia escalaría."
    else: flow="La plataforma chatbot detectaría intención y haría respuesta o handoff hacia Intercom."
    ans=resp if resp and not agent else (f"Voy a transferir tu solicitud a un agente de {company}." if agent else f"Para responder con seguridad pasaré tu caso a un agente de {company}.")
    if demand: ans += " En este momento tenemos alta demanda; por favor espera mientras un agente queda disponible."
    return f"**Cómo actuaría esta tecnología:** {flow}\n\n**Respuesta al cliente:** {ans}"

# Cálculos internos no editables para cliente.
ia_conversations=CONVERSACIONES_MES*PCT_IA/100
ai_monthly=(ia_conversations*TOKENS_IN/1_000_000*INPUT_PRICE)+(ia_conversations*TOKENS_OUT/1_000_000*OUTPUT_PRICE)
fin_monthly=(ia_conversations*FIN_OUTCOME_PRICE)+(FIN_SEATS*FIN_SEAT_PRICE)

st.markdown('<div class="hero"><h1>🤖 Intercom AI Options Lab</h1><p>Comparador profesional de alternativas para atención al cliente: Fin, Python propio, OpenAI, Zapier, Make, n8n, RAG y plataformas chatbot.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎛️ Panel")
    categoria=st.selectbox("Categoría", ["Todas"]+sorted(set(s["categoria"] for s in SOLUTIONS)))
    nivel=st.selectbox("Nivel técnico", ["Todos","Básico-Medio","Medio","Medio-Avanzado","Avanzado"])
    modo=st.radio("Vista", ["Todas las opciones","Solo recomendadas para demo","Solo producción"])
    st.divider()
    st.header("💬 Simulador")
    company=st.text_input("Empresa", value="Mi Empresa")
    queue_size=st.number_input("Personas en espera", min_value=0, value=12, help="Si supera el umbral, el simulador muestra mensaje de alta demanda.")
    threshold=st.number_input("Umbral alta demanda", min_value=1, value=10)

filtered=SOLUTIONS
if categoria!="Todas": filtered=[s for s in filtered if s["categoria"]==categoria]
if nivel!="Todos": filtered=[s for s in filtered if s["nivel"]==nivel]
if modo=="Solo recomendadas para demo": filtered=[s for s in filtered if any(k in s["nombre"] for k in ["Zapier","Make","Fin"])]
if modo=="Solo producción": filtered=[s for s in filtered if any(k in s["nombre"] for k in ["Python","RAG","Fin"])]

left,right=st.columns([1.02,1.58],gap="large")
with left:
    st.markdown('<div class="card"><h3>📚 Opciones disponibles</h3><p class="small">Selecciona una tecnología para ver inversión, requisitos y simulador adaptado.</p></div>', unsafe_allow_html=True)
    if not filtered:
        st.warning("No hay opciones con esos filtros."); selected=None
    else:
        selected=st.radio("Selecciona", [s["nombre"] for s in filtered], label_visibility="collapsed")
        st.markdown("### Resumen rápido")
        for s in filtered:
            extra=fin_monthly if s.get("fin") else ai_monthly
            total_low,total_high=s["mensual"][0]+extra,s["mensual"][1]+extra
            st.markdown(f'<div class="card"><span class="{badge(s["color"])}">{s["tag"]}</span><span class="badge">{s["nivel"]}</span><b>{s["nombre"]}</b><br><span class="small">Inicial: {usd(s["inicial"][0])}-{usd(s["inicial"][1])} · Mensual estimado: {usd(total_low)}-{usd(total_high)}</span></div>', unsafe_allow_html=True)

with right:
    if selected:
        s=next(x for x in filtered if x["nombre"]==selected)
        extra=fin_monthly if s.get("fin") else ai_monthly
        total_low,total_high=s["mensual"][0]+extra,s["mensual"][1]+extra
        st.markdown(f'<div class="card"><span class="{badge(s["color"])}">{s["tag"]}</span><span class="badge purple">{s["categoria"]}</span><h3>{s["nombre"]}</h3><p><b>Mejor para:</b> {s["mejor"]}</p><p>{s["desc"]}</p></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2); c1.metric("Tiempo / nivel", f"{s['tiempo']} · {s['nivel']}"); c2.metric("Mensual total estimado", f"{usd(total_low)} - {usd(total_high)}")
        st.markdown(f'<div class="explain">El valor mensual combina la licencia o servicio principal, el uso estimado de IA y posibles costos operativos. Es una referencia para comparar alternativas, no una cotización final.</div>', unsafe_allow_html=True)
        c3,c4=st.columns(2); c3.metric("Inicial estimado", f"{usd(s['inicial'][0])} - {usd(s['inicial'][1])}"); c4.metric("Mensual estimado COP", f"{cop(total_low)} - {cop(total_high)}")
        st.markdown(f'<div class="explain">El valor inicial representa configuración, desarrollo, integración y pruebas. El valor en COP usa una TRM de referencia de {USD_TO_COP:,} COP por USD.</div>'.replace(',', '.'), unsafe_allow_html=True)
        tab1,tab2,tab3,tab4=st.tabs(["💰 Inversión","✅ Requisitos","🧭 Paso a paso","💬 Simulador"])
        with tab1:
            st.markdown("#### ¿A qué se deben los cobros?")
            for n,a,no in s["rubros"]:
                st.markdown(f"**{n}: {a}**")
                st.markdown(f'<div class="explain">{no}</div>', unsafe_allow_html=True)
            if s.get("fin"):
                st.info(f"Para Fin se usa como referencia un escenario de {int(ia_conversations)} outcomes potenciales al mes + {FIN_SEATS} seats. Si el cliente resuelve menos conversaciones con Fin, baja el variable; si resuelve más, sube.", icon="ℹ️")
            else:
                st.info(f"Para IA externa se usa como referencia un escenario de {int(ia_conversations)} conversaciones procesadas por IA. El costo de IA estimado es {usd(ai_monthly)} / {cop(ai_monthly)}; el resto corresponde a licencias, hosting o mantenimiento según la opción.", icon="ℹ️")
        with tab2:
            for r in s["req"]: st.write(f"- {r}")
            st.markdown("#### Arquitectura"); st.code(s["arq"], language="text")
            a,b=st.columns(2)
            with a:
                st.markdown("#### Pros"); [st.write(f"✅ {p}") for p in s["pros"]]
            with b:
                st.markdown("#### Contras"); [st.write(f"⚠️ {c}") for c in s["cons"]]
        with tab3:
            for i,p in enumerate(s["pasos"],1): st.write(f"**{i}.** {p}")
            st.markdown("#### Ejemplo"); st.code(s["ejemplo"], language="text")
        with tab4:
            q_demo=st.selectbox("Pregunta de ejemplo", ["¿Cuál es el horario?","Quiero hablar con un asesor","Tengo una queja por facturación","¿Dónde están ubicados?"])
            custom=st.text_input("O escribe una pregunta", placeholder="Ej: necesito ayuda con mi factura")
            st.markdown(simular(s, custom if custom.strip() else q_demo, queue_size, threshold, company))

st.divider()
st.markdown('<div class="card"><h3>✅ Lectura ejecutiva</h3><ul><li><b>Comparar siempre Fin:</b> puede competir por rapidez y menor desarrollo.</li><li><b>Demo rápida:</b> Zapier + OpenAI o Make + OpenAI.</li><li><b>Balance control/costo:</b> n8n + OpenAI.</li><li><b>Producción robusta:</b> Python + Intercom API/Webhooks + OpenAI/Azure OpenAI.</li><li><b>Documentos extensos:</b> RAG documental + Intercom.</li></ul></div>', unsafe_allow_html=True)
st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
