import math


def _rows(n=60):
    return [
        {"close": 100 + i * 0.5, "high": 101 + i * 0.5, "low": 99 + i * 0.5, "volume": 1000 + i}
        for i in range(n)
    ]


def test_analyze_ok():
    from src.indicators import analyze

    r = analyze(_rows())
    assert r["ok"] is True
    assert r["trend"] == "up"
    assert r["sma20"] is not None


def test_sma():
    from src.indicators.technical import sma

    assert sma([1, 2, 3, 4, 5], 5) == 3.0
    assert sma([1, 2], 5) is None


def test_rsi_bounds():
    from src.indicators.technical import rsi

    v = rsi([100 + i for i in range(30)], 14)
    assert v is None or 0 <= v <= 100


def test_macd_shape():
    from src.indicators.technical import macd

    out = macd([100 + math.sin(i / 5) * 2 for i in range(60)])
    assert set(["macd", "signal", "hist"]).issubset(out.keys())


def test_volume_ratio():
    from src.indicators.technical import volume_ratio

    v = volume_ratio(_rows())
    assert v is None or v > 0