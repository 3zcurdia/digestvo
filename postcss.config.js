export default {
  plugins: {
    // Must stay first so Tailwind's directives are expanded before the
    // compatibility passes below rewrite its output.
    '@tailwindcss/postcss': {},
    'postcss-flexbugs-fixes': {},
    'postcss-preset-env': {
      autoprefixer: {
        flexbox: 'no-2009'
      },
      stage: 3
    }
  }
}
