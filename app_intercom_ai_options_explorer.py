
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Intercom AI Options Lab", page_icon="🔬", layout="wide")

st.markdown("""
<style>
:root{--ink:#0f172a;--muted:#64748b;--line:#e5e7eb;--card:#fff;--blue:#2563eb;--violet:#7c3aed;--green:#16a34a;--amber:#d97706;}
.block-container{padding-top:1.35rem!important;padding-left:2rem!important;padding-right:2rem!important;max-width:1440px;}
html,body,[class*="css"]{font-size:14.2px;color:var(--ink)}
h1{font-size:1.55rem!important;line-height:1.2!important;margin-bottom:.25rem!important} h2{font-size:1.16rem!important} h3{font-size:1.02rem!important;margin-top:.5rem!important}
.stMarkdown p,.stMarkdown li{font-size:.89rem!important;line-height:1.4!important}.small{font-size:.78rem;color:var(--muted)}
.hero{background:linear-gradient(135deg,#020617 0%,#1d4ed8 56%,#7c3aed 100%);padding:24px 28px;border-radius:0 0 22px 22px;color:white;margin:0 0 16px 0;box-shadow:0 18px 42px rgba(15,23,42,.20);overflow:visible;}
.hero h1{color:white!important;margin:.35rem 0 .45rem 0!important;line-height:1.25!important}.hero p{color:#dbeafe!important;margin:.35rem 0 0 0!important}.hero .kicker{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:#bfdbfe;font-weight:700;line-height:1.35;margin-bottom:.35rem;}
.card{background:var(--card);border:1px solid var(--line);border-radius:17px;padding:15px 17px;box-shadow:0 4px 18px rgba(15,23,42,.045);margin-bottom:11px}
.explain{background:#f8fafc;border-left:4px solid var(--blue);border-radius:13px;padding:11px 13px;margin:9px 0 13px;color:#334155;font-size:.86rem;line-height:1.42}.explain strong{color:#0f172a}.warn{border-left-color:var(--amber);background:#fffbeb}.research{border-left-color:var(--violet);background:#faf5ff}.ok{border-left-color:var(--green);background:#f0fdf4}
.badge{display:inline-block;padding:3px 8px;border-radius:999px;background:#eff6ff;color:#1d4ed8;font-size:.70rem;font-weight:700;margin-right:5px;margin-bottom:4px}.green{background:#dcfce7;color:#15803d}.purple{background:#f3e8ff;color:#6d28d9}.orange{background:#ffedd5;color:#c2410c}.dark{background:#e2e8f0;color:#334155}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:14px;padding:9px 10px;box-shadow:0 3px 12px rgba(15,23,42,.04);min-height:68px}div[data-testid="stMetricLabel"] p{font-size:.70rem!important;color:var(--muted)!important;white-space:normal!important}div[data-testid="stMetricValue"]{font-size:.88rem!important;line-height:1.12!important;white-space:normal!important;overflow-wrap:anywhere!important;word-break:break-word!important}
pre,code{font-size:.76rem!important;line-height:1.28!important;border-radius:12px!important}hr{margin:.75rem 0!important}label{font-size:.83rem!important}.stButton>button{border-radius:10px}
</style>
""", unsafe_allow_html=True)

USD_TO_COP = 4000
FAQ = {"horario":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.","horarios":"Nuestro horario de atención es de lunes a viernes de 8:00 a.m. a 6:00 p.m. y sábados de 9:00 a.m. a 1:00 p.m.","precio":"Para darte precios exactos necesito saber el producto o servicio. Si quieres, te conecto con un agente comercial.","ubicacion":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.","ubicación":"Compártenos tu ciudad y te indicamos la sede o canal más cercano.","pago":"Aceptamos los métodos de pago definidos por la empresa. Un agente puede confirmar el detalle según tu caso."}
ESCALATION_KEYWORDS=["reclamo","queja","cancelar","devolución","devolucion","factura","garantía","garantia","asesor","humano","agente"]

