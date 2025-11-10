source "https://rubygems.org"

# Use the latest GitHub Pages gem (includes Jekyll and most plugins)
gem "github-pages", "~> 232", group: :jekyll_plugins

# Required for timezone data
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]
gem "wdm", "~> 0.1.1", platforms: [:mingw, :mswin, :x64_mingw, :jruby]

# Additional plugins not included in github-pages gem
# Note: Most Jekyll plugins below are already included in github-pages gem
group :jekyll_plugins do
  # These are already in github-pages gem, but keeping for explicit dependency management:
  # gem "jekyll-paginate"     # included in github-pages
  # gem "jekyll-sitemap"      # included in github-pages
  # gem "jekyll-gist"         # included in github-pages
  # gem "jekyll-feed"         # included in github-pages
  # gem "jemoji"              # included in github-pages
  # gem "jekyll-include-cache" # included in github-pages

  # This plugin is NOT supported by GitHub Pages - remove if using GitHub Pages hosting
  gem "jekyll-algolia"
end