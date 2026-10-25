#!/usr/bin/env bash
set -euo pipefail

print_usage() {
  echo "Uso:"
  echo "  bash .cursor/skills/software-factory/scripts/init-wo-execution.sh \\"
  echo "    --work-order-number <number> --work-order-title \"<title>\""
  echo
  echo "Crea: scratch/wo-execution/WO-<number>/"
  echo "  - checklist.md            Checklist de ejecución (completar progresivamente)"
  echo "  - context.md              Metadatos de la orden de trabajo, enlaces y contexto de entrega"
  echo "  - review-log.md           Log de revisión (escrito por los agentes de revisión)"
  echo "  - implementation-plan.md  Plan de implementación (escrito después de recopilar contexto)"
  echo
  echo "Seguridad:"
  echo "  Falla si los archivos de destino ya existen, para evitar sobrescrituras accidentales."
}

escape_sed_replacement() {
  printf '%s' "$1" | sed -e 's/[\\/&]/\\&/g'
}

WORK_ORDER_NUMBER=""
WORK_ORDER_TITLE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --work-order-number)
      WORK_ORDER_NUMBER="${2:-}"
      shift 2
      ;;
    --work-order-title)
      WORK_ORDER_TITLE="${2:-}"
      shift 2
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Argumento desconocido: $1" >&2
      print_usage
      exit 1
      ;;
  esac
done

if [[ -z "$WORK_ORDER_NUMBER" || -z "$WORK_ORDER_TITLE" ]]; then
  echo "Error: --work-order-number y --work-order-title son obligatorios." >&2
  print_usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TEMPLATES=(
  "$SCRIPT_DIR/checklist-template.md:checklist.md"
  "$SCRIPT_DIR/context-template.md:context.md"
  "$SCRIPT_DIR/review-log-template.md:review-log.md"
  "$SCRIPT_DIR/implementation-plan-template.md:implementation-plan.md"
)

for entry in "${TEMPLATES[@]}"; do
  template="${entry%%:*}"
  if [[ ! -f "$template" ]]; then
    echo "Error: no se encontró la plantilla en $template" >&2
    exit 1
  fi
done

OUTPUT_DIR="scratch/wo-execution/WO-${WORK_ORDER_NUMBER}"
mkdir -p "$OUTPUT_DIR"

INITIALIZED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

NUMBER_ESCAPED="$(escape_sed_replacement "$WORK_ORDER_NUMBER")"
TITLE_ESCAPED="$(escape_sed_replacement "$WORK_ORDER_TITLE")"
TIMESTAMP_ESCAPED="$(escape_sed_replacement "$INITIALIZED_AT")"

apply_substitutions() {
  sed \
    -e "s/__WORK_ORDER_NUMBER__/${NUMBER_ESCAPED}/g" \
    -e "s/__WORK_ORDER_TITLE__/${TITLE_ESCAPED}/g" \
    -e "s/__INITIALIZED_AT__/${TIMESTAMP_ESCAPED}/g" \
    "$1" > "$2"
}

for entry in "${TEMPLATES[@]}"; do
  output_name="${entry##*:}"
  if [[ -e "$OUTPUT_DIR/$output_name" ]]; then
    echo "Error: $OUTPUT_DIR/$output_name ya existe." >&2
    echo "Se rechaza sobrescribir artefactos de ejecución existentes." >&2
    echo "Retomá desde los archivos existentes o eliminalos intencionalmente antes de volver a ejecutar init." >&2
    exit 1
  fi
done

echo "Directorio de la orden de trabajo inicializado: $OUTPUT_DIR/"
for entry in "${TEMPLATES[@]}"; do
  template="${entry%%:*}"
  output_name="${entry##*:}"
  apply_substitutions "$template" "$OUTPUT_DIR/$output_name"
  echo "  - $output_name"
done
