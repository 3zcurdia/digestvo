class Shared::VideoList < Bridgetown::Component
  # The /videos index. Built like PostList so the front page and this page share
  # one voice: no card chrome, the serif headline carries the hierarchy, and a
  # hairline separates one video from the next.
  #
  # The one structural difference is the grouping. Stories are grouped into
  # editions by publication day, the way a paper's front page is. A video has
  # no edition — you watched it whenever you watched it — so videos group by
  # month instead and the label repeats the section-label treatment.
  #
  # Each row shows the video's own facts and its first insight. The insight is
  # the hook: it is the reason a reader would click a video rather than a story,
  # and without it the index is a list of titles with nothing to judge them by.
  # `limit` caps the list and turns on a link to the full archive.
  def initialize(videos:, limit: nil, more_url: nil)
    @all = videos.to_a
    @videos = limit ? @all.first(limit) : @all
    @more_url = more_url
  end

  def any?
    @videos.any?
  end

  # Resources arrive newest-first, and group_by keeps insertion order, so the
  # months come out newest-first too without a second sort.
  def months
    @videos.group_by { |video| month_start(video) }
  end

  def insight(video)
    Array(video.data.insights).first
  end

  def more_url
    @more_url if @all.size > @videos.size
  end

  private

  # Date#beginning_of_month is ActiveSupport, which Bridgetown does not load.
  def month_start(video)
    date = video.date.to_date
    Date.new(date.year, date.month, 1)
  end
end