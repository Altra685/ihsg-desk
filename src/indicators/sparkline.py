"""Tiny SVG sparklines — pure, no deps."""
from __future__ import annotations

from typing import Sequence


def svg_sparkline(
    values: Sequence[float],
    width: int = 96,
    height: int = 28,
    stroke: str = "#d4a574",
) -> str:
    nums = [float(v) for v in values if v is not None]
    if len(nums) < 2:
        return ""
    lo, hi = min(nums), max(nums)
    span = (hi - lo) or 1.0
    n = len(nums)
    pts = []
    for i, v in enumerate(nums):
        x = 0 if n == 1 else i * (width - 2) / (n - 1) + 1
        y = height - 2 - ((v - lo) / span) * (height - 4)
        pts.append(f"{x:.1f},{y:.1f}")
    poly = " ".join(pts)
    up = nums[-1] >= nums[0]
    color = "#6bcb8f" if up else "#e07a7a"
    if stroke:
        color = stroke if up else "#e07a7a"
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<polyline fill="none" stroke="{color}" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{poly}"/>'
        f"</svg>"
    )


def closes_from_rows(rows: Sequence[dict], n: int = 24) -> list[float]:
    closes = [float(r["close"]) for r in rows if r.get("close") is not None]
    return closes[-n:] if closes else []
