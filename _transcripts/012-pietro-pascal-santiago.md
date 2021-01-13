---
episode: _episodes/012-pietro-pascal-santiago.md
---

* placeholder to generate bulleted TOC
{:toc}

#### Pietro Albini on Rust Release Engineering

__Ben Striegel__: Welcome to Rustacean Station, here at Rust 2019 from
Barcelona. I am here with Pietro Albini.

__Pietro Albini__: Yeah.

__Ben__: Great to have you here. You gave a talk today about Crater, and about
the Rust release process.

__Pietro__: Yeah, like, the talk was— it started, like, how can the Rust team
ensure that the— with the fast release cycle we don't have regressions.  Then it
moved into the tool that actually guarantees these, which is Crater, which is,
for those who didn't listen to the talk, it's basically a tool that fetches all
the crates, all the projects on crates.io and GitHub and compiles them with the
compiler, with stable and beta.

__Ben__: Let's back up— your credentials. You are on the Rust team.

__Pietro__: Yeah.

__Ben__: Which Rust teams?

__Pietro__: So I'm the co-leader of the Rust infrastructure team, and I'm a
member of the release team.

__Ben__: The release and infrastructure teams, okay.

__Pietro__: I'm also involved in some other teams, but I do most of my work on
infrastructure and release.

__Ben__: And I don't want to rehash the talk you gave today. We should
definitely— someone should— go watch the video. I assume RustFest has videos of
this talk somewhere. I wanted to kind of follow up on that, though, but in a way
that people wouldn't have needed to see the talk to appreciate. And so one thing
is, kind of, the— Rust has a six week release schedule. Kind of hard to ignore;
if you follow Rust at all, you get the regular release announcements and you can
do a `rustup update`, and it's very simple. And you mentioned before in your
talk, some tension with Rust 2018, where suddenly you move from time-based
releases to, like, a feature-based thing where it's, like, we want to have this
future out by this time. And it did not go very well, from what I hear. I mean,
it ended up pretty okay. Rust 2018 is a success, but it took a lot of blood,
sweat, and tears to get there.

__Pietro__: Yeah, like, we are pretty satisfied with the outcome on the release.
But that wasn't something that we can take for granted because we as a team, we
don't have experience with feature-based release cycles and, like, we broke a
lot of our internal policies, like, we made a lot of changes close to the
stabilization, or even directly on beta. And so, like, it's something that the
whole team felt a lot, and we learned a lot about that experiment, because we
started working on the edition late. I think we started planning it by the mid-
to end of 2017. And so, like, we didn't really have much time to actually get
the work done. So the period that would have been reserved to just test this
stuff, fix regressions, was really squeezed in at the end of the cycle, and we
mostly forgot about that, for the most part. So if we actually end up doing
another release, which— I don't know if we have made a decision yet whether to
do a 2021 edition. If we do that, we're surely going to, take things more slowly
and learn from the mistakes made in the past.

__Ben__: If I may speak my own personal opinion, I feel, like, people want to
extrapolate, Rust 2015, Rust 2018, so obviously: 2021. But I think in this case,
2015 came out just because it was time to do a stable release. And in terms of
2018 I feel like the most important kind of thing to change there was more like,
the non-lexical borrows— and also introducing keywords for async/await. And
there were a few very high priority features that kind of motivated, this quote-
unquote "breaking" change. And is there even a need for that in the future?

__Pietro__: Like, I'm not aware of one? I think most of the team members have
their own little wishlist, of maybe some small things that they'd love to
change.  But I don't think we have— so we have as many changes— as many possible
breaking changes for 2021 edition, like we did for 2018. 2018 also had the whole
module system revamp, which improved the learnability and usability of the
language as a whole. Like, we don't really have that many headline features to
go—

__Ben__: Yeah. So I would say, don't feel pressure to, you know, let's not try
to assume there's going to be a Rust 2021. Maybe in the future when we batch up
enough things that could be breaking changes, it would make sense. But in the
meantime, just— let's try and— there's a great talk today on burnout by
Katharina Fey. And I think it shouldn't really go into, like, open source
burnout; it was more about corporate company burnout for a programmers in
industry, but it definitely applies to open source developers, even including,
especially, Rust developers, who work themselves very hard.

__Pietro__: I mean, like, one another point of the edition was also, not just to
have a way to make breaking changes, but also to be a sort of rallying
point where we can sort of celebrate all the features that we introduced
since the previous edition. And more for a marketing point of view, and like,
then I think— I personally think those are still really useful things. Like, all
of these is just my personal opinion. It's not something that the whole team
agreed on. But, like, I don't know if using the edition mechanism to actually
make those changes is good. Like we we might want to figure out another
mechanism, I guess.

__Ben__: And it might even be a more frequent thing if you can find, like, ways
of doing it that aren't breaking. But you still want to celebrate a certain
period of time like maybe, for example, when, if— Rust recently just released,
or stabilized the async/await feature. And so— but there's still plenty to do
with regard to things to add to the standard library, language features like
async closures, that kind of thing. Maybe when that's all done, wrapped up, you
could have, like Rust 202x, where here it's like, "let's celebrate all the async
stuff we've done" but more of a marketing thing than a technological thing. So
that sounds great.

