# erleben.github.io
Erleben's Personal Web Page repository, go have a look at the real thing

https://erleben.github.io/



# Setting up local Jekyll

First do this

``` bash
cd xxx/docs/
bundle init
emacs Gemfile
```

In Gemfile make sure to add

``` bash
source "https://rubygems.org"
gem "github-pages"
```

Now do this

``` bash
bundle add jekyll
bundle update
bundle exec jekyll serve
```

Goto [http://localhost:4000/](http://localhost:4000/)

