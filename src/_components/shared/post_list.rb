class Shared::PostList < Bridgetown::Component
  # The home page and /posts list stories the same way, so the markup lives here
  # instead of being copy-pasted into two templates where it would drift.
  #
  # Stories are grouped into editions by publication day, newest first, the way
  # a paper's front page is. Only front matter is rendered: title, the edition
  # date, summary. The comments summary stays in the post body — a reader
  # scanning the index wants to know what a story is, not what the thread
  # argued about.
  #
  # `limit` caps the list (the home page shows the latest 10) and turns on a
  # link to the full archive when stories were cut. `lead` sets the newest
  # story as the front-page lead, with a larger headline.
  def initialize(posts:, limit: nil, lead: false, more_url: nil)
    @all = posts.to_a
    @posts = limit ? @all.first(limit) : @all
    @lead = lead
    @more_url = more_url
  end

  def any?
    @posts.any?
  end

  def editions
    @posts.group_by { |post| post.date.to_date }
  end

  def lead?(post)
    @lead && post.equal?(@posts.first)
  end

  def more_url
    @more_url if @all.size > @posts.size
  end
end
