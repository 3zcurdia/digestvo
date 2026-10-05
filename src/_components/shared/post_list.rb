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
  # `limit` caps the list and turns on a link to the full archive when
  # stories were cut. `latest_day` keeps only the newest edition day (the home
  # page shows just the current day's stories) while `more_url` still compares
  # against the full archive, so the "All stories" link stays visible whenever
  # older editions exist. `lead` sets the newest story as the front-page lead,
  # with a larger headline.
  def initialize(posts:, limit: nil, lead: false, more_url: nil, latest_day: false)
    @all = posts.to_a
    filtered = latest_day ? latest_edition(@all) : @all
    @posts = limit ? filtered.first(limit) : filtered
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

  private

  # The current edition is the newest publication day, not the calendar day,
  # so the front page still shows stories when the site hasn't rebuilt today.
  def latest_edition(posts)
    latest = posts.map { |post| post.date.to_date }.max
    latest ? posts.select { |post| post.date.to_date == latest } : []
  end
end