I wanted to talk to you about— you showed a slide in your talk today about
showing different languages and how often they release, where like, Python: 18
months; Java: one year. That's a new thing, even, the one year release cycle for
Java, and most languages are at one year, some are at six months, Rust is at six
weeks.  Kind of with, like, you know, showing up with web browsers. And even
Firefox is moving to an even faster release schedule, four weeks. Do you feel
any pressure to move to a faster schedule?

__Pietro__: Like honestly, no. Also because, like, it's— we are sort in a
comfortable spot.

__Ben__: Comfortable spot.

__Pietro__: Where we actually have the time to test the release to make sure
there are no breaking changes. And like, right now, if you look at— except for
1.49 when we actually added async/await, most of the releases don't have a lot
of groundbreaking changes. There are incremental changes that make the language
better, add new stable APIs to the standard library. But like, we probably don't
even have as many features to ship in a fast release cycle. Like, to be honest,
the release cycle being fast, yes, it's really useful for us because we don't
have to worry about deadlines. But still, it's work for the release team to make
releases out, because we need to write blog posts, so we need to test that there
are no regressions. So with a release team that's only made of volunteers, we
need to be careful about switching to a faster release cycle.

__Ben__: At the same sense then, does that maybe imply that a slower release
schedule is what you want? Have you considered, maybe, moving to an eight week
schedule of a six week? Would that give you more time to test, more breathing
room for beta testing? That kind of thing?

__Pietro__: Like, I think we are in a sweet spot right now.

__Ben__: You think so? It was like, six weeks, the first time we picked it out
was perfect. It was just ideal.

__Pietro__: I don't know if it's perfect, but like, it works. We don't feel, in
the release team— I don't feel like there's much pressure.

__Ben__: That's good.

__Pietro__: And like we're good at doing this, nowadays. We have processes. We
have roles inside the team, who gets to write the blog post, who gets to review
it, who does (_unintelligible— 8:31_). And so, like, I don't really see a reason
to change that, honestly.

__Ben__: Okay. Yeah, one of the themes, I guess, of this RustFest is, like,
avoiding burnout and, as long as the team itself isn't too stressed out or
pushing themselves too hard, because they're all just volunteers, so people have
to get on with their lives, their work and their personal lives. All that stuff.
So, great, I'm glad to hear that you're still rolling with it.

You also mentioned in your talk Crater, which is a tool that is used to test
for— to make sure that the Rust compiler doesn't break, so kind of like— used
to— You have crates.io and then you have the old compiler and then you have the
new compiler and you compile them both and make sure everything still compiles
and passes as expected. And you even run all the test cases, which I didn't know
about, on all the crates.io crates. So it's fantastic. You did mention that
there are a few regressions, like in one release there was, like, four, another
there were three. And are these usually, like, type inference changes, or what
is actually regressing here?

__Pietro__: Like, those regressions that you mentioned, that Crater didn't
catch?

__Ben__: That crater didn't catch. Those that were filed as issues after the
release came out.

__Pietro__: Yeah, because Crater does not have perfect coverage. Like of course,
we don't test the private code.

__Ben__: So where those in private code?

__Pietro__: Like, those were actually other stuff, because Crater is currently
running just on Linux x86.

__Ben__: Oh, okay, so other platforms—

__Pietro__: Yeah, a lot of those regressions were, for example, on ARM, or other
tier 2 platforms. And also, performance regressions or error messages
regressions are things that Crater can't catch yet. So like, Crater is not
perfect. We know there are a lot of flaws in Crater and we don't test
everything.  But still, it provides enough test coverage that people don't fear
upgrading the compiler. Like, Red Hat Enterprise Linux, which is one of the most
conservative Linux distributions, is actually starting to update their Rust
compiler every two releases on their stable release.  And the accomplishment we
made here is that we are so good of a track record about testing our releases
with Crater, that we actually convinced them to do these—

__Ben__: For enterprise users, which is very significant. I'd say.

In terms of— you mentioned a thing in the talk today that caught my attention,
which was— you mentioned that if, say, Rust adoption took off— right now out
crates.io has, like, 70,000 crates or something?

__Pietro__: I think crates.io is more about 20,000. Because Crater also, other
than crates.io, tests all the public repositories on GitHub.

__Ben__: Okay.

__Pietro__: So if Crater—

__Ben__: So Crater is using 70,000 or so.

__Pietro__: Yeah.

__Ben__: Okay. But if that ever, like, increased dramatically, it just wouldn't
become feasible economically to continue to do this. And then, what is the plan
for then? Would you only try and find the most popular crates, and then just
test those, or what?

__Pietro__: The honest answer is that we don't actually know because we didn't—
we are not at that point yet, and I think there is no point in, like,
prematurely optimizing Crater when it works great right now. Because if every
solution that we can implement is either to, just, do a longer release cycle
because we can't afford to test any more, or just test just a subset of crates.
But implementing that doesn't really make much sense at the moment, because we
just— it works right now.

