# Especificación de Redacción de Blueprints de Software Factory (SOFA-BWS)

Esta es la especificación canónica para redactar Blueprints: documentos de especificación técnica creados en Software Factory.

---

## Introducción a los Blueprints

### ¿Qué son los Blueprints?

Software Factory define cada producto mediante dos conjuntos de documentos complementarios: Requisitos y Blueprints. Los Requisitos capturan los resultados y restricciones esperados externamente a través de historias de usuario y criterios de aceptación estructurados; los Blueprints son las especificaciones técnicas que definen cómo opera el sistema de software para satisfacer esos requisitos.
Ambos tipos de documento se redactan en markdown y están pensados para ser legibles como documentos fuente en texto plano, sin dejar de soportar referencias estructuradas y flujos de trabajo asistidos por máquinas.

En términos de ingeniería de requisitos, los Requisitos describen *qué* debe ser cierto desde la perspectiva del usuario y del negocio, mientras que los Blueprints describen *cómo* está estructurado y se comporta el sistema para que eso sea cierto. Los Blueprints asignan comportamiento a componentes concretos de runtime, definen los datos/contratos que cruzan los límites entre componentes y describen la dependencia y el flujo de control que convierten la intención del usuario en comportamiento del sistema.

En conjunto, los Requisitos y los Blueprints forman una definición completa del producto que es verificable en ambas direcciones: cada Blueprint debería trazarse hacia arriba hasta los Requisitos y hacia abajo hasta símbolos de código reales e interacciones de runtime.

### Dos Tipos de Blueprint

**Component Blueprint** — Describe una **capacidad reutilizable del sistema**: un grupo cohesivo de servicios, controladores, hooks, estrategias y otros componentes de runtime que juntos habilitan una capacidad. Es el equivalente en prosa de un diagrama de componentes C4: los bloques de componente estructurados son los nodos, y los párrafos entre los bloques de componente son las aristas de relación. Los Component Blueprints son **agnósticos a la funcionalidad** (describen lo que el sistema *puede* hacer, no lo que usa una funcionalidad en particular) y comúnmente **abarcan múltiples contenedores C4** (por ejemplo, API Server y Client App). En los sistemas de software modernos, la mayoría de las capacidades son inherentemente multi-contenedor, porque el comportamiento de punta a punta típicamente combina interfaz de usuario, orquestación de API, procesamiento en segundo plano y persistencia.

**Feature Blueprint** — Describe cómo se combinan las capacidades de los **Component Blueprints**, más los componentes específicos de la funcionalidad, para satisfacer un conjunto de Requisitos de producto. Cada Feature Blueprint corresponde a un Documento de Requisitos de Funcionalidad (FRD) y es su contraparte técnica: los Requisitos dicen *qué*; el Feature Blueprint dice *cómo*. Los Feature Blueprints son **composición primero**: conectan capacidades compartidas, las configuran para la funcionalidad y documentan el código de unión exclusivo de la funcionalidad.

### Cómo se Relacionan los Dos Tipos

**El Product Manager define funcionalidades:**
  "Checkout" (se inicializa automáticamente: FRD `Checkout` + Feature Blueprint `Checkout`)
  "Order Tracking" (se inicializa automáticamente: FRD `Order Tracking` + Feature Blueprint `Order Tracking`)

**El Product Manager escribe requisitos estructurados en los FRDs:**
  → Checkout (REQ-CHECKOUT-001, REQ-CHECKOUT-002, …)
  → Order Tracking (REQ-TRACK-001, REQ-TRACK-002, …)

**El Ingeniero lee los requisitos, identifica capacidades compartidas del sistema y crea Component Blueprints:**
  → Identity and Session Management (que contiene componentes como `AuthenticationService`, `SessionTokenStore`, `UserProfileClient`)
  → Notification Delivery (que contiene componentes como `NotificationRouter`, `EmailDeliveryService`, `SmsDeliveryService`)

**El Ingeniero escribe los Feature Blueprints:**
  → Checkout Feature Blueprint (compone Identity and Session Management + componentes específicos de checkout)
  → Order Tracking Feature Blueprint (compone Identity and Session Management + Notification Delivery + componentes específicos de order tracking)


