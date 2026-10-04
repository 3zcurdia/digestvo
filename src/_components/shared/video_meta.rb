class Shared::VideoMeta < Bridgetown::Component
  # The facts about a video that are not opinions about it: how long it runs,
  # who published it, and where to watch it. The verdict and the insights are
  # the editorial part, and those live in the layout and the body instead.
  #
  # The videos skill only writes front matter, the same contract the digest has
  # with SourceLinks: `channel`, `channel_url`, `duration` and `video_url`. A
  # key is present or absent, never empty. One component serves both the video
  # page and the index, so the two cannot drift.
  #
  # `watch_link` is the one difference between those two call sites. On the
  # video page the watch link is the point of the page. On the index it would
  # repeat the same label down every row and say nothing the title has not
  # already said, so the index turns it off and shows only the facts.
  def initialize(data:, watch_link: true)
    @data = data
    @watch_link = watch_link
  end

  def channel
    present(@data["channel"])
  end

  def channel_url
    present(@data["channel_url"])
  end

  def duration
    present(@data["duration"])
  end

  def video_url
    present(@data["video_url"]) if @watch_link
  end

  def render?
    channel || duration || video_url
  end

  private

  def present(value)
    value = value.to_s.strip
    value.empty? ? nil : value
  end
end