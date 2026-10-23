// Brand typeface for the navbar wordmark. Alfa Slab One is a single-weight
// (400) heavy slab cut, so the wordmark must not ask for font-weight: 900.
import "@fontsource/alfa-slab-one/latin-400.css"

// Text face for headlines and body copy. Newsreader is a variable serif drawn
// for on-screen reading, with an optical-size axis that tightens the display
// sizes and opens up the text sizes on its own.
import "@fontsource-variable/newsreader/opsz.css"
import "@fontsource-variable/newsreader/opsz-italic.css"

import "$styles/index.css"

// Import all JavaScript files from src/_components (no component CSS remains;
// every component is styled with Tailwind utilities in its .erb template)
import components from "$components/**/*.{js,jsx,js.rb}"

// The footer's edition switch: plain text, no widget. The device picks the
// scheme until a reader chooses one; the choice sticks in localStorage and is
// applied before first paint by the inline script in _head.erb, which is what
// sets `data-theme` in the first place.
const editionKey = "edition"
const root = document.documentElement
const toggle = document.querySelector("[data-edition-toggle]")
const deviceScheme = matchMedia("(prefers-color-scheme: dark)")

// What the page is actually showing: the reader's pick, else the device's.
const currentEdition = () =>
  root.dataset.theme || (deviceScheme.matches ? "dark" : "light")

const renderToggle = () => {
  if (!toggle) return
  // The label offers the *other* edition — in the day's paper you are offered
  // the night edition, and the other way around.
  toggle.textContent =
    currentEdition() === "dark" ? "Edición de día" : "Edición de noche"
  toggle.hidden = false
}

toggle?.addEventListener("click", () => {
  root.dataset.theme = currentEdition() === "dark" ? "light" : "dark"
  try {
    localStorage.setItem(editionKey, root.dataset.theme)
  } catch (error) {}
  renderToggle()
})

// With no explicit pick, the device can flip mid-visit — keep the offer in
// step with what a click would actually do.
deviceScheme.addEventListener("change", () => {
  if (!root.dataset.theme) renderToggle()
})

renderToggle()

// AI Watchdog: the live AI-release tracker under the masthead. The shell is
// server-rendered, but the figures and the latest model link come from
// watchdog.9exp.net at read time, so the bar stops depending on deployments.
// /api/latest drives the ticker line; /api/releases fills the radar list.
const watchdog = document.querySelector("[data-watchdog]")