__Ben__: Do you have a threshold where you feel like— so for example, right now,
you said doing a `cargo check` on every crate in Crater takes, like, three days.
And a full `cargo build` and `test` takes, like, an entire week for one thing.
And so, at what point would that become too slow? Would you actually pass a
threshold where you would need to say, hey, to the team, this is getting too
slow. We need to come up with a plan.

__Pietro__: So the plan right now, if it gets too slow, is to actually get just
more machines, because we're still at a scale where we can ask sponsors to get
us some virtual machines where can run the tests.

__Ben__: And is that the Microsoft sponsorship I saw recently?

__Pietro__: Like, we have— at the moment we have two different agents. One is
sponsored by AWS and one is sponsored by Microsoft. And there are other big
companies that want to give us agents, but we still don't need them, so we don't
want to just waste resources.

__Ben__: Fair.

__Pietro__: And, like, Crater, my personal limit is, if it takes more than three
weeks—

__Ben__: Oh, okay.

__Pietro__: If it takes more than three weeks to do a full test, it becomes
useless, because then we don't actually have the time to prepare the fixes for
the regression it found.

__Ben__: That's a good point.

__Pietro__: But, like, we use Crater not just for regressions, but also when we
get a pull request to the Rust repo that we think is probably going to break
something, we actually run a separate Crater run just for that pull request. And
so, if we get to a point where the Crater queue is too big, we can just tell the
teams to stop doing those pull requests, be our answer.

__Ben__: Okay, so you did mention you have good utilization, currently, of all
the machines, where there's pretty much always— someone's in line, waiting to do
something. But you have priorities where, hey, we're doing stability stuff, like
hold off on these PRs for a while. It sounds like you have a really good system
for making sure you have enough machines. You have plenty of room to scale,
still, with adding more machines and tolerating more delays, so it seems like
you're doing pretty good from where you're at. And I think plenty of people
still balk at the idea of, you know, I have to wait a week for my results to
come back. But I guess if you're— it's not that unreasonable to say, hey, this
is the stability of an entire project with a big, huge library ecosystem
involved, and so it's worth the time it takes to check.

__Pietro__: And also, if you are a developer on the Rust compiler, you're sort
of used to wait a lot because, like, we have, our CI is pretty slow— it takes
three to four hours at the moment to do a single test, of a pull request, and we
merge one pull request at a time. So that means that we have a theoretical
maximum of seven pull requests we can merge in a day. So, like, you're already
used to wait days in the queue before your pull request even gets tested.

__Ben__: And what I need to mention too there are rollup PRs. Which means— that
doesn't mean that only seven commits per day get committed. Because if you look
at This Week in Rust, there's often around 100 commits per week that get in, in
which I presume are from rollups.

__Pietro__: Yeah, mostly, but there are some pull requests that can't be rolled
up, because if there's some pull requests that we know are risky, that could
fail, and those pull requests— if we put them in the rollup will just break— the
rollup is probably going to fail. So there's a lot of people, especially if you
do performance improvements or CI improvements, you are pretty used to waiting a
lot of time to get your pull request merged. I guess if you're a Rust developer,
you're sort of used to that. In the infrastructure team, we try to reduce those
times. But, like, there's so much we can do, with the—

__Ben__: At some point, there's no more you can do, in terms of— you guys need
to— it's the compilers team's job to try and find ways to make the compiler
faster, I guess, or everyone's job— it's the compiler team's implementation. So,
yeah, great. Thanks for talking to us. Is there anything else you want to say,
or shout outs? Or, how can people get involved with infrastructure or any of
these other teams?

__Pietro__: So, getting actually involved in infrastructure is an issue we need
to figure out. Because to do most of this stuff the infrastructure team does,
you need privileged access to our infra. But to get privileged access to our
infra, you need to be a team member. It's like this catch-22 that you don't
actually— we don't actually know how to onboard new people.  But still, Crater
is fully open source; you can propose new features, send pull requests. And
there are other projects managed by the release team, or the infra team, that
allow easily contributors. And you're interested in working on Crater, just
contact me. I'm on the Rust Discord, pietroalbini, and on GitHub. So I'm happy
to welcome you all if you want to—

__Ben__: Awesome. Great. Thanks so much for talking to us.

__Pietro__: Thank you for asking.

(Musical break)

#### Pascal Hertleif on Developing the Developer Tools

__Ben__: Welcome to the Rustacean Station Podcast. I am Ben Striegel, live at
RustFest. I am here right now, in our improvised studio, with Pascal Hertleif.

__Pascal Hertleif__: It's very close. Try "Hertleif".

__Ben__: "Hertlief."

__Pascal__: Perfect. Perfect, first try.

__Ben__: Excellent. I am German by origin, I suppose, thousands of years ago.
Carries down in the genes. So you are here at RustFest.

__Pascal__: Yeah, long time listener, first time caller. I'm very glad to—

__Ben__: Do you want to talk about about, what song do you want to request?

__Pascal__: So, see, last night at karaoke, we never did Wonderwall, did we?

__Ben__: We could do it right now. Actually, would we— is it possible get
copyright striked on your podcast, because we might sing it so well that it
might be indistinguishable.

__Pascal__: Unlikely. I mean, you did invite me and not someone who can actually
sing.

