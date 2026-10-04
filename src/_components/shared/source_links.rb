class Shared::SourceLinks < Bridgetown::Component
  # Where a story came from and where it was argued about. The digest skill
  # only writes front matter: `source_url`, plus `hn_url` and/or `lobsters_url`
  # for every site the story ran on. The presence of those keys is the whole
  # contract — this component is the one place that turns them into links, so
  # the marks cannot drift between templates.
  SOURCES = [
    { key: "hn_url", label: "Hacker News", mark: :hn },
    { key: "lobsters_url", label: "Lobsters", mark: :lobsters },
  ].freeze

  def initialize(data:)
    @data = data
  end

  def original_url
    present(@data["source_url"])
  end

  def discussions
    SOURCES.filter_map do |source|
      url = present(@data[source[:key]])
      source.merge(url: url) if url
    end
  end

  def render?
    original_url || discussions.any?
  end

  private

  def present(value)
    value = value.to_s.strip
    value.empty? ? nil : value
  end
end
