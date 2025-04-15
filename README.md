# 📄 Documentación de la App - Generador de SQL desde Excel

## 🚀 Propósito de la app
La app permite leer archivos Excel, extraer datos y generar sentencias SQL dinámicas. Además, puedes guardar plantillas de SQL, asociando variables con las columnas del Excel, y luego generar sentencias SQL personalizadas para cada fila de datos.

## Funcionalidades:
- **Subida de archivos Excel**: Permite al usuario cargar un archivo Excel.
- **Edición de plantillas SQL**: Permite crear y editar plantillas SQL con variables.
- **Generación automática de sentencias SQL**: Con las plantillas y los datos del Excel, genera automáticamente las sentencias SQL.
- **Guardar plantillas**: Guarda las plantillas creadas para su reutilización.
- **Exportación de sentencias SQL**: Permite exportar todas las sentencias generadas en un archivo `.sql`.

## 🔑 Componentes principales
### Interfaz de usuario (Frontend):
- Permite subir archivos Excel.
- Edición y creación de plantillas SQL con variables.
- Vista previa de las sentencias SQL generadas.
- Botones para insertar variables y guardar plantillas.

### Backend (Lógica de la app):
- **SQLite**: Base de datos para almacenar las plantillas SQL y sus descripciones de columnas.
- **pandas**: Para procesar los datos del Excel.
- **Streamlit**: Framework para crear la app de forma sencilla y rápida.

---

## 🌟 Flujo detallado de la app - Generador de SQL desde Excel

### 1. Inicio de la aplicación
Cuando accedes a la app, la interfaz de usuario se carga con los siguientes elementos:
- **Subir archivo Excel**: Un botón para subir el archivo Excel que contiene los datos.
- **Área para crear y editar plantillas SQL**: Una caja de texto donde puedes escribir una plantilla SQL.
- **Botones para insertar variables**: Botones para insertar las variables de las columnas del archivo Excel en la plantilla SQL.
- **Opciones para guardar plantillas**: Un espacio para guardar las plantillas SQL que hayas creado.

### 2. Subir el archivo Excel
El primer paso es que el usuario suba un archivo Excel. Esto es lo que sucede:
- **El usuario sube el archivo**: Haces clic en el botón "Sube tu archivo Excel" y seleccionas el archivo `.xlsx` desde tu computadora.
- **El sistema lee el archivo Excel**: Una vez subido, la app lee el archivo utilizando la biblioteca **pandas** y lo carga en un **DataFrame** (una estructura de datos que almacena las filas y columnas del Excel).
- **Visualización del archivo**: La app muestra una tabla con todos los datos del archivo Excel. Cada columna corresponde a una variable que luego podrás usar en la plantilla SQL.

