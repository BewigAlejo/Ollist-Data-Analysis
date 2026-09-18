# Olist E-commerce Data Analysis

## About the Project

This project is an end-to-end data analytics case study based on the **Olist Brazilian E-Commerce Public Dataset**.

Olist is a Brazilian e-commerce marketplace that connects small businesses with customers across Brazil. The dataset contains information about orders, customers, sellers, products, payments, reviews and deliveries.

The objective of this project is to work through a complete analytics workflow:

**Data acquisition → Data quality assessment → Data cleaning → SQL/Pandas analysis → Dashboard → Business insights → Recommendations**

The main business problem explored in this project is:

> **What factors are associated with late deliveries and poor customer reviews, and where should the business prioritize improvements?**

The project focuses not only on building visualizations, but on understanding the data, identifying quality issues, answering business questions and translating the findings into actionable recommendations.

### Technologies

- Python
- pandas
- SQL
- Power BI
- Power Query
- DAX
- Git / GitHub

---

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**, available on Kaggle.

Dataset:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains multiple CSV files representing different parts of the e-commerce operation, including:

- Orders
- Customers
- Order items
- Products
- Sellers
- Payments
- Customer reviews
- Geolocation
- Product category translations

Because the dataset is relational, the different tables can be connected through identifiers such as `order_id`, `customer_id`, `product_id` and `seller_id`.

---

## Getting the Data

The raw dataset is **not stored directly in this repository**.

Instead, it can be downloaded directly from Kaggle using the `kagglehub` Python library. This makes the project easier to reproduce without uploading the original dataset to GitHub.

### 1. Install the required libraries

```bash
pip install kagglehub pandas
```

### 2. Authenticate with Kaggle

If Kaggle authentication is required in your environment:

```python
import kagglehub

kagglehub.login()
```

You can create your Kaggle API credentials from your Kaggle account settings.

> Never upload your Kaggle API token, `kaggle.json` or `.env` file to GitHub.

---

### 3. Download the dataset

```python
import kagglehub

path = kagglehub.dataset_download(
    "olistbr/brazilian-ecommerce"
)

print("Dataset path:", path)
```

`kagglehub` stores the dataset in its local cache and returns the directory containing the downloaded files.

There is no need to manually move the original CSV files into the repository.

---

### 4. Inspect the downloaded files

```python
import os

files = os.listdir(path)

for file in files:
    print(file)
```

You should find files similar to:

```text
olist_orders_dataset.csv
olist_customers_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
olist_geolocation_dataset.csv
product_category_name_translation.csv
```

---

### 5. Load a table with pandas

For example, the orders table can be loaded with:

```python
import pandas as pd
import os

orders = pd.read_csv(
    os.path.join(path, "olist_orders_dataset.csv")
)

orders.head()
```

From this point, the dataset is ready for the **data profiling and quality assessment stage**.

---

## Historia del análisis

El trabajo realizado hasta ahora está documentado en el notebook [01_data_profiling.ipynb](notebooks/01_data_profiling.ipynb). Se descargaron y cargaron las nueve tablas del dataset y se elaboró un perfil inicial de su tamaño, tipos de datos, valores faltantes y filas duplicadas. Luego se auditó cada dataset, se prepararon copias limpias y se construyeron tablas analíticas con diferentes niveles de detalle.

### Calidad de datos

#### `orders`

Se evaluaron los valores faltantes, la unicidad de `order_id` y la coherencia de las fechas del ciclo de cada pedido. `order_id` no contiene nulos ni duplicados, por lo que funciona como clave primaria.

La mayoría de las fechas faltantes corresponde a pedidos cancelados o que no alcanzaron esa etapa del proceso. Entre los pedidos marcados como `delivered` se encontraron estas excepciones:

- 14 no tienen fecha de aprobación, aunque registran despacho y entrega.
- 2 no tienen fecha de entrega al transportista.
- 8 no tienen fecha de entrega al cliente.

Las cinco columnas temporales se convirtieron a `datetime` para comprobar la secuencia esperada **compra → aprobación → transportista → cliente**. No se encontraron aprobaciones anteriores a la compra, pero sí 1.359 registros con entrega al transportista anterior a la aprobación. El 66,3 % de estos casos presenta una diferencia inferior a 24 horas, mientras que 14 superan los siete días. También se detectaron 23 pedidos cuya entrega al cliente figura antes que la entrega al transportista.

Los valores faltantes y las inconsistencias cronológicas se conservaron sin cambios porque no existe evidencia para reconstruir las fechas correctas. La fecha estimada de entrega no se utilizó como reemplazo de la fecha real.

#### `customers`

El dataset no presenta valores faltantes ni duplicados en `customer_id`. Todos sus registros tienen un pedido asociado y todos los `customer_id` de `orders` existen en `customers`, por lo que la relación entre ambas tablas mantiene integridad referencial completa.

Se comprobó que `customer_id` identifica al cliente dentro de cada pedido, mientras que `customer_unique_id` permite reconocer a una misma persona en compras diferentes. Se identificaron 96.096 clientes reales: 93.099 realizaron una sola compra, 2.997 compraron más de una vez y el máximo registrado fue de 17 pedidos. Las repeticiones de `customer_unique_id` se conservaron porque representan recurrencia y no duplicación.

