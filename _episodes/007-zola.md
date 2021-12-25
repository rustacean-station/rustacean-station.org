---
title: "Creating Static Sites in Rust with Vincent Prouillet"
date: 2019-12-19T23:00:00+00:00
file: https://audio.rustacean-station.org/file/rustacean-station/rustacean-station-e007-zola-vincent-prouillet.mp3
duration: "54:24"
length: "52224834"
reddit: https://www.reddit.com/r/rust/comments/ed3qyd/an_interview_with_the_creator_of_zola_formerly/
---

[Vincent Prouillet](https://www.vincentprouillet.com/){:target="_blank"} talks about his experience building the [Zola](https://twitter.com/jertype){:target="_blank"} static site generator (formerly known as Gutenberg) and reflects on five years of working with Rust.

### Contributing to Rustacean Station

<!-- You can probably leave this as-is -->

Rustacean Station is a community project; get in touch with us if you'd like to be interviewed, propose a topic for an episode, or help create the podcast itself!

 - Twitter: [@rustaceanfm](https://twitter.com/rustaceanfm){:target="_blank"}
 - Discord: [Rustacean Station](https://discord.gg/cHc3Gyc){:target="_blank"}
 - Github: [@rustacean-station](https://github.com/rustacean-station/){:target="_blank"}
 - Email: [hello@rustacean-station.org](mailto:hello@rustacean-station.org){:target="_blank"}

### Timestamps

- [@00:59] - What's a static site generator?
- [@03:52] - How easy is it to build and edit a site?
- [@07:58] - Why create a new static site generator?
- [@12:35] - The Tera template engine and Vincent's experience building it
- [@17:53] - Creating filters and tests to use with Tera
- [@24:29] - What's a taxonomy?
- [@25:48] - Mapping content to URLs
- [@30:53] - The experience of being an open source maintainer
- [@33:57] - Rust crates and features used by Zola
- [@36:57] - How the Rust ecosystem ensured fast performance
- [@40:35] - Is Rust ready for web applications?
- [@43:25] - What applications are best suited to Rust now?
- [@46:50] - Issues or things you wish existed in Rust?
- [@51:08] - Helping out with Zola

<!--
In this section, leave timestamped notes of the form:

 - [@HH:MM:SS] - Topic at first timestamp
 - [@HH:MM:SS] - Topic at second timestamp
     - A link to additional material discussed during the preceding topic

-->

### References and Resources

#### Vincent Prouillet
- [Personal Site](https://www.vincentprouillet.com/){:target="_blank"}
- [@20100Prouillet](https://twitter.com/20100Prouillet){:target="_blank"}

#### Zola
- [Zola Website](https://www.getzola.org){:target="_blank"}
- [Zola Forum](https://zola.discourse.group/){:target="_blank"}

#### Tools/Crates used by Zola
- [pulldown-cmark](https://github.com/raphlinus/pulldown-cmark){:target="_blank"} (Markdown)
- [syntec](https://github.com/trishume/syntect){:target="_blank"} (Syntax highlighting using Sublime Text definitions)
- [rayon](https://github.com/rayon-rs/rayon){:target="_blank"} (Parallel computation)
- [heaptrack](https://github.com/KDE/heaptrack){:target="_blank"} (Memory Profiler)

#### Static Site Hosts
- [Github Pages](https://pages.github.com/){:target="_blank"}
- [Netlify](https://www.netlify.com/){:target="_blank"}

#### Crates for Web Applications
- [jsonwebtoken](https://github.com/Keats/jsonwebtoken){:target="_blank"}
- [Bcrypt](https://github.com/Keats/rust-bcrypt){:target="_blank"}
- [Validator](https://github.com/Keats/validator){:target="_blank"}

#### Compiled Template Engines
- [askama](https://github.com/djc/askama){:target="_blank"}
- [maud](https://maud.lambda.xyz/){:target="_blank"}
- [horrowshow](https://github.com/Stebalien/horrorshow-rs){:target="_blank"}

#### Runtime Template Engines
- [Tera](https://github.com/Keats/tera){:target="_blank"} ([Jinja2](https://www.palletsprojects.com/p/jinja/){:target="_blank"}-like HTML template engine)
- [ramhorns](https://github.com/maciejhirsz/ramhorns){:target="_blank"}
- [rust-mustache](https://github.com/nickel-org/rust-mustache){:target="_blank"}

#### Static Site Generators
- [Hugo](https://www.gohugo.io){:target="_blank"}
- [Jekyll](https://www.jekyllrb.com){:target="_blank"}
- [Pelican](https://blog.getpelican.com/){:target="_blank"}

#### Other links
- [Forestry](https://forestry.io/){:target="_blank"} (WYSIWYG CMS for Static Sites)
- [Keyword Arguments RFC](https://github.com/rust-lang/rfcs/issues/323){:target="_blank"}
- [kickstart](https://github.com/Keats/kickstart){:target="_blank"} (Scaffolding tool)

### Credits

Intro Theme: [Aerocity](https://twitter.com/AerocityMusic){:target="_blank"}

Audio Editing: [Jeremy Jung](https://twitter.com/jertype){:target="_blank"}

Hosting Infrastructure: [Jon Gjengset](https://twitter.com/jonhoo/){:target="_blank"}

Show Notes: [Ben Striegel](https://twitter.com/bstrie){:target="_blank"}

Hosts: [Jeremy Jung](https://twitter.com/jertype){:target="_blank"}