__Ben__: True.

__Pascal__: We can try.

__Ben__: We'll save that for the extra content, after (_unintelligible— 18:18_)

__Pascal__: Looking forward to the autotuning.

__Ben__: So you're the lead of the dev-tools team, I hear.

__Pascal__: Yeah, and indeed, this year, it's an interesting team because the
dev-tools team, in contrast to many other Rust teams, and there are a lot, right
now, actually, is not a team of people who just happened to work on dev-tools,
since Rust is actually in a very good position of having a lot of different
tools that help developers out, in their daily usage of Rust, we decided to
structure the team in the way that, the actual leads of the sub-teams that
manage the tools are part of the dev-tools team. So it's like an umbrella
corporation of the sub-teams. Which is interesting because right now I am
technically only responsible for the `rustfix` tool, which has, to be fair, not
seen a lot of action this year. But my role as co-lead in this team is basically
boiling down to facilitating meetings and talking to people about what they're
doing and how we can work together to make tools interop.

__Ben__: And what tools besides `rustfix` fall under the purview, the umbrella,
of the dev-tools team?

__Pascal__: It's a long list. Let me try. So, Cargo is on the list, `rustup` is
on the list, RLS (Rust Language Server) is on the list. There are a few smaller
ones. For example, `bindgen` is technically also on the list.  Clippy. And, I'm
forgetting at least one... `compile-test`.

__Ben__: And don't Cargo and some other ones possibly have their own teams?

__Pascal__: Yes, Cargo, especially, is like, a very large team of people. In
contrast to, for example, `bindgen`. That's a project that is progressing at a
very slow pace, compared to all the features that Cargo has. It is doing one
thing, and not the whole of package managing.

__Ben__: So you say that `rustfix` hasn't had a lot of development this year,
but does it really need it? Is there, like, after the edition came out, is there
much to be fixed?

__Pascal__: Ideally, yes. But the fixing itself is pretty trivial, actually, it
is reading the compiler diagnostics output and applying it to files. So that is
what `rustfix` does. The source of the diagnostics output is in `rustc` or in
`clippy`. And that is what actually provides the fixes themselves. So we as
`rust-fix`, just apply them.

And there's one big open issue and that is having the ability to fix diagnostics
that span multiple items. So, for example, one good thing is, Rust provides the
`Default` trait. So when you implement a method called `new` and it takes no
parameters and returns `Self`, you pretty much always instead want to implement
`Default`. And maybe still keep `new` as just calling `default`, because then
every container or method that takes a thing that implements `Default` can use
your new type. So one of the clippy suggestions is, when it sees a method called
`new` without parameters, returning `Self`, it wants to to tell you, just
basically, implement `Default`. And it can do that by copy-pasting the function
body of `new` into this `impl` block, for `impl Default` for your type. That
involves two parts, though. The first part is removing the `new` function, and
the second part is inserting the new `impl` block. That is in contrast to other
diagnostics that could have multiple possible solutions. For example, if we're
not sure what to import, you might, say you're using an `Error` type and we say,
we don't know what you mean by `Error` because you haven't imported it yet, so
you might use `io::Error`, or the `std::Error` trait, actually, or the
formatting `Error`. There's multiple solutions, so this looks, right now, the
same. It is multiple fixes, and we can't differentiate between possible
solutions and one solution applying multiple things to make it work.

__Ben__: Interesting. So aside from `rustfix` and, let's leave aside Cargo for
now, some of these other ones, like `compile-test`, isn't as well known.

__Pascal__: Yeah, it's a really good crate, though.

__Ben__: What does it do?

__Pascal__: It allows you to write tests, that are especially relevant to crates
that generate code. Where you say, oh, you see, I want to have this specific
error message from my macro, for example.

__Ben__: I feel like I've seen this in the source for the Rust test suite, the
Rust compiler test, where there's little comments and they have a little arrow
and it says "error so-and-so".

__Pascal__: Yeah, exactly, that's—

__Ben__: With the UI test, they call it, possibly.

__Pascal__: That's exactly what it is, and `compile-test` is basically the same
codebase, as far as I understand it, taken out and made usable outside of the
compiler, because the compiler contains its own implementation for that, for
historical reasons.

__Ben__: So you think a crate like `syn` or `quote` or `serde`, things that
generate code, or help you generate code, or— would use this kind of thing?

__Pascal__: Yeah, I've seen used in several codebases. `diesel`, for example,
has a huge codebase. I was also previously involved a lot in `diesel`.  And we,
kind of, want to make sure that the errors users see are at least
understandable, and especially if we generate code by using a macro, we can
easily mess it up. So we want to have some consistency there.

__Ben__: That's a great idea, actually. Often, one of the downsides of using
macros is, you make errors way more opaque. But if you can test for that, to
have a regression test for, oh, our errors got worse, that sounds like a
fantastic thing for usability.

__Pascal__: Yeah, exactly. And you can make sure that your errors actually still
work. Like you don't want to generate code that suddenly allows something that
was explicitly forbidden.

__Ben__: So what else did you want to, maybe, signal boost, of the things that
you listed?

