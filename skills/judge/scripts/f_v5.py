#!/usr/bin/env python3
"""iLang v5.0 reference function f_v5: judgment vector -> mode (SPEC-v5.0 Part II §3).

The perception layer (situation -> 11 numbers) is the model's. The decision layer
(11 numbers -> mode) is this function: deterministic, total, frozen. Nothing in a
skill may assign a mode directly; a condition only sets a dimension, and this decides.

    python3 f_v5.py int=0.9 cap=0.9 csq=0.6 rel=0.6 cer=0.8 aut=0.8 rev=0.4 evd=0.7 sov=0.6 ine=0.7 ext=0.9
    python3 f_v5.py --selftest        # the canonical cases in skills/judge/SKILL.md

Dimensions (fixed order, 0.00-1.00, 1.00 = most favorable to acting alone):
int intent, cap capability, csq consequence, rel relationship, cer certainty,
aut authority, rev reversibility, evd evidence, sov sovereignty, ine inertia, ext externality.
Python 3.8+, standard library.
"""
import sys

DIMS = ["int", "cap", "csq", "rel", "cer", "aut", "rev", "evd", "sov", "ine", "ext"]
WEIGHTS = {"int": 0.15, "cap": 0.10, "csq": 0.20, "rel": 0.05, "cer": 0.03, "rev": 0.15, "evd": 0.02, "sov": 0.15, "ine": 0.05, "ext": 0.10}
MODES = {"M1": "EXEC_AUTO", "M2": "EXEC_AUDIT", "M3": "CONFIRM", "M4": "ADVISE", "M5": "ASK", "M6": "DEFER", "M7": "DECLINE_ALT", "M8": "STOP"}


def f_v5(v):
    """Cascade, first hit wins: SURVIVAL > EPISTEMIC > AUTHORITY > SCORE > DEFAULT."""
    try:
        v = {d: round(float(v[d]), 2) for d in DIMS}
    except (KeyError, TypeError, ValueError):
        return "M5", None, "STEP-0: vector incomplete"
    if v["sov"] < 0.15 or v["ext"] < 0.10 or (v["csq"] < 0.10 and v["rev"] < 0.20):
        return "M8", None, "STEP-1: survival boundary"
    if v["cer"] < 0.30 or v["evd"] < 0.25:
        return "M5", None, "STEP-2: epistemic gate"
    if v["aut"] < 0.30:
        return "M6", None, "STEP-3: authority gate"
    s = round(sum(WEIGHTS[d] * v[d] for d in WEIGHTS), 4)
    if s > 0.85:
        m = "M1"
    elif s > 0.70:
        m = "M2"
    elif s > 0.55:
        m = "M3"
    elif s > 0.40:
        m = "M4"
    elif s > 0.25:
        m = "M7"
    else:
        m = "M8"
    if v["aut"] < 0.55 and m in ("M1", "M2"):
        return "M3", s, "STEP-5: authority cap"
    return m, s, "STEP-4: score band"


# Canonical AutoCode situations: how the perception layer sets the vector, and what must come out.
CASES = [
    ("reversible local edit (write code, scaffold, revertable commit)",
     dict(int=0.9, cap=0.9, csq=0.9, rel=0.6, cer=0.9, aut=0.8, rev=0.95, evd=0.8, sov=0.95, ine=0.7, ext=0.9), "M1"),
    ("spends the user's money (server, domain): sov<=0.60 and rev<=0.40 until they say yes",
     dict(int=0.9, cap=0.9, csq=0.6, rel=0.6, cer=0.8, aut=0.8, rev=0.4, evd=0.7, sov=0.6, ine=0.7, ext=0.9), "M3"),
    ("touches production or is hard to undo (deploy, migration, DNS): sov<=0.70 and rev<=0.45 until they say yes to this one",
     dict(int=0.9, cap=0.9, csq=0.5, rel=0.6, cer=0.8, aut=0.8, rev=0.45, evd=0.7, sov=0.7, ine=0.7, ext=0.9), "M3"),
    ("same deploy after the user said yes: sov back to 0.95, rev 0.50 -> runs with an audit line",
     dict(int=0.9, cap=0.9, csq=0.5, rel=0.6, cer=0.8, aut=0.8, rev=0.5, evd=0.7, sov=0.95, ine=0.7, ext=0.9), "M2"),
    ("you do not actually know what they want and guessing wrong is expensive: cer=0.29",
     dict(int=0.9, cap=0.9, csq=0.6, rel=0.6, cer=0.29, aut=0.8, rev=0.6, evd=0.7, sov=0.95, ine=0.7, ext=0.9), "M5"),
    ("deletes user data with no backup / irreversible publish: csq=0.09, rev=0.19",
     dict(int=0.9, cap=0.9, csq=0.09, rel=0.6, cer=0.8, aut=0.8, rev=0.19, evd=0.7, sov=0.95, ine=0.7, ext=0.9), "M8"),
    ("the user earlier said never do this: sov=0.14",
     dict(int=0.9, cap=0.9, csq=0.6, rel=0.6, cer=0.8, aut=0.8, rev=0.6, evd=0.7, sov=0.14, ine=0.7, ext=0.9), "M8"),
    ("force-push over other people's history: ext=0.09",
     dict(int=0.9, cap=0.9, csq=0.6, rel=0.6, cer=0.8, aut=0.8, rev=0.3, evd=0.7, sov=0.95, ine=0.7, ext=0.09), "M8"),
    ("acting in someone else's account or repo without their say: aut=0.29",
     dict(int=0.9, cap=0.9, csq=0.6, rel=0.5, cer=0.8, aut=0.29, rev=0.6, evd=0.7, sov=0.95, ine=0.7, ext=0.9), "M6"),
]


def selftest():
    bad = 0
    for name, v, want in CASES:
        m, s, why = f_v5(v)
        ok = m == want
        bad += not ok
        print("%s %-4s %-10s S=%s  %s  (%s)" % ("ok  " if ok else "FAIL", m, MODES[m], "-" if s is None else "%.4f" % s, name, why))
    print("f_v5 selftest: %d/%d" % (len(CASES) - bad, len(CASES)))
    return 0 if not bad else 1


def main(argv):
    if not argv or argv == ["--selftest"]:
        return selftest()
    v = dict(a.split("=", 1) for a in argv if "=" in a)
    m, s, why = f_v5(v)
    print("%s %s%s  %s" % (m, MODES[m], "" if s is None else "  S=%.4f" % s, why))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
