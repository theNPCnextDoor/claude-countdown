"""Solveur du jeu « Des chiffres et des lettres » (Countdown).

Recherche exhaustive : on combine deux nombres à la fois (+, -, ×, ÷)
en ne gardant que les résultats entiers positifs. On mémorise les
états déjà explorés pour éviter le travail en double. À écart égal avec
l'objectif, on garde la solution qui utilise le moins de nombres.
"""

from collections.abc import Sequence
from typing import TypedDict


class Item(TypedDict):
    """Un nombre disponible, avec l'opération qui l'a produit (None si tiré)."""
    value: int
    used: int  # nombre de nombres du tirage utilisés pour l'obtenir
    node: "Node | None"


class Node(TypedDict):
    a: Item
    op: str
    b: Item
    value: int


class Step(TypedDict):
    left: int
    op: str
    right: int
    result: int


class Best(TypedDict):
    diff: int | None
    used: int | None
    value: int | None
    node: "Node | None"


class SolveResult(TypedDict):
    exact: bool
    value: int | None
    difference: int | None
    steps: list[Step]


def _steps(node: Node | None) -> list[Step]:
    """Aplatit l'arbre d'opérations en liste ordonnée d'étapes."""
    if node is None:
        return []
    a, b = node["a"], node["b"]
    return _steps(a["node"]) + _steps(b["node"]) + [
        {"left": a["value"], "op": node["op"], "right": b["value"], "result": node["value"]}
    ]


def solve(numbers: Sequence[int], target: int) -> SolveResult:
    best: Best = {"diff": None, "used": None, "value": None, "node": None}
    seen: set[tuple[tuple[int, int], ...]] = set()

    def consider(item: Item) -> None:
        """Garde le plus proche de l'objectif ; à écart égal, le moins de nombres utilisés."""
        diff = abs(item["value"] - target)
        if (
            best["diff"] is None
            or best["used"] is None
            or (diff, item["used"]) < (best["diff"], best["used"])
        ):
            best["diff"] = diff
            best["used"] = item["used"]
            best["value"] = item["value"]
            best["node"] = item["node"]

    def search(items: list[Item]) -> None:
        key = tuple(sorted((i["value"], i["used"]) for i in items))
        if key in seen:
            return
        seen.add(key)

        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                x, y = items[i], items[j]
                big, small = (x, y) if x["value"] >= y["value"] else (y, x)
                bv, sv = big["value"], small["value"]
                candidates: list[tuple[int, str]] = [(bv + sv, "+")]
                if bv != sv:  # a - a = 0, inutile
                    candidates.append((bv - sv, "-"))
                if sv != 1:  # × 1 ne change rien
                    candidates.append((bv * sv, "×"))
                if sv != 1 and bv % sv == 0:  # ÷ 1 ne change rien
                    candidates.append((bv // sv, "÷"))

                rest = [items[k] for k in range(n) if k not in (i, j)]
                for value, op in candidates:
                    if value <= 0:
                        continue
                    new: Item = {
                        "value": value,
                        "used": big["used"] + small["used"],
                        "node": {"a": big, "op": op, "b": small, "value": value},
                    }
                    consider(new)
                    if rest:
                        search(rest + [new])

    items: list[Item] = [{"value": v, "used": 1, "node": None} for v in numbers]
    for item in items:
        consider(item)
    search(items)

    return {
        "exact": best["diff"] == 0,
        "value": best["value"],
        "difference": best["diff"],
        "steps": _steps(best["node"]),
    }