__Pascal__: Especially `rustup` has in the the past few months, seen a bunch of
features, like the latest release, for example, contains this awesome
possibility of, you're saying you want to update your nightly version, but you
require `rustfmt` and `clippy` to be there. And previously would just say, oh,
sadly, on this day's nightly, `clippy` didn't build, so I can't update. But now,
with the newest release, it will actually try to go back in time and fetch a
nightly that is newer than the one you have, that contains all the components
that you want, so you can update to the latest possible date. But talking to the
people involved in `rustup` right now, that's a lot of possibilities, but
there's only so much bandwidth that people actually have, to review the code. So
there's first time contributors, and people who want to actively be involved in
this project, but to make sure that it actually works, because it is a part of
the core infrastructure of using Rust right now, we need more people to go in
and review the code, and make sure that the newest pull requests actually don't
break anything, because it is complex and especially, `rustup` installing
something in a broken state will frustrate a lot of people.

__Ben__: You mentioned RLS. A thing that I've heard recently is a tool called
`rust-analyzer`, and I've heard it's, kind of— referring to it as both as a
replacement for RLS and even potentially for `rustc`. And we can get into that
in general, but let's give it— Can you tell me what `rust-analyzer` is? It's not
part of the dev-tools team, but you know what it is.

__Pascal__: I know what it is. I'm not sure I can precisely represent the
current status of the project. But I'll try. Take it with a grain of salt. And
don't don't trust me on the small details. It is a, right now, experimental
approach towards building a better IDE experience for Rust by re-implementing
parts of the compiler front-end, in a fashion that it's easy to incrementally
update, which is what you're doing when you're editing a source file. You don't
just paste in, like, a new module, and it's perfect the first time. You add
lines, you want to have auto-completion, and the compiler right now is— it does
have support for incremental compilation, but it historically has not been
architected in the way that it is easy to to query what is actually going on,
and to to incrementally update the trait resolution, for example. And people
felt like it would be a good idea to implement an experimental way to do that
outside of the compiler. With the intent of figuring out which parts actually
work, and moving those back into the compiler. So as I understand it, the
tokenizer, for example, is shared right now between `rustc` and `rust-analyzer`.

__Ben__: And do you think that would— isn't that kind of what RLS was designed
for? The whole, like, incrementally updating thing, especially with the IDE use
case in mind?

__Pascal__: I guess so. It always sounded to me like it was targeting the same
goals. But as far as I can tell, the technical implementation is different. Like
it is using the compiler as it is right now, and trying to tweak this source
code that we have in the `rustc` codebase right now to emit analysis data, while
`rust-analyzer` is going from from the other side, of saying, okay, we can have
these components that do trait resolution or macro expansion, and rebuild them
in isolated environments, and make sure that we can now incrementally update
macro expansion, for example. And ideally, they work together really well
because the changes made to the compiler to accommodate RLS go in the same
direction as the designs chosen to implement `rust-analyzer`.

__Ben__: Very cool. So kind of, they might just naturally fuse into one thing
over time as enough things get imported from `rust-analyzer` into `rustc`.

__Pascal__: Exactly.

__Ben__: So, pretty cool. As a lead of a team, you say that your job is mostly
to coordinate meetings. But can you give me an idea, for people who have ever
seen a Rust team in action, what is actually like? How many people show up to a
general meeting? Like, Where do you meet? How long does it take?

__Pascal__: Oh, that's a tough question, especially because the dev-tools team
feels like it's kind of special in this way because— I expect the community
team, for example, to act in a very different fashion just because they're
tackling different topics. We mostly do, right now at least, these check-in
meetings where we basically just go through the list of sub-teams we're composed
of. That is, the tools that we want to to maintain, and go around and ask, like,
how everyone's doing, what they're busy with, where they need help, if they,
maybe, need to talk to some other people from other teams, and just make sure
that there's a good flow of information going, and the way we do that is, right
now in a monthly meeting, we sometimes do this, of a video call, sometimes just
in the Discord channel, and it is pretty informal, I'd say.

I can't speak for larger teams, like the language team is way, way, way larger
than we are. And they have a bunch of very different topics they want to tackle,
so I expect them to act in different ways than we do. But it is kind of nice to
feel the connection between all these people, and that is what the team stands
for, basically, that it's not just someone who randomly says, oh yeah, actually,
I wanted to have this feature in Cargo. There is a team that is responsible for
making sure that the features compose nicely, and then it kind of bubbles up to
the next layer of teams, in this case, the dev-tools team or, in other cases,
the actual core team, where we make sure that across the whole project, this is
harmonious.

__Ben__: very cool. You did show up here with that entire notebook full of
notes. Is there anything that you wanted to talk about?

__Pascal__: Well, it is a long list, I have to say, and basically it is also the
same list of— how I liked RustFest, actually.

__Ben__: Oh, yeah. go ahead and tell me more about RustFest.

