---
name: software-factory
description: Referencia general de la plataforma Software Factory — tipos de documento, módulos, herramientas MCP y flujo de ejecución de órdenes de trabajo. Usar al trabajar con requisitos, blueprints, órdenes de trabajo o cualquier herramienta MCP de Software Factory.
---

# Software Factory

Software Factory conecta los requisitos de producto con código funcional a través de un pipeline estructurado. La plataforma está organizada en módulos especializados, cada uno diseñado para una persona y una etapa específica del proceso de desarrollo. Este enfoque modular permite que product managers, arquitectos, planificadores de proyecto y desarrolladores trabajen en su dominio manteniendo traspasos claros entre etapas.

---

## Flujo de Documentos

El proceso comienza con los Documentos de Requisitos de Funcionalidad (FRDs) escritos por autores en Refinery. Cada FRD describe los requisitos funcionales de una funcionalidad específica: qué debe hacer la funcionalidad desde la perspectiva del usuario. Cuando se crea un FRD, el sistema crea automáticamente un Feature Node (la columna vertebral organizativa) y un Blueprint correspondiente. Luego, los ingenieros escriben los Blueprints en Foundry, que son especificaciones técnicas que definen cómo implementar cada funcionalidad. Los Blueprints se descomponen en Órdenes de Trabajo en Planner: las tareas específicas que implementarán los desarrolladores. Finalmente, los desarrolladores usan el MCP Server para acceder al contexto del proyecto mientras escriben código. Los Artefactos (documentos de investigación, diseños, especificaciones de API) pueden adjuntarse en cualquier etapa para aportar contexto adicional.

---

## Módulos y Personas

- **Refinery** — Para product managers y stakeholders que definen qué construir. Los autores escriben Documentos de Requisitos de Funcionalidad (FRDs) que describen los requisitos funcionales y las capacidades del usuario. El sistema crea Feature Nodes para organizar estos requisitos jerárquicamente. Los Artefactos aportan contexto de apoyo, como investigación de mercado o entrevistas a usuarios.
- **Foundry** — Para arquitectos técnicos que definen cómo construirlo. Cada Feature Node tiene un Blueprint correspondiente que especifica la implementación técnica. Los Blueprints reflejan la jerarquía de los FRDs y se vinculan con archivos de código, brindando el puente entre los requisitos de producto y las especificaciones técnicas.
- **Planner** — Para project managers y tech leads que organizan el trabajo. Los Blueprints se descomponen en Órdenes de Trabajo (tareas concretas de desarrollo) y se organizan en Fases para una entrega estructurada. Las Órdenes de Trabajo especifican qué archivos crear o modificar e incluyen pasos de implementación detallados.
- **MCP Server** — Para desarrolladores que están escribiendo código activamente. Las herramientas de programación externas obtienen el contexto del proyecto (órdenes de trabajo, blueprints y artefactos) para informar las decisiones de implementación.

---

## Entidades Clave y Relaciones

- Los **Feature Nodes** forman una jerarquía en la que las funcionalidades padre contienen funcionalidades hijas
- Los **FRDs** se vinculan con su Feature Node de origen
- Los **Blueprints** se vinculan con su Feature Node de origen y con los archivos de código que especifican
- Las **Órdenes de Trabajo** se conectan con su Blueprint de origen y se agrupan en Fases
- Los **Artefactos** pueden adjuntarse en cualquier etapa para aportar contexto adicional

---

## Requisitos

Los requisitos definen *qué* debe ser cierto desde la perspectiva del usuario y del negocio. Son la base de todo el resto del trabajo en Software Factory: los Blueprints contienen la especificación técnica que los implementa, y las órdenes de trabajo descomponen esa especificación en tareas implementables.

Hay dos tipos de documento de Requisitos:

- **Requisitos de Visión General (Overview Requirements)** — Documentos narrativos que establecen el contexto de todo el producto (Problema de Negocio, Estado Actual, Personas, Descripción del Producto). Sin IDs estructurados ni criterios de aceptación.
- **Documentos de Requisitos de Funcionalidad (FRDs)** — Documentos estructurados que especifican el comportamiento de una funcionalidad mediante historias de usuario (`REQ-{PREFIX}-{NNN}`) y criterios de aceptación (`AC-{PREFIX}-{NNN}.{N}`). Los FRDs pueden anidarse en jerarquías que reflejan la descomposición de la funcionalidad.

