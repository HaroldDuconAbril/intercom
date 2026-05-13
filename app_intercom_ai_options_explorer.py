
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Intercom AI Options Lab", page_icon="🔬", layout="wide")

st.markdown("""
<style>
:root{
  --ink:#0f172a;--muted:#64748b;--line:#e5e7eb;--card:#ffffff;
  --blue:#2563eb;--violet:#7c3aed;--green:#16a34a;--amber:#d97706;
}
.block-container{padding-top:1.35rem!important;padding-left:2rem!important;padding-right:2rem!important;max-width:1440px;}
html,body,[class*="css"]{font-size:14.2px;color:var(--ink)}
h1{font-size:1.55rem!important;line-height:1.2!important;margin-bottom:.25rem!important} h2{font-size:1.16rem!important} h3{font-size:1.02rem!important;margin-top:.5rem!important}
.stMarkdown p,.stMarkdown li{font-size:.89rem!important;line-height:1.4!important}.small{font-size:.78rem;color:var(--muted)}
.hero{background:linear-gradient(135deg,#020617 0%,#1d4ed8 56%,#7c3aed 100%);padding:24px 28px 24px 28px;border-radius:0 0 22px 22px;color:white;margin:0 0 16px 0;box-shadow:0 18px 42px rgba(15,23,42,.20);overflow:visible;}
.hero h1{color:white!important;margin:.35rem 0 .45rem 0!important;line-height:1.25!important}.hero p{color:#dbeafe!important;margin:.35rem 0 0 0!important}.hero .kicker{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:#bfdbfe;font-weight:700;line-height:1.35;margin-bottom:.35rem;}
.card{background:var(--card);border:1px solid var(--line);border-radius:17px;padding:15px 17px;box-shadow:0 4px 18px rgba(15,23,42,.045);margin-bottom:11px}
.explain{background:#f8fafc;border-left:4px solid var(--blue);border-radius:13px;padding:11px 13px;margin:9px 0 13px;color:#334155;font-size:.86rem;line-height:1.42}.explain strong{color:#0f172a}.warn{border-left-color:var(--amber);background:#fffbeb}.research{border-left-color:var(--violet);background:#faf5ff}
.badge{display:inline-block;padding:3px 8px;border-radius:999px;background:#eff6ff;color:#1d4ed8;font-size:.70rem;font-weight:700;margin-right:5px;margin-bottom:4px}.green{background:#dcfce7;color:#15803d}.purple{background:#f3e8ff;color:#6d28d9}.orange{background:#ffedd5;color:#c2410c}.dark{background:#e2e8f0;color:#334155}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:14px;padding:9px 10px;box-shadow:0 3px 12px rgba(15,23,42,.04);min-height:68px}div[data-testid="stMetricLabel"] p{font-size:.70rem!important;color:var(--muted)!important;white-space:normal!important}div[data-testid="stMetricValue"]{font-size:.88rem!important;line-height:1.12!important;white-space:normal!important;overflow-wrap:anywhere!important;word-break:break-word!important}
pre,code{font-size:.76rem!important;line-height:1.28!important;border-radius:12px!important}hr{margin:.75rem 0!important}label{font-size:.83rem!important}.stButton>button{border-radius:10px}
</style>
""", unsafe_allow_html=True)

USD_TO_COP = 4000
CONVERSACIONES_MES = 5000
PCT_IA = 60
AI_MONTHLY = 4.0
FIN_MONTHLY = (CONVERSACIONES_MES * PCT_IA / 100 * 0.99) + (3 * 29)

FAQ = {
    "horario":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.",
    "horarios":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.",
    "precio":"Para darte precios exactos necesito saber el producto o servicio. Si quieres, te conecto con un agente comercial.",
    "ubicacion":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.",
    "ubicación":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.",
    "pago":"Aceptamos los métodos de pago definidos por la empresa. Un agente puede confirmar el detalle según tu caso."
}
ESCALATION_KEYWORDS=["reclamo","queja","cancelar","devolución","devolucion","factura","garantía","garantia","asesor","humano","agente"]

def usd(x): return f"USD {x:,.0f}".replace(",",".")
def cop(x): return f"COP {x*USD_TO_COP:,.0f}".replace(",",".")
def badge(color): return {"green":"badge green","purple":"badge purple","orange":"badge orange","dark":"badge dark"}.get(color,"badge")
def solution_cost(s):
    extra = FIN_MONTHLY if s.get("fin") else AI_MONTHLY
    return s["mensual"][0] + extra, s["mensual"][1] + extra

