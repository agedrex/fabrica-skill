# Especificación de Redacción de Requisitos de Software Factory (SOFA-RWS)

Esta es la especificación canónica para redactar Documentos de Requisitos: documentos de especificación de producto creados en Software Factory.

---

## Introducción a los Requisitos

### ¿Qué son los Requisitos?

Software Factory define cada producto mediante dos conjuntos de documentos complementarios: Requisitos y Blueprints. Los Requisitos capturan los resultados y restricciones esperados externamente a través de historias de usuario y criterios de aceptación estructurados; los Blueprints son las especificaciones técnicas que definen cómo opera el sistema de software para satisfacer esos requisitos. Ambos tipos de documento se redactan en markdown y están pensados para ser legibles como documentos fuente en texto plano, sin dejar de soportar referencias estructuradas y flujos de trabajo asistidos por máquinas.

Los requisitos describen *qué* debe ser cierto desde la perspectiva del usuario y del negocio. Son la base de todo el resto del trabajo en Software Factory: los Blueprints contienen la especificación técnica que los implementa, y las órdenes de trabajo descomponen esa especificación en tareas implementables. Cuando los requisitos son claros y están bien mantenidos, cada artefacto posterior hereda esa claridad; cuando son vagos o están desactualizados, esa ambigüedad se acumula a lo largo de todo el ciclo de desarrollo.

### Dos Tipos de Documento de Requisitos

**Requisitos de Visión General (Overview Requirements)** — Un documento narrativo que establece el contexto de todo el producto: el problema de negocio, el estado actual, las personas, la descripción del producto u otro encuadre que aplique a todas las funcionalidades. Los Requisitos de Visión General no tienen asociación con una funcionalidad, ni IDs de requisito estructurados, ni criterios de aceptación. Son documentos en prosa escritos para una audiencia humana.

**Documento de Requisitos de Funcionalidad (Feature Requirements Document, FRD)** — Un documento estructurado que especifica el comportamiento esperado de una única funcionalidad mediante una visión general, definiciones de terminología y un conjunto de requisitos numerados, cada uno con una historia de usuario y criterios de aceptación. Todo FRD pertenece a una funcionalidad y tiene un Feature Blueprint correspondiente en Foundry. Los FRDs son la entrada principal para la implementación de ingeniería. Los FRDs pueden anidarse: un FRD padre puede contener FRDs hijos, formando una jerarquía que refleja la descomposición de la funcionalidad en subfuncionalidades.

### Cómo se Relacionan los Dos Tipos

Los Requisitos de Visión General preparan el escenario; los FRDs especifican el producto.

Un lector debería poder empezar por los Requisitos de Visión General (Problema de Negocio, Estado Actual, Personas, Descripción del Producto) y comprender el contexto completo del producto antes de leer cualquier FRD. Los FRDs luego especifican qué debe hacer el sistema, funcionalidad por funcionalidad, sin repetir el encuadre del producto.

Como los FRDs pueden anidarse, las funcionalidades grandes se descomponen naturalmente en un árbol. Un **FRD de nivel módulo** está en la cima de ese árbol: describe el propósito del módulo y lista sus subfuncionalidades hijas con breves resúmenes, pero no contiene IDs de requisito estructurados; esos viven en los FRDs hijos. Esto mantiene el documento padre liviano y navegable, mientras los hijos llevan las especificaciones detalladas.

---

## Requisitos de Visión General

Los Requisitos de Visión General son documentos narrativos de formato libre que se inicializan con cada nuevo proyecto de Software Factory. No tienen una estructura interna prescrita más allá de un encabezado y prosa. Los documentos por defecto son:

- **Problema de Negocio (Business Problem)** — Por qué existe el producto; los puntos de dolor que aborda.
- **Estado Actual (Current State)** — El statu quo que el producto viene a transformar.
- **Personas** — Los arquetipos de usuario y sus objetivos.
- **Descripción del Producto (Product Description)** — Qué es el producto y cómo encajan sus módulos.

### Guía

Escribí en prosa clara y directa. Evitá la jerga salvo que la audiencia sea exclusivamente técnica. Los Requisitos de Visión General deben ser legibles tanto por product managers como por ejecutivos e ingenieros. Deben ser estables: se actualizan con poca frecuencia y solo cuando cambia el encuadre fundamental del producto.

---

## Requisitos de Funcionalidad

Los Requisitos de Funcionalidad siguen una estructura consistente con tres secciones: **Overview** (Visión General), **Terminology** (Terminología) y **Requirements** (Requisitos).

### Sección de Visión General (Overview)

Una breve descripción en prosa (1–3 párrafos) del propósito de la funcionalidad, su alcance y cómo encaja en el producto en general. Esta sección establece el contexto para los requisitos estructurados que siguen.

Ejemplo:

```markdown
## Overview

El módulo de Checkout provee el flujo de compra de punta a punta, desde la
revisión del carrito hasta la confirmación del pago. Se integra con el
catálogo de productos para precios e inventario, y con el sistema de
notificaciones para el envío de la confirmación del pedido.
```

### Sección de Terminología (Terminology)

Un glosario en viñetas de los términos de dominio usados en los requisitos. Definí los términos una sola vez acá; no los redefinas en línea. Cada entrada tiene el formato de un término en negrita seguido de dos puntos y su definición.

