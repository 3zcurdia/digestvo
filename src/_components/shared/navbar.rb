class Shared::Navbar < Bridgetown::Component
  # Collection members don't nest under their index page's URL on this site —
  # posts live at /updates/YYYY/MM/DD/slug/ while the listing lives at /posts/
  # — so those nav items match on the collection label instead.
  COLLECTION_SECTIONS = { "/posts" => "posts" }.freeze

  def initialize(metadata:, resource:)
    @metadata, @resource = metadata, resource
  end

  def active?(path)
    url = @resource&.relative_url.to_s

    url == path || url == "#{path}/" || section_collection(path) == @resource&.collection&.label
  end

  def nav_link_class(path)
    active?(path) ? "site-nav__link is-active" : "site-nav__link"
  end

  private

  def section_collection(path)
    COLLECTION_SECTIONS[path]
  end
end
