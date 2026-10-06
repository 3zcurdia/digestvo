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
    # GeneratedPages (tag archives, etc.) have no collection; only resources
    # in a collection can match a COLLECTION_SECTIONS entry.
    resource_collection = @resource.collection if @resource.respond_to?(:collection)

    url == path || url == "#{path}/" || section_collection(path) == resource_collection&.label
  end

  # Nav links are Tailwind utilities (no site-nav CSS remains). The only
  # difference between states is the text color: body ink at rest, the neon
  # accent on hover or when the section is active.
  NAV_LINK_BASE = "font-bold no-underline underline-offset-[0.18em] hover:text-action-color focus-visible:rounded-[2px] focus-visible:outline-2 focus-visible:outline-action-color focus-visible:outline-offset-[3px]".freeze

  def nav_link_class(path)
    "#{NAV_LINK_BASE} #{active?(path) ? 'text-action-color' : 'text-body-color'}"
  end

  private

  def section_collection(path)
    COLLECTION_SECTIONS[path]
  end
end