if (watchdog) {
  const copy = watchdog.dataset
  const fallback = watchdog.querySelector("[data-watchdog-fallback]")
  const readout = watchdog.querySelector("[data-watchdog-readout]")
  const latestLink = watchdog.querySelector("[data-watchdog-latest]")
  const latestName = watchdog.querySelector("[data-watchdog-latest-name]")
  const since = watchdog.querySelector("[data-watchdog-since]")
  const average = watchdog.querySelector("[data-watchdog-average]")
  const averageRow = watchdog.querySelector("[data-watchdog-average-row]")
  const live = watchdog.querySelector("[data-watchdog-live]")
  const radarToggle = watchdog.querySelector("[data-watchdog-radar-toggle]")
  const radarPanel = watchdog.querySelector("[data-watchdog-radar]")
  const radarList = watchdog.querySelector("[data-watchdog-radar-list]")
  const radarUpdated = watchdog.querySelector("[data-watchdog-radar-updated]")

  const lang = document.documentElement.lang || "es"
  const numberFormat = new Intl.NumberFormat(lang, { maximumFractionDigits: 1 })
  const dayFormat = new Intl.DateTimeFormat(lang, {
    day: "numeric",
    month: "short",
    timeZone: "UTC",
  })
  const updatedFormat = new Intl.DateTimeFormat(lang, {
    dateStyle: "medium",
    timeStyle: "short",
  })

  const fill = (template, values) =>
    Object.entries(values).reduce(
      (text, [key, value]) => text.replaceAll(`%{${key}}`, String(value)),
      template || ""
    )

  // Date-only strings are UTC by definition; comparing them against the
  // reader's local calendar day keeps "hace N días" right across timezones.
  const daysSince = (isoDate) => {
    const [year, month, day] = isoDate.split("-").map(Number)
    if (!year || !month || !day) return null
    const last = Date.UTC(year, month - 1, day)
    const now = new Date()
    const today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate())
    return Math.max(0, Math.round((today - last) / 86_400_000))
  }

  const sinceLabel = (days) => {
    if (days === 0) return copy.sinceToday || ""
    if (days === 1) return copy.sinceOne || ""
    return fill(copy.sinceOther, { count: days })
  }

  const releaseDateLabel = (value, approximate) => {
    const date = new Date(`${value}T00:00:00Z`)
    if (Number.isNaN(date.getTime())) return ""
    const label = dayFormat.format(date)
    return approximate ? `≈ ${label}` : label
  }

  // Only models.dev URLs from the API become links; anything else falls back
  // to the site root rather than turning the ticker into an open redirect.
  const modelHref = (value) => {
    try {
      const url = new URL(value)
      if (
        url.protocol === "https:" &&
        (url.hostname === "models.dev" || url.hostname.endsWith(".models.dev"))
      ) {
        return url.href
      }
    } catch (error) {}
    return "https://models.dev"
  }

  const fetchJson = async (url) => {
    const response = await fetch(url, {
      headers: { Accept: "application/json" },
      cache: "no-cache",
      credentials: "omit",
      referrerPolicy: "no-referrer",
    })
    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}`)
    }
    return response.json()
  }

  const renderLatest = (data) => {
    const latest = data?.latest
    if (!latest?.name || !latestLink || !latestName) return

    latestName.textContent = latest.name
    latestLink.href = modelHref(latest.url)
    latestLink.title = fill(copy.linkTitle, { name: latest.name })

    const datedDays = latest.releaseDate
      ? daysSince(latest.releaseDate)
      : null
    const days =
      datedDays ??
      Math.max(0, Math.round(Number(data.daysSinceLastRelease) || 0))
    if (since) since.textContent = sinceLabel(days)

    if (average && Number.isFinite(data.averageDaysBetweenReleases)) {
      const value = numberFormat.format(data.averageDaysBetweenReleases)
      average.textContent = fill(
        data.averageDaysBetweenReleases === 1
          ? copy.averageOne
          : copy.averageOther,
        { avg: value }
      )
      if (averageRow) averageRow.hidden = false
    } else if (averageRow) {
      averageRow.hidden = true
    }

    if (fallback) fallback.hidden = true
    if (readout) readout.hidden = false
    if (live) live.hidden = false
  }

  const renderReleases = (data) => {
    if (!radarList || !radarToggle) return
    const releases = Array.isArray(data?.releases)
      ? data.releases.filter((release) => release?.name)
      : []
    if (!releases.length) return

    radarList.replaceChildren(
      ...releases.map((release) => {
        const item = document.createElement("li")
        item.className = "flex items-baseline justify-between gap-3"

        const link = document.createElement("a")
        link.className = "link-plain text-body-color hover:underline focus-ring"
        link.href = modelHref(release.url)
        link.target = "_blank"
        link.rel = "noopener"
        link.textContent = release.name
        link.title = fill(copy.linkTitle, { name: release.name })

        const date = document.createElement("time")
        date.className = "flex-none text-[0.6875rem] text-muted-color"
        if (release.releaseDate) {
          date.dateTime = release.releaseDate
          date.textContent = releaseDateLabel(
            release.releaseDate,
            release.isApproximate
          )
        }

        item.append(link, date)
        return item
      })
    )

    if (radarUpdated && data.updatedAt) {
      const updated = new Date(data.updatedAt)
      if (!Number.isNaN(updated.getTime())) {
        radarUpdated.textContent = fill(copy.radarUpdated, {
          date: updatedFormat.format(updated),
        })
      }
    }

    radarToggle.hidden = false
  }

  const setRadar = (open) => {
    if (!radarPanel || !radarToggle) return
    radarPanel.hidden = !open
    radarToggle.setAttribute("aria-expanded", String(open))
    radarToggle.setAttribute(
      "aria-label",
      open ? copy.radarClose : copy.radarLabel
    )
    radarToggle.querySelector("svg")?.classList.toggle("rotate-180", open)
  }

  radarToggle?.addEventListener("click", () => {
    setRadar(radarPanel?.hidden ?? false)
  })

  watchdog.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && radarPanel && !radarPanel.hidden) {
      setRadar(false)
      radarToggle?.focus()
    }
  })

  let loadedAt = 0
  const load = async () => {
    const [latest, releases] = await Promise.allSettled([
      fetchJson(copy.apiLatest),
      fetchJson(copy.apiReleases),
    ])
    if (latest.status === "fulfilled") renderLatest(latest.value)
    if (releases.status === "fulfilled") renderReleases(releases.value)
    loadedAt = Date.now()
  }

  void load()

  // A tab left open all day should not keep yesterday's release count. The
  // API revalidates on every request, so returning to the page is enough.
  document.addEventListener("visibilitychange", () => {
    if (
      document.visibilityState === "visible" &&
      Date.now() - loadedAt > 300_000
    ) {
      void load()
    }
  })
}

// Layout-integrated search (Pagefind, no dedicated page). The panel lives in
// the masthead on every page, so the WASM index stays out of the homepage
// bundle until a reader actually opens the search. All copy comes from data
// attributes rendered by Shared::Search (locale es.yml) — nothing hardcoded.
const searchRoot = document.querySelector("[data-search-root]")
const searchToggle = document.querySelector("[data-search-toggle]")

if (searchRoot && searchToggle) {
  const searchForm = searchRoot.querySelector("[data-search-form]")
  const searchInput = searchRoot.querySelector("[data-search-input]")
  const searchClear = searchRoot.querySelector("[data-search-clear]")
  const searchStatus = searchRoot.querySelector("[data-search-status]")
  const searchResults = searchRoot.querySelector("[data-search-results]")
  // The archive list below the panel. Only /posts renders both, so this is
  // null everywhere else and every call below is a safe no-op there.
  const searchArchive = document.querySelector("[data-search-archive]")

  const siteBase = searchRoot.dataset.siteBase || "/"
  const pagefindJs =
    searchRoot.dataset.pagefindJs || `${siteBase.replace(/\/$/, "")}/pagefind/pagefind.js`
  const msgHint = searchRoot.dataset.msgHint || ""
  const msgTooShort = searchRoot.dataset.msgTooShort || ""
  const msgLoading = searchRoot.dataset.msgLoading || ""
  const msgError = searchRoot.dataset.msgError || ""
  const msgOne = searchRoot.dataset.msgOne || ""
  const msgOther = searchRoot.dataset.msgOther || ""
  const msgNoResults = searchRoot.dataset.msgNoResults || ""

  const msgClose = searchRoot.dataset.msgClose || ""
  const msgOpen = searchRoot.dataset.msgOpen || ""

  // The toggle is rendered hidden like the edition toggle: no JS (or no
  // index) means no control that does nothing.
  searchToggle.hidden = false

  const isOpen = () => !searchRoot.hidden

  const setStatus = (text) => {
    if (!searchStatus) return
    // textContent only — the query is user input and must never land in HTML.
    searchStatus.textContent = text
    searchStatus.hidden = !text
  }

  const clearResults = () => {
    if (searchResults) {
      searchResults.replaceChildren()
      searchResults.hidden = true
    }
  }

  // While a query is present the archive list steps aside so the page shows
  // results only; clearing (or closing) brings it back. The wrapper is
  // visible by default, so no-JS readers always get the full archive.
  const syncArchive = () => {
    if (!searchArchive || !searchInput) return
    searchArchive.hidden = searchInput.value.trim() !== ""
  }

  const openSearch = () => {
    searchRoot.hidden = false
    searchToggle.setAttribute("aria-expanded", "true")
    if (msgClose) searchToggle.setAttribute("aria-label", msgClose)
    searchInput?.focus()
  }

  const closeSearch = () => {
    // Closing resets the search so the page can never end up with both the
    // panel and the archive hidden.
    if (searchInput) searchInput.value = ""
    if (searchClear) searchClear.hidden = true
    clearResults()
    setStatus(msgHint)
    syncArchive()
    searchRoot.hidden = true
    searchToggle.setAttribute("aria-expanded", "false")
    if (msgOpen) searchToggle.setAttribute("aria-label", msgOpen)
    searchToggle.focus()
  }

  searchToggle.addEventListener("click", () => {
    if (isOpen()) {
      closeSearch()
    } else {
      openSearch()
      // Warm the index on open so the first keystroke already hits cache.
      void getPagefind()
    }
  })

  let pagefind = null
  let pagefindFailed = false

  async function getPagefind() {
    if (pagefind || pagefindFailed) return pagefind
    try {
      // Variable URL on purpose: the bundle lives in output/pagefind/
      // (post-build, outside the esbuild manifest), so it must stay a
      // runtime import and never be bundled.
      const mod = await import(pagefindJs)
      pagefind = mod
      try {
        await pagefind.options({ baseUrl: siteBase })
      } catch (error) {}
      return pagefind
    } catch (error) {
      pagefindFailed = true
      return null
    }
  }

  const toHref = (url) => {
    if (!url) return siteBase
    if (/^https?:\/\//.test(url)) return url
    const base = siteBase.replace(/\/$/, "")
    if (!base) return url.startsWith("/") ? url : `/${url}`
    // Pagefind may already prefix result URLs with the baseUrl option —
    // never double it when falling back to BRIDGETOWN_BASE_PATH builds.
    if (url === base || url.startsWith(`${base}/`)) return url
    return `${base}${url.startsWith("/") ? url : `/${url}`}`
  }

  const formatCount = (count) =>
    count === 1 ? msgOne : msgOther.replace("%{count}", String(count))

  const renderResults = async (items) => {
    clearResults()
    if (!searchResults) return
    const withData = await Promise.all(
      items.map(async (item) => {
        try {
          return { item, data: await item.data() }
        } catch (error) {
          return null
        }
      })
    )
    let shown = 0
    for (const entry of withData) {
      if (!entry?.data) continue
      const title = entry.data.meta?.title || entry.data.title || entry.data.url
      if (!title) continue
      const li = document.createElement("li")
      li.className = "group relative py-4 card-focus"
      const h3 = document.createElement("h3")
      h3.className =
        "m-0 font-serif text-[1.25rem] leading-[1.2] font-[650] tracking-[-0.005em] text-balance text-heading-color"
      const a = document.createElement("a")
      a.className = "link-card group-hover:text-action-color"
      a.href = toHref(entry.data.url)
      a.textContent = title
      h3.appendChild(a)
      li.appendChild(h3)
      const rawExcerpt = entry.data.excerpt || ""
      if (rawExcerpt) {
        const p = document.createElement("p")
        p.className = "mt-2 mb-0 text-[1.0625rem] leading-[1.55] text-body-color"
        // Pagefind excerpts are escaped HTML with <mark> highlights. Restyle
        // the marks with utilities (flat accent tint, like selection) instead
        // of adding global CSS for an element that only exists at runtime.
        p.innerHTML = rawExcerpt.replace(
          /<mark>/g,
          '<mark class="bg-action-color/25 text-inherit rounded-[2px] px-[1px]">'
        )
        li.appendChild(p)
      }
      searchResults.appendChild(li)
      shown += 1
    }
    searchResults.hidden = shown === 0
    return shown
  }

  let debounce = null
  let lastQuery = ""

  async function runSearch(rawQuery) {
    const query = rawQuery.trim()
    lastQuery = query
    if (searchClear) searchClear.hidden = !query
    // Immediate, not debounced: the archive must step aside on the first
    // keystroke and return the moment the field empties.
    syncArchive()
    if (!query) {
      clearResults()
      setStatus(msgHint)
      return
    }
    if (query.length < 2) {
      clearResults()
      setStatus(msgTooShort)
      return
    }
    setStatus(msgLoading)
    const pf = await getPagefind()
    // The query may have changed while the index loaded — drop stale runs.
    if (query !== lastQuery) return
    if (!pf) {
      clearResults()
      setStatus(msgError)
      return
    }
    let res = null
    try {
      res = await pf.search(query)
    } catch (error) {
      res = null
    }
    if (query !== lastQuery) return
    if (!res?.results?.length) {
      clearResults()
      setStatus(msgNoResults.replace("%{query}", query))
      return
    }
    // Pagefind returns most relevant first; eight keeps the panel scannable
    // within the single column without pushing the article far down.
    const shown = await renderResults(res.results.slice(0, 8))
    if (query !== lastQuery) return
    if (!shown) {
      setStatus(msgNoResults.replace("%{query}", query))
    } else {
      setStatus(formatCount(shown))
    }
  }

  searchInput?.addEventListener("input", () => {
    // Sync here too, outside the debounce, so there is no flicker between
    // the keystroke and the delayed search.
    syncArchive()
    clearTimeout(debounce)
    debounce = setTimeout(() => void runSearch(searchInput.value), 200)
  })

  searchForm?.addEventListener("submit", (event) => {
    event.preventDefault()
    clearTimeout(debounce)
    void runSearch(searchInput?.value || "")
  })

  searchInput?.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      if (searchInput.value) {
        searchInput.value = ""
        void runSearch("")
        searchInput.focus()
      } else {
        closeSearch()
      }
    }
  })

  searchClear?.addEventListener("click", () => {
    if (searchInput) {
      searchInput.value = ""
      void runSearch("")
      searchInput.focus()
    }
  })

  // Panel starts closed; the hint only appears once opened, so readers who
  // never search never pay the vertical space.
  setStatus(msgHint)
}

console.info("Bridgetown is loaded!")
