# Aettia

**Demo funcional** de una plataforma de inteligencia que analiza la oferta académica de educación continua y la demanda laboral en Latinoamérica.

🌐 **Sitio en vivo:** [https://www.aettia.com](https://www.aettia.com)

---

## ¿Qué es Aettia?

AETTIA no es un directorio de cursos ni un portal de empleo. Es una plataforma de inteligencia que responde a una pregunta que nadie más responde:

> ¿Qué skills específicas faltan en la oferta académica y qué programas cubren las que el mercado está pidiendo?

Aettia cruza dos mundos que rara vez se miran entre sí:

- **Oferta académica** de educación continua (Perú e internacional).
- **Demanda laboral** real (Perú, Chile y Argentina).

El resultado: análisis de skills, dominios temáticos, productos académicos y tendencias temporales — todo desde fuentes públicas.

---

## Alcance actual

Esta es una **demo funcional** para validación. Permite:

- **Analista de Talento** — consultar las skills más demandadas por el mercado laboral:
  - SKILLS (co-ocurrencia de habilidades)
  - PUESTOS (búsqueda por puesto)
  - DOMINIOS (búsqueda por dominio temático)
- **Diseñador Curricular** — analizar la oferta académica disponible:
  - SKILLS (cobertura de skills por producto)
  - ESCUELAS (productos por institución)
  - TIPOS (productos por tipo: diplomado, curso, etc.)

Filtros por país, ubicación, tipo de habilidad, dominio, rango de fechas, y exportación a CSV.

---

## Stack Tecnológico

- **Python 3.12**
- **Streamlit** — interfaz de usuario
- **PostgreSQL** — base de datos (alojada en Railway)
- **SQLAlchemy + psycopg2** — conexión a la base
- **Pandas** — procesamiento de datos
- **Docker + Nginx** — contenedorización y proxy inverso para metadatos sociales
- **Railway** — hosting y despliegue continuo

*(Nota: NLTK fue removido del proyecto. La extracción de n-gramas ahora se hace de forma precalculada desde la base de datos para mayor velocidad).*

---

## Infraestructura y Despliegue

- **Hosting:** Railway (Plan Hobby).
- **Base de datos:** PostgreSQL en Railway (migrada desde local con éxito, ~1 GB de datos).
- **Dominio:** Configurado en Namecheap con CNAME a Railway (`www.aettia.com`).
- **Proxy Inverso:** Nginx configurado dentro de un contenedor Docker para inyectar metadatos Open Graph (para previsualización en WhatsApp y redes sociales).
- **SSL:** Generado y gestionado automáticamente por Railway.

---

## Fuentes de datos

Toda la información proviene de **fuentes públicas**:

- Programas de educación continua universitaria (Perú).
- Programas internacionales (Harvard, MIT, Oxford, etc.).
- Anuncios laborales públicos (Perú, Chile, Argentina).

Aettia **no está afiliada** a ninguna organización educativa ni portal de empleo. Los análisis presentados se basan en datos públicos y pueden no ser completamente precisos.

---

## Estado y Próximos Pasos

La demo está **en vivo** y recolectando métricas de uso reales. 

Próximamente:
- Autenticación de usuarios (Login con Google/Microsoft).
- Pasarela de pagos para suscripciones (evaluando Mercado Pago, Lemon Squeezy o Creem).
- Nuevas vistas y funcionalidades (Reportes).

---

## Contacto

- GitHub: [@goraffo](https://github.com/goraffo)
- Mail: disponible bajo pedido.

---

---

# English

**Aettia** is a functional demo of an intelligence platform that analyzes continuing education offerings and labor market demand across Latin America.

🌐 **Live Site:** [https://www.aettia.com](https://www.aettia.com)

AETTIA is not a course directory or a job board. It is an intelligence platform that answers a question no one else is answering:

> Which specific skills are missing from academic offerings, and which programs cover what the market is demanding?

It cross-references public data from two worlds that rarely look at each other:

- **Academic offerings** in continuing education (Peru and international).
- **Real labor demand** (Peru, Chile, Argentina).

The result: skill analysis, thematic domains, academic products, and time-based trends — all from public sources.

**Current status:** Live and collecting user metrics. Built with Python, Streamlit, PostgreSQL, SQLAlchemy, Pandas, Docker, and Nginx (for Open Graph metadata).

Aettia is not affiliated with any educational organization or job board. All data comes from public sources.

**Contact:** GitHub [@goraffo](https://github.com/goraffo)