def usd(x): return f"USD {x:,.0f}".replace(",",".")
def cop(x): return f"COP {x*USD_TO_COP:,.0f}".replace(",",".")
def badge(color): return {"green":"badge green","purple":"badge purple","orange":"badge orange","dark":"badge dark"}.get(color,"badge")

def simular(s,q,queue,threshold,company):
    low=q.lower(); resp=next((a for k,a in FAQ.items() if k in low),None)
    agent=any(k in low for k in ESCALATION_KEYWORDS); demand=queue>=threshold
    if s.get("fin"):
        flow="Fin buscaría la respuesta en Knowledge Hub/Procedures y, si no puede resolver, haría handoff nativo a Intercom."
    elif "Python" in s["nombre"]:
        flow="Python recibiría el webhook de Intercom, consultaría reglas/conocimiento y respondería o asignaría por API."
    elif "Zapier" in s["nombre"]:
        flow="Zapier ejecutaría trigger de Intercom, paso OpenAI, filtros y acción final en Intercom/Webhook."
    elif "Make" in s["nombre"]:
        flow="Make ejecutaría un escenario visual con routers para FAQ, OpenAI o escalamiento."
    elif "n8n" in s["nombre"]:
        flow="n8n ejecutaría un workflow con IF/Switch, OpenAI y llamada HTTP/API a Intercom."
    elif "RAG" in s["nombre"]:
        flow="RAG buscaría evidencia en documentos antes de responder; sin evidencia, escalaría."
    else:
        flow="La plataforma chatbot detectaría intención, seguiría flujo visual y enviaría respuesta o handoff."
    ans=resp if resp and not agent else (f"Voy a transferir tu solicitud a un agente de {company}." if agent else f"Para responder con seguridad pasaré tu caso a un agente de {company}.")
    if demand: ans += " En este momento tenemos alta demanda; por favor espera mientras un agente queda disponible."
    return f"**Cómo actuaría esta tecnología:** {flow}\n\n**Respuesta al cliente:** {ans}"

