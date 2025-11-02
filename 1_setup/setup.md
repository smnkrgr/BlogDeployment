# Setup

This note details how to setup the blog hosted for free via Github pages and prepared to be filled with markdown formatted content via Jekyll and Obsidian.

## Jekyll and Minima (Theme)
We will use the Jekyll Ruby Gem to create a static blog from markdown files.
Start by creating a public Github repo and clone the repository to your local machine.
Make sure to let Github create a .gitignore file with the "Jekyll" flavor to ignore e.g. the gem bundle folder.

```
git clone <repo>
```

Enter the repository folder, install bunder  and create a Gemfile for jekyll:
```
cd <repo>
```
Install bunderl:
```
gem install bundler
```
Gemfile contents:
```
source "https://rubygems.org"

gem "jekyll"
gem "webrick"
gem "minima"
```

Then install the required gems locally into the vendor/bundle folder:
```
bundle install --path vendor/bundle
```
And create the blog structure in the repository:
```
bundle exec jekyll new . --force
```
Now you can test locally:
```
bundle exec jekyll serve
```
Visit http://localhost:4000 to see what it looks like.
You should see a working Jekyll blog with an example post running the Minima theme.
This blog needs to be customized to your liking, which will be covered in a later section.
For now we assume this is you finished blog and cover how to publish it via Github pages.

## Publish via Github Pages
From the previous section you should have a working blog.
Stage, commit and push your working state to the repository you created and enter the Github repository settings.
In the "Pages" section of the settings, you can choose to deploy from Github Actions:
![Pages Settings](images/pages_settings.png)
For this to work, we need a Github workflow action.
Create the workflow definition file:
```
.github/workflows/github-pages.yml
```
It should contain the following for your blog to be deployed successfully:
```
name: Deploy Jekyll site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build with Jekyll
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
_config.yml base URL should match deployment settings:
```
baseurl: ""   # leave empty if deploying to username.github.io/repo
url: "https://<username>.github.io/<repo>"

```
Now when you push changes to your blog, they will be deployed "https://<username>.github.io/<repo>"

# Customization

## Theme
## Favicons
## Domain