def simular(s,q,queue,threshold,company):
    low=q.lower(); resp=next((a for k,a in FAQ.items() if k in low),None)
    agent=any(k in low for k in ESCALATION_KEYWORDS); demand=queue>=threshold
    if s.get("fin"):
        flow="Fin buscaría la respuesta en el Knowledge Hub, aplicaría Procedures si existen y escalaría con handoff nativo dentro de Intercom."
    elif "Python" in s["nombre"]:
        flow="El backend Python recibiría el webhook de Intercom, clasificaría la intención, consultaría la base de conocimiento y respondería o asignaría con la API de Intercom."
    elif "Zapier" in s["nombre"]:
        flow="Zapier ejecutaría un Zap: disparador de Intercom, paso de OpenAI, filtro de decisión y acción final en Intercom o Webhook."
    elif "Make" in s["nombre"]:
        flow="Make usaría un escenario visual con routers para decidir entre FAQ, respuesta con OpenAI o escalamiento a agente."
    elif "n8n" in s["nombre"]:
        flow="n8n ejecutaría un workflow con IF/Switch, nodo OpenAI y llamada HTTP/API a Intercom."
    elif "RAG" in s["nombre"]:
        flow="El RAG buscaría evidencia documental antes de responder. Si no encuentra soporte suficiente, escalaría a humano."
    else:
        flow="La plataforma chatbot detectaría intención, seguiría el flujo visual y enviaría respuesta o handoff hacia Intercom."
    ans=resp if resp and not agent else (f"Voy a transferir tu solicitud a un agente de {company}." if agent else f"Para responder con seguridad pasaré tu caso a un agente de {company}.")
    if demand: ans += " En este momento tenemos alta demanda; por favor espera mientras un agente queda disponible."
    return f"**Cómo actuaría esta tecnología:** {flow}\n\n**Respuesta al cliente:** {ans}"