El trabajo del ingeniero: (1) identificar las capacidades compartidas que sustentan las funcionalidades, (2) documentarlas como Component Blueprints, (3) componerlas en Feature Blueprints que se mapeen a los Requisitos. El resultado ideal es que los Feature Blueprints sean mayormente *composición*; los componentes específicos de la funcionalidad existen donde hacen falta. Los componentes a menudo nacen en los Feature Blueprints y se refactorizan a Component Blueprints cuando surge la reutilización: ese ciclo de vida es el esperado.

---

## Sintaxis y Semántica Central

La sintaxis de los Blueprints define los elementos estructurales canónicos que pueden aparecer en un documento Blueprint (bloques `component` y `model`). La semántica de los Blueprints define cómo deben interpretarse esos elementos: qué significa cada elemento, cómo se relacionan entre secciones y documentos, y cómo las referencias se mapean a propiedad en runtime, contratos y comportamiento.

### Bloques Component

Los componentes se definen en bloques de código estructurados que actúan como los **nodos** de la arquitectura:

- **name:** PascalCase, coincide con la identidad del componente en el código.
- **container:** Contenedor(es) C4, separados por comas si son varios (por ejemplo, `Client App`, `API Server`, `Task Server` o `Client App, API Server`).
- **responsibilities:** Lista de viñetas (`- `) con sangría de tabulación de lo que hace este componente. Usá menciones de elemento (`` `...` ``) para datos/contratos y menciones de componente (`` `#...` ``) o de elemento cuando las responsabilidades dependen de otros componentes o colaboran con ellos (incluidos componentes definidos en otros Blueprints).

Cualquier cosa definida con un bloque `component` (por ejemplo, `name: MyComponent`) en un documento puede referenciarse como `#MyComponent` desde cualquier documento.

Ejemplo:
````
```component
name: NotificationDeliveryService
container: API Server
responsibilities:
	- Seleccionar canales de entrega según `NotificationPreference` y el tipo de mensaje
	- Renderizar payloads específicos de cada canal a partir de `NotificationTemplate`
	- Despachar mensajes a través de adaptadores de proveedores con reintentos y protecciones de idempotencia
```
````


### Bloques Model

Usá un bloque **model** cuando un Blueprint necesita un modelo de datos/dominio explícito y canónico que es central para la implementación pero no es un componente de runtime:

- **name:** Nombre del modelo.
- **store:** Dónde se almacena el modelo (por ejemplo, `Postgres`, `S3`, `DynamoDb`, `CacheMemory`).
- **description:** Breve declaración de propósito.
- **fields:** Lista de viñetas con sangría de tabulación de los campos canónicos y sus tipos.
- **constraints:** Reglas invariantes aplicadas por la lógica de dominio.

Los modelos se mencionan con backticks como un elemento (ver Menciones más abajo).

Ejemplo:
````
```model
name: CustomerOrder
store: Postgres
description: Modelo canónico de pedido persistido, usado por los flujos de checkout, cumplimiento y soporte.
fields:
	- id: UUID (required)
	- order_number: string (required)
	- customer_account_id: UUID (required; foreign key -> `CustomerAccount.id`)
	- status: Draft | Placed | Packed | Shipped | Delivered | Cancelled (required)
	- total_amount: decimal (required)
	- placed_at: datetime (nullable)
constraints:
	- unique `order_number`
	- `total_amount` is non-negative
	- `placed_at` is present when `status` is not `Draft`
```
````

### Menciones

Los Blueprints usan tres tipos de mención para crear enlaces navegables:

- `` `#ComponentName` `` para componentes (comportamiento de runtime).
- `` `ElementName` `` para elementos (formas de datos y contratos).
- `@SystemEntity` para documentos completos y entidades de la plataforma.

La tabla siguiente resume la sintaxis, el alcance y dónde se define cada tipo.

| Sintaxis | A qué referencia | Ejemplo | ¿Definido en Blueprints? |
|----------|------------------|---------|--------------------------|
| `` `#Name` `` | Componentes (comportamiento de runtime) | `` `#NotificationDeliveryService` `` | Sí, mediante bloques component |
| `` `Name` `` | Elementos (formas de datos, contratos) | `` `CustomerOrder` `` | Símbolos de código o bloques model |
| `@Name` | Otras entidades/documentos del sistema | `@Checkout Requirements` | Entidades de la plataforma |

**`` `#ComponentName` ``** — Hashtag entre backticks para componentes (servicios, controladores, hooks, estrategias, proveedores). Son cosas que tienen (o podrían tener) un bloque `component`. Los componentes son cosas de runtime que *hacen trabajo*. Ejemplos: `` `#NotificationDeliveryService` ``, `` `#OrderLifecycleService` ``, `` `#CheckoutApiController` ``. Los componentes definidos en *cualquier* Blueprint con la sintaxis de bloque ` ```component ``` ` pueden mencionarse de esta forma desde cualquier otro Blueprint; esta referencia entre Blueprints es la forma en que se expresa la composición.

