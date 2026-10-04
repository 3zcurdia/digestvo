class Shared::PostList < Bridgetown::Component
  # The home page and /posts list stories the same way, so the markup lives here
  # instead of being copy-pasted into two templates where it would drift.
  #
  # Only front matter is rendered: title, date, summary. The comments summary
  # stays in the post body, out of the listing — a reader scanning the index
  # wants to know what a story is, not what the thread argued about.
  def initialize(posts:)
    @posts = posts.to_a
  end

  def any?
    @posts.any?
  end

  def entries(&block)
    @posts.each(&block)
  end
end
