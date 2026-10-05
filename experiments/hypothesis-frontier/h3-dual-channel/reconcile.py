"""Small H3 dual-channel reconciliation probe.

The probe accepts already-sanitized observations from the hook and transcript
channels. It deliberately does not parse live runtime files or retain fields
outside the small allowlist below.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping


class Channel(str, Enum):
    HOOK = "hook"
    TRANSCRIPT = "transcript"


class ReconciliationState(str, Enum):
    HOOK_OBSERVED = "HOOK_OBSERVED"
    TRANSCRIPT_OBSERVED = "TRANSCRIPT_OBSERVED"
    CORRELATED = "CORRELATED"
    HOOK_ONLY = "HOOK_ONLY"
    TRANSCRIPT_ONLY = "TRANSCRIPT_ONLY"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class SanitizedEvent:
    """Allowlisted, sanitized event fields used by the probe."""

    source: Channel
    event_id: str | None = None
    provider_event_id: str | None = None
    provider: str | None = None
    run_id: str | None = None
    agent_id: str | None = None
    kind: str | None = None
    tool_name: str | None = None
    value: Any = None
    observed_at: str | None = None

    @property
    def identity_aliases(self) -> frozenset[str]:
        aliases: set[str] = set()
        if self.event_id:
            aliases.add(f"event_id:{self.event_id}")
        if self.provider_event_id:
            aliases.add(f"provider_event_id:{self.provider_event_id}")
        return frozenset(aliases)

    @property
    def primary_identity(self) -> str | None:
        aliases = sorted(self.identity_aliases)
        return aliases[0] if aliases else None

    @property
    def semantic_payload(self) -> tuple[Any, ...]:
        """Return comparable content without source, identity, or timestamps."""

        return (
            self.run_id,
            self.agent_id,
            self.kind,
            self.tool_name,
            _freeze(self.value),
        )


@dataclass(frozen=True)
class ReconciliationRecord:
    """One retained observation or correlated pair."""

    states: tuple[ReconciliationState, ...]
    terminal_state: ReconciliationState
    hook: SanitizedEvent | None
    transcript: SanitizedEvent | None
    correlation_key: str | None
    reason: str


_ALLOWED_FIELDS = frozenset(
    {
        "event_id",
        "provider_event_id",
        "provider",
        "run_id",
        "agent_id",
        "kind",
        "tool_name",
        "value",
        "observed_at",
    }
)


def normalize_event(raw: Mapping[str, Any], source: Channel) -> SanitizedEvent:
    """Create an event from sanitized, allowlisted fixture fields only."""

    unknown_fields = set(raw) - _ALLOWED_FIELDS
    if unknown_fields:
        raise ValueError(f"unsupported event fields: {sorted(unknown_fields)}")

    return SanitizedEvent(
        source=source,
        event_id=_optional_string(raw.get("event_id")),
        provider_event_id=_optional_string(raw.get("provider_event_id")),
        provider=_optional_string(raw.get("provider")),
        run_id=_optional_string(raw.get("run_id")),
        agent_id=_optional_string(raw.get("agent_id")),
        kind=_optional_string(raw.get("kind")),
        tool_name=_optional_string(raw.get("tool_name")),
        value=raw.get("value"),
        observed_at=_optional_string(raw.get("observed_at")),
    )


def reconcile(
    hook_events: Iterable[Mapping[str, Any]],
    transcript_events: Iterable[Mapping[str, Any]],
) -> list[ReconciliationRecord]:
    """Reconcile sanitized hook and transcript fixtures.

    Stable event/provider identifiers are the only cross-channel correlation
    keys. Timestamps are retained for inspection but never participate in
    matching or deduplication.
    """

    hooks = _deduplicate(
        normalize_event(raw, Channel.HOOK) for raw in hook_events
    )
    transcripts = _deduplicate(
        normalize_event(raw, Channel.TRANSCRIPT) for raw in transcript_events
    )

    remaining_transcripts = list(transcripts)
    records: list[ReconciliationRecord] = []

    for hook in hooks:
        candidates = [
            transcript
            for transcript in remaining_transcripts
            if _can_correlate(hook, transcript)
        ]

        if not candidates:
            records.append(
                ReconciliationRecord(
                    states=(
                        ReconciliationState.HOOK_OBSERVED,
                        ReconciliationState.HOOK_ONLY,
                    ),
                    terminal_state=ReconciliationState.HOOK_ONLY,
                    hook=hook,
                    transcript=None,
                    correlation_key=hook.primary_identity,
                    reason="no matching transcript identity",
                )
            )
            continue

        transcript = candidates[0]
        remaining_transcripts.remove(transcript)
        identity_conflict = not _identifiers_agree(hook, transcript)
        payload_conflict = hook.semantic_payload != transcript.semantic_payload
        terminal_state = (
            ReconciliationState.CONFLICT
            if identity_conflict or payload_conflict
            else ReconciliationState.CORRELATED
        )
        reason = (
            "stable identity matched but observations disagree"
            if terminal_state is ReconciliationState.CONFLICT
            else "stable identity matched"
        )
        records.append(
            ReconciliationRecord(
                states=(
                    ReconciliationState.HOOK_OBSERVED,
                    ReconciliationState.TRANSCRIPT_OBSERVED,
                    terminal_state,
                ),
                terminal_state=terminal_state,
                hook=hook,
                transcript=transcript,
                correlation_key=_shared_identity(hook, transcript),
                reason=reason,
            )
        )

    for transcript in remaining_transcripts:
        records.append(
            ReconciliationRecord(
                states=(
                    ReconciliationState.TRANSCRIPT_OBSERVED,
                    ReconciliationState.TRANSCRIPT_ONLY,
                ),
                terminal_state=ReconciliationState.TRANSCRIPT_ONLY,
                hook=None,
                transcript=transcript,
                correlation_key=transcript.primary_identity,
                reason="no matching hook identity",
            )
        )

    return records


def _deduplicate(events: Iterable[SanitizedEvent]) -> list[SanitizedEvent]:
    """Collapse repeated same-channel observations with the same stable ID."""

    retained: list[SanitizedEvent] = []
    seen: set[tuple[frozenset[str], tuple[Any, ...]]] = set()
    for event in events:
        if not event.identity_aliases:
            retained.append(event)
            continue
        fingerprint = (event.identity_aliases, event.semantic_payload)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        retained.append(event)
    return retained


def _can_correlate(left: SanitizedEvent, right: SanitizedEvent) -> bool:
    return bool(left.identity_aliases & right.identity_aliases)


def _shared_identity(left: SanitizedEvent, right: SanitizedEvent) -> str | None:
    shared = sorted(left.identity_aliases & right.identity_aliases)
    return shared[0] if shared else None


def _identifiers_agree(left: SanitizedEvent, right: SanitizedEvent) -> bool:
    if left.event_id and right.event_id and left.event_id != right.event_id:
        return False
    if (
        left.provider_event_id
        and right.provider_event_id
        and (
            left.provider_event_id != right.provider_event_id
            or (
                left.provider
                and right.provider
                and left.provider != right.provider
            )
        )
    ):
        return False
    return True


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("identity and metadata fields must be strings")
    value = value.strip()
    return value or None


def _freeze(value: Any) -> Any:
    """Make sanitized JSON-like fixture values comparable and deterministic."""

    if isinstance(value, Mapping):
        return tuple(sorted((str(key), _freeze(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise ValueError("value must contain only JSON-like sanitized data")
