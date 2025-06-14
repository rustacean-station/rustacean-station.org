---
title: Rust at Work - conversation with Eli Shalom and Igal Tabachnik of Eureka Labs
date: 2025-06-14T07:15:00Z
file: https://audio.rustacean-station.org/file/rustacean-station/2025-06-14-eli-shalom-and-igal-tabachnik.mp3
duration: "1:18:49"
length: "56739526"
#reddit:
---

[Eli Shalom](https://www.linkedin.com/in/elishalom/) Co-Founder and CTO & [Igal Tabachnik](https://www.linkedin.com/in/igaltabachnik/) Senior Software Engineer of [Eureka Labs](https://eurekalabs.xyz/).

In this episode, we explore how Rust is powering infrastructure at Eureka Labs - a blockchain company operating in a low-latency, high-throughput environment.

Eureka Labs is pioneering next-generation block building on Ethereum. Their work focuses on advancing the logic of block construction to support more efficient execution and expand the functionality that can be packed into each block's limited timeframe.

Eli and Igal discuss how Rust has been instrumental in developing their high-performance block builder. Before founding Eureka, the team tackled large-scale engineering and algorithmic problems across industries.

### Contributing to Rustacean Station

Rustacean Station is a community project; get in touch with us if you'd like to suggest an idea for an episode or offer your services as a host or audio editor!

 - Twitter: [@rustaceanfm](https://twitter.com/rustaceanfm)
 - Discord: [Rustacean Station](https://discord.gg/cHc3Gyc)
 - Github: [@rustacean-station](https://github.com/rustacean-station/)
 - Email: [hello@rustacean-station.org](mailto:hello@rustacean-station.org)

### Timestamps & referenced resources

- [@0:00] - The [Code-Maven live](https://live.code-maven.com/) meeting series on Rust at Work.
- [@1:14] - [Eli Shalom](https://www.linkedin.com/in/elishalom/) Co-Founder and CTO of [Eureka Labs](https://eurekalabs.xyz/).
- [@2:20] - [Igal Tabachnik](https://www.linkedin.com/in/igaltabachnik/) Senior Software Engineer.
  - [Scala](https://www.scala-lang.org/)
- [@4:00] - Tell me more about the company.
  - [Blockchain](https://en.wikipedia.org/wiki/Blockchain)
  - Block Builder
  - [Ethereum Networks](https://ethereum.org/en/developers/docs/networks/)
- [@6:13] - Do I understand correctly that you started the company without having any specific product or service in mind?
- [@7:10] - What is blockchain? What is block building?
  - [Smart contract](https://en.wikipedia.org/wiki/Smart_contract)
  - [Smart contracts on Ethereum](https://ethereum.org/en/developers/docs/smart-contracts/)
  - [NP-Hard problem](https://en.wikipedia.org/wiki/NP-hardness)
- [@10:13] - Who builds the block? Isn't the Ethereum network doing it?
  - Off-chain
- [@12:07] - Igal continues to explain what block builders do and how the Ethereum Network functions.
- [@14:40] - A block builder runs on a separate computer independent from the Ethereum Network and can be either open source or closed source.
- [@15:00] - The biggest reason we chose Rust is because there are other open source block builders we could fork.
- [@16:18] - Is your code open source or closed source?
- [@17:30] - How do you earn money from this?
- [@18:00] - The reasons to pick Rust for such a project.
- [@19:45] - Was any other programming language considered?
  - [reth](https://reth.rs/)
- [@25:45] - So Ethereum is basically just the nodes. There are many implementations of nodes.
  - [Ethereum specs and standards](https://ethereum.org/en/developers/docs/standards/)
- [@27:30] - How can new features be added to Ethereum?
  - [EIP - Ethereum Improvement Proposals](https://eips.ethereum.org/)
- [@31:14] - How many nodes are there? How big are the machines?
- [@34:29] - It sounds like the data of git except of the branching and the mutability.
- [@35:06] - How did you get started with Rust? (Igal)
  - [Scala](https://www.scala-lang.org/)
  - [Haskell](https://www.haskell.org/)
  - [functional programming](https://en.wikipedia.org/wiki/Functional_programming)
  - virtual threads / green threads / [tokio](https://tokio.rs/)
  - [Eq trait](https://doc.rust-lang.org/std/cmp/trait.Eq.html)
  - [F#](https://fsharp.org/)
  - [Constraints Liberate, Liberties Constrain](https://www.youtube.com/watch?v=GqmsQeSzMdw) talk by Runar Bjarnason.
- [@45:57] - How did you solve the problem of comparing floating point numbers?
- [@46:41] - How did you get started with Rust? (Eli)
- [@48:40] - How do you select the crates you use?
  - [Elm](https://elm-lang.org/)
- [@55:03] - How much do you use AI? Which AI tools do you use?
  - [Claude Code](https://claude.ai/)
  - [Amp of Sourcegraph](https://sourcegraph.com/)
  - [GitHub Co-pilot](https://github.com/features/copilot)
  - [ChatGPT](https://chatgpt.com/)
  - [LLMs](https://en.wikipedia.org/wiki/Large_language_model)
  - [Perlexity](https://www.perplexity.ai/)
  - [JetBrains](https://www.jetbrains.com/)
- [@1:04:05] - What should people do in order to be a better candidate for a job at your company?
  - [Vibe coding](https://en.wikipedia.org/wiki/Vibe_coding)
- [@1:07:25] - Would open source contributions be seen favorably?
- [@1:08:30] - What would you recommend other managers to take in account when selecting a language?
- [@1:10:48] - Training and mentoring new developers.
  - [Redis](https://redis.io/)
  - Learning Rust: [The Rust Book](https://doc.rust-lang.org/book/).
  - Live coding streams by [Jon Gjengset](https://www.youtube.com/c/JonGjengset).
  - [Rust for Rustaceans](https://rust-for-rustaceans.com/) book by Jon Gjengset.
- [@1:16:00] - Final notes
  - Igal can be contacted on X/twitter [@hmemcpy](https://x.com/hmemcpy) or via email at hmemcpy@gmail.com

### Credits

Intro Theme: [Aerocity](https://twitter.com/AerocityMusic)

Audio Editing: Gábor Szabó

Hosting Infrastructure: [Jon Gjengset](https://twitter.com/jonhoo/)

Show Notes: Gábor Szabó

Hosts: [Gábor Szabó](https://www.linkedin.com/in/szabgab/)

