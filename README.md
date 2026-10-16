# Aettia

**Demo freemium** de una plataforma de inteligencia que analiza la oferta académica de educación continua y la demanda laboral en Latinoamérica.

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

## Stack

- **Python 3**
- **Streamlit** — interfaz
- **PostgreSQL** — base de datos
- **SQLAlchemy + psycopg2** — conexión a la base
- **NLTK** — extracción de n-gramas y análisis de texto
- **Pandas** — procesamiento de datos

---

## Fuentes de datos

Toda la información proviene de **fuentes públicas**:

- Programas de educación continua universitaria (Perú).
- Programas internacionales (Harvard, MIT, Oxford, etc.).
- Anuncios laborales públicos (Perú, Chile, Argentina).

Aettia **no está afiliada** a ninguna organización educativa ni portal de empleo. Los análisis presentados se basan en datos públicos y pueden no ser completamente precisos.

---

## Estado

Demo en validación. Próximamente:
- URL pública para acceso.
- Nuevas vistas y funcionalidades.

---

## Contacto

- GitHub: [@goraffo](https://github.com/goraffo)
- Mail: disponible bajo pedido.

---

---

# English

**Aettia** is a freemium demo of an intelligence platform that analyzes continuing education offerings and labor market demand across Latin America.

AETTIA is not a course directory or a job board. It is an intelligence platform that answers a question no one else is answering:

> Which specific skills are missing from academic offerings, and which programs cover what the market is demanding?

It cross-references public data from two worlds that rarely look at each other:

- **Academic offerings** in continuing education (Peru and international).
- **Real labor demand** (Peru, Chile, Argentina).

The result: skill analysis, thematic domains, academic products, and time-based trends — all from public sources.

**Current status:** functional demo for validation. Built with Python, Streamlit, PostgreSQL, SQLAlchemy, NLTK, and Pandas.

Aettia is not affiliated with any educational organization or job board. All data comes from public sources.

**Contact:** GitHub [@goraffo](https://github.com/goraffo)