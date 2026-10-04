---
layout: default
---

<section class="mb-10">
  <h1 class="!m-0 !text-left !text-4xl tracking-tight">digestvo</h1>

  <p class="mt-3 max-w-prose text-lg text-muted-color">
    A digested newsletter. The signal, minus the noise.
  </p>

  <p class="mt-6 flex flex-wrap gap-3">
    <a
      href="<%= relative_url '/posts' %>"
      class="rounded-md bg-action-color px-4 py-2 font-semibold text-action-contrast no-underline hover:opacity-90"
      >Read the posts</a
    >
    <a
      href="<%= relative_url '/about' %>"
      class="rounded-md border border-border-color px-4 py-2 font-semibold text-body-color no-underline hover:opacity-80"
      >About</a
    >
  </p>
</section>

<% posts = collections.posts.to_a %>

<% if posts.any? %>
  <h2 class="text-xs font-bold uppercase tracking-widest text-muted-color">Latest issues</h2>

  <ul class="mt-4 space-y-3">
    <% posts.each do |post| %>
      <li>
        <a
          href="<%= post.relative_url %>"
          class="block rounded-lg bg-surface-background p-4 no-underline hover:opacity-80"
        >
          <span class="block font-bold text-heading-color"><%= post.data.title %></span>

          <time
            class="mt-1 block text-sm text-muted-color"
            datetime="<%= post.date.strftime('%Y-%m-%d') %>"
          >
            <%= post.date.strftime('%B %-d, %Y') %>
          </time>

          <% if post.data.excerpt %>
            <span class="mt-2 block text-sm text-muted-color"><%= post.data.excerpt %></span>
          <% end %>
        </a>
      </li>
    <% end %>
  </ul>
<% else %>
  <p class="text-muted-color">No issues published yet.</p>
<% end %>