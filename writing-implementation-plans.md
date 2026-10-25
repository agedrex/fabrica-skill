# Escribir Planes de Implementación

Escribí el plan de implementación inmediatamente después de la Fase 1 (recopilación de contexto). El blueprint ya define la arquitectura de componentes: el plan de implementación completa los detalles sintácticos y específicos del lenguaje que sostienen esa arquitectura.

## Qué incluir

1. **Estructura de archivos y paquetes** — listá cada archivo que vas a crear o modificar y dónde vive. Seguí la guía de división de código y estructura de paquetes de `.cursor/skills/review/architecture-and-conventions.md` (esto se verificará durante la revisión).

2. **Firmas de componentes y métodos** — definí las interfaces públicas antes de escribir los cuerpos. Para cada nueva clase, servicio, hook o componente, escribí la firma (nombre, parámetros, tipo de retorno). Esto fija a nivel de código los límites de contrato del blueprint.

3. **Flujo de control** — describí la cadena de llamadas: qué componente llama a cuál, en qué orden y con qué datos. Es la prosa de los párrafos de relaciones del blueprint traducida a llamadas concretas de funciones.

4. **Pasos** — dividí el trabajo en pasos ordenados. Cada paso debe producir un estado intermedio que compile. Indicá qué pasos pueden correr en paralelo (tocan archivos distintos, sin dependencia entre ellos).

## Mantenerlo actualizado

Si la implementación revela que el plan debe cambiar, actualizá el plan antes de continuar. El plan y la implementación deben mantenerse sincronizados.