### 3. Crear una plantilla SQL
Una vez que has subido el archivo, puedes crear una plantilla SQL para generar las sentencias:
- **Escribir la plantilla SQL**: En el área de texto que aparece, puedes escribir una plantilla SQL. La plantilla debe tener **placeholders** (lugares donde se insertarán los valores de las columnas del Excel). Estos placeholders se escriben entre llaves `{}`, por ejemplo: `{ACCOUNT_NUMBER}`, `{ACCOUNT_TYPE}`, `{ENTITY_ADDRESS}`.
  
  La plantilla podría verse así:
  ```sql
  INSERT INTO COM_CLIENT_ACCOUNTS (
      SID,
      ACCOUNT_NUMBER,
      ACCOUNT_TYPE,
      ENTITY_ADDRESS,
      ENTITY_PHONE,
      ACCOUNT_HOLDER
  ) VALUES (
      SEQ_COM_CLIENT_ACCOUNTS.nextval,
      '{ACCOUNT_NUMBER}',
      '{ACCOUNT_TYPE}',
      '{ENTITY_ADDRESS}',
      '{ENTITY_PHONE}',
      '{ACCOUNT_HOLDER}'
  );
- **Insertar variables en la la plantilla SQL**:  La app te permite insertar automáticamente las columnas del archivo Excel en la plantilla SQL:
  Verás botones como: "Insertar {ACCOUNT_NUMBER}", "Insertar {ACCOUNT_TYPE}", etc.
  Cuando haces clic en uno de estos botones, el sistema inserta la variable correspondiente de la columna de tu archivo Excel en la plantilla SQL. Por ejemplo, si haces clic en el botón para insertar {ACCOUNT_NUMBER}, la plantilla se actualizará automáticamente para incluir ese placeholder.

  ### 4. Guardar plantillas
Una vez que tienes la plantilla SQL creada, puedes guardar esa plantilla para usarla en el futuro. Esto es lo que sucede:
- **Dar un nombre a la plantilla**: Antes de guardar, debes dar un nombre a la plantilla que estás creando (por ejemplo, "Plantilla para cuentas de clientes").
- **Guardar la plantilla**: Al hacer clic en el botón "Guardar plantilla", la app guarda:
El nombre de la plantilla.
La plantilla SQL (con los placeholders de las columnas).
Las descripciones de las columnas (si las has introducido).
La plantilla guardada se almacena en una base de datos local (SQLite). Esto te permite acceder a esta plantilla en el futuro sin necesidad de escribirla de nuevo.

 ### 5. Seleccionar una plantilla guardada
Si ya has guardado plantillas previamente, puedes seleccionar una plantilla guardada para generar sentencias SQL automáticamente con los datos de tu archivo Excel:

- **Seleccionar la plantilla:** En la interfaz, verás un desplegable (un "select box") donde podrás elegir una de las plantillas que has guardado previamente.
- **Cargar la plantilla seleccionada:** Cuando seleccionas una plantilla guardada, el sistema carga automáticamente la plantilla SQL y las descripciones de las columnas asociadas.
- 
 ### 6. Generar las sentencias SQL
Con la plantilla seleccionada y los datos del archivo Excel, ahora puedes generar las sentencias SQL automáticamente
- **Reemplazo de variables por valores:** El sistema toma la plantilla SQL que seleccionaste y reemplaza los placeholders (como {ACCOUNT_NUMBER}, {ACCOUNT_TYPE}, etc.) con los valores reales de cada fila del archivo Excel.
Por ejemplo, si la primera fila de datos tiene el valor ES4521037843320030224398 en la columna ACCOUNT_NUMBER, ese valor reemplazará {ACCOUNT_NUMBER} en la plantilla.
Ejemplo de sentencia generada:
   ```sql
  INSERT INTO COM_CLIENT_ACCOUNTS (
      SID,
      ACCOUNT_NUMBER,
      ACCOUNT_TYPE,
      ENTITY_ADDRESS,
      ENTITY_PHONE,
      ACCOUNT_HOLDER
  ) VALUES (
      SEQ_COM_CLIENT_ACCOUNTS.nextval,
      'ES4521037843320030224398',
      2,
      NULL,
      NULL,
      'ARAL DEL BAÑO, JOSE MARIA'
  );
- **Generación para todas las filas**:  El sistema genera una sentencia SQL para cada fila de datos en el archivo Excel. Si tienes 20 filas de datos, se generarán 20 sentencias SQL.

 ### 7. Exportar las sentencias SQL
Cuando las sentencias SQL están listas, puedes exportarlas como un archivo .sql para que puedas ejecutarlas directamente en tu base de datos:
- **Generar el archivo SQL:** Al hacer clic en el botón "Exportar todo a SQL", el sistema recoge todas las sentencias generadas y las guarda en un archivo de texto .sql.
- **Descargar el archivo:** El sistema te ofrece un botón para descargar el archivo SQL generado, el cual contiene todas las sentencias que puedes ejecutar en tu base de datos.

## Resumen del flujo de la app
- **Subir archivo Excel** → El usuario sube el archivo Excel con los datos.
- **Crear o editar plantilla SQL** → El usuario crea una plantilla SQL con placeholders de las columnas del archivo.
- **Guardar plantillas** → El usuario guarda las plantillas para su reutilización futura.
- **Generar sentencias SQL** → El sistema genera las sentencias SQL reemplazando los placeholders con los valores reales del archivo Excel.
- **Exportar archivo SQL** → El usuario puede descargar las sentencias SQL generadas como un archivo .sql.

