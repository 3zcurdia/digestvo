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
    currentEdition() === "dark" ? "Day edition" : "Night edition"
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

console.info("Bridgetown is loaded!")