Ejemplo:

```markdown
## Terminology

* **Carrito**: La colección de ítems en trabajo que un cliente pretende comprar.
* **Pedido**: Un registro de compra finalizado que se crea cuando se completa el checkout.
* **Retención de Cumplimiento**: Un bloqueo temporal del procesamiento de un
  pedido, pendiente de revisión manual.
```

### Sección de Requisitos (Requirements)

El cuerpo estructurado del documento. Cada requisito es un bloque numerado que contiene una **historia de usuario** y uno o más **criterios de aceptación**.

Cada requisito dentro de un documento de Requisitos de Funcionalidad es un bloque numerado con tres partes:

- **ID y título:** `REQ-{PREFIX}-{NNN}: Nombre del Requisito` — un identificador único con un prefijo mnemotécnico corto derivado del título del FRD (por ejemplo, `CHK` para "Checkout", `NOTIF` para "Notificaciones") y un número de secuencia con ceros a la izquierda. El prefijo se elige una vez por documento y se usa de forma consistente en todos los requisitos del mismo.
- **Historia de usuario:** Una única oración con el formato `Como [rol], quiero [acción], para [resultado].`
- **Criterios de aceptación:** Uno o más criterios numerados (`AC-{PREFIX}-{NNN}.{N}`), cada uno con el formato `Cuando [disparador o condición], el sistema deberá [comportamiento esperado].`

Ejemplo:

```markdown
### REQ-CHK-003: Confirmación de Pago

**User Story:** Como cliente, quiero recibir una confirmación luego de que
mi pago sea procesado, para saber que mi pedido se realizó con éxito.

**Acceptance Criteria:**

* **AC-CHK-003.1:** Cuando el procesamiento del pago sea exitoso, el sistema
  deberá mostrar una página de confirmación con el número de pedido y la
  fecha estimada de entrega.
* **AC-CHK-003.2:** Cuando el procesamiento del pago falle, el sistema
  deberá devolver al usuario al formulario de pago con un mensaje de error
  que describa el motivo de la falla.
* **AC-CHK-003.3:** Cuando el usuario navegue a otra página durante el
  procesamiento, el sistema deberá completar la transacción y mostrar la
  confirmación en su próxima visita.
```

### Subfuncionalidades

Algunas funcionalidades son lo suficientemente grandes como para descomponerse en subfuncionalidades. En esos casos el documento padre funciona como una **visión general del módulo**: enuncia el propósito del módulo y lista las subfuncionalidades con breves resúmenes. No contiene identificadores `REQ-`; esos pertenecen a los documentos de las subfuncionalidades.

```markdown
# Módulo de Gestión de Pedidos

El Módulo de Gestión de Pedidos maneja el ciclo de vida completo del pedido,
desde su realización hasta el cumplimiento y el procesamiento de devoluciones.

## Sub-Features

**Realización de Pedidos**: Provee el flujo de checkout para enviar nuevos
pedidos con validación de pago y de dirección.

**Seguimiento de Pedidos**: Muestra el estado del pedido en tiempo real, el
seguimiento del envío y la información de entrega estimada.

**Devoluciones y Reembolsos**: Gestiona el inicio de devoluciones, los flujos
de aprobación y el procesamiento de reembolsos.
```

---

## Principios de los Requisitos

1. **Centrados en el usuario.** Los requisitos describen lo que los usuarios necesitan y lo que el sistema debe hacer por ellos, no cómo está construido el sistema internamente.
2. **Verificables.** Cada criterio de aceptación debe ser lo bastante claro como para derivar casos de prueba a partir de él.
3. **Atómicos.** Cada criterio de aceptación cubre un único comportamiento. Los comportamientos compuestos se dividen en criterios separados.
4. **Identificadores estructurados.** Los requisitos y los criterios de aceptación usan esquemas de ID consistentes y legibles por máquina (`REQ-{PREFIX}-{NNN}`, `AC-{PREFIX}-{NNN}.{N}`).
5. **Nativos de markdown.** Los requisitos son documentos markdown con convenciones estructurales livianas.
6. **Artefactos vivos.** Los requisitos evolucionan con el producto a medida que se profundiza el entendimiento y cambia el alcance.

---

## Checklist de Redacción

- **Elegir el tipo de documento** — Requisito de Visión General (contexto de todo el producto) vs. Requisito de Funcionalidad (historias de usuario y criterios de aceptación estructurados).
- **Escribir la sección Overview** — 1–3 párrafos de contexto y alcance de la funcionalidad.
- **Definir la Terminología** — Glosario de los términos de dominio usados en el documento; definir cada término una sola vez.
- **Asignar un prefijo** — Derivar un mnemotécnico corto y consistente del título del FRD para los IDs de requisito (por ejemplo, `CHK` de "Checkout", `NOTIF` de "Notificaciones").
- **Escribir historias de usuario** — Una por requisito, en formato "Como / quiero / para".
- **Escribir criterios de aceptación** — Un comportamiento verificable por criterio, en formato "Cuando / el sistema deberá".
- **Usar referencias cruzadas** — Referenciar documentos relacionados con menciones `@DocumentName`.
- **Mantener livianos los documentos de nivel módulo** — Solo declaración de propósito y resúmenes de subfuncionalidades; sin bloques `REQ-`.