**`` `ElementName` ``** — Backticks para elementos: símbolos de código arquitectónicamente significativos que *no* están definidos como componentes: esquemas, configuraciones, tipos de dominio, enums, modelos de request/response, excepciones, feature flags, matrices de permisos y modelos (incluidos los definidos en bloques `model`). Los elementos *describen la forma*; definen contratos y configuración que los componentes leen, producen o comparten. Los modelos de request/response y los tipos de excepción son especialmente buenos como menciones de elemento porque sus nombres suelen ser autoexplicativos. Usá la capitalización del lenguaje de origen (por ejemplo, `CustomerOrder`, `OrderStatus`, `NotificationTemplate`, `CheckoutRequest`, `CheckoutResponse`). Las menciones de elemento no crean dependencia entre blueprints; varios blueprints pueden mencionar el mismo elemento sin implicar una dependencia.

**`@SystemEntity`** — Arroba para otras entidades/documentos del sistema gestionados por la plataforma: Requisitos, Blueprints, Órdenes de Trabajo y Artefactos. Ejemplos: `@Checkout Requirements`, `@Order Tracking Feature Blueprint`, `@WO-123`, `@Customer Call Artifact`. Estos enlazan con documentos y entidades reales de Software Factory.

**Cuándo usar cada una:** Hace trabajo (procesa, orquesta, renderiza, obtiene) -> `#Component`. Describe forma o contrato (esquema, tipo, configuración, enum, modelo, request/response, excepción) -> `Element`. Documento (Requisitos, Blueprint) o artefacto en Software Factory -> `@SystemEntity`.

**Párrafo de ejemplo:**  
`#CheckoutApiController` (ver @Checkout Feature Blueprint) valida `CheckoutRequest` y llama a `#OrderLifecycleService` para crear un `CustomerOrder`. El servicio establece `OrderStatus` en `Placed` y luego llama a `#NotificationDeliveryService` con un `NotificationTemplate`.  
Acá los nombres con `#` son componentes con definiciones en algún lugar; `` `CheckoutRequest` ``, `CustomerOrder`, `OrderStatus` y `NotificationTemplate` son elementos; `@Checkout Feature Blueprint` es una entidad de la plataforma.

---

## Redacción de Párrafos de Relación entre Componentes

Las relaciones entre componentes se describen en **párrafos en lenguaje natural** que actúan como las **aristas** de la arquitectura: qué fluye entre componentes, quién depende de quién y por qué.

**Principios clave:** Usá cada párrafo para conectar componentes concretos definidos mediante bloques `component`; mencioná ambos componentes al principio para que la arista sea explícita. Indicá la dirección (quién depende de quién). Usá menciones de componente (`#...`) y de elemento (`...`) para agregar detalle de implementación y claridad en el flujo de datos, no como fin en sí mismas. Explicá el *por qué*, no solo el *qué*. Una relación por párrafo, de 2 a 4 oraciones. No repitas las responsabilidades del bloque de componente; describí la *interacción* y lo que cruza el límite.

---

## Guía de Component Blueprints

### Qué Son y Cuándo Crear Uno

Un Component Blueprint es la documentación técnica de una capacidad reutilizable del sistema. Es agnóstico a la funcionalidad y puede abarcar múltiples contenedores C4. Los Component Blueprints sirven principalmente a los Feature Blueprints, definiendo las capacidades reutilizables que las funcionalidades componen, y secundariamente a ingenieros y agentes de IA durante la implementación, la depuración y la extensión.

**Creá un Component Blueprint cuando:** estés construyendo un sistema técnico compartido del que dependen (o dependerán) dos o más funcionalidades; estés abstrayendo una capacidad reutilizable; el sistema tenga suficiente estructura interna (múltiples componentes y relaciones) como para justificar su propio documento; o quieras establecer los contratos (elementos) que otros Blueprints van a referenciar.

**No crees uno para:** una única utilidad o helper sin estructura interna; lógica específica de una funcionalidad que solo tiene sentido en un contexto (eso pertenece a un Feature Blueprint); o infraestructura que ya está bien documentada en otro lado (referenciala como dependencia externa si hace falta).

