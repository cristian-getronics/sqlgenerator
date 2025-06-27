import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import zipfile
import os

# Configuración de la página
st.set_page_config(page_title="Generador SQL desde Excel", layout="wide")
st.title("🧾 Generador de sentencias SQL desde Excel")

# ------------------ BASE DE DATOS ------------------

Base = declarative_base()
DB_PATH = "db/templates.db"
os.makedirs("db", exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    content = Column(Text, nullable=False)

Base.metadata.create_all(engine)

# ------------------ FUNCIONES ------------------

def save_template(name, content):
    template = session.query(Template).filter_by(name=name).first()
    if template:
        template.content = content
    else:
        template = Template(name=name, content=content)
        session.add(template)
    session.commit()

def get_template(name):
    return session.query(Template).filter_by(name=name).first()

def get_all_template_names():
    return [t.name for t in session.query(Template).all()]

# ------------------ UI ------------------

st.subheader("✍️ Gestor de Plantillas SQL")

plantilla_nombres = get_all_template_names()
selected_name = st.selectbox("Selecciona plantilla guardada", options=["Nueva plantilla"] + plantilla_nombres)

if selected_name != "Nueva plantilla":
    loaded_template = get_template(selected_name)
    sql_template = loaded_template.content
    plantilla_nombre = loaded_template.name
else:
    sql_template = ""
    plantilla_nombre = ""

template_editor = st.text_area("Contenido de la plantilla", value=sql_template, height=400)

new_name = st.text_input("Nombre de la plantilla", value=plantilla_nombre)

if st.button("💾 Guardar plantilla"):
    if new_name and template_editor:
        save_template(new_name, template_editor)
        st.success(f"Plantilla '{new_name}' guardada con éxito")
    else:
        st.warning("⚠️ Debes introducir un nombre y contenido para guardar la plantilla.")

# ------------------ CARGA DEL ARCHIVO ------------------

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel (.xlsx)", type=["xlsx"])

# ------------------ GENERACIÓN SQL ------------------

if uploaded_file is not None:
    try:
        # Comprobamos tamaño del archivo
        if uploaded_file.size == 0:
            st.error("❌ El archivo está vacío. Por favor, sube uno válido.")
            st.stop()

        # Mostrar información del archivo
        st.info(f"📄 Archivo subido: {uploaded_file.name} ({uploaded_file.size // 1024} KB)")

        # Intentar leer el archivo Excel
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        st.subheader("👀 Vista previa del Excel")
        st.dataframe(df)
        st.markdown("### 🧩 Columnas disponibles:")
        st.write(", ".join(df.columns))

        # Validar que hay datos en el DataFrame
        if len(df) == 0:
            st.warning("⚠️ El archivo está vacío (sin filas).")
            st.stop()

        # Generar sentencias SQL
        st.subheader("📄 Sentencias SQL generadas")
        sql_statements = []
        for _, row in df.iterrows():
            statement = template_editor
            for col in df.columns:
                value = row[col]
                if pd.isnull(value):
                    value = "NULL"
                elif isinstance(value, str) and not value.startswith("{"):
                    value = value.replace("'", "''")  # Escapar comillas simples
                    value = f"'{value}'"
                statement = statement.replace(f"{{{col}}}", str(value))
            sql_statements.append(statement)

        st.code("\n\n".join(sql_statements), language="sql")

        # Botón de descarga
        st.download_button(
            "⬇️ Descargar como .sql",
            data="\n\n".join(sql_statements),
            file_name="sentencias.sql",
            mime="text/plain"
        )

    except zipfile.BadZipFile:
        st.error("❌ El archivo no es un Excel válido (.xlsx). Puede estar corrupto o no ser un archivo Excel.")
    except KeyError as e:
        st.error(f"❌ Error: La columna {e} no existe en el archivo Excel.")
    except Exception as e:
        st.error(f"⚠️ Ocurrió un error al procesar el archivo: {e}")
        st.exception(e)  # Muestra el traceback completo en modo desarrollo

else:
    st.info("📂 Por favor, sube un archivo Excel (.xlsx) para comenzar.")