__Pascal__: Yeah, yeah, it was— so I've been to every RustFest, starting from
the first one in Berlin. I actually talked at the second one in Kiev. I was
emceeing Zurich, and it just kept going. So I kind of feel like, I can always
get the same vibe from from every RustFest, because familiar people show up,
cool stuff happens. The community always goes in with this expectation of, there
is always one more project that we haven't seen, that is really impressive. And
we want to give some new person the chance to go in and say, by the way, I'm
doing this, and if you want to help out, feel free to join in, and that is
really nice. So this RustFest specifically also felt like, this has scaled up by
quite a lot. Like, it is the largest RustFest, as far as I can tell, at least. I
don't know, 400, maybe 450 people? So you really felt like, this is on a larger
scale than the 100 people— maybe 80, I don't know— who showed up for the first
one. And it is quite humbling to see that this has— that Rust has this impact,
and that people show up because they actually, like, right now, work in Rust.
And because they see this as a language where they can immediately go in and
say, like, oh, yeah, this this all exists, I'm going to do my next project in
Rust, because why not? A lot of people are still hobbyists, of course, but to
get the feeling that it has become a bit larger than, just the core interest is
programming languages, and Rust seems to fit the bill. It is— Rust is a
household name, maybe, to a lot more people now.

__Ben__: Great. I imagine in the first RustFest, there weren't quite as many
people using it at their jobs.

__Pascal__: Yeah, yeah.

__Ben__: So, very cool. All right. And then, next one's in the Netherlands. Will
you be there too?

__Pascal__: I will try to be there.

__Ben__: You had a streak going.  You can't lose that.

__Pascal__: That's kind of the thing, right? I mean, I'm going to make sure that
there will be at least someone that looks like me. And maybe talks like me.
Maybe also, we'll sit with you and do another episode of this podcast, in the
Netherlands. But I can't promise it's actually be me.

__Ben__: "Rascal."

__Pascal__: For example. I can't tell you next year, right.

__Ben__: True, true. So, any last words?

__Pascal__: I'm actually using Rust in my job now.

__Ben__: Oh, yeah, that's right.

__Pascal__: So this also feels, like, maybe that's why this RustFest feels also
different because I'm not just going in there, paying for myself and everything,
but it feels like a thing that is related to work now.

__Ben__: Yeah, I watched you expense your tapas last night.

__Pascal__: Yeah, that's what I did, yeah. It was a company dinner, and I hope
we can actually hire you. If you haven't noticed.

__Ben__: We'll see. I mean, Sweden is very nice, some time of year, not this
time of year, but—

__Pascal__: I mean, if you really need the sun, I guess you can always fly out
to Barcelona.

__Ben__: True.

__Pascal__: Right?

__Ben__: Very nice. So, all right. Well, thanks for being on.

__Pascal__: Yeah, thanks for having me.

__Ben__: Alright, let's, 3, 2, 1... "today is going to be the day, when they
gonna throw it back to you..."

__Pascal__: You're not even playing the music.

__Ben__: I don't have a guitar on me. Next RustFest, bring your guitar.

__Pascal__: Okay, we'll do that.

__Ben__: See you around.

__Pascal__: See you.

(Musical break)

#### Santiago Pastorino on Rust in Latin America

__Ben__: Okay. Welcome to Rustacean Station. It is day four of RustFest. We get
to have our improvised studio here, so please bear with us with any audio
troubles we may be having. We have a kind of a hilarious set up right now, but
with me, enduring this, is Santiago Pastorino. How are you doing, Santiago?

__Santiago Pastorino__: I'm doing great. How are you, Ben?

__Ben__: I'm doing good. You are the organizer of Rust Latam, which is a
conference in South America. You want to tell us more about that?

__Santiago__: Yeah, it's a conference, actually, in Latin America. I'm one of
the organizers. We have a team of, like, eight people working right now. We are
going for Rust Latam 2020 in Mexico City, May 22 and 23. We have already, like a
local, which is an important local team, consisting of five people working in
the local duties. But there's also an international organization, as RustFest
also have, a similar setup. And yeah, we're kind of starting with that, we are
starting to look for sponsors, were going open the CFP, closely, probably start
to get— just sells tickets, but yeah, we're kind of just starting.

__Ben__: Great. What, like, inspired you to start a Rust conference in Latin
America?

__Santiago__: So there wasn't any, basically. I have been going to Rust
conferences since since day one I attended to Rust Camp, actually, that was in—

__Ben__: That was the very first one. In Portland.

__Santiago__: The first one, that was in the bay area.

__Ben__: It was in Berkeley, yeah.

__Santiago__: Yeah, in Berkeley. I think it was 2014 or 15, I don't remember
exactly. Then I attended to all Rust Confs, Rust Belt Rust, and some of the
RustFest. So yeah, I thought to myself, well, okay, there's conferences in U.S.,
in Europe, why not having one in Latin America too? And I knew there were a lot
of people active, more or less active in the community from there— like, for
instance, in Brazil, they invite me to a Telegram group of Rustaceans, Brazilian
Rustaceans, and to my surprise, this was, kind of, two years ago to my surprise
it was like a 700 people group, which really amuse me. Then there is a huge
community in Mexico too. In Argentina, there's people. There's people doing some
Rust, like, everywhere there. But we are kind of growing, or wanting to grow the
community in Latin America.

__Ben__: How big is Rust Latam? How many attendees do you have?