SOLUTIONS = [
    {"nombre":"Fin AI Agent nativo de Intercom","categoria":"Nativo Intercom","nivel":"Básico-Medio","tiempo":"Horas a pocos días","tag":"Nativo","color":"green","inicial":(0,500),"mensual":(29,800),"fin":True,
     "mejor":"Comparar contra alternativas externas; ideal si se quiere activar rápido y reducir desarrollo.","desc":"Usa Fin dentro de Intercom o como Fin standalone. Responde con conocimiento configurado, escala a agente y cobra por outcome/resolución.","arq":"Intercom/Fin -> Knowledge Hub/Procedures -> Respuesta automática -> Handoff a Inbox/agente",
     "pros":["Implementación rápida","Menos desarrollo","Escalamiento nativo","Reportes integrados","Puede salir mejor si se valora velocidad"],"cons":["Menos control que una solución propia","Costo variable por outcome","Dependencia del ecosistema Intercom"],"req":["Plan Intercom o Fin standalone","Knowledge Hub/FAQs organizado","Reglas de handoff","Agentes/equipos configurados","Medición de outcomes mensuales"],
     "rubros":[("Fin AI Agent","USD 0,99/outcome aprox.","Un outcome es un resultado exitoso medible. En atención al cliente suele significar que Fin resolvió una conversación o completó un procedimiento configurado sin que el agente tenga que intervenir de forma manual. No es lo mismo que un mensaje: una conversación puede tener varios mensajes, pero normalmente se cobra una vez si el resultado se considera exitoso."),("Intercom seat","Desde USD 29/seat/mes aprox.","Es el costo de usuarios o agentes que trabajan dentro del helpdesk de Intercom. Este rubro depende del tamaño del equipo humano, no del número de preguntas de clientes."),("Configuración inicial","USD 0 - 500","Incluye cargar contenido en Knowledge Hub, ajustar tono, definir reglas de escalamiento, probar respuestas y validar qué temas deben ir siempre a humano.")],
     "pasos":["Activar Fin o trial","Cargar FAQs/Knowledge Hub","Definir tono y reglas","Configurar handoff","Probar simulaciones","Publicar y medir outcomes"],"ejemplo":"Cliente: ¿Cuál es el horario?\nFin: Responde con Knowledge Hub.\n\nCliente: Tengo un reclamo de factura\nFin: deriva al equipo configurado."},
    {"nombre":"Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI","categoria":"Código / Backend propio","nivel":"Avanzado","tiempo":"2 a 8 semanas","tag":"Producción","color":"purple","inicial":(1500,8000),"mensual":(80,600),"fin":False,
     "mejor":"Cliente que no quiere Fin y necesita control total del bot, reglas, base de conocimiento, alta demanda y escalamiento.","desc":"Backend propio en Python/FastAPI que recibe eventos de Intercom, consulta FAQs/documentos, usa OpenAI o Azure OpenAI y responde o escala a agente.","arq":"Intercom Messenger -> Webhook Intercom -> Backend Python/FastAPI -> FAQ/RAG -> OpenAI/Azure OpenAI -> Respuesta o asignación a agente",
     "pros":["Máximo control","Preguntas abiertas","Reglas de espera y alta demanda","Integración con CRM/ERP/BD","Escalamiento personalizado"],"cons":["Requiere desarrollo","Mantenimiento técnico","Seguridad y monitoreo","Costos de hosting y API"],"req":["Intercom Developer Hub/API/Webhooks","Token Intercom","OpenAI o Azure OpenAI","Servidor público","Base de conocimiento","Logs/BD","Equipo técnico Python"],
     "rubros":[("Desarrollo inicial","USD 1.500 - 8.000","Construcción a la medida: backend, conexión con Intercom, reglas de negocio, clasificación de preguntas, lógica de alta demanda, handoff a agentes, pruebas y despliegue. Es el rubro más alto porque se crea una solución propia."),("Hosting/API","USD 20 - 200/mes","Servidor o servicio cloud que mantiene el bot disponible. Debe recibir webhooks de Intercom en tiempo real y responder sin interrupciones."),("OpenAI/Azure OpenAI","Según uso","Se paga por consumo del modelo IA. Depende del volumen de conversaciones, longitud de preguntas, contexto enviado y longitud de respuestas."),("Mantenimiento","USD 100 - 500/mes","Ajustes de prompts, mejora de respuestas, revisión de errores, actualización de FAQs y monitoreo de casos escalados.")],
     "pasos":["Crear app privada Intercom","Configurar webhooks","Crear backend Python","Construir conocimiento","Integrar OpenAI/Azure","Clasificar intención","Responder/asignar","Medir y publicar"],"ejemplo":"Cliente: ¿Cuál es el horario?\nBot Python: consulta FAQ y responde.\n\nCliente: Tengo queja por facturación\nBot Python: detecta caso sensible y asigna agente."},
    {"nombre":"Zapier + Intercom + ChatGPT/OpenAI","categoria":"No-code / Low-code","nivel":"Básico-Medio","tiempo":"1 a 5 días","tag":"Demo rápida","color":"orange","inicial":(100,800),"mensual":(20,150),"fin":False,
     "mejor":"Demo rápida o automatizaciones simples sin backend propio.","desc":"Zaps donde Intercom dispara una acción en ChatGPT/OpenAI y luego registra nota, tag, ticket, respuesta o escalamiento.","arq":"Intercom Trigger -> Zapier -> ChatGPT/OpenAI -> Filtros/Paths -> Intercom Action/Webhook",
     "pros":["Muy rápido","No-code","Buen prototipo","Conecta muchas apps"],"cons":["Costos por tareas","Menor control","Responder directo puede requerir API","Dependencia de Zapier"],"req":["Cuenta Zapier","Intercom conectado","OpenAI conectado","Triggers","Prompts","Paths/Filtros"],
     "rubros":[("Configuración","USD 100 - 800","Creación de Zaps, conexión de cuentas, filtros, prompts y pruebas con casos reales. Es menor que Python porque no se desarrolla backend desde cero."),("Zapier","Desde USD 19,99/mes aprox.","Zapier cobra por plan y tareas. Una tarea es una acción ejecutada dentro del flujo; si un mensaje dispara varias acciones, el consumo sube más rápido."),("OpenAI","Según uso","Cada vez que Zapier consulta OpenAI para clasificar o generar una respuesta, se genera consumo de IA. Normalmente es bajo al inicio, pero crece con volumen.")],
     "pasos":["Crear Zap","Agregar OpenAI","Crear filtros","Acción Intercom/Webhook","Probar","Publicar"],"ejemplo":"Nueva conversación -> ChatGPT clasifica -> FAQ responde/sugiere -> reclamo escala."},
    {"nombre":"Make.com + Intercom + OpenAI","categoria":"No-code / Automatización visual","nivel":"Medio","tiempo":"2 a 10 días","tag":"Visual","color":"orange","inicial":(200,1200),"mensual":(12,120),"fin":False,
     "mejor":"Flujos visuales con routers, filtros y llamadas HTTP/API más flexibles.","desc":"Escenarios visuales en Make que reciben eventos de Intercom, consultan OpenAI y actualizan Intercom con reglas.","arq":"Intercom/Webhook -> Make Scenario -> Router -> OpenAI + Knowledge Base -> Intercom API",
     "pros":["Visual","Routers potentes","HTTP flexible","Buen costo para prototipos"],"cons":["Requiere configuración","Costos por créditos","Dependencia de Make"],"req":["Cuenta Make","Módulo Intercom o webhook","OpenAI","Base de conocimiento","Routers","Errores/reintentos"],
     "rubros":[("Configuración","USD 200 - 1.200","Diseño de escenarios, routers, condiciones, conexiones con Intercom, pruebas y manejo de errores."),("Make","Desde USD 12/mes aprox.","Make cobra por créditos u operaciones. Cada módulo ejecutado dentro de un escenario puede consumir créditos."),("OpenAI","Según uso","Se genera costo cada vez que el escenario llama a OpenAI para responder, resumir o clasificar una solicitud.")],
     "pasos":["Crear escenario","Recibir evento","Agregar router","Consultar FAQ","Llamar OpenAI","Responder/asignar"],"ejemplo":"Router horario -> respuesta fija. Router factura -> agente. Router abierta -> OpenAI."},
    {"nombre":"n8n + Intercom + OpenAI","categoria":"Low-code / Self-hosted opcional","nivel":"Medio-Avanzado","tiempo":"1 a 3 semanas","tag":"Flexible","color":"purple","inicial":(300,2000),"mensual":(0,800),"fin":False,
     "mejor":"Automatización visual con opción self-hosted y más control técnico.","desc":"Workflows con Intercom, OpenAI, reglas, HTTP y logs; puede ser cloud o self-hosted.","arq":"Intercom Webhook -> n8n Workflow -> OpenAI Node/HTTP -> IF/Switch -> Intercom API",
     "pros":["Self-host opcional","Flexible","Bueno para APIs","Económico en flujos complejos"],"cons":["Curva técnica","Self-host requiere mantenimiento","Hay que asegurar disponibilidad"],"req":["n8n Cloud o servidor","Credenciales Intercom","OpenAI","Dominio/SSL si self-hosted","Base de conocimiento"],
     "rubros":[("Configuración","USD 300 - 2.000","Construcción de workflows, nodos, condiciones, conexión con Intercom/OpenAI, pruebas y monitoreo."),("n8n Cloud/self-host","USD 0 - 800/mes","Cloud cobra por ejecuciones. Self-host puede bajar costo, pero exige servidor, backups, seguridad y administración técnica."),("OpenAI","Según uso","Se paga por llamadas al modelo cuando el workflow necesita clasificar o generar una respuesta.")],
     "pasos":["Crear workflow","Webhook/Intercom","OpenAI","IF/Switch","Intercom API","Logs","Activar"],"ejemplo":"Webhook -> OpenAI clasifica -> IF horario responde -> baja confianza asigna agente."},
    {"nombre":"Asistente RAG documental + Intercom","categoria":"IA documental","nivel":"Avanzado","tiempo":"3 a 8 semanas","tag":"Documentos","color":"purple","inicial":(2500,12000),"mensual":(150,1000),"fin":False,
     "mejor":"Empresas con manuales, políticas o documentación extensa.","desc":"Indexa documentos, busca fragmentos relevantes y genera respuestas con evidencia; si no encuentra contexto, escala.","arq":"Intercom -> Backend Python -> Vector DB/Azure AI Search/Pinecone -> LLM -> Intercom",
     "pros":["Basado en documentos","Mejor para preguntas abiertas","Reduce respuestas inventadas","Escalable"],"cons":["Mayor desarrollo","Limpiar documentos","Evaluación continua","Costo de búsqueda/vector DB"],"req":["Todo lo de Python propio","Documentos limpios","Embeddings","Vector DB/buscador","Actualización documental"],
     "rubros":[("Desarrollo","USD 2.500 - 12.000","Más costoso porque no solo responde FAQs: procesa documentos, los divide, los indexa y recupera evidencia antes de responder."),("Vector DB","USD 0 - 500/mes","Base donde se guardan representaciones de documentos para búsqueda semántica. Puede ser local o cloud."),("OpenAI/Azure","Según uso","Se paga por crear embeddings de documentos y por generar respuestas basadas en contexto recuperado.")],
     "pasos":["Recolectar documentos","Limpiar/fragmentar","Embeddings","Integrar Intercom","Recuperar contexto","Responder con evidencia","Escalar si no hay confianza"],"ejemplo":"Cliente pregunta garantía -> busca política oficial -> responde o escala."},
    {"nombre":"Botpress / Voiceflow / plataforma chatbot + Intercom","categoria":"Plataforma chatbot","nivel":"Medio","tiempo":"1 a 4 semanas","tag":"Chatbot visual","color":"green","inicial":(500,3000),"mensual":(50,1000),"fin":False,
     "mejor":"Equipos que prefieren flujos visuales administrables por negocio.","desc":"Bot en plataforma especializada conectado a Intercom mediante integración, webhook o API.","arq":"Intercom -> Webhook/API -> Plataforma chatbot -> LLM/KB -> Handoff Intercom",
     "pros":["Flujos visuales","Menos código","Administrable por negocio","Analítica"],"cons":["Costo proveedor","Lock-in","Integración custom","Limitaciones por plataforma"],"req":["Cuenta plataforma","Licencia","Conector/API Intercom","Intents","Base de conocimiento","Handoff"],
     "rubros":[("Diseño/configuración","USD 500 - 3.000","Diseño de flujos, intents, mensajes, reglas de fallback, pruebas y conexión con Intercom."),("Licencia","USD 50 - 1.000+/mes","Depende del proveedor, número de conversaciones, usuarios, canales o funciones avanzadas."),("OpenAI/LLM","Incluido o separado","Algunas plataformas incluyen IA en la licencia; otras cobran aparte por consumo del modelo.")],
     "pasos":["Elegir plataforma","Crear intents","Cargar conocimiento","Conectar Intercom","Fallback","Probar"],"ejemplo":"Saludo -> pregunta abierta -> intención -> FAQ o handoff."}
]

