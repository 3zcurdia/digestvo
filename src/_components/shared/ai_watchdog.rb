class Shared::AiWatchdog < Bridgetown::Component
  # Live AI-release tracker below the masthead. Unlike the rest of the page,
  # nothing here is baked at build time: the browser fetches
  # watchdog.9exp.net/api/latest for the ticker figures and the models.dev
  # link, and /api/releases for the expandable radar. That keeps the bar
  # moving between deployments. The template carries only the shell, the
  # locale copy and a static fallback for readers without JavaScript.
  API_BASE = "https://watchdog.9exp.net/api".freeze
  LATEST_URL = "#{API_BASE}/latest".freeze
  RELEASES_URL = "#{API_BASE}/releases".freeze

  def latest_url
    LATEST_URL
  end

  def releases_url
    RELEASES_URL
  end
end
