class Shared::ShareLinks < Bridgetown::Component
  # Header share action for a story. Takes the already-absolute post URL
  # (resource.absolute_url bakes in site.config.url) and the post's share_text
  # (falling back to the title when share_text is absent), and turns them
  # into an X Web Intent link. Renders as a single inline anchor
  # matching the SourceLinks row, so it sits next to "Leer el original" /
  # discussion links in the post header.
  def initialize(data, url:)
    text = data["share_text"]
    text = data["title"] if text.nil? || text.to_s.strip.empty?
    @content = text.to_s.strip
    @url = url.to_s.strip
  end

  def intent_url
    "https://x.com/intent/post?text=#{ERB::Util.url_encode(@content)}&url=#{ERB::Util.url_encode(@url)}"
  end

  def render?
    !@content.empty? && !@url.empty?
  end
end