### Estructura

1. **Título y resumen de la capacidad** — Empezá con el título del Blueprint y luego agregá `## Capability Summary`, que explica qué hace la capacidad en 2–3 oraciones y nombra los elementos clave que fluyen por ella.
2. **Componentes centrales (agrupados lógicamente)** — Agregá `## Core Components` y definí los bloques de componente en grupos lógicos (por ejemplo, ingesta, orquestación, persistencia y presentación; o backend y luego frontend).
3. **Párrafos de relación como aristas** — Tratá los bloques `component` como nodos y los párrafos en prosa como aristas. Insertá un párrafo de relación entre componentes o grupos cuando la dirección, el flujo de datos o la intención no sean obvios por la mera cercanía. Si la adyacencia ya vuelve inequívoca la relación, el párrafo es opcional.
4. **Encabezados de sección y divisores** — Mantené todas las definiciones de componente bajo `## Core Components`, y usá subencabezados `###` para agrupar componentes relacionados (por ejemplo, "### API Layer", "### Frontend: Api Hooks"). Usá `---` entre límites mayores (por ejemplo, backend vs frontend) cuando ayude una separación visual adicional.

### Secciones Opcionales

- **`## System Contracts`** — Opcional pero recomendada cuando la capacidad tiene garantías no triviales o interfaces de frontera. Organizá esta sección con `### Key Contracts` (invariantes, reglas de corrección, semánticas de confiabilidad como idempotencia/orden/consistencia/comportamiento de reintentos) y `### Integration Contracts` (eventos publicados/consumidos, interfaces de API, payloads de webhooks y expectativas de composición). Usá `### Integration Boundaries` cuando el énfasis esté en la propiedad y la separación de responsabilidades más que en el detalle de payloads/API.
- **`## Architecture Decision Records`** — Sección opcional para decisiones de diseño no obvias y sus compromisos. Usá entradas ADR concisas con `Context`, `Decision` y `Consequences`; ubicá esta sección después de `## System Contracts` cuando estén presentes ambas.
- Usá estas secciones solo cuando reduzcan la ambigüedad; no son requeridas para que un Blueprint sea válido.

---

## Guía de Feature Blueprints

### Qué Son y Cuándo Crear Uno

Un Feature Blueprint describe cómo se componen los Component Blueprints — más cualquier componente específico de la funcionalidad — para satisfacer los Requisitos de producto. Es composición primero: las capacidades compartidas hacen el trabajo pesado; el Feature Blueprint las conecta, las configura y documenta el código de unión exclusivo de la funcionalidad.

**Creá un Feature Blueprint cuando:** un product manager haya definido una funcionalidad con Requisitos estructurados; la funcionalidad componga uno o más Component Blueprints; necesites documentar cómo esas capacidades se configuran y conectan para esta funcionalidad; o existan componentes específicos de la funcionalidad que no pertenecen a ningún Component Blueprint.

### Conexión con los Requisitos

Todo Feature Blueprint tiene un **Documento de Requisitos de Funcionalidad** correspondiente en formato estructurado, por ejemplo:

```
### REQ-XXX-001: Nombre del Requisito
**User Story:** Como [rol], quiero [acción], para [resultado].
**Acceptance Criteria:**
* **AC-XXX-001.1:** Cuando el usuario [acción], el sistema deberá [comportamiento].
* **AC-XXX-001.2:** Cuando [condición], el sistema deberá [comportamiento].
```

Se asume que el autor de un Feature Blueprint leyó el Documento de Requisitos correspondiente. El Feature Blueprint provee el camino técnico para satisfacer esos requisitos; no se requiere referencia cruzada formal.

### Estructura

