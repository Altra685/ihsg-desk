from __future__ import annotations

from typing import Sequence


def _closes(rows: Sequence[dict]) -> list[float]:
    out: list[float] = []
    for r in rows:
        try:
            c = float(r.get("close"))
        except (TypeError, ValueError):
            continue
        if c > 0:
            out.append(c)
    return out


def _series(rows: Sequence[dict], key: str) -> list[float]:
    return [float(r[key]) for r in rows if r.get(key) is not None]


def sma(values: Sequence[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def ema(values: Sequence[float], period: int) -> list[float]:
    if not values:
        return []
    k = 2 / (period + 1)
    out = [values[0]]
    for v in values[1:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def rsi(values: Sequence[float], period: int = 14) -> float | None:
    if len(values) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(values)):
        d = values[i] - values[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(values: Sequence[float]) -> dict:
    if len(values) < 26:
        return {"macd": None, "signal": None, "hist": None}
    e12 = ema(values, 12)
    e26 = ema(values, 26)
    line = [a - b for a, b in zip(e12, e26)]
    sig = ema(line, 9)
    hist = line[-1] - sig[-1] if sig else None
    return {"macd": line[-1], "signal": sig[-1] if sig else None, "hist": hist}


def atr(rows: Sequence[dict], period: int = 14) -> float | None:
    if len(rows) < period + 1:
        return None
    trs = []
    for i in range(1, len(rows)):
        try:
            h = float(rows[i].get("high") or 0)
            l = float(rows[i].get("low") or 0)
            pc = float(rows[i - 1].get("close") or 0)
        except (TypeError, ValueError):
            continue
        if h <= 0 or l <= 0 or pc <= 0:
            continue
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    if len(trs) < period:
        return None
    return sum(trs[-period:]) / period


def bollinger(values: Sequence[float], period: int = 20, nstd: float = 2.0) -> dict:
    if len(values) < period:
        return {"mid": None, "upper": None, "lower": None, "bandwidth": None}
    window = values[-period:]
    mid = sum(window) / period
    var = sum((x - mid) ** 2 for x in window) / period
    std = var**0.5
    upper = mid + nstd * std
    lower = mid - nstd * std
    bw = (upper - lower) / mid if mid else None
    return {"mid": mid, "upper": upper, "lower": lower, "bandwidth": bw}


def volume_ratio(rows: Sequence[dict], period: int = 20) -> float | None:
    vols = _series(rows, "volume")
    if len(vols) < period:
        return None
    avg = sum(vols[-period:]) / period
    if avg <= 0:
        return None
    return vols[-1] / avg


# IDX single-session hard limit ~35% (ARA/ARB); above = data garbage
_MAX_SANE_DAY_CHG = 35.0


def analyze(rows: Sequence[dict]) -> dict:
    c = _closes(rows)
    if len(c) < 5:
        return {
            "ok": False,
            "reason": "insufficient_bars",
            "last_close": c[-1] if c else None,
            "change_pct": 0.0,
            "change_sane": False,
        }
    last = c[-1]
    prev = c[-2]
    chg = (last - prev) / prev * 100 if prev else 0.0
    sane = abs(chg) <= _MAX_SANE_DAY_CHG
    # if insane jump, still report raw but mark flag — scorers must not trust it
    m = macd(c)
    bb = bollinger(c, 20)
    atr14 = atr(rows, 14)
    vr = volume_ratio(rows, 20)
    s20 = sma(c, 20)
    s50 = sma(c, min(50, len(c)))
    return {
        "ok": True,
        "last_close": last,
        "change_pct": round(chg, 3),
        "change_sane": sane,
        "sma20": s20,
        "sma50": s50,
        "rsi14": rsi(c, 14),
        "macd": m,
        "atr14": atr14,
        "bollinger": bb,
        "volume_ratio": vr,
        "bars": len(c),
        "trend": (
            "up"
            if m.get("hist") is not None and m["hist"] > 0 and (s20 or 0) <= last
            else "down"
            if m.get("hist") is not None and m["hist"] < 0
            else "sideways"
        ),
    }