#### `order_items`

Como un pedido puede contener varios productos, `order_id` se repite de forma válida. La combinación `(order_id, order_item_id)` no contiene nulos ni duplicados y se adoptó como clave compuesta. Todos los pedidos, productos y vendedores referenciados existen en sus tablas correspondientes, y no se encontraron filas completamente duplicadas.

Se detectaron 775 pedidos sin ítems: 603 `unavailable`, 164 `canceled`, 5 `created`, 2 `invoiced` y 1 `shipped`. La mayoría es coherente con pedidos que no completaron el proceso; el pedido `shipped` sin ítems se documentó como anomalía y se conservó sin modificación.

`shipping_limit_date` se convirtió a `datetime` sin generar nulos y no se encontraron fechas límite de envío anteriores a la compra. Tampoco se hallaron precios o fletes negativos ni precios iguales a cero. Los 383 fletes con valor cero se mantuvieron porque pueden corresponder a envíos gratuitos o promociones. Los precios extremos también se conservaron para estudiarlos durante el análisis exploratorio.

#### `payments`

No se encontraron nulos, filas completamente duplicadas ni referencias a pedidos inexistentes. Como una orden puede utilizar más de un registro de pago, se validó `(order_id, payment_sequential)` como clave compuesta. Se encontró un pedido `delivered` sin pago asociado, que quedó documentado como anomalía.

Los importes y las cuotas no presentan valores negativos. Hay 9 pagos con valor cero, incluidos 3 con tipo `not_defined`; todos pertenecen a pedidos que también tienen pagos positivos, por lo que no representan necesariamente órdenes impagas. Además, se encontraron 2 pagos con tarjeta de crédito, importe positivo y cero cuotas. Estos casos se conservaron sin reclasificar ni imputar valores por falta de evidencia.

#### `products`

`product_id` es único y completo, no existen filas duplicadas y todos los productos aparecen en `order_items`. Se encontraron 610 productos donde faltan simultáneamente la categoría, la longitud del nombre, la longitud de la descripción y la cantidad de fotos, lo que indica un único patrón de metadatos descriptivos ausentes.

También se detectaron 2 productos sin peso ni dimensiones y 4 con peso no positivo. No se encontraron largos, altos o anchos no positivos. Los campos faltantes y los pesos anómalos se conservaron sin imputación porque no existe información suficiente para corregirlos.

#### `sellers`

El dataset no presenta nulos, duplicados ni problemas en `seller_id`, que puede utilizarse como clave primaria. Todos los vendedores tienen ítems asociados y todos los vendedores referenciados desde `order_items` existen en `sellers`, por lo que la integridad referencial es completa.

La concentración de vendedores en estados como São Paulo se interpretó como información del negocio y no como un problema de calidad. No fue necesario realizar transformaciones adicionales.

#### `order_reviews`

No se encontraron filas completamente duplicadas ni reseñas asociadas a pedidos inexistentes. Como `review_id` y `order_id` pueden repetirse por separado, se comprobó que la combinación `(review_id, order_id)` identifica cada registro sin nulos ni duplicados.

Los títulos y mensajes tienen numerosos valores faltantes, pero se conservaron porque los comentarios son opcionales y una reseña puede contener únicamente una puntuación. También existen 768 pedidos sin reseña, ausencia esperable por depender de la participación del cliente. Todas las puntuaciones están entre 1 y 5. Las fechas se convirtieron a `datetime` sin generar nulos y no se encontraron respuestas anteriores a la creación de la reseña.

#### `geolocation`

No se detectaron valores faltantes, coordenadas fuera de rango ni coordenadas iguales a cero. La repetición de códigos postales es válida porque un mismo prefijo puede estar asociado a diferentes coordenadas.

Sí se encontraron 261.831 filas completamente duplicadas. Se eliminaron con `drop_duplicates()` únicamente en la copia destinada al análisis, reduciendo la tabla de 1.000.163 a 738.332 filas y preservando los datos originales. Además, 278 clientes y 7 vendedores tienen códigos postales sin correspondencia geográfica; se documentaron como una limitación de cobertura y no se imputaron coordenadas.

#### `product_category_name_translation`

La tabla contiene 71 categorías y no presenta nulos ni duplicados en los nombres originales o traducidos. Todas sus categorías tienen productos asociados.

Se identificaron dos categorías de `products` sin traducción al inglés: `pc_gamer` y `portateis_cozinha_e_preparadores_de_alimentos`. Se conservaron sus nombres originales para no incorporar traducciones externas durante la limpieza.

### Preparación de los datos

Después de la auditoría se crearon copias limpias de los nueve datasets, manteniendo intactas las tablas originales. En ellas se aplicaron únicamente transformaciones respaldadas por los controles anteriores:

- Conversión a `datetime` de las fechas de pedidos, ítems y reseñas.
- Eliminación de duplicados exactos en la copia de `geolocation`.
- Incorporación de las traducciones de categorías a `products`, utilizando el nombre original cuando no existe traducción.

