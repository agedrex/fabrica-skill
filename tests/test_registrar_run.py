"""Tests del hook `skills/agedrex-factory/hooks/registrar_run.py` (WO-33).

Es un script fuera de `app/`, de la biblioteca estándar, así que se importa por ruta con
`importlib` en vez de como paquete. Solo prueba las funciones puras: no pega contra la red ni
contra el disco real del usuario (el único I/O que toca es `leer_transcript` sobre un archivo
temporal que el propio test escribe).
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

HOOK_PATH = (
    Path(__file__).resolve().parents[1] / "skills" / "agedrex-factory" / "hooks" / "registrar_run.py"
)

_spec = importlib.util.spec_from_file_location("registrar_run", HOOK_PATH)
assert _spec is not None and _spec.loader is not None
registrar_run = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = registrar_run
_spec.loader.exec_module(registrar_run)


def _assistant(
    message_id: str,
    *,
    output_tokens: int,
    timestamp: str,
    input_tokens: int = 0,
    cache_read: int | None = None,
    cache_creation: int | None = None,
    model: str = "claude-sonnet-4-5",
) -> dict:
    """Una línea `assistant` del transcript. Los campos de caché son opcionales (`.get(clave, 0)`)."""
    usage = {"input_tokens": input_tokens, "output_tokens": output_tokens}
    if cache_read is not None:
        usage["cache_read_input_tokens"] = cache_read
    if cache_creation is not None:
        usage["cache_creation_input_tokens"] = cache_creation
    return {
        "type": "assistant",
        "timestamp": timestamp,
        "message": {"id": message_id, "model": model, "usage": usage},
    }


def _user(texto_o_bloques, *, timestamp: str = "2026-09-09T10:00:00.000Z") -> dict:
    return {"type": "user", "timestamp": timestamp, "message": {"content": texto_o_bloques}}


# --------------------------------------------------------------------------------------
# resumir_uso: la deduplicación por message.id es EL punto crítico del WO.
# --------------------------------------------------------------------------------------


def test_resumir_uso_dedupe_por_message_id_se_queda_con_la_ultima_linea():
    """Un mismo `message.id` en 3 líneas (output_tokens 2 → 180 → 360) cuenta 360 una sola vez.

    Si se sumaran las tres líneas en vez de deduplicar, el output total daría 2 + 180 + 360 = 542
    en vez de 360. Este es el escenario que el WO marca como "hay que testear sí o sí".
    """
    eventos = [
        _user("Ejecutá WO-31 del proyecto factory", timestamp="2026-09-09T10:00:00.000Z"),
        _assistant(
            "msg_1", output_tokens=2, input_tokens=5, timestamp="2026-09-09T10:00:01.000Z"
        ),
        _assistant(
            "msg_1", output_tokens=180, input_tokens=5, timestamp="2026-09-09T10:00:02.000Z"
        ),
        _assistant(
            "msg_1",
            output_tokens=360,
            input_tokens=5,
            cache_read=100,
            cache_creation=20,
            timestamp="2026-09-09T10:00:03.000Z",
        ),
    ]

    resumen = registrar_run.resumir_uso(eventos)

    assert resumen["tokens_output"] == 360
    assert resumen["tokens_input"] == 5
    assert resumen["tokens_cache_read"] == 100
    assert resumen["tokens_cache_creation"] == 20


def test_resumir_uso_suma_las_ultimas_lineas_de_cada_message_id_distinto():
    """Dos `message.id` distintos: cada uno aporta su ÚLTIMA línea, y se suman entre sí."""
    eventos = [
        _user("Ejecutá WO-31 del proyecto factory"),
        _assistant("msg_1", output_tokens=2, input_tokens=10, timestamp="2026-09-09T10:00:01.000Z"),
        _assistant(
            "msg_1",
            output_tokens=360,
            input_tokens=10,
            cache_read=100,
            timestamp="2026-09-09T10:00:02.000Z",
        ),
        _assistant(
            "msg_2",
            output_tokens=50,
            input_tokens=8,
            cache_creation=30,
            timestamp="2026-09-09T10:00:05.500Z",
            model="claude-haiku-4-5",
        ),
    ]

    resumen = registrar_run.resumir_uso(eventos)

    assert resumen["tokens_output"] == 360 + 50
    assert resumen["tokens_input"] == 10 + 8
    assert resumen["tokens_cache_read"] == 100
    assert resumen["tokens_cache_creation"] == 30


def test_resumir_uso_duracion_es_diferencia_entre_primer_y_ultimo_timestamp():
    eventos = [
        _user("Ejecutá WO-31 del proyecto factory", timestamp="2026-09-09T10:00:00.000Z"),
        _assistant("msg_1", output_tokens=2, timestamp="2026-09-09T10:00:01.500Z"),
        _assistant("msg_1", output_tokens=360, timestamp="2026-09-09T10:00:12.750Z"),
    ]

    resumen = registrar_run.resumir_uso(eventos)

    assert resumen["duration_seconds"] == pytest.approx(12.75)
    assert resumen["started_at"] == "2026-09-09T10:00:00.000Z"
    assert resumen["ended_at"] == "2026-09-09T10:00:12.750Z"


def test_resumir_uso_model_es_el_de_la_ultima_linea_assistant():
    eventos = [
        _user("Ejecutá WO-31 del proyecto factory"),
        _assistant(
            "msg_1",
            output_tokens=2,
            timestamp="2026-09-09T10:00:01.000Z",
            model="claude-haiku-4-5",
        ),
        _assistant(
            "msg_2",
            output_tokens=50,
            timestamp="2026-09-09T10:00:02.000Z",
            model="claude-sonnet-4-5",
        ),
    ]

    resumen = registrar_run.resumir_uso(eventos)

    assert resumen["model"] == "claude-sonnet-4-5"


# --------------------------------------------------------------------------------------
# detectar_wo
# --------------------------------------------------------------------------------------


def test_detectar_wo_en_string():
    eventos = [_user("Ejecutá WO-31 del proyecto factory")]
    assert registrar_run.detectar_wo(eventos) == "WO-31"


def test_detectar_wo_en_lista_de_bloques():
    eventos = [
        _user(
            [
                {"type": "text", "text": "Ejecutá "},
                {"type": "text", "text": "WO-83 del proyecto factory"},
            ]
        )
    ]
    assert registrar_run.detectar_wo(eventos) == "WO-83"


def test_detectar_wo_sin_match_devuelve_none():
    eventos = [_user("Revisá el estado del proyecto, no hay ningún ticket puntual")]
    assert registrar_run.detectar_wo(eventos) is None


def test_detectar_wo_solo_mira_el_primer_mensaje_user():
    eventos = [
        _user("Sin ticket acá"),
        _user("Este después sí menciona WO-99, pero ya no cuenta"),
    ]
    assert registrar_run.detectar_wo(eventos) is None


def test_detectar_wo_no_se_engancha_con_el_wo_83_de_ejemplo_de_las_reglas_de_la_casa():
    """Bug real: el prompt de todo ejecutor abre con las reglas duras, que mencionan `WO-83`
    como EJEMPLO de referencia legible mucho antes de decir cuál WO ejecutar. Un patrón que
    tomara el primer `WO-\\d+` suelto del mensaje le atribuiría todo run a WO-83 en vez del WO
    real. Con las reglas de detección nuevas (marcador o mención explícita), tiene que ganar
    WO-27."""
    texto = (
        "Reglas duras (no negociables):\n"
        "- Referencias legibles (`WO-83`, `FRD-X`, `F3`, `E1`) en toda superficie pública; "
        "nunca UUIDs.\n\n"
        "Ejecutá WO-27: arreglá el bug de la carrera en record_run."
    )
    eventos = [_user(texto)]
    assert registrar_run.detectar_wo(eventos) == "WO-27"


def test_detectar_wo_prioriza_el_marcador_explicito_sobre_cualquier_mencion():
    texto = (
        "Reglas duras: Referencias legibles (`WO-83`, `FRD-X`) en toda superficie pública.\n"
        "[wo: WO-40] Ejecutá el WO que corresponda a esta ronda."
    )
    eventos = [_user(texto)]
    assert registrar_run.detectar_wo(eventos) == "WO-40"


def test_detectar_wo_sin_marcador_ni_mencion_no_adivina_con_un_wo_suelto():
    """Sin marcador y sin `Ejecutá/ejecución de/ejecutor de`, un `WO-\\d+` mencionado de pasada
    (por ejemplo, en las reglas de la casa) NO cuenta como el WO del run."""
    texto = "Reglas duras: Referencias legibles (`WO-83`, `FRD-X`, `F3`, `E1`) en toda superficie."
    eventos = [_user(texto)]
    assert registrar_run.detectar_wo(eventos) is None


# --------------------------------------------------------------------------------------
# rol_de
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("agent_type", "esperado"),
    [
        ("wo-reviewer", "reviewer"),
        ("wo-executor-hard", "executor"),
        ("wo-executor-easy", "executor"),
        ("general-purpose", "other"),
        (None, "other"),
    ],
)
def test_rol_de(agent_type, esperado):
    assert registrar_run.rol_de(agent_type) == esperado


# --------------------------------------------------------------------------------------
# leer_transcript: una línea corrupta no aborta el archivo.
# --------------------------------------------------------------------------------------


def test_leer_transcript_saltea_lineas_corruptas(tmp_path):
    archivo = tmp_path / "agent-muestra.jsonl"
    archivo.write_text(
        "\n".join(
            [
                '{"type": "user", "timestamp": "2026-09-09T10:00:00.000Z", '
                '"message": {"content": "Ejecutá WO-31 del proyecto factory"}}',
                "{esto no es json valido",
                '{"type": "assistant", "timestamp": "2026-09-09T10:00:01.000Z", '
                '"message": {"id": "msg_1", "model": "claude-sonnet-4-5", '
                '"usage": {"input_tokens": 5, "output_tokens": 2}}}',
            ]
        ),
        encoding="utf-8",
    )

    eventos = registrar_run.leer_transcript(archivo)

    assert len(eventos) == 2
    assert registrar_run.detectar_wo(eventos) == "WO-31"


# --------------------------------------------------------------------------------------
# armar_payload
# --------------------------------------------------------------------------------------


def test_armar_payload_trae_los_campos_del_contrato():
    resumen = {
        "tokens_input": 42,
        "tokens_output": 360,
        "tokens_cache_read": 148_947,
        "tokens_cache_creation": 0,
        "duration_seconds": 134.55,
        "model": "claude-sonnet-4-5",
        "started_at": "2026-09-09T10:00:00.000Z",
        "ended_at": "2026-09-09T10:02:14.550Z",
    }

    payload = registrar_run.armar_payload(
        resumen,
        role="executor",
        agent_type="wo-executor-medium",
        agent_id="ad1526f09e36ee82d",
        session_id="619fbb97-ef7e-4091-9bea-817c2df8470b",
    )

    assert payload["source"] == "hook"
    assert payload["role"] == "executor"
    assert payload["tokens_input"] == 42
    assert payload["tokens_output"] == 360
    assert payload["tokens_cache_read"] == 148_947
    assert payload["tokens_cache_creation"] == 0
    assert payload["duration_seconds"] == 134.55
    assert payload["model"] == "claude-sonnet-4-5"
    assert payload["agent_type"] == "wo-executor-medium"
    assert payload["agent_id"] == "ad1526f09e36ee82d"
    assert payload["session_id"] == "619fbb97-ef7e-4091-9bea-817c2df8470b"
    assert payload["started_at"] == "2026-09-09T10:00:00.000Z"
    assert payload["ended_at"] == "2026-09-09T10:02:14.550Z"


# --------------------------------------------------------------------------------------
# resolver_transcript_subagente y obtener_proyecto: I/O de disco/entorno, sin red.
# --------------------------------------------------------------------------------------


def test_resolver_transcript_subagente_con_agent_id(tmp_path):
    slug_dir = tmp_path / "slug"
    subagents_dir = slug_dir / "sess-1" / "subagents"
    subagents_dir.mkdir(parents=True)
    esperado = subagents_dir / "agent-abc123.jsonl"
    esperado.write_text("{}\n", encoding="utf-8")

    payload = {
        "transcript_path": str(slug_dir / "sess-1.jsonl"),
        "session_id": "sess-1",
        "agent_id": "abc123",
    }

    assert registrar_run.resolver_transcript_subagente(payload) == esperado


def test_resolver_transcript_subagente_sin_agent_id_no_adivina(tmp_path):
    """Regla nueva: sin `agent_id` NO se elige el `agent-*.jsonl` más reciente por `mtime` — con
    varios subagentes en paralelo ese archivo puede ser el de OTRO work order."""
    slug_dir = tmp_path / "slug"
    subagents_dir = slug_dir / "sess-1" / "subagents"
    subagents_dir.mkdir(parents=True)
    (subagents_dir / "agent-de-otro-wo.jsonl").write_text("{}\n", encoding="utf-8")

    payload = {"transcript_path": str(slug_dir / "sess-1.jsonl"), "session_id": "sess-1"}

    assert registrar_run.resolver_transcript_subagente(payload) is None


def test_resolver_transcript_subagente_sin_carpeta_devuelve_none(tmp_path):
    payload = {"transcript_path": str(tmp_path / "sess-x.jsonl"), "session_id": "sess-x"}
    assert registrar_run.resolver_transcript_subagente(payload) is None


def test_obtener_proyecto_prioriza_env(monkeypatch):
    monkeypatch.setenv("FACTORY_PROJECT", "factory")
    assert registrar_run.obtener_proyecto({"cwd": "/no/existe"}) == "factory"


def test_obtener_proyecto_lee_factory_json_si_no_hay_env(tmp_path, monkeypatch):
    monkeypatch.delenv("FACTORY_PROJECT", raising=False)
    (tmp_path / ".factory.json").write_text('{"project": "factory"}', encoding="utf-8")
    assert registrar_run.obtener_proyecto({"cwd": str(tmp_path)}) == "factory"


def test_obtener_proyecto_sin_env_ni_archivo_devuelve_none(tmp_path, monkeypatch):
    monkeypatch.delenv("FACTORY_PROJECT", raising=False)
    assert registrar_run.obtener_proyecto({"cwd": str(tmp_path)}) is None


# --------------------------------------------------------------------------------------
# resumir_uso: la duración nunca es negativa, aunque los timestamps vengan desordenados.
# --------------------------------------------------------------------------------------


def test_resumir_uso_duracion_nunca_negativa_con_timestamps_desordenados():
    eventos = [
        _user("Ejecutá WO-31 del proyecto factory", timestamp="2026-09-09T10:00:10.000Z"),
        _assistant("msg_1", output_tokens=2, timestamp="2026-09-09T10:00:05.000Z"),
    ]
    resumen = registrar_run.resumir_uso(eventos)
    assert resumen["duration_seconds"] == 0.0
    assert resumen["duration_seconds"] >= 0


# --------------------------------------------------------------------------------------
# main(): el flujo completo, con stdin/entorno monkeypatcheados y sin red real.
# --------------------------------------------------------------------------------------


def _correr_main(monkeypatch, tmp_path, payload: dict, *, enviar_run=None):
    """Corre `main()` con el payload dado por stdin y devuelve el contenido del log."""
    log_path = tmp_path / "factory-runs.log"
    monkeypatch.setenv("FACTORY_RUNS_LOG", str(log_path))
    monkeypatch.setenv("FACTORY_PROJECT", "factory")
    monkeypatch.setenv("FACTORY_URL", "http://localhost:8000")
    monkeypatch.setenv("FACTORY_TOKEN", "un-token")
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    if enviar_run is not None:
        monkeypatch.setattr(registrar_run, "enviar_run", enviar_run)

    registrar_run.main()

    return log_path.read_text(encoding="utf-8") if log_path.exists() else ""


def test_main_sin_agent_id_no_adivina_el_transcript_de_otro_subagente(tmp_path, monkeypatch):
    """Bug real de WO-33: con varios subagentes corriendo en paralelo, sin `agent_id` el hook
    viejo tomaba el `agent-*.jsonl` más reciente por `mtime` — que bien puede ser el de OTRO work
    order. La regla nueva: sin `agent_id` no se adivina, se loguea y no se manda nada. Antes del
    fix, este payload (sin `agent_id`, con un transcript de OTRO subagente ya en disco) hacía que
    el hook leyera ESE transcript, detectara `WO-99` y llamara a `enviar_run` igual."""
    subagents_dir = tmp_path / "sess-1" / "subagents"
    subagents_dir.mkdir(parents=True)
    (subagents_dir / "agent-de-otro-wo.jsonl").write_text(
        '{"type": "user", "timestamp": "2026-09-09T10:00:00.000Z", '
        '"message": {"content": "Ejecutá WO-99 del proyecto factory"}}\n'
        '{"type": "assistant", "timestamp": "2026-09-09T10:00:01.000Z", '
        '"message": {"id": "msg_1", "model": "claude-sonnet-4-5", '
        '"usage": {"input_tokens": 5, "output_tokens": 2}}}\n',
        encoding="utf-8",
    )

    llamadas = []
    contenido = _correr_main(
        monkeypatch,
        tmp_path,
        {"transcript_path": str(tmp_path / "sess-1.jsonl"), "session_id": "sess-1"},
        enviar_run=lambda *a, **k: (llamadas.append((a, k)), (True, "HTTP 201"))[1],
    )

    assert llamadas == [], "sin agent_id, el hook no puede adivinar de qué WO es este run"
    assert "sin agent_id: no se registra" in contenido


def test_main_con_agent_id_pero_sin_transcript_no_llama_a_enviar_run(tmp_path, monkeypatch):
    llamadas = []
    contenido = _correr_main(
        monkeypatch,
        tmp_path,
        {
            "transcript_path": str(tmp_path / "sess-1.jsonl"),
            "session_id": "sess-1",
            "agent_id": "abc123",
        },
        enviar_run=lambda *a, **k: (llamadas.append((a, k)), (True, "HTTP 201"))[1],
    )

    assert llamadas == []
    assert "no se encontró el transcript" in contenido
