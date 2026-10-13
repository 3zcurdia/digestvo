class Shared::ShareLinks < Bridgetown::Component
  # Header share action for a story. Takes the already-absolute post URL
  # (resource.absolute_url bakes in site.config.url) and the post title, and
  # turns them into an X Web Intent link. Renders as a single inline anchor
  # matching the SourceLinks row, so it sits next to "Read the original" /
  # discussion links in the post header.
  def initialize(content, url:)
    @content = content.to_s.strip
    @url = url.to_s.strip
  end

  def intent_url
    "https://x.com/intent/post?text=#{ERB::Util.url_encode(@content)}&url=#{ERB::Util.url_encode(@url)}"
  end

  def render?
    !@content.empty? && !@url.empty?
  end
end
