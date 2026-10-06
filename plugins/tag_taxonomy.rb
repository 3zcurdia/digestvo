# Reader-facing topic tags on each post (`tags:` in front matter, one bucket
# from the digest skill's categories). This module is the single place that
# turns those labels into URLs, archive indexes and related-story lists, so
# the slug rule cannot drift between the builder and the templates.
module TagTaxonomy
  module_function

  # Display names stay verbatim ("AI/ML", "Security & Privacy"); the slug is
  # only for the path. `downcase → non-alphanumerics become "-" → strip
  # edges` keeps every current bucket collision-free and URL-safe.
  def slug(tag)
    tag.to_s.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/\A-+|-+\z/, "")
  end

  def path(tag)
    "/tags/#{slug(tag)}/"
  end

  # [{display:, slug:, path:, count:, posts:}, …] newest stories first inside
  # each tag; the list itself is count desc then A–Z. Warns if two display
  # names ever collapse onto one slug.
  def index(posts)
    grouped = Hash.new { |hash, key| hash[key] = [] }
    posts.each do |post|
      Array(post.data.tags).each { |tag| grouped[tag] << post }
    end

    claimed = {}
    grouped.map do |display, tag_posts|
      s = slug(display)
      if claimed[s] && claimed[s] != display
        Bridgetown.logger.warn(
          "TagTaxonomy:",
          "slug collision: #{claimed[s].inspect} and #{display.inspect} both map to #{s.inspect}"
        )
      end
      claimed[s] ||= display

      {
        display: display,
        slug: s,
        path: "/tags/#{s}/",
        count: tag_posts.size,
        posts: newest_first(tag_posts),
      }
    end.sort_by { |tag| [-tag[:count], tag[:display].downcase] }
  end

  # Other posts sharing any tag with `current`, newest first, self excluded.
  def related_posts(posts, current, limit: 4)
    current_slugs = Array(current.data.tags).map { |tag| slug(tag) }
    return [] if current_slugs.empty?

    posts
      .reject { |post| post.equal?(current) }
      .select { |post| Array(post.data.tags).any? { |tag| current_slugs.include?(slug(tag)) } }
      .then { |matched| newest_first(matched).first(limit) }
  end

  def newest_first(posts)
    posts.sort_by(&:date).reverse
  end
end
