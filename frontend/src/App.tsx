import { useEffect, useMemo, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_URL?.replace(/\/$/, "") || "/api";

type Journey = "settlement" | "tourism";

type Resource = {
  id: number;
  name: string;
  category: string;
  journey: Journey;
  city: string;
  description: string | null;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  website: string | null;
  min_budget: number | null;
  max_budget: number | null;
};

const categories: Record<Journey, string[]> = {
  settlement: [
    "All",
    "housing",
    "healthcare",
    "jobs",
    "education",
    "transport",
    "government",
  ],
  tourism: [
    "All",
    "attractions",
    "restaurants",
    "accommodation",
    "activities",
  ],
};

const journeyCopy: Record<Journey, { title: string; description: string }> = {
  settlement: {
    title: "Settle in, at your own pace.",
    description:
      "Find the everyday essentials that make a new city feel a little more like home.",
  },
  tourism: {
    title: "See Ghaziabad your way.",
    description:
      "Explore local places, find a bite to eat, and make the most of your time here.",
  },
};

function App() {
  const [journey, setJourney] = useState<Journey>("settlement");
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reload, setReload] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    const params = new URLSearchParams({ journey, city: "Ghaziabad" });
    if (category !== "All") params.set("category", category);
    if (search.trim()) params.set("q", search.trim());

    setLoading(true);
    setError("");
    fetch(`${API_BASE_URL}/resources?${params.toString()}`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) {
          const detail = await response.json().catch(() => null);
          throw new Error(detail?.detail ?? "Could not load local places.");
        }
        return response.json() as Promise<{ results: Resource[] }>;
      })
      .then((data) => setResources(data.results))
      .catch((reason: unknown) => {
        if (reason instanceof Error && reason.name !== "AbortError") {
          setError(reason.message);
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });

    return () => controller.abort();
  }, [journey, category, search, reload]);

  const heading = journeyCopy[journey];
  const resultText = useMemo(
    () => `${resources.length} ${resources.length === 1 ? "place" : "places"}`,
    [resources.length],
  );

  function chooseJourney(value: Journey) {
    setJourney(value);
    setCategory("All");
  }

  return (
    <main className="page-shell">
      <header className="topbar">
        <a className="brand" href="#" aria-label="Ankommen home">
          <span className="brand-mark" aria-hidden="true">a.</span>
          <span>ankommen</span>
        </a>
        <div className="location-pill"><span aria-hidden="true">⌖</span> Ghaziabad, India</div>
        <a className="top-link" href="#about">About Ankommen <span aria-hidden="true">↗</span></a>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow"><span className="eyebrow-dot" /> YOUR LOCAL GUIDE</div>
          <h1>{heading.title}</h1>
          <p>{heading.description}</p>
          <div className="journey-switch" role="tablist" aria-label="Choose your journey">
            <button
              className={journey === "settlement" ? "journey-tab active" : "journey-tab"}
              onClick={() => chooseJourney("settlement")}
              role="tab"
              aria-selected={journey === "settlement"}
            >
              <span aria-hidden="true">⌂</span> I’m settling in
            </button>
            <button
              className={journey === "tourism" ? "journey-tab active" : "journey-tab"}
              onClick={() => chooseJourney("tourism")}
              role="tab"
              aria-selected={journey === "tourism"}
            >
              <span aria-hidden="true">✳</span> I’m just visiting
            </button>
          </div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="sun" />
          <div className="art-label">A GOOD PLACE<br />TO BEGIN</div>
          <div className="hill hill-back" />
          <div className="hill hill-front" />
          <div className="art-path" />
          <div className="art-flower flower-one">✳</div>
          <div className="art-flower flower-two">✳</div>
        </div>
      </section>

      <section className="discover" aria-label="Search local places">
        <div className="search-box">
          <span className="search-icon" aria-hidden="true">⌕</span>
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Try “housing”, “food”, or “healthcare”"
            aria-label="Search places and services"
          />
          {search && <button className="clear-search" onClick={() => setSearch("")} aria-label="Clear search">×</button>}
          <span className="search-city">⌖ &nbsp;Ghaziabad</span>
        </div>

        <div className="results-heading">
          <div>
            <div className="eyebrow">A FEW GOOD PLACES TO START</div>
            <h2>{journey === "settlement" ? "Find what you need" : "Out and about"}</h2>
          </div>
          <span className="result-count">{resultText}</span>
        </div>

        <div className="category-list" aria-label="Filter by category">
          {categories[journey].map((item) => (
            <button
              key={item}
              className={category === item ? "category-chip selected" : "category-chip"}
              onClick={() => setCategory(item)}
            >
              {item === "All" ? "Everything" : item}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="message-panel" role="status">Finding places for you…</div>
        ) : error ? (
          <div className="message-panel error-panel" role="alert">
            <strong>We couldn’t reach your local guide.</strong>
            <span>{error} Check that the Ankommen API is running, then try again.</span>
            <button className="retry-button" onClick={() => setReload((value) => value + 1)}>Try again</button>
          </div>
        ) : resources.length === 0 ? (
          <div className="message-panel">
            <strong>No places found just yet.</strong>
            <span>Try another search or choose a different category.</span>
          </div>
        ) : (
          <div className="resource-grid">
            {resources.map((resource, index) => (
              <article className="resource-card" key={resource.id}>
                <div className={`card-illustration illustration-${index % 4}`}>
                  <span className="card-category">{resource.category}</span>
                  <span className="card-symbol" aria-hidden="true">{symbolFor(resource.category)}</span>
                  <span className="card-number">{String(index + 1).padStart(2, "0")}</span>
                </div>
                <div className="card-content">
                  <div className="card-location"><span aria-hidden="true">⌖</span> {resource.address || resource.city}</div>
                  <h3>{resource.name}</h3>
                  <p>{resource.description || "A local resource in Ghaziabad."}</p>
                  <div className="card-footer">
                    <span>{budgetLabel(resource)}</span>
                    {resource.website ? (
                      <a href={resource.website} target="_blank" rel="noreferrer">Visit website <span aria-hidden="true">↗</span></a>
                    ) : (
                      <span className="demo-label">Website unavailable</span>
                    )}
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <footer id="about" className="footer">
        <span className="footer-brand">ankommen<span>.</span></span>
        <p>Helping a new place feel a little more like yours.</p>
        <span className="demo-notice">Some details are unverified. Data © OpenStreetMap contributors. Please confirm details before visiting.</span>
      </footer>
    </main>
  );
}

function symbolFor(category: string) {
  const symbols: Record<string, string> = {
    housing: "⌂",
    healthcare: "＋",
    jobs: "↗",
    education: "✳",
    transport: "↝",
    government: "▤",
    attractions: "✺",
    restaurants: "◒",
    accommodation: "⌂",
    activities: "✳",
  };
  return symbols[category] ?? "✳";
}

function budgetLabel(resource: Resource) {
  if (resource.min_budget == null && resource.max_budget == null) return "Details to confirm";
  if (resource.min_budget == null) return `Up to ₹${resource.max_budget}`;
  if (resource.max_budget == null) return `From ₹${resource.min_budget}`;
  return `₹${resource.min_budget} – ₹${resource.max_budget}`;
}

export default App;
