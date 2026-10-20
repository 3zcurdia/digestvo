module Builders
  # Indexes the built HTML with Pagefind after every site write, except in
  # production where `rake deploy` owns the pipeline (the Rakefile runs the
  # same command after Build). Without this, `bin/bridgetown start` never
  # builds output/pagefind, so the layout-integrated search 404s on its
  # bundle and reports no results locally. Pagefind indexes ~60 pages in a
  # fraction of a second, so reindexing on watch rebuilds stays unnoticed.
  class SearchIndex < SiteBuilder
    def build
      return if Bridgetown.env.production?

      hook :site, :post_write do
        ok = system("npx pagefind --site #{site.destination}")
        Bridgetown.logger.warn("SearchIndex:", "pagefind indexing failed") unless ok
      end
    end
  end
end