__Santiago__: So the first one was in in my country, which is very small
country, we have, three million and a half people living there, So we, kind of,
made the— so the decision was to do it there— it wasn't the only place that it
could run the thing. But actually, if— we may have prefer, like from the
attendees' perspective, to do that in Brazil, maybe, we will have way more
people. But actually we have 200 people.

__Ben__: That's really good. That was your very first Rust Latam.

__Santiago__: That's— exactly. So, probably, in a place like— if we do that in
Brazil we would get way more, I'm pretty sure. But yeah, we complicated
ourselves by making the decision. But it was— it ended turning, like, very well,
very nicely.

__Ben__: Yeah, well, 200 for your first conference is great. Like, Rust Camp,
the very first one had maybe 100. That was, you know, all of the core teams
celebrating 1.0 back then, and even RustFest, their first one was only 80 or so
people.

__Santiago__: Yeah.

__Ben__: So, yeah, it's doing pretty good. So, you mentioned doing it in Brazil?
Do you have any, like— what is the overall community like, in South America in
terms of, like, Portuguese speakers or Spanish speakers or any of that?

__Santiago__: I think proportionally, you know, Brazil is a huge country and a
lot of people. But yeah, the strongest community in Latin America is the
Brazilian one, for sure. But there are, like, from from the Spanish-speaking,
there are the rest, actually, the Spanish speaking countries in Latin America
there is a— so I would say in Mexico, with a huge amount of Rustaceans, and it's
also a huge country with a lot of population. There will be probably for the
next one, which is in 2020, I think I already said this: May 22 and 23. I guess
we're going to have a lot of, also, people that are curious to hear what's going
on. So that was basically the aim to try to get people that are not from Rust to
to show them, hey, this is a cool technology. This is kind of new, probably not
mainstream yet, but yeah, a lot of curious people are going to show up, and I
guess they're, like, start to get emboldened. They're going to like the
language. So this is more or less our aim.

__Ben__: And even Mexico City, it's like, there's no real Rust conference in the
southwest of the U.S. And so, the closest one is, like, Colorado Gold Rust in
the Midwest.

__Santiago__: Yeah.

__Ben__: So I mean, maybe someone from that area might even find their way down
to Mexico.

__Santiago__: Yeah, exactly. And we actually had a lot of people going to the
first Rust Latam in Montevideo in Uruguay. So Montevideo is the southern capital
of the world, so it's not close to U.S.

__Ben__: It's quite far, yeah.

__Santiago__: Yeah. And we had a lot of people going from U.S. Some were
speakers, but some were actually attendees. Yeah, probably this one. And I have
already heard that a lot of people are excited that this is going to be there.
I'm pretty sure that a lot of people from U.S. are going to go there. And
actually, another nice thing is that we have Central America, which— it's also
far from me, like, from from where I live. But, I am pretty sure that people
from Central America, maybe Costa Rica, Panama? I don't know exactly. I don't
know the community's exactly there yet, but I'm pretty sure that they're going.
They're going to show up there, too.

__Ben__: Can you give me an idea of what the overall software industry is like?
Like open source wise, but also in terms of people using— what languages are in
use, generally? Professionally, that kind of thing?

__Santiago__: My guess in general, and what I have seen, is it's pretty similar
over all over the world. Like, main languages are the ones that are mainstream
in general, like the stuff that is run in the JVM, like .NET stuff, these kind
of things are, I guess, what is mostly used. There's a lot of people, and— I was
in the Rust community— in the Ruby community before, and there's a lot of huge
community also in Latin America about Ruby. There is a lot of people doing
Elixir in my country also. But also, I know that there is an Elixir conference,
Latam conference, that was in Colombia, I think. So in Colombia, there is also a
lot of people, like, doing very nice stuff, using kind of, not really mainstream
languages, kind of new, like Elixir. And there's a lot of people doing Go, and I
guess it's more or less like everywhere else.

__Ben__: I guess, Elixir, is that from Latin America? I'm not sure, I think the—
who is the— do you know who the creator of that is?

__Santiago__: Exactly, yeah. You remind me about that. The creator of Elixir is
José Valim; he is from Brazil. I think he's living in U.S. now. He used to live
in Poland. I know him from the Rails community, the Ruby community in general,
but he used to do Rails work. And he was in the Rails core team. So I used to
share, like, working the Rails core team with him. I remember when he started
doing the— building the language. But yeah, it's originally from from his
company, from— out of his work. But it grew a lot in in U.S., mainly, and then a
lot of people started to use it because there there are some startups investing
on Elixir too. I think that's spread it, like, everywhere else.  So, yeah.

__Ben__: And then after Mexico City is there, a city that you have in mind for
the future? Do you want to share? Or is it a secret?

__Santiago__: No, there's no such secret or anything like that. Like, what we're
trying to do, is to have, like, the people that are involved in the organization
of the next edition. So this one, the Mexico edition, we have people from
Argentina, from Brazil. I don't know if somebody else is gonna join us too, but
we're probably going to have the next one in a place where we have a really—
organizers. So right now it's Argentina or Brazil. But yeah, like, if we keep
doing that thing, is probably gonna be in Argentina or Brazil, I guess.

