class Shared::ReleaseBanner < Bridgetown::Component
  # Ticker below the masthead nav: days since the last "AI Release" story and
  # the mean gap between those stories. Both numbers derive from post front
  # matter at build time; a small script in frontend/javascript/index.js
  # refreshes the "days since" count on the client so the figure stays right
  # without waiting for the next daily rebuild.
  #
  # All visible words come from the locale (`release_banner` in
  # src/_locales/es.yml) via the `t` helper in the template — this class only
  # exposes numbers, dates and the latest post resource, never prose.
  RELEASE_TAG_SLUG = "ai-release".freeze

  def initialize(posts:, today: ::Date.today)
    @posts = posts.to_a
    @today = today
  end

  def render?
    !last_release.nil?
  end

  def release_posts
    @release_posts ||= @posts
      .select { |post| Array(post.data.tags).any? { |tag| TagTaxonomy.slug(tag) == RELEASE_TAG_SLUG } }
      .sort_by(&:date)
  end

  def release_days
    @release_days ||= release_posts.map { |post| post.date.to_date }.uniq.sort
  end

  # Newest "AI Release" story by full timestamp — the banner links its
  # days-since count to this article.
  def latest_post
    release_posts.last
  end

  def last_release
    latest_post&.date&.to_date
  end

  def days_since
    return nil unless last_release

    [(@today - last_release).to_i, 0].max
  end

  def avg_gap
    return nil if release_days.size < 2

    gaps = release_days.each_cons(2).map { |earlier, later| (later - earlier).to_i }
    gaps.sum.to_f / gaps.size
  end

  # One decimal with a dot ("3.3"), bare integer when whole ("3"). The
  # surrounding words come from the locale (release_banner.average).
  def formatted_avg_number
    return nil unless avg_gap

    rounded = avg_gap.round(1)
    rounded == rounded.to_i ? rounded.to_i.to_s : format("%.1f", rounded)
  end
end
