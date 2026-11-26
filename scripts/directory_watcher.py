#!/usr/bin/env python3
"""Monitor de integridade de arquivos via SHA-256 para ./sandbox_files.

Calcula hashes SHA-256 dos arquivos no diretorio de laboratorio e emite um
alerta de auditoria caso detecte modificacoes rapidas em lote dentro de uma
janela configuravel de tempo.
"""

import argparse
import hashlib
import os
import sys
import time
from collections import deque

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANDBOX_DIR = os.path.join(BASE_DIR, "sandbox_files")


def calculate_sha256(filepath: str) -> str:
    """Calcula o hash SHA-256 de um arquivo em blocos."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def snapshot_directory(target_dir: str) -> dict[str, str]:
    """Gera um mapa {caminho_relativo: sha256} para os arquivos do diretorio."""
    snapshot: dict[str, str] = {}
    if not os.path.isdir(target_dir):
        return snapshot

    for root, _, filenames in os.walk(target_dir):
        for filename in sorted(filenames):
            full_path = os.path.join(root, filename)
            if os.path.islink(full_path) or not os.path.isfile(full_path):
                continue
            rel_path = os.path.relpath(full_path, target_dir)
            try:
                snapshot[rel_path] = calculate_sha256(full_path)
            except OSError as exc:
                print(f"[AVISO] Nao foi possivel ler {rel_path}: {exc}")
    return snapshot


def format_timestamp() -> str:
    """Retorna o horario atual formatado para logs de auditoria."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def watch_directory(
    target_dir: str,
    interval: float = 1.0,
    window_seconds: float = 10.0,
    batch_threshold: int = 2,
    duration: float = 0.0,
) -> None:
    """Monitora continuamente o diretorio e alerta sobre alteracoes em lote."""
    if not os.path.isdir(target_dir):
        print(f"[ERRO] Diretorio monitorado nao encontrado: {target_dir}")
        sys.exit(1)

    baseline = snapshot_directory(target_dir)
    recent_events: deque[tuple[float, str, str]] = deque()
    start_time = time.monotonic()

    print(f"[{format_timestamp()}] Iniciando monitoramento de integridade em: {target_dir}")
    print(
        f"[CONFIG] Intervalo: {interval:.1f}s | Janela: {window_seconds:.1f}s | "
        f"Limiar de alerta em lote: {batch_threshold} eventos"
    )
    print(f"[BASELINE] {len(baseline)} arquivo(s) catalogado(s):")
    for rel_path, digest in baseline.items():
        print(f"  - {rel_path}: {digest}")
    print("Pressione Ctrl+C para encerrar.\n")

    try:
        while True:
            time.sleep(interval)
            now = time.monotonic()
            current = snapshot_directory(target_dir)

            cycle_events: list[tuple[str, str]] = []

            for rel_path, digest in current.items():
                if rel_path not in baseline:
                    cycle_events.append(("CRIADO", rel_path))
                    print(
                        f"[{format_timestamp()}] [INFO] Arquivo criado: {rel_path} "
                        f"(SHA-256: {digest[:16]}...)"
                    )
                elif baseline[rel_path] != digest:
                    cycle_events.append(("MODIFICADO", rel_path))
                    print(
                        f"[{format_timestamp()}] [INFO] Arquivo modificado: {rel_path} "
                        f"({baseline[rel_path][:12]}... -> {digest[:12]}...)"
                    )

            for rel_path in baseline:
                if rel_path not in current:
                    cycle_events.append(("REMOVIDO", rel_path))
                    print(f"[{format_timestamp()}] [INFO] Arquivo removido: {rel_path}")

            for event_type, rel_path in cycle_events:
                recent_events.append((now, event_type, rel_path))

            # Remove eventos fora da janela deslizante
            while recent_events and (now - recent_events[0][0]) > window_seconds:
                recent_events.popleft()

            if cycle_events and len(recent_events) >= batch_threshold:
                affected_files = sorted({item[2] for item in recent_events})
                print(
                    f"\n[{format_timestamp()}] [ALERTA DE AUDITORIA] "
                    f"Detectadas {len(recent_events)} alteracoes rapidas em lote "
                    f"nos ultimos {window_seconds:.1f}s!"
                )
                print(f"  Arquivos afetados: {', '.join(affected_files)}")
                print(
                    "  Acao recomendada: verificar processo responsavel, validar hashes "
                    "e consultar docs/SECURITY_GUIDELINES.md.\n"
                )

            baseline = current

            if duration > 0 and (now - start_time) >= duration:
                print(f"[{format_timestamp()}] Tempo de monitoramento concluido ({duration:.1f}s).")
                break
    except KeyboardInterrupt:
        print(f"\n[{format_timestamp()}] Monitoramento encerrado pelo usuario.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitora hashes SHA-256 dos arquivos em ./sandbox_files."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Intervalo entre verificacoes em segundos (padrao: 1.0).",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=10.0,
        help="Janela deslizante em segundos para deteccao de lote (padrao: 10.0).",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=2,
        help="Quantidade minima de alteracoes na janela para disparar alerta (padrao: 2).",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Tempo maximo de execucao em segundos (0 = continuo).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    watch_directory(
        target_dir=SANDBOX_DIR,
        interval=args.interval,
        window_seconds=args.window,
        batch_threshold=args.threshold,
        duration=args.duration,
    )


if __name__ == "__main__":
    main()
