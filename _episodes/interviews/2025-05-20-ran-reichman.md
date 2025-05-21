---
title: "Rust at Work with Ran Reichman Co-Founder & CEO of Flarion"
date: 2025-05-20T18:30:00Z
file: https://audio.rustacean-station.org/file/rustacean-station/2025-05-20-ran-reichman.mp3
duration: "56:39"
length: "20388989"
#reddit: (leave blank on initial publish, amend with link and uncomment this line after Reddit thread has been posted)
---

Gábor Szabó talks with [Ran Reichman](https://www.linkedin.com/in/ran-reichman-740163b7/), Co-Founder & CEO of [Flarion](https://www.flarion.io/), a company building high-performance data processing systems using Rust.

### Contributing to Rustacean Station

Rustacean Station is a community project; get in touch with us if you'd like to suggest an idea for an episode or offer your services as a host or audio editor!

 - Twitter: [@rustaceanfm](https://twitter.com/rustaceanfm)
 - Discord: [Rustacean Station](https://discord.gg/cHc3Gyc)
 - Github: [@rustacean-station](https://github.com/rustacean-station/)
 - Email: [hello@rustacean-station.org](mailto:hello@rustacean-station.org)

### Timestamps & referenced resources

- [@0:00] - Welcome to the [Code-Maven live](https://live.code-maven.com/) podcast, self introduction.
- [@0:55] - Welcome to the [Ran Reichman](https://www.linkedin.com/in/ran-reichman-740163b7/), Co-Founder & CEO of [Flarion](https://www.flarion.io/).
- [@1:17] - Ran Reichman introducing himself.
- [@2:00] - Can you tell us a bit about yourself?
  - [Talpiot program](https://en.wikipedia.org/wiki/Talpiot_program)
  - [Wiz](https://www.wiz.io/), [About Wiz](https://en.wikipedia.org/wiki/Wiz,_Inc.)
- [@3:11] - When did you start using Rust?
  - Background in C++
- [@3:50] - Why did you think that Rust is good for this start-up company? Is Rust good for start-up companies?
  - High expectation for reliability. No need to worry about memory corruptions.
  - A lot of interesting infrastructure in Rust such as [Polars](https://pola.rs/), [Apache Data Fusion](https://datafusion.apache.org/).
  - We like the people who are into Rust.
- [@5:35] - Inviting the audience in the live conversation to ask questions in the chat.
- [@6:14] - Have you considered other languages?
  - C++
- [@6:54] - Can you describe the type of people who you find interested in Rust who you felt are a better fit to your company?
  - People interested in Rust tend to be people curious about technology in general.
  - We have a very broad stack so we need people who wan to learn new technologies.
- [@8:15] - Is any part of Flarion open source? Is it on GitHub?
  - Flarion does not currently have public repositories. We contribute to some open source projects such as [Apache Data Fusion](https://datafusion.apache.org/) and [Apache Arrow](https://arrow.apache.org/).
- [@9:14] - How do you handle the hundreds of open source dependencies of Flarion?
  - We invest in the CI (continuous integration) infrastructure to make the build as far as possible.
- [@10:37] - How do you make sure the crates you depend on are secure and fast?
  - We rely on a very extensive suite of tests.
  - Security: mainly on reputation.
- [@12:05] - Have you considered sponsoring open source developers? Bug bounties?
- [@13:15] - Could you, please, elaborate a bit more on the nature of Rust in your use case? What do you mainly do with Rust? Do you use async Rust?
  - [Scala](https://www.scala-lang.org/), [Apache Spark](https://spark.apache.org/), [Python](https://www.python.org/), [Ray](https://www.ray.io/)
  - [JNI](https://en.wikipedia.org/wiki/Java_Native_Interface)
- [@14:30] - Besides Rust, what other programming languages do you use?
- [@15:10] - Are the new employees in the company already experienced in Rust or do they learn it on the job?
  - Most are experienced in Rust
  - Some with Crypto background because of [Solana](https://solana.com/)
  - There are a few without Rust background but strong C++ developers.
  - We try not to push Rust to the limit. Not to be too sophisticated, too clever with the language.
- [@17:36] - Can you elaborate a bit more what are you avoiding in Rust?
  - Channels, async. If it is possible we prefer to use single core.
- [@18:33] - How easy for you to recruit developers? Our company is mostly C++ and Python.  When I introduced Rust code into the Python group, for performance, I saw a lot of resistance from the developers.
  - If people (e.g. C++ programmers) don't want to change their programming language we don't try to convince them.
  - You don't want to migrate to anything, in general. You want to gradually add functionality, show value.
  - It is easier to say that "in this new team in this new project we try something else, something new".
- [@20:48] - What was the learning process and learning resources of the people who learned Rust in the company that you might recommend?
  - [The Rust book](https://doc.rust-lang.org/book/)
  - AI is quite useful: Explain this, explain that.
  - It is easier to learn a programming language by doing.
  - Getting things to compile is usually the hard part in Rust.
- [@23:10] - I do a lot of training. Practice and feedback provides the real value.
  - If you are in a Rust team, if there is a core of a team, then more juniors ask a lot of questions and seniors can help with that.
- [@24:20] - The more experienced people also learn a lot from the interaction with the junior developers.
  - The same with management.
- [@24:56] - Do you have any suggestions for someone who'd like to find work in Rust/C/etc. and is comfortable with them, but only has web dev experience (career wise)? The transition seems borderline impossible.
  - I did one thing so far now I want to do something else.
  - The solution, which is not easy, is to contribute to open source projects.
  - You have to invest a lot in that.
- [@26:53] - What should I do to increase my chances to get employed by you?
  - apply...
  - The interview process is very similar to the actual work process.
  - We want our candidates to know how they work process will look like so they understand and can decide if they like it?
  - Go to our website to see what kind of project we interact with. So look at these project, use them, you don't even have to contribute to the project.
  - E.g. learn how Polars is used.
- [@29:41] - Time-travel: What would you say to someone who has 1-2 years to prepare, what to learn to increase their chances in getting hired?
  - To be more ambitious.
  - 99% of all projects churn.
  - Pick something that interests you an be persistent with it.
- [@31:44] - Some specific types of projects to work on?
  - Game engines
  - Pick one of the big data projects in Rust. The top 15-20 Rust projects.
  - What excites me? Benchmark or test?
  - Build connections.
  - When you reach out to successful people that are technical and you engage with what they work on, the response rate is huge. People like if others are excited about their technology.
- [@33:20] - I also recommend people to invest in open source, but most people abandon it quickly. Those who do continue will stand out.
  - Most people don't go deep so if you do you are ahead of most people.
- [@34:07] - For those, a good start is trying to help in an existing open source project. What do you think about that? Contribute to an existing project or create your own?
  - Helping, even just using.
  - There is a huge variety in open source project: some are huge and robust and easy to use. Other are hard to use, rough edges etc.
  - It might be intimidating to try to contribute. Just by starting using it can be valuable.
- [@35:38] - A lot of this work is not difficult, but time-consuming.
  - [Proof of work](https://en.wikipedia.org/wiki/Proof_of_work)
- [@36:03] - How do you evaluate your decision to use Rust?
  - we don't regret it
  - benefit of starting from scratch
  - to early to say
- [@37:11] - What are the parts of Rust and crates that are exceptionally good for you and what are the areas where the Rust world could improve? Things that hurt you?
  - Rust matured in the past 5 years
  - Data Lake
  - Data processing
  - Data storage
  - There is usually a crate for that!
  - Reliability is real.
  - To be improved: shorten the build time
  - There are lots of crates that don't really work.
- [@39:45] - Follow up to finding work as a web dev: any suggestions for types of repos to that would be appreciated by employers? In your opinion of course. I'm contributing to programming languages, for example. (compilers)
  - There aren't too many companies hiring Rust developers yet.
  - Flarion
  - AWS
  - Try to understand the stack of the company and gain experience in those areas.
- [@41:57] - Companies to give home assignments to candidates fixing issues in open source projects.
  - Engage with the project of the company to gain a better understanding if you'd like to work there.
- [@43:10] - High-performance data processing is what you are "fly around inside" - so, could you share any valuable practical examples or tricks how you debug distributed and high-performance use cases? Do you use tokio for development? Or just something, like wrappers around Arrow, DataFusion, etc? Any other valuable recommendations?
  - Tests! Especially for mission critical software.
  - [Tracy](https://github.com/wolfpld/tracy) Frame profiler
- [@46:27] - What is your experience using AI tools writing Rust code? Which tools, which models do you prefer?
  - [Claude](https://claude.ai/)
  - [ChatGPT](https://chatgpt.com/)
  - [Deep Seek](https://www.deepseek.com/) [R1](https://github.com/deepseek-ai/DeepSeek-R1)
  - Where AI helps the most:
  - Understanding a huge error message
  - Basic functionality is good but does not save that much money. Percent of code written by AI is a vanity metric. Does not mean much.
  - AI isn't too good is where you need to do something complex. AI usually focuses on local minimum.
- [@49:37] - If you are talking to other founders, CTOs, technology manager, what would you recommend them how to decide to use or not to use Rust?
  - You want a champion of the technology?
  - You need someone who can experiment, mentor, make decisions then you are more likely to be successful.
  - Choosing the right project is critical for success.
- [@51:35] - What other subject would you like to talk about?
  - [Flarion on Linkedin](https://www.linkedin.com/company/flarion/) for available jobs.
- [@53:17] - What are the main technological challenges ahead of Flarion for the new people who join the team?
  - Distributed database for data processing.
  - Issues of scale
  - Memory management
  - New and interesting technologies at customers.
- [@54:50] - Who are your customers? What kind of companies could be your customers?



### Credits

Intro Theme: [Aerocity](https://twitter.com/AerocityMusic)

Audio Editing: (fill me in with the editor's name + twitter handle)

Hosting Infrastructure: [Jon Gjengset](https://twitter.com/jonhoo/)

Show Notes: [Gábor Szabó](https://www.linkedin.com/in/szabgab/)

Hosts: [Gábor Szabó](https://www.linkedin.com/in/szabgab/)
