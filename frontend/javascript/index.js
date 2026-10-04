// Brand typeface for the navbar wordmark. Archivo Black is a single-weight
// (400) black cut, so the wordmark must not ask for font-weight: 900.
import "@fontsource/archivo-black/latin-400.css"

import "$styles/index.css"
import "$styles/syntax-highlighting.css"

// Import all JavaScript & CSS files from src/_components
import components from "$components/**/*.{js,jsx,js.rb,css}"

console.info("Bridgetown is loaded!")