No se eliminaron anomalías ni se imputaron valores cuando no había evidencia suficiente para determinar el dato correcto.

### Construcción de tablas analíticas

Para evitar que las relaciones de uno a muchos multipliquen filas y generen sobreconteos, no se combinaron directamente todos los datasets. En su lugar se construyeron tres tablas con granularidades diferentes:

- **`orders_analysis` — una fila por pedido:** reúne datos del cliente y métricas agregadas de ítems, pagos y reseñas. Incluye 99.441 filas y 99.441 pedidos únicos, además de variables de tiempo de entrega, retraso, valor, flete y disponibilidad de información relacionada.
- **`order_items_analysis` — una fila por ítem vendido:** combina los 112.650 ítems con producto, categoría, vendedor, pedido y cliente. Conserva la unicidad de `(order_id, order_item_id)` e incorpora el valor total del ítem como precio más flete.
- **`customer_analysis` — una fila por cliente real:** agrupa los pedidos por `customer_unique_id` para calcular cantidad de compras, gasto total, ticket promedio, primera y última compra, tiempo de vida, entrega media, puntuación media y recurrencia. Contiene 96.096 clientes, de los cuales 2.997 son recurrentes.

Estas tablas dejan los datos preparados para la siguiente etapa: el análisis exploratorio de ventas, clientes, productos, vendedores, logística, reseñas y recurrencia.

### EDA con pandas

El análisis exploratorio está documentado en [02_eda.ipynb](notebooks/02_eda.ipynb). Para mantener comparables las métricas económicas y operativas, se trabajó principalmente con pedidos `delivered` y se utilizaron las tablas analíticas construidas en la etapa anterior.

#### ¿Cuál es el volumen general de operaciones de Olist?

Se calcularon los principales indicadores de pedidos, clientes, ítems, pagos, productos y fletes. De los 99.441 pedidos registrados, 96.478 fueron entregados (97,02 %). Estos pedidos suman 15,42 millones en pagos, con un ticket promedio de 159,86, y contienen 110.197 ítems. El flete total representa aproximadamente el 14,25 % del valor pagado.

#### ¿Cómo evolucionaron los pedidos y el valor pagado?

Se agruparon los pedidos entregados por mes para comparar su cantidad, el valor pagado y el ticket promedio. La actividad creció durante 2017 y alcanzó su máximo en noviembre, con 7.289 pedidos y 1,15 millones pagados; en 2018 se mantuvo generalmente entre 6.000 y 7.000 pedidos mensuales. La correlación de 0,996 entre pedidos y valor pagado indica que el crecimiento económico estuvo asociado principalmente al aumento del volumen de órdenes.

#### ¿Qué categorías venden más y cuáles generan mayor valor?

Se compararon ítems, pedidos, productos, valor vendido, flete y precio promedio por categoría. `bed_bath_table` lidera el volumen con 10.953 ítems, mientras que `health_beauty` genera el mayor valor, con aproximadamente 1,23 millones. `watches_gifts` ocupa el segundo lugar por valor pese a vender menos unidades, debido a su mayor precio promedio. Esto muestra que volumen y contribución económica deben evaluarse por separado.

#### ¿Dónde se concentran los clientes, los pedidos y el valor pagado?

Se analizaron clientes, pedidos entregados, pagos y ticket promedio por estado. São Paulo concentra el 41,98 % de los pedidos, pero el 37,41 % del valor pagado y presenta un ticket promedio de 142,48, inferior al promedio general. Junto con Rio de Janeiro y Minas Gerais reúne cerca de dos tercios de los pedidos y más del 60 % del valor pagado, lo que evidencia una fuerte concentración regional.

#### ¿Cuánto tardan las entregas y qué proporción llega tarde?

Se calcularon el tiempo de entrega y la diferencia entre la fecha real y la estimada para 96.470 pedidos con información completa. La entrega tarda en promedio 12,56 días y el 91,89 % llega en fecha o antes; el pedido típico se entrega cerca de 12 días antes de lo previsto. El 8,11 % llegó tarde y, dentro de ese grupo, el retraso medio fue de 9,55 días, con algunos casos extremos cercanos a 189 días.

#### ¿Los retrasos están asociados con peores puntuaciones?

Se compararon 95.824 pedidos con datos válidos de entrega y reseña. Los pedidos en fecha obtuvieron una puntuación media de 4,29 y un 9,19 % de reviews bajas, frente a 2,57 y 53,99 % en los pedidos tardíos. La puntuación desciende conforme aumenta el retraso y la correlación entre días de demora y review es de -0,267. Los resultados muestran una asociación relevante entre incumplimiento logístico y menor satisfacción, aunque no demuestran causalidad por sí solos.

---

## Project Workflow

The project will follow these stages:

1. Data acquisition
2. Dataset and table understanding
3. Data profiling
4. Null and duplicate analysis
5. Primary and foreign key validation
6. Data cleaning and transformation
7. Exploratory Data Analysis with pandas
8. SQL analysis
9. KPI definition
10. Power BI dashboard
11. Business insights
12. Business recommendations
13. Documentation and case study
