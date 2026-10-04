// Brand typeface for the navbar wordmark. Alfa Slab One is a single-weight
// (400) heavy slab cut, so the wordmark must not ask for font-weight: 900.
import "@fontsource/alfa-slab-one/latin-400.css"

// Text face for headlines and body copy. Newsreader is a variable serif drawn
// for on-screen reading, with an optical-size axis that tightens the display
// sizes and opens up the text sizes on its own.
import "@fontsource-variable/newsreader/opsz.css"
import "@fontsource-variable/newsreader/opsz-italic.css"

import "$styles/index.css"
import "$styles/syntax-highlighting.css"

// Import all JavaScript & CSS files from src/_components
import components from "$components/**/*.{js,jsx,js.rb,css}"

console.info("Bridgetown is loaded!")