1. **Título y resumen de la funcionalidad** — Empezá con el título del Blueprint y luego agregá `## Feature Summary` con un resumen centrado en el usuario de 2–3 oraciones que referencie el Documento de Requisitos correspondiente.
2. **Composición de Component Blueprints** — Agregá `## Component Blueprint Composition` para documentar qué capacidades compartidas compone esta funcionalidad y cómo se configura o delimita cada una. Usá menciones de documento (`@...`) para los Blueprints/Requisitos referenciados y menciones de componente (`#...`) para los componentes concretos de runtime involucrados en la composición.
3. **Componentes específicos de la funcionalidad** — Agregá `## Feature-Specific Components` para los componentes que existen solo para esta funcionalidad (paneles, páginas, hooks específicos de la funcionalidad); dales bloques de componente completos.
4. **Párrafos de composición** — Usá párrafos de relación/composición entre secciones para explicar cómo las capacidades referenciadas y los componentes específicos de la funcionalidad se conectan, desde la acción del usuario hasta el comportamiento del sistema. Mencioná explícitamente los componentes concretos de otros Blueprints que participan en la implementación usando menciones `#...`, y usá menciones de elemento para los contratos/datos que cruzan los límites.
5. **Contratos y ADRs cuando la lógica de la funcionalidad es sustancial** — Agregá `## System Contracts` y/o `## Architecture Decision Records` cuando el Feature Blueprint defina comportamiento específico significativo de la funcionalidad (por ejemplo, cuando los Component Blueprints no cubren gran parte de la funcionalidad y las garantías clave o los compromisos de diseño se definen acá).

### Referenciar Component Blueprints y Componentes Específicos de la Funcionalidad

Al referenciar un Component Blueprint, no redefinas sus componentes: describí *cómo* la funcionalidad *usa* la capacidad (por ejemplo, delimitación por funcionalidad, límites de sección, transformación de respuestas). Ejemplo:

> La funcionalidad Checkout usa las capacidades compartidas de Identity and Session Management y Order Lifecycle. `#CheckoutApiController` valida `CheckoutRequest`, delega las verificaciones de autenticación/sesión a `#AuthenticationService` y envía el comando de pedido a `#OrderLifecycleService`. El `CustomerOrder` resultante se mapea a `CheckoutResponse` para el cliente.

Los componentes específicos de la funcionalidad reciben bloques de componente completos en el Feature Blueprint. Los Feature Blueprints también pueden extender capacidades compartidas con bloques de componente completos cuando la extensión es específica de la funcionalidad. Cualquier componente definido en cualquier Blueprint puede referenciarse con `#` desde cualquier otro.

---

## Principios de los Blueprints

1. **Basados en el código.** Los Blueprints referencian símbolos de código reales. Los componentes se mapean a componentes de runtime; los elementos se mapean a esquemas, tipos, modelos y contratos concretos.
2. **Composición primero.** Los Component Blueprints definen capacidades reutilizables; los Feature Blueprints componen esas capacidades y agregan componentes específicos de la funcionalidad solo donde hace falta.
3. **Estructurados y narrativos.** Los bloques estructurados proveen puntos de anclaje (`component`, `model`); los párrafos en prosa explican interacciones, dirección e intención.
4. **Implementables.** Un Feature Blueprint debe proveer suficiente claridad arquitectónica para implementar sin ambigüedad material.
5. **Nativos de markdown.** Los Blueprints y los Requisitos son documentos markdown con convenciones estructuradas livianas.
6. **Artefactos vivos.** Los Blueprints evolucionan con el sistema a medida que cambian la arquitectura y los requisitos.

---

## Checklist de Redacción

- **Elegir el tipo de Blueprint** — Component Blueprint (capacidad reutilizable) vs Feature Blueprint (composición + comportamiento específico de la funcionalidad).
- **Seguir las secciones base** — Los Component Blueprints usan `## Capability Summary` y `## Core Components`; los Feature Blueprints usan `## Feature Summary`, `## Component Blueprint Composition` y `## Feature-Specific Components`.
- **Declarar componentes y modelos** — Usar bloques `component` para los nodos de runtime; usar bloques `model` solo cuando haga falta una definición canónica de modelo de dominio.
- **Usar correctamente la sintaxis de menciones** — Usar `#...` para componentes, `` `...` `` para elementos (esquemas, tipos, modelos de request/response, excepciones, modelos) y `@...` para entidades/documentos del sistema y artefactos.
- **Escribir párrafos de composición/relación** — Nombrar componentes concretos (incluidas referencias `#...` entre blueprints), indicar la dirección, identificar los datos/contratos que cruzan los límites y explicar por qué existe la interacción.
- **Agregar secciones opcionales cuando corresponda** — Usar `## System Contracts` (`### Key Contracts`, `### Integration Contracts`/`### Integration Boundaries`) y `## Architecture Decision Records` cuando reduzcan la ambigüedad, especialmente cuando el Feature Blueprint define comportamiento significativo de la funcionalidad.
- **Confirmar la alineación con los requisitos (Feature Blueprints)** — Asumir que el autor leyó el Documento de Requisitos y asegurar que cada tema principal de requisitos tenga un camino técnico claro a través del Blueprint.