Para la ejecución, toda verificación de implementación y de finalización debe referenciar explícitamente el alcance de los requisitos y verificar que se satisfagan todos los criterios de aceptación vinculados.

**Especificación completa:** [sofa-rws.md](sofa-rws.md) (documento extenso; leelo solo si vas a escribir requisitos)

---

## Blueprints

Los Blueprints son especificaciones técnicas que describen *cómo* está estructurado y se comporta el sistema para satisfacer los requisitos. Definen componentes, contratos, modelos y relaciones a través de los límites de runtime.

Hay dos tipos de Blueprint:

- **Component Blueprints** — Capacidades reutilizables del sistema (agnósticas a la funcionalidad, a menudo multi-contenedor). Se definen con bloques `component` y `model`; los párrafos de relación describen cómo interactúan los componentes.
- **Feature Blueprints** — Composición de capacidades de Component Blueprints más componentes específicos de la funcionalidad para satisfacer un conjunto de Requisitos de producto. Cada Feature Blueprint corresponde a un FRD.

Los Blueprints usan tres tipos de mención: `#ComponentName` para componentes, `ElementName` para formas de datos/contratos y `@SystemEntity` para documentos y entidades de la plataforma.

**CRÍTICO durante la ejecución de una orden de trabajo:** cuando un blueprint referencia a otro blueprint con `@OtherBlueprint`, DEBÉS leer el blueprint referenciado para comprender la composición completa de componentes y los contratos.

**Especificación completa:** [sofa-bws.md](sofa-bws.md) (documento extenso; leelo solo si vas a escribir blueprints)

---

## Ejecución de Órdenes de Trabajo

Las órdenes de trabajo son las tareas concretas de desarrollo descompuestas a partir de los Blueprints. Al ejecutar una orden de trabajo, seguí la guía específica de la fase en la que estés.

### Enrutamiento por Fase

- **Iniciar una orden de trabajo** (después de `get_next_work_order` o `start_work_order`): seguí [start-work-order.md](start-work-order.md)
- **Completar una orden de trabajo** (verificación, `complete_work_order` y traspaso): seguí [complete-work-order.md](complete-work-order.md)

La fase de inicio ([start-work-order.md](start-work-order.md)) incluye instrucciones para inicializar el directorio de ejecución, el protocolo del checklist y las salvaguardas.

Si `scratch/wo-execution/WO-<number>/` ya existe, retomá desde ahí. Inicializá una nueva carpeta de orden de trabajo solo cuando no exista una.

---

## Índice de Archivos del Skill

| Archivo | Propósito |
|---------|-----------|
| [sofa-rws.md](sofa-rws.md) | Especificación de Redacción de Requisitos — convenciones completas para leer y escribir documentos de Requisitos |
| [sofa-bws.md](sofa-bws.md) | Especificación de Redacción de Blueprints — convenciones completas para leer y escribir documentos Blueprint |
| [start-work-order.md](start-work-order.md) | Guía de la fase de inicio — flujo de recopilación de contexto antes de implementar |
| [complete-work-order.md](complete-work-order.md) | Guía de la fase de finalización — verificación, llamada de completado y flujo de traspaso |
| [writing-implementation-plans.md](writing-implementation-plans.md) | Guía para escribir planes de implementación — estructura, ejecución en paralelo y actualización |
| [scripts/init-wo-execution.sh](scripts/init-wo-execution.sh) | Script para inicializar un directorio de ejecución de orden de trabajo |
| [scripts/checklist-template.md](scripts/checklist-template.md) | Plantilla de checklist de ejecución — registra el progreso a través de todas las fases |
| [scripts/context-template.md](scripts/context-template.md) | Plantilla de contexto de la orden de trabajo — IDs, resumen de la solicitud del usuario, referencias a documentos de requisitos/blueprint vinculados y URL del PR |
| [scripts/implementation-plan-template.md](scripts/implementation-plan-template.md) | Plantilla de plan de implementación — plan estructurado escrito después de la recopilación de contexto |
| [scripts/review-log-template.md](scripts/review-log-template.md) | Plantilla de log de revisión — hallazgos de revisión de múltiples rondas escritos por agentes de revisión |