st.markdown('<div class="hero"><div class="kicker">Research preview · Customer support automation</div><h1>🔬 Intercom AI Options Lab</h1><p>Comparador profesional de alternativas para atención al cliente: Fin, Python propio, OpenAI, Zapier, Make, n8n, RAG y plataformas chatbot.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎛️ Panel")
    categoria=st.selectbox("Categoría", ["Todas"]+sorted(set(s["categoria"] for s in SOLUTIONS)))
    nivel=st.selectbox("Nivel técnico", ["Todos","Básico-Medio","Medio","Medio-Avanzado","Avanzado"])
    modo=st.radio("Vista", ["Todas las opciones","Solo recomendadas para demo","Solo producción"])
    st.divider()
    with st.expander("📘 Glosario ejecutivo", expanded=False):
        st.markdown("""
**Outcome:** resultado exitoso que se puede medir. En Fin suele asociarse a una conversación resuelta o a un procedimiento completado.

**Seat:** usuario o agente con licencia para usar la plataforma.

**Webhook:** aviso automático que Intercom envía a otro sistema cuando ocurre algo, por ejemplo un nuevo mensaje.

**RAG:** método para responder con base en documentos internos, no solo con memoria del modelo.
""")
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
        st.warning("No hay opciones con esos filtros.")
        selected=None
    else:
        selected=st.radio("Selecciona", [s["nombre"] for s in filtered], label_visibility="collapsed")
        st.markdown("### Resumen rápido")
        for s in filtered:
            total_low,total_high=solution_cost(s)
            st.markdown(f'<div class="card"><span class="{badge(s["color"])}">{s["tag"]}</span><span class="badge">{s["nivel"]}</span><b>{s["nombre"]}</b><br><span class="small">Inicial: {usd(s["inicial"][0])}-{usd(s["inicial"][1])} · Mensual estimado: {usd(total_low)}-{usd(total_high)}</span></div>', unsafe_allow_html=True)

with right:
    if selected:
        s=next(x for x in filtered if x["nombre"]==selected)
        total_low,total_high=solution_cost(s)
        st.markdown(f'<div class="card"><span class="{badge(s["color"])}">{s["tag"]}</span><span class="badge purple">{s["categoria"]}</span><h3>{s["nombre"]}</h3><p><b>Mejor para:</b> {s["mejor"]}</p><p>{s["desc"]}</p></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        c1.metric("Tiempo / nivel", f"{s['tiempo']} · {s['nivel']}")
        c2.metric("Mensual total estimado", f"{usd(total_low)} - {usd(total_high)}")
        st.markdown('<div class="explain"><strong>¿Qué significa este mensual?</strong><br>Este valor combina licencias, uso estimado de IA, hosting o plataforma y soporte operativo. Sirve para comparar alternativas, pero no reemplaza una cotización final con volumen real.</div>', unsafe_allow_html=True)
        c3,c4=st.columns(2)
        c3.metric("Inicial estimado", f"{usd(s['inicial'][0])} - {usd(s['inicial'][1])}")
        c4.metric("Mensual estimado COP", f"{cop(total_low)} - {cop(total_high)}")
        st.markdown(f'<div class="explain research"><strong>Lectura investigativa del costo</strong><br>El valor inicial representa configuración, integración, desarrollo, pruebas y puesta en marcha. El valor en COP usa una TRM de referencia de {USD_TO_COP:,} COP por USD. Para decisión final conviene validar volumen real, canales, cantidad de agentes y nivel de automatización esperado.</div>'.replace(',', '.'), unsafe_allow_html=True)
        tab1,tab2,tab3,tab4=st.tabs(["💰 Inversión","✅ Requisitos","🧭 Paso a paso","💬 Simulador"])
        with tab1:
            st.markdown("#### ¿A qué se deben los cobros?")
            if s.get("fin"):
                st.markdown('<div class="explain warn"><strong>Nota clave sobre outcomes</strong><br>Un outcome no es un mensaje ni una pregunta individual. Es un resultado de negocio medible: por ejemplo. una conversación resuelta por Fin o un procedimiento completado. Por eso el costo puede crecer cuando Fin resuelve más casos; no necesariamente es algo malo, porque también significa menos carga para agentes humanos.</div>', unsafe_allow_html=True)
            for n,a,no in s["rubros"]:
                st.markdown(f"**{n}: {a}**")
                st.markdown(f'<div class="explain">{no}</div>', unsafe_allow_html=True)
        with tab2:
            for r in s["req"]:
                st.write(f"- {r}")
            st.markdown("#### Arquitectura")
            st.code(s["arq"], language="text")
            a,b=st.columns(2)
            with a:
                st.markdown("#### Pros")
                for p in s["pros"]:
                    st.write(f"✅ {p}")
            with b:
                st.markdown("#### Contras")
                for c in s["cons"]:
                    st.write(f"⚠️ {c}")
        with tab3:
            for i,p in enumerate(s["pasos"],1):
                st.write(f"**{i}.** {p}")
            st.markdown("#### Ejemplo")
            st.code(s["ejemplo"], language="text")
        with tab4:
            q_demo=st.selectbox("Pregunta de ejemplo", ["¿Cuál es el horario?","Quiero hablar con un asesor","Tengo una queja por facturación","¿Dónde están ubicados?"])
            custom=st.text_input("O escribe una pregunta", placeholder="Ej: necesito ayuda con mi factura")
            st.markdown(simular(s, custom if custom.strip() else q_demo, queue_size, threshold, company))

st.divider()
st.markdown('<div class="card"><h3>✅ Lectura ejecutiva</h3><ul><li><b>Comparar siempre Fin:</b> puede competir por rapidez y menor desarrollo.</li><li><b>Demo rápida:</b> Zapier + OpenAI o Make + OpenAI.</li><li><b>Balance control/costo:</b> n8n + OpenAI.</li><li><b>Producción robusta:</b> Python + Intercom API/Webhooks + OpenAI/Azure OpenAI.</li><li><b>Documentos extensos:</b> RAG documental + Intercom.</li></ul></div>', unsafe_allow_html=True)
st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
