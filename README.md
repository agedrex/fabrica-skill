# Fábrica Skill

La skill `agedrex-factory`: el método de trabajo de La Fábrica (Etapas → FRD → Blueprint → Work
Order) y la ejecución repetible de Work Orders por MCP. Incluye guías, plantillas, agentes de
ejecución y revisión, y el hook que registra el run de cada subagente.

## Instalación

```bash
npx skills add agedrex/fabrica-skill --skill agedrex-factory
```

En Claude Code también se puede instalar como plugin:

```text
/plugin marketplace add agedrex/fabrica-skill
/plugin install fabrica@agedrex
```

## Conexión al MCP

El plugin declara el servidor MCP en `.mcp.json` sin ningún secreto. Antes de abrir el cliente,
definí en tu entorno (nunca en un archivo versionado):

| Variable | Contenido |
|---|---|
| `LA_FABRICA_MCP_URL` | URL del MCP de tu despliegue, terminada en `/mcp/` |
| `LA_FABRICA_MCP_TOKEN` | Tu token personal de La Fábrica |

Codex no expande variables dentro de `.mcp.json`: configurá el servidor con
`bearer_token_env_var = "LA_FABRICA_MCP_TOKEN"` en su `config.toml`.

## Estructura

```text
skills/agedrex-factory/
  SKILL.md        entrada del método
  guides/         cómo escribir FRDs, Blueprints y Work Orders
  templates/      plantillas de FRD, Blueprint y WO
  execution/      ejecución de un WO: plan, checklist, review, dossier, registro de runs
  agents/         ejecutores (fácil, medio, difícil) y revisor
  hooks/          registrar_run.py, el hook de registro de runs
  references/     material de apoyo
```

## Licencia

MIT. Parte del método parte de [8090 Software Factory](https://github.com/8090-inc/software-factory-plugin)
(MIT, © 2026 8090 Solutions Inc.); se conserva su aviso de copyright.
