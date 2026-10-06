module Builders
  # Generates one archive page per topic tag at /tags/<slug>/, plus the
  # helpers' data contract those pages rely on. The /tags/ index itself is a
  # normal page (src/tags.md); only the per-tag archives are built here.
  #
  # Bridgetown's prototype pages were rejected: with the site's `pretty`
  # slugify mode, "Security & Privacy" becomes /tags/security-&-privacy/.
  # TagTaxonomy.slug produces the clean path instead, and this builder owns
  # both sides so display names never leak into URLs.
  class TagArchives < SiteBuilder
    def build
      generator do
        TagTaxonomy.index(site.collections.posts.resources).each do |tag|
          page = Bridgetown::GeneratedPage.new(
            site, ".", "tags/#{tag[:slug]}", "index.html"
          )
          page.data = HashWithDotAccess::Hash.new(
            "layout"    => "tag",
            "title"     => "Stories in #{tag[:display]}",
            "summary"   => "#{tag[:count]} #{tag[:count] == 1 ? "story" : "stories"} " \
                           "filed under #{tag[:display]}",
            "tag"       => tag[:display],
            "tag_slug"  => tag[:slug],
            "prose"     => false
          )
          page.content = ""
          site.add_generated_page(page)
        end
      end
    end
  end
end