SOLUTIONS = [
    {"nombre":"Fin AI Agent nativo de Intercom","categoria":"Nativo Intercom","nivel":"Básico-Medio","tiempo":"Horas a pocos días","tag":"Nativo","color":"green","inicial":(0,500),"mensual_text":"Desde USD 49,50/mes standalone o USD 29/seat + USD 0,99/outcome","fin":True,
     "mejor":"Comparar contra alternativas externas; ideal si se quiere activar rápido y reducir desarrollo.","desc":"Fin usa conocimiento de Intercom y cobra por outcome/resolución. Es la alternativa nativa y debe compararse aunque el cliente quiera evaluar opciones externas.","arq":"Intercom/Fin -> Knowledge Hub/Procedures -> Respuesta automática -> Handoff a Inbox/agente",
     "pros":["Implementación rápida","Menos desarrollo","Escalamiento nativo","Reportes integrados"],"cons":["Menos control que una solución propia","Costo variable por outcome","Dependencia de Intercom"],"req":["Intercom o Fin standalone","Knowledge Hub/FAQs organizado","Reglas de handoff","Agentes/equipos configurados"],
     "rubros":[("Fin AI Agent","USD 0,99/outcome","Un outcome no es un mensaje: es un resultado exitoso medible, normalmente conversación resuelta o procedimiento completado. Si Fin resuelve más, el costo sube, pero también baja la carga operativa humana."),("Mínimo standalone","50 outcomes/mes = USD 49,50/mes","Si se usa Fin sin Intercom Helpdesk, el mínimo mensual público equivale a 50 outcomes."),("Intercom seat","Desde USD 29/seat/mes anual","Si se usa Fin con Intercom Helpdesk, además del outcome se paga el asiento de agente o usuario del helpdesk."),("Configuración inicial","USD 0 - 500 estimado","Carga de conocimiento, configuración de tono, pruebas y reglas de handoff. Puede ser bajo si el equipo ya tiene artículos bien organizados.")],
     "pasos":["Activar Fin o trial","Cargar FAQs/Knowledge Hub","Definir tono y reglas","Configurar handoff","Probar simulaciones","Medir outcomes"],"ejemplo":"Cliente: ¿Cuál es el horario?\nFin: Responde con Knowledge Hub.\n\nCliente: Tengo un reclamo de factura\nFin: deriva al equipo configurado."},
    {"nombre":"Solución propia con Python + Intercom API/Webhooks + OpenAI/Azure OpenAI","categoria":"Código / Backend propio","nivel":"Avanzado","tiempo":"2 a 6 semanas MVP","tag":"Producción","color":"purple","inicial":(800,4000),"mensual_text":"USD 25 - 250/mes + soporte técnico","fin":False,
     "mejor":"Cliente que no quiere Fin y necesita control total del bot, reglas, base de conocimiento, alta demanda y escalamiento.","desc":"Backend propio en Python/FastAPI conectado a webhooks de Intercom y a OpenAI/Azure OpenAI. Los costos reales de proveedor suelen ser bajos; el mayor costo es implementación y mantenimiento.","arq":"Intercom Messenger -> Webhook -> Python/FastAPI -> OpenAI/Azure OpenAI -> Intercom API",
     "pros":["Máximo control","Se adapta a reglas del negocio","Integrable con CRM/BD","Evita dependencia de Fin"],"cons":["Requiere desarrollo","Debe mantenerse","Responsabilidad de seguridad y monitoreo"],"req":["Intercom API/Webhooks","Token Intercom","OpenAI/Azure OpenAI","Servidor cloud","Base de conocimiento","Equipo técnico"],
     "rubros":[("Implementación MVP","USD 800 - 4.000 estimado","Rango realista para un primer bot funcional: webhook, clasificación básica, respuesta FAQ/OpenAI y handoff. Si se piden integraciones complejas, auditoría, RAG o alta disponibilidad, el valor sube."),("Hosting","USD 5 - 50/mes","Servidor pequeño o PaaS para recibir webhooks. En fases iniciales suele ser económico."),("OpenAI API","Desde centavos hasta decenas de USD/mes en bajo volumen","Con modelos económicos como GPT-4o mini, el costo por conversación puede ser muy bajo. El costo crece con volumen y contexto."),("Mantenimiento","USD 50 - 300/mes estimado","Revisión de errores, ajustes de prompts, cambios de reglas y mejoras de respuestas.")],
     "pasos":["Crear app privada Intercom","Configurar webhooks","Crear backend Python","Conectar OpenAI/Azure","Implementar reglas de escalamiento","Probar y publicar"],"ejemplo":"Cliente: ¿Cuál es el horario?\nBot Python: consulta FAQ y responde.\n\nCliente: Tengo queja por facturación\nBot Python: asigna agente."},
    {"nombre":"Zapier + Intercom + ChatGPT/OpenAI","categoria":"No-code / Low-code","nivel":"Básico-Medio","tiempo":"1 a 5 días","tag":"Demo rápida","color":"orange","inicial":(100,600),"mensual_text":"USD 19,99 - 69/mes + OpenAI","fin":False,
     "mejor":"Demo rápida o automatizaciones simples sin backend propio.","desc":"Automatización no-code usando Intercom como trigger, OpenAI como paso IA y Zapier como orquestador.","arq":"Intercom Trigger -> Zapier -> OpenAI -> Intercom/Webhook",
     "pros":["Muy rápido","No-code","Útil para demo","Muchas integraciones"],"cons":["Costo por tareas","Menor control","Puede ser limitado para producción compleja"],"req":["Zapier paid si requiere webhooks/premium","Intercom conectado","OpenAI conectado","Filtros/Paths"],
     "rubros":[("Zapier","Desde USD 19,99/mes anual; Team desde USD 69/mes","Costo de plataforma. El costo real depende de tareas mensuales: cada acción ejecutada consume tareas."),("OpenAI","Según uso","Costo del modelo. En un flujo simple suele ser menor que el costo de Zapier."),("Configuración","USD 100 - 600 estimado","Armado de Zaps, prompts, filtros, pruebas y documentación.")],
     "pasos":["Crear Zap","Conectar Intercom","Agregar OpenAI","Crear filtros","Acción Intercom/Webhook","Probar"],"ejemplo":"Nueva conversación -> OpenAI clasifica -> FAQ responde/sugiere -> reclamo escala."},
    {"nombre":"Make.com + Intercom + OpenAI","categoria":"No-code / Automatización visual","nivel":"Medio","tiempo":"2 a 10 días","tag":"Visual","color":"orange","inicial":(150,800),"mensual_text":"USD 12 - 38/mes + OpenAI","fin":False,
     "mejor":"Flujos visuales con routers, filtros y HTTP/API más flexibles.","desc":"Make permite escenarios visuales con routers y llamadas HTTP/API, útil cuando Zapier se queda corto.","arq":"Intercom/Webhook -> Make Scenario -> Router -> OpenAI -> Intercom API",
     "pros":["Visual","Routers potentes","Buen costo base","HTTP flexible"],"cons":["Requiere configuración","Consume créditos","Dependencia de Make"],"req":["Cuenta Make","Intercom/Webhook","OpenAI","Base de conocimiento"],
     "rubros":[("Make","Core USD 12/mes; Pro USD 21/mes; Teams USD 38/mes para 10k créditos","Costo de plataforma. Cada módulo/acción del escenario consume créditos."),("OpenAI","Según uso","Costo por consultas al modelo IA."),("Configuración","USD 150 - 800 estimado","Diseño de escenarios, routers, pruebas y control de errores.")],
     "pasos":["Crear escenario","Webhook Intercom","Router","OpenAI","Intercom API","Monitorear"],"ejemplo":"Router horario -> respuesta fija. Router factura -> agente. Router abierta -> OpenAI."},
    {"nombre":"n8n + Intercom + OpenAI","categoria":"Low-code / Self-hosted opcional","nivel":"Medio-Avanzado","tiempo":"1 a 2 semanas MVP","tag":"Flexible","color":"purple","inicial":(200,1200),"mensual_text":"Self-host USD 5 - 30/mes o Cloud €20 - €50/mes","fin":False,
     "mejor":"Automatización visual con opción self-hosted y más control técnico.","desc":"n8n cobra por ejecución completa en cloud, no por cada paso. Self-host puede ser muy económico si hay equipo técnico.","arq":"Intercom Webhook -> n8n Workflow -> OpenAI -> Intercom API",
     "pros":["Self-host opcional","Flexible","Bueno para APIs","Costo eficiente en flujos complejos"],"cons":["Más técnico","Self-host requiere mantenimiento","Hay que asegurar disponibilidad"],"req":["n8n Cloud o servidor","Intercom API","OpenAI","Dominio/SSL si self-host"],
     "rubros":[("n8n Cloud","Starter €20/mes anual; Pro €50/mes anual","Costo administrado por n8n. Starter incluye 2.500 ejecuciones; Pro incluye 10.000 ejecuciones."),("Self-host","USD 5 - 30/mes estimado","Servidor pequeño, backups y dominio/SSL. El software puede ser gratis, pero requiere mantenimiento técnico."),("Configuración","USD 200 - 1.200 estimado","Workflows, nodos, condiciones, API de Intercom y pruebas.")],
     "pasos":["Crear workflow","Webhook/Intercom","OpenAI","IF/Switch","Intercom API","Activar"],"ejemplo":"Webhook -> OpenAI clasifica -> IF horario responde -> baja confianza asigna agente."},
    {"nombre":"Asistente RAG documental + Intercom","categoria":"IA documental","nivel":"Avanzado","tiempo":"3 a 6 semanas","tag":"Documentos","color":"purple","inicial":(1500,6000),"mensual_text":"USD 30 - 300/mes + mantenimiento","fin":False,
     "mejor":"Empresas con manuales, políticas o documentación extensa.","desc":"RAG agrega búsqueda documental para responder con evidencia. Es más costoso que un bot FAQ porque requiere preparar e indexar documentos.","arq":"Intercom -> Backend/n8n -> Vector DB -> OpenAI -> Intercom",
     "pros":["Basado en documentos","Reduce alucinaciones","Escalable","Mejor para preguntas abiertas"],"cons":["Mayor implementación","Requiere limpiar documentos","Evaluación continua"],"req":["Documentos limpios","Vector DB/buscador","OpenAI embeddings","Intercom API"],
     "rubros":[("Implementación RAG","USD 1.500 - 6.000 estimado","Preparar documentos, crear embeddings, buscador semántico, backend/automatización e integración con Intercom."),("Vector DB/buscador","USD 0 - 150/mes en MVP","Puede empezar con opciones económicas o self-host; servicios administrados suben según volumen."),("OpenAI/Azure","Según uso","Embeddings y generación de respuestas.")],
     "pasos":["Recolectar documentos","Limpiar y fragmentar","Embeddings","Conectar Intercom","Recuperar contexto","Responder o escalar"],"ejemplo":"Cliente pregunta garantía -> busca política oficial -> responde o escala."},
    {"nombre":"Botpress / Voiceflow / plataforma chatbot + Intercom","categoria":"Plataforma chatbot","nivel":"Medio","tiempo":"1 a 4 semanas","tag":"Chatbot visual","color":"green","inicial":(300,2000),"mensual_text":"Botpress desde USD 0 + AI Spend; Plus USD 79-89. Voiceflow Pro USD 60/editor","fin":False,
     "mejor":"Equipos que prefieren flujos visuales administrables por negocio.","desc":"Plataformas chatbot visuales con IA y handoff. Costos dependen de proveedor, AI Spend, editores y volumen.","arq":"Intercom -> Webhook/API -> Plataforma chatbot -> LLM/KB -> Handoff",
     "pros":["Flujos visuales","Administrable por negocio","Menos código","Analítica"],"cons":["Licencia adicional","Lock-in","Integración puede ser custom"],"req":["Cuenta plataforma","Conector/API Intercom","Base de conocimiento","Flujos e intents"],
     "rubros":[("Botpress","Pay-as-you-go USD 0 + AI Spend; Plus USD 79 anual / USD 89 mensual","Base de plataforma + consumo IA. Plus agrega handoff humano, insights y elimina marca."),("Voiceflow","Pro USD 60/editor/mes; Business USD 150/editor/mes","Costo por editor y créditos de uso; algunas empresas requieren plan con precio por demo."),("Configuración","USD 300 - 2.000 estimado","Diseño conversacional, intents, handoff, conexión con Intercom y pruebas.")],
     "pasos":["Elegir plataforma","Crear intents","Cargar conocimiento","Conectar Intercom","Probar handoff","Publicar"],"ejemplo":"Saludo -> intención -> FAQ o handoff a Intercom."}
]

