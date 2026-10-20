class Shared::SearchToggle < Bridgetown::Component
  # Icon-only toggle for the archive search. Rendered in the page header next
  # to the title when the page sets `search: true` in front matter (see
  # src/_layouts/page.erb); the panel it toggles lives in the page body as
  # Shared::Search. Paired via data-search-toggle and
  # aria-controls="site-search-panel", which is what frontend/javascript/index.js
  # wires together.
  def initialize
  end
end
