import { useState } from "react";

const ALLOWED = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 75, 100]);
const MAX_SMALL_REPEATS = 2; // un petit nombre (1 à 10) ne peut apparaître que deux fois
const MAX_LARGE_REPEATS = 1; // un grand nombre (25, 50, 75, 100) ne peut apparaître qu'une fois

function parse(v) {
  return /^\d+$/.test(v) ? parseInt(v, 10) : null;
}

export default function App() {
  const [nums, setNums] = useState(Array(6).fill(""));
  const [target, setTarget] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const counts = {};
  nums.forEach((v) => { const n = parse(v); if (n !== null) counts[n] = (counts[n] || 0) + 1; });
  const tooMany = (v) => {
    const n = parse(v);
    if (n === null) return false;
    return counts[n] > (n <= 10 ? MAX_SMALL_REPEATS : MAX_LARGE_REPEATS);
  };
  const isBad = (v) => v !== "" && (!ALLOWED.has(parse(v)) || tooMany(v));
  const numsOk = nums.every((v) => ALLOWED.has(parse(v)) && !tooMany(v));
  const t = parse(target);
  const targetOk = t !== null && t >= 100 && t <= 999;
  const ready = numsOk && targetOk;

  const setNum = (i, v) => {
    setNums(nums.map((n, k) => (k === i ? v.replace(/\D/g, "").slice(0, 3) : n)));
    setResult(null);
  };

  async function submit(e) {
    e.preventDefault();
    if (!ready) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch("/api/solve/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ numbers: nums.map(Number), target: t }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Erreur du serveur.");
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Le compte est bon ?</h1>
      <p className="intro">
        Entrez les six nombres tirés (1 à 10, ou 25, 50, 75, 100), puis l'objectif.
      </p>

      <form onSubmit={submit}>
        <div className="tiles">
          {nums.map((v, i) => {
            const bad = isBad(v);
            return (
              <input
                key={i}
                className={"tile" + (bad ? " bad" : "")}
                inputMode="numeric"
                aria-label={`Nombre ${i + 1}`}
                value={v}
                onChange={(e) => setNum(i, e.target.value)}
              />
            );
          })}
        </div>

        {nums.some((v) => tooMany(v) && parse(v) <= 10) && (
          <p className="error" role="alert">
            Un petit nombre (1 à 10) ne peut apparaître que deux fois.
          </p>
        )}
        {nums.some((v) => tooMany(v) && parse(v) > 10) && (
          <p className="error" role="alert">
            Un grand nombre (25, 50, 75, 100) ne peut apparaître qu'une fois.
          </p>
        )}

        <label className="target">
          Objectif (100 à 999)
          <input
            inputMode="numeric"
            value={target}
            onChange={(e) => {
              setTarget(e.target.value.replace(/\D/g, "").slice(0, 3));
              setResult(null);
            }}
          />
        </label>

        <button type="submit" disabled={!ready || loading}>
          {loading ? "Recherche en cours…" : "Lancer la recherche"}
        </button>
      </form>

      {error && <p className="error" role="alert">{error}</p>}

      {result && (
        <section className="result" aria-live="polite">
          <h2>
            {result.exact
              ? `Le compte est bon : ${t}`
              : `Impossible d'atteindre ${t}. Meilleure approche : ${result.value} (écart de ${result.difference})`}
          </h2>
          {result.steps.length === 0 ? (
            <p>Ce nombre fait déjà partie du tirage.</p>
          ) : (
            <ol>
              {result.steps.map((s, i) => (
                <li key={i}>
                  {s.left} {s.op} {s.right} = <strong>{s.result}</strong>
                </li>
              ))}
            </ol>
          )}
        </section>
      )}
    </main>
  );
}