st.markdown('<div class="hero"><div class="kicker">Research pricing · Customer support automation</div><h1>🔬 Intercom AI Options Lab</h1><p>Comparador profesional con precios de mercado base y explicación de costos. Los valores de implementación son estimaciones de servicios, no tarifas oficiales de proveedores.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎛️ Panel")
    categoria=st.selectbox("Categoría", ["Todas"]+sorted(set(s["categoria"] for s in SOLUTIONS)))
    nivel=st.selectbox("Nivel técnico", ["Todos","Básico-Medio","Medio","Medio-Avanzado","Avanzado"])
    modo=st.radio("Vista", ["Todas las opciones","Solo recomendadas para demo","Solo producción"])
    st.divider()
    with st.expander("📘 Glosario ejecutivo", expanded=False):
        st.markdown("""
**Outcome:** resultado exitoso medible. En Fin suele ser una conversación resuelta o procedimiento completado.

**Seat:** usuario/agente con licencia.

**Webhook:** evento que Intercom envía automáticamente a otro sistema.

**RAG:** técnica para responder con documentos internos.
""")
    st.divider()
    st.header("💬 Simulador")
    company=st.text_input("Empresa", value="Mi Empresa")
    queue_size=st.number_input("Personas en espera", min_value=0, value=12)
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
            st.markdown(f'<div class="card"><span class="{badge(s["color"])}">{s["tag"]}</span><span class="badge">{s["nivel"]}</span><b>{s["nombre"]}</b><br><span class="small">Inicial estimado: {usd(s["inicial"][0])}-{usd(s["inicial"][1])}<br>Mensual mercado/base: {s["mensual_text"]}</span></div>', unsafe_allow_html=True)

with right:
    if selected:
        s=next(x for x in filtered if x["nombre"]==selected)
        st.markdown(f'<div class="card"><span class="{badge(s["color"])}">{s["tag"]}</span><span class="badge purple">{s["categoria"]}</span><h3>{s["nombre"]}</h3><p><b>Mejor para:</b> {s["mejor"]}</p><p>{s["desc"]}</p></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        c1.metric("Tiempo / nivel", f"{s["tiempo"]} · {s["nivel"]}")
        c2.metric("Mensual mercado/base", s["mensual_text"])
        st.markdown('<div class="explain"><strong>Importante:</strong><br>Los valores mensuales corresponden a tarifas públicas o rangos base de mercado. El costo real cambia por volumen, plan contratado, consumo de IA, número de agentes y alcance de implementación.</div>', unsafe_allow_html=True)
        c3,c4=st.columns(2)
        c3.metric("Implementación inicial", f"{usd(s["inicial"][0])} - {usd(s["inicial"][1])}")
        c4.metric("Inicial aprox. COP", f"{cop(s["inicial"][0])} - {cop(s["inicial"][1])}")
        st.markdown(f'<div class="explain research"><strong>Lectura investigativa del costo</strong><br>La implementación inicial es una estimación de servicio profesional para configurar, integrar, probar y documentar. No es tarifa oficial de proveedor. El valor COP usa TRM referencial de {USD_TO_COP:,} COP/USD.</div>'.replace(',', '.'), unsafe_allow_html=True)
        tab1,tab2,tab3,tab4=st.tabs(["💰 Inversión","✅ Requisitos","🧭 Paso a paso","💬 Simulador"])
        with tab1:
            st.markdown("#### ¿A qué se deben los cobros?")
            if s.get("fin"):
                st.markdown('<div class="explain warn"><strong>Outcome en Fin</strong><br>Un outcome no es cada mensaje enviado por el cliente. Es un resultado exitoso medible. Por ejemplo: una conversación resuelta por Fin o un procedimiento completado. Si Fin resuelve más casos, el cobro variable sube, pero también se reduce carga de agentes.</div>', unsafe_allow_html=True)
            for n,a,no in s["rubros"]:
                st.markdown(f"**{n}: {a}**")
                st.markdown(f'<div class="explain">{no}</div>', unsafe_allow_html=True)
        with tab2:
            for r in s["req"]: st.write(f"- {r}")
            st.markdown("#### Arquitectura")
            st.code(s["arq"], language="text")
            a,b=st.columns(2)
            with a:
                st.markdown("#### Pros")
                for p in s["pros"]: st.write(f"✅ {p}")
            with b:
                st.markdown("#### Contras")
                for c in s["cons"]: st.write(f"⚠️ {c}")
        with tab3:
            for i,p in enumerate(s["pasos"],1): st.write(f"**{i}.** {p}")
            st.markdown("#### Ejemplo")
            st.code(s["ejemplo"], language="text")
        with tab4:
            q_demo=st.selectbox("Pregunta de ejemplo", ["¿Cuál es el horario?","Quiero hablar con un asesor","Tengo una queja por facturación","¿Dónde están ubicados?"])
            custom=st.text_input("O escribe una pregunta", placeholder="Ej: necesito ayuda con mi factura")
            st.markdown(simular(s, custom if custom.strip() else q_demo, queue_size, threshold, company))

st.divider()
st.markdown('<div class="card"><h3>✅ Lectura ejecutiva</h3><ul><li><b>Fin:</b> más rápido de activar, con cobro por outcome.</li><li><b>Zapier / Make:</b> mejores para demo o validación rápida.</li><li><b>n8n:</b> balance entre control y costo, especialmente si se autohospeda.</li><li><b>Python propio:</b> mayor control; el costo principal es implementación y mantenimiento.</li><li><b>RAG:</b> mejor cuando hay muchos documentos internos.</li></ul></div>', unsafe_allow_html=True)
st.caption(f"Última actualización del prototipo: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
