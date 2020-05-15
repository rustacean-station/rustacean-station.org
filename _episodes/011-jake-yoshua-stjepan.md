---
title: "RustFest Interviews Triple Feature: Rust for AAA Game Development; Async Foundations with `async-std`; and Powerful Concurrency Primitives with `crossbeam`"
date: 2020-01-22T23:30:00Z
file: https://audio.rustacean-station.org/file/rustacean-station/rustacean-station-e011-rustfest-jake-yoshua-stjepan.mp3
duration: "53:43"
length: "38682435"
reddit: https://www.reddit.com/r/rust/comments/eslbuv/rustacean_station_triple_feature_rust_for_aaa/
---

Three more interviews from RustFest 2019: [Jake Shadle](https://twitter.com/Ca1ne) on using Rust for high-performance game engines at [Embark](https://www.embark-studios.com/), applying lessons learned from working on EA DICE's Frostbite engine; [Yoshua Wuyts](https://twitter.com/yoshuawuyts) on `async-std` and Rust's async ecosystem; and [Stjepan Glavina](https://twitter.com/stjepang) on `crossbeam`, Rust's foundational library for powerful concurrency primitives.

### Contributing to Rustacean Station

<!-- You can probably leave this as-is -->

Rustacean Station is a community project; get in touch with us if you'd like to suggest an idea for an episode or offer your services as a host or audio editor!

 - Twitter: [@rustaceanfm](https://twitter.com/rustaceanfm)
 - Discord: [Rustacean Station](https://discord.gg/cHc3Gyc)
 - Github: [@rustacean-station](https://github.com/rustacean-station/)
 - Email: [hello@rustacean-station.org](mailto:hello@rustacean-station.org)

### Timestamps & referenced resources

#### [@00:00] Part 1: Game Development @ Embark Studios w/ Jake Shadle

- [@01:25] - What is yours (and Embark's) background in game development?
- [@02:14] - What is the relevance of the Frostbite engine and what is your experience with it?
- [@04:15] - What makes you think that Rust as a language is suitable for game development?
- [@06:13] - How is parallelism employed in a game engine on the scale of Frostbite?
- [@07:07] - Where is the Rust library ecosystem lacking for your use case, and what crates are you making use of?
- [@11:13] - Why is Embark interested in WebAssembly?
- [@14:20] - How can someone get in touch or learn more about Embark?
    - [embark.dev](https://www.embark.dev/)
    - [Inside Rust at Embark](https://medium.com/embarkstudios/inside-rust-at-embark-b82c06d1d9f4)

#### [@15:09] Part 2: `async-std` w/ Yoshua Wuyts

- [@15:48] - How much of the Rust standard library is `async-std` intended to emulate?
- [@17:12] - Is there anything from `async-std` that ought to be upstreamed into the standard library?
- [@19:20] - Does `async-std` run into any conflicts with the types or traits defined in `futures-rs` or the standard library?
- [@22:21] - How complete or incomplete is Rust's async ecosystem and async language support?
    - [`async-trait`: a procedural macro for providing async trait methods on stable Rust](https://crates.io/crates/async-trait)
- [@26:21] - How close is `async-std` to being a drop-in replacement for the standard library?
- [@28:32] - What's next for the development of `async-std`?
- [@30:07] - With the advent of `async-std` version 1.0, what would an eventual 2.0 release look like?
- [@32:09] - Who is using `async-std`?
- [@32:54] - How can someone get in touch or get involved?
    - [async.rs](https://async.rs/)
    - [github.com/async-rs](https://github.com/async-rs/)

#### [@34:02] Part 3: `crossbeam` w/ Stjepan Glavina

- [@34:29] - What is `crossbeam` and what is its history?
- [@36:41] - What is epoch-based garbage collection, and why would a Rust user want to use it?
- [@38:17] - How does epoch-based garbage collection compare to `std::sync::Arc`?
- [@41:30] - What is your background in concurrent programming?
- [@42:59] - How do `crossbeam`'s channels compare to those in the standard library?
- [@44:33] - How much research was involved in writing `crossbeam`?
- [@45:35] - Do `crossbeam`'s channels provide a selection interface?
- [@46:34] - What other primitives does `crossbeam` provide?
- [@48:37] - How confident are you in the correctness of `crossbeam`'s implementation?
- [@49:46] - How is `crossbeam` related to `rayon` and `async-std`?
- [@51:53] - What's next for `crossbeam`?

### Credits

Intro Theme: [Aerocity](https://twitter.com/AerocityMusic)

Audio Editing: [Zoran Zaric](https://twitter.com/zoranzaric)

Hosting Infrastructure: [Jon Gjengset](https://twitter.com/jonhoo/)

Show Notes: [Ben Striegel](https://twitter.com/bstrie/), [Zoran Zaric](https://twitter.com/zoranzaric)

Hosts: [Ben Striegel](https://twitter.com/bstrie/)