__Ben__: Very cool. So what do you do with Rust? And how did you get into Rust?

__Santiago__: I got into Rust, like— first, I was doing Ruby on Rails. And I
have a consultancy company. We do like, (_unintelligible— 45:54_), like web
development with Ruby, Elixir, and JavaScript. But I started to get— I always
liked low-level programming, and I started to see Rust as a side thing for a
long while. When I was going to Rust Camp, and these conferences, I was kind off
just taking a look at Rust, and I decided to go to the conference to see what it
was like, and I always like it a lot. The community, and like, the ideas that
are in Rust, I enjoyed the way things are done, and the values that the
community share. So, yeah, I mean, first I started to like Rust, like the idea
behind Rust in that you have a way to do low-level as you do with C or C++, but
in a safe way. And like, the type system, all these things. I started to love
those things. Then, given that I was working in web development, and mainly at
that time— I mean, it's debatable if Rust is suitable for web development, in my
opinion. But yeah, like I started to enjoy more, doing more low-level stuff
rather than what I used to do. So I got involved in the community. I started to
contribute to projects, in particular to the compiler. Yeah, that's mostly what
I have spent working on, the Rust compiler. And, like, trainings and giving
workshops or talks and things like that.

__Ben__: But I guess, actually, I remember one of the ways I first saw you
working on the compiler was during the 2018 edition cycle. You were instrumental
in helping to push the non-lexical lifetimes. And that was one of your first
contributions. You're kind of just like, hey, I want to dig into this very low-
level part of the compiler, let me just try this. And everyone's just, like,
yeah. Very helpful.

__Santiago__: Yeah, yeah. Like during Rust Belt Rust. There was an impl day.
Like, it was a couple of days or three days that, I don't remember.  And Niko
was there. He wanted people to contribute. So I join him, and we were working—
yeah, he was kind enough to share a lot of knowledge with me—

__Ben__: Yeah, Niko's great.

__Santiago__: Yeah, he's great. And, yeah, like, I had the opportunity to work
with him and learn from— he has been doing Rust since a long—

__Ben__: Pretty much as long as it's been Rust.

__Santiago__: Yeah, and I also, like, from the perspective of a person that
knows a lot about compilers, it was great for me to be with him. Like, I started
compilers since a long while in university. But I mainly spent most of my
professional career working in a different field, so it's kind of— I know when I
came back to this stuff, it was, kind of, everything was new to me anyway.  And
yeah, like in the way you study things, in the theory, like on a very high
level, then this compiler doesn't work exactly the same as described in these
kind of books or these kind of courses. But yeah, this was the way I got
involved, and I still spend time doing Rust compiler stuff.

__Ben__: I think it's a great success story of people being onboarded or
mentored, and kind of, how people can contribute. So welcoming.

__Santiago__: This is great, about the community, is a lot of people willing to
mentor you if you want to do something. And, like, as much as I can, I also like
to share some— a bit knowledge that I may have. So there's always somebody
around that is interested in help getting people on board in projects. I think
that's what makes— one of the things that makes this community great. There's
people that are really curious and they want— they like to investigate things,
like, reach the best solutions possible.  And also are kind, kind of people, you
know, generous to share knowledge. And I know, like, trying to— If you're— maybe
you don't know something or you're stuck working in some particular thing.
There's always somebody that's willing to help you.

__Ben__: Is there any kind of native Spanish speaking or Portuguese speaking
Rust community that you know of, like, a forum online or some kind of of chat
channel?

__Santiago__: Yeah, in Portuguese, what I was saying: this telegram group, and I
was invited there at some point. And I used to share the space for some days. I
know there is, like a group, an Argentinian group too, they are 50 people, and
I'm there too. There are meetups around everywhere. I run the the Uruguay Rust
meetup. But yeah— not huge communities, still. It's kind of, we're in the phase
of, like, growing the communities around. And this is why I think something like
Rust Latam is important. So we, given that the conference is itinerant, we move
cities every year. So already is to like to have the event and eventually, like,
make people feel motivated about the event and the technology and the community.
And, that may help grow in communities or meet ups or groups or whatever.

__Ben__: If someone wanted to get involved with this community or if they wanted
to watch for Rust Latam's CFP, or know more about it, do you want to plug some
websites that they can look at?

__Santiago__: Yeah, we have [rustlatam.org](https://www.rustlatam.org/), and
there is the Twitter account RustLatamConf. Yeah, we are probably going to share
everywhere we can, also in the users group from rust-lang. But yeah, we're going
to spread the word, in all the possible channels that we have. So if people take
a— is taking a look or following the Twitter account or just reading users
(_unintelligible— 52:11_), they're going to figure out when when things happen.
We don't know exactly when we're gonna open the CFP yet. But just keep an eye on
that, and you will see it.

__Ben__: Great. Well, thanks for talking to us today.

__Santiago__: Yeah, thank you very much for having me.

__Ben__: Alright, see you around.

__Santiago__: This is a very cool set up.

__Ben__: What we have right now, where we're hanging out the window, to try to
reduce the echoes in this abysmally acoustic room? Yeah, it's great. So, okay,
see you.

__Santiago__: See you.
