---
episode: _episodes/011-jake-yoshua-stjepan.md
---

* placeholder to generate bulleted TOC
{:toc}

#### Jake Shadle on Rust for AAA Game Development

__Ben Striegel__: Welcome to the Rustacean Station podcast. I'm here live at
RustFest. I will continue to misuse the word "live" until someone stops me. I am
here with Jake— I didn't get the last name, Jake.

__Jake Shadle__: Shadle.

__Ben__: Jake Shadle, with Embark, one of the sponsors of RustFest. And I came
to RustFest, I saw this great big banner, just with the words "Embark" over a
night night sky and an astronaut looking longingly at the stars with no other
information about what Embark actually does. Apparently, they are some kind of
game development company, which, I thought to myself, I must interview one of
these people, because it's a very— game development in Rust is actually one of
the longest, like, hobbyist use cases in Rust. I can think of, like, `piston` as
one of the oldest big Rust projects. Still ongoing, as far as I know. But
apparently, you have actual triple-A industry experience. And you come from that
background and so, I wanted to kind of talk today about just, your background
in, I presume C++, what got you into Rust? How ready or not-ready you think Rust
is, for this kind of field. But let's not get into that too quick. So you are
Jake. And you are— what's your experience in triple-A games?

__Jake__: So I've been working in games for about 12.5 years. A little bit in— a
couple of years in Austin, Texas, and then, I moved to Sweden and worked at
Frostbite, EA's internal engine for most of the games now, and, worked there
for, like, six years before joining Embark about— actually, earlier this year,
like January, and Embark just celebrated its one-year anniversary on Friday. So
we're a pretty young studio, made up mostly of former DICE people, but also
other people around Stockholm, and Europe in general.

__Ben__: and in case people know video games, but not what Frostbite is. Can you
name some games that use Frostbite?

__Jake__: Well, Battlefield is a big one. Battlefront, the Star Wars—

__Ben__: Lovely game.

__Jake__: Need for speed.

__Ben__: Visually, very impressive.

__Jake__: Yeah, it's been known throughout the industry for its high graphical
fidelity, which is annoying because a lot of people call it a graphics engine,
which it does way more than that, but yeah, so basically, I've been working with
Rust. There is some Rust code in Frostbite. I don't know how many people know
that, still, that work there. But there's a bit of it, and— yeah, I just was
drawn to the language for you know, the typical reasons of safety and all the
stuff that I like from C++, but don't like about it.

__Ben__: Choosing your words carefully there.

__Jake__: So yeah, I've been using it, kind of internally, like on personal
projects and stuff. And then the opportunity came to work at Embark, and our
CTO, who's also former Frostbite, was, you know, had picked up Rust earlier, and
was like, this is a great language, and I want to use it. And, yeah, so this— it
became, like, our primary language for our long term projects. We're also doing
other projects right now in Unreal, so those are still C++. But yeah, Rust is
our, kind of, long term future.

__Ben__: Okay, so the plan is to entirely rewrite Frostbite in Rust. Rust bite.

__Jake__: No. Because then we would get sued or something.

__Ben__: Oh, that's true.

__Jake__: Yeah, but no, I mean, we're doing, like, we're kind of making a game
engine, but not really a game engine. It's— it'll— Yeah, we'll share more as we
get more—

__Ben__: I don't want to press you for too many details just yet. It seems like
they're still in the initial phases.

__Jake__: Yeah, we're still very, very early.

__Ben__: I wanted to get your impressions on Rust as a language. You mentioned
you like the safety aspect of it. I know that what I've heard in the past,
especially when Rust was very young, was that game developers, especially, they
care more about iteration speed than about memory safety. What's your opinion on
that?

__Jake__: Yeah, So, I mean, iteration speed is definitely very important. And
there are a lot of good things that you get out of faster iteration because you
can try out more ideas, and all that kind of stuff. But at the same time, like
when you're shipping a game, typically, the thing that you're doing at the end
is, you know, optimizing performance, but also tracking down that one bug that
you've had for like, two years, that has never been such a big problem that you
need to fix it but is now shipping out to, you know, hopefully millions of
people, and you do need to fix it. And, you know, data races. And that's just
getting worse over time because, you know, previously you would maybe have two
threads on the CPU to actually do anything. So it wasn't like, a huge issue to
have data races and stuff because they weren't— they weren't very frequent. But
now that, you know, you have to have more and more threads to actually be able
to do anything, at least on the CPU, means that you're going to have more and
more problems that come with that. So Rust, kind of eliminating whole classes of
bugs, just means you can spend more time on the things that actually matter. And
to me, the trade off is definitely worth it. Like I, in my opinion, the
differences between C++ and Rust compile times for, like, equivalent code—
that's really hard to define, which is why you can't really do a one-to-one
comparison. But it's like, to me that, they're not really that wildly different.
So, yeah, I'll definitely take a similar compile time for way fewer debugging
hours in the future.

__Ben__: Talking about parallel stuff, like, how thoroughly parallel is an
engine like Frostbite, in terms of, is it, like, a few threads? Is it, like,
1000 threads? Is it—

__Jake__: So Frostbite is like super complicated. It has pretty advanced thread
scheduling and it has a whole job graph job manager, that it basically has a
graph of tasks that, I mean, you're rendering and a frame is generally, like, 16
milliseconds or less. So you have to do, you know, thousands, tens of thousands
of things in 16 milliseconds. Every single minute, every single hour. So it's
pretty intense and a lot of work was put into it, and is being put into it. But
yeah, it's a really hard problem. We've actually talked— like, that's another
thing that, kind of, Rust doesn't really have a good story for at the moment,
like, it has really nice— like, `rayon` and `crossbeam` and stuff are really,
really good, but they're not really made for games.

__Ben__: In what way, like low latency?

__Jake__: Well, it's just— there's certain things that you have in games that,
kind of, are— so one example would be a linear frame allocator, where you have
this nice advantage of, if you just have a linear bump allocator. So you could
just do a bunch of allocations that are super fast because they're pre-
allocated, and then you know that you're going to, say, dispatch to the GPU, if
you're doing, like, draw calls, and so you can allocate a bunch of stuff. But
then you have this convenience where, you know, once the thing has been pushed
to the GPU you can deallocate that memory, but instead of deallocating it and
doing, like, clean up on all that kind of stuff. You just reset the pointer to
the beginning and then start again the next frame. And that's something that you
can't do in a general purpose thing, but because you're in a game, you have the—
you know, all the context and stuff. So certain things like that, I think, will
percolate into Rust and more of the general libraries as more and more games
start being used. And it's one of the things that we've been doing for months is
basically, for certain crates that we use, getting our use case in or improving
it so that we can do what we want with it. And that's just, like, a lot of work.
But I mean, that's also why we sponsor things like Amethyst, because—

__Ben__: Very cool.

__Jake__: Even though we don't use Amethyst ourselves, like, if they improve a
crate for them, that's maybe also improving it for us. And so, it's well worth
the money that we give them.

__Ben__: What kind of crates do you use? Like, can you name some?

__Jake__: Yeah, well, so—

__Ben__: What are your favorite crates that you use?

__Jake__: What are our favorite crates?

__Ben__: Open source, public crates.

__Jake__: Yeah, well, I have our least favorite crate is probably `openssl`.

__Ben__: OK.

__Jake__: We'll say that. Let's see. What's our favorite crate? I mean, we use a
lot of the classics, I guess, like `serde`, and—

__Ben__: Any that are specific to game design, or people haven't heard of?

__Jake__: Anything specific? Like, right now, not really. I don't think— I can't
think of any off the top of my head.

__Ben__: Which crates were you forking to add in this kind of bump allocator
support?

__Jake__: We haven't— well, we didn't fork any crates for that yet, but like,
that kind of stuff, we will be adding more into, and all that kind of things,
but most of the stuff that we've open sourced so far have been tools that we've
developed and then, also a lot of pull requests to bump versions and make things
easier to use, and things like that. But, you know— what is our favorite? Yeah,
I don't know. We're doing a lot of current stuff, like `http` and `serde` and
things like that, so yeah, we're using `reqwest`, because it's pretty nice. Oh,
yeah, we're also using `tonic`, the gRPC thing. That's still in alpha, I think,
but is going to be hopefully released officially pretty soon.

__Ben__: What does a game engine want to use a gRPC or http for?

__Jake__: So we're not really doing, like, a game engine in the traditional
sense, like Unreal or Unity or anything like that. It's more of a toolkit for
other people to make games. So yeah, we're going to— it's not going to be the
same kind of constraints that a game engine has. And then also, we'll be pulling
in services in the cloud, and things like that. So there's going to be a lot of
interaction between different opponents and stuff. And then, one thing we're
really interested in is wasm, that's actually one of the top three reasons to
use Rust right now, for games specifically, is because wasm and Rust are just a
really great fit right now. Rust is easily the best language for doing wasm,
because not only is it compiled to wasm, but most of the great wasm runtimes
like Wasmer, Wasmtime, are all written in Rust. So there's a really nice
ecosystem around that right know, that we're really interested in.

__Ben__: Great. Are there any wasm crates that you can talk about that you like
a lot?

__Jake__: Yeah. I mean, right now we're using Wasmer for our runtime and it's
really quite good.

__Ben__: What is Wasmer? I'm not familiar with it.

__Jake__: So Wasmtime is kind of Firefox's or Mozilla's wasm runtime, to load
wasm binaries and execute them in a sandbox. Wasmer's a different one that still
has a lot of the same features and stuff. But it, for us, Wasmtime at the time
didn't have good Windows support, but I think that's hopefully getting better
now. But yeah, Wasmer's another, kind of, alternative runtime.

__Ben__: So this would let you actually run wasm compiled applications outside
of the browser? Is that the idea?

__Jake__: Yes, outside of the browser, Yeah.

__Ben__: So why would you want to do that?

__Jake__: Well, because, so browsers have a lot of restrictions, and those are
sometimes, you know, when you're browsing the web, they're good restrictions.
But when you're going to have a high performance application they're maybe not
so good. So we're doing— basically right now, we have, like, Vulcan and wasm in
a desktop app for Linux, Mac, and Windows. And so we can do high performance
desktop stuff. But also, you have the guarantees of wasm, so it's, like, a
really nice way to have small sandbox code to do things that you don't have to
trust, and can be from, you know, whoever.

__Ben__: Great. Okay, that sounds fantastic. Do you think you'll anything to
show any time soon? With regard to, like, an actual— a Pong clone that we can
run?

__Jake__: Yeah. so we have been working recently on this idea of getting our
stuff into a state where we can hopefully sent a tweet out with a link, and then
you can actually download the client. And then the link is actually a deep link
into the application. And so you can— yeah, we don't know what we're going to
release yet. We have a lot of stuff, but we're trying to, like, find actually
the best thing to release, and we might get it before the end of the year or
early next year. we'll have something, hopefully to show.

__Ben__: Okay. Very cool. All right. Thanks for talking to me, Jake.

__Jake__: No problem.

__Ben__: If people wanted to get in touch with you, or learn more about Embark,
is there any kind of website you want to point them to or chat channel or—?

__Jake__: Yeah. So I think the best site that we have is embark.dev, that
basically has links to all of our open source projects, links to, like, the
sponsorships that we're doing through GitHub sponsors and Patreon, and all those
kind of things. And then I think it also probably will have email links and
stuff to us so that you can open a communication channel.

__Ben__: Great. Well, thanks so much. I'll let you get back to whatever you were
doing before I grabbed you by the collar and dragged you in here.

__Jake__: Yeah, thanks.

__Ben__: Awesome.

(Musical break)

#### Yoshua Wuyts on Async Foundations with `async-std`

__Ben__: Welcome to Rustacean Station. I'm Ben Striegel here, live at RustFest.
No one has yet stopped me from using the word "live" on these clearly-
prerecorded episodes. I will continue to do so. I am here now with Yoshua Wuyts.

__Yoshua Wuyts__: Yeah.

__Ben__: Did I get that correct? Why don't you say it yourself so that everyone
knows.

__Yoshua__: Yoshua Wuyts.

__Ben__: Wuyts, I see.

__Yoshua__: That's Dutch.

__Ben__: Dutch. Excellent. Oh, that's where we are having a RustFest next year,
I hear.

__Yoshua__: Yeah, I'm very excited for that.

__Ben__: Oh, yeah. is it in Amsterdam? They didn't say the city.

__Yoshua__: No, they haven't.

__Ben__: Okay, curious.

__Yoshua__: I'm hoping not.

__Ben__: No?

__Yoshua__: It's always in Amsterdam.

__Ben__: But, like, I want to go there really bad. I need an excuse to.

__Yoshua__: We'll see.

__Ben__: Anyway. So you are a contributor to `async-std`.

__Yoshua__: Yes.

__Ben__: And I wanted to— it's a big topic right now, async stuff, and so for
me, I know I had a talk from Florian today at RustFest kind of going over what
`async-std` is and does. But still, I want to talk more about the broader, like,
high-level stuff where, for example, if I am just (_unintelligible— 16:06_) and
it seemed almost like they don't— wanted you to never have to import `std` at
all. So does `async-std`, for example, export things like `Option`, which, you
wouldn't ever think would need to care about futures— which, I hope not. Does
it?

__Yoshua__: Well, you'd be surprised.

__Ben__: Surprise me.

__Yoshua__: Well, `Option` implements `Iterator`, right? And we have an
asynchronous version of `Iterator` called `Stream`. So in a perfect world, or—
well, it does implement— yeah, so implement— it implements `IntoIterator`, so it
can convert an `Option` into an `Iterator`, which is nice when you're combining
things. We may someday want to implement `IntoStream` for it, and have its own,
like, dedicated stream type, so we might explore `Option` at some point.

__Ben__: That's a good point. So in terms of— I can pinpoint, kind of— I'm still
working on the async ecosystem. Because I was, kind of, trying not to look at it
until it was stable. And it's kind of getting there, and so maybe now I'm— just
want to learn about it, which I figure plenty of folks are in the the same boat.
And so I can think of a few things where it's like, `Stream` seems like a pretty
fundamental piece. Would that be, kind of, would that go next to `futures`, say,
in the `futures` standard library? Like, someday. I guess let me back up. Do you
feel like there are things from `async-std` that should go in to actual `std`?
Like, they actually belong there.

__Yoshua__: That's a very interesting question. So I think the things that are
closest to being merged into `std` are part of what is called the `futures-core`
library.

__Ben__: That's `future-rs`.

__Yoshua__: Yeah, `futures-rs`. And the library is split up into multiple parts.
Most people, they use the `futures` library. So, put `futures` in your
`Cargo.toml`. But there's another library, which is like the core parts of that,
called `futures-core`, which is now 0.3.1, I believe now. And the `Future` trait
used to be part of that, but has moved into core, and there's a few others, but
the most predominant one, the one that everyone is using, and seems to be
agreeing on is the shape of the `Stream` trait.

__Ben__: `Stream`. Okay.

__Yoshua__: So I think that would indeed be something—

__Ben__: I'm not sure how, like, in-tune you are with Rust development, with the
library team and that kind of thing. But do you feel like, in the next year or
so, `Stream` might be accepted? Or you're not quite that optimistic, or you
don't want to say?

__Yoshua__: So it's hard for me to, like, gauge whether or not something will
happen. There's often times independent RFC, and people have opinions—

__Ben__: And there isn't even an RFC—

__Yoshua__: Exactly.

__Ben__: —for all I know, for this kind of thing?

__Yoshua__: But I think everyone in the ecosystem is agreeing on the shape of
this. And if everyone's agreeing on that, then it seems logical to at least
start putting into nightlies.

__Ben__: Great.

__Yoshua__: So I would like to see it.

__Ben__: I was looking at a few things today, in Florian's presentation. It
seemed like `Stream`— some things were pretty cool with that.

__Yoshua__: Yes.

__Ben__: And I know for a long time, people have asked for, kind of, streaming
iterators as a concept. And I'm not sure if that— if they were using streaming
in the same way that you are?

__Yoshua__: Ah, no.

__Ben__: Okay.

__Yoshua__: So, confusingly, the phrase "streaming iterator," could also be
called "iterable iterator." It's something with borrows and lifetimes. So, yeah,
dammit, I don't really want to get into the details.

__Ben__: Let's not worry about that.

__Yoshua__: It's used differently.

__Ben__: We're here about async stuff. So actually, what you were— to get back
to the `async-std`— so the `Option` example. So there are, for example, plenty
of `std` types that actually do want to have, certain— I'm not sure if you
export `Option` from that crate, but they want to implement things for `Option`.
And if the `Stream` trait is from futures, and— do you have to wrap something to
get around coherence?

__Yoshua__: No, not quite. You're asking, like, all the questions that are like,
well, let me break it down into the sort of murky explanation—

__Ben__: I'm here all day. Go ahead.

__Yoshua__: No, so, what you really like is for certain types such as String— so
the— a very nice thing you can do with iterators is you can `collect`. So you
have an iterator, and then you do a `map` or something, and you say, OK, now
let's collect all this stuff back into a `Vec`, or a `Result<Vec>` or back into
a `String`, right? There's always types. And the way this mechanism works is,
something like a `Vec<T>` implements `FromIterator`. And then you can be like,
okay, cool. So from an iterator into a vector, there's a transition path there.
Right? Now it's very nice to have an asynchronous version of this. Imagine
you're doing a bunch of calls to a database, right? So you get a bunch of, like,
queries or something, you do some transformation on it. And then you say, like,
cool. Let's write this this list of struct or whatever back into, like, an array
and then let's continue from there, or a vector or whatever.

But having an asynchronous version of `IntoStream` and `FromStream` is extremely
useful, next to having, like, the `Stream` trait. Unfortunately, these are not
defined in the core stream or in the core future, sorry— in the `futures` core
library yet. That's an invention that we've come with—

__Ben__: So `async-std` defines these `FromStream` traits.

__Yoshua__: Exactly.

__Ben__: Okay

__Yoshua__: And indeed, due to coherence, we can implement it one way, namely,
we can we can make `collect` work, but we can't say, for example, here's a `Vec`
of numbers, `.into_stream()`. So that would indeed require for these traits to
go into `futures-core` library, and then move from there. But, you know, I'm
optimistic that we might get there.

__Ben__: It's good to have upgrade paths, where it's like, you know, you can do
experiments with— (_unintelligible— 21:30_), some time, with some kind of thing,
and then gradually it becomes more and more— like goes from de-facto stable to
de-jure stable, which is a pretty decent way of doing things, I think.

__Yoshua__: We're seeing a really fun one there, recently, where we looked at
(_unintelligible— 21:42_), I guess someone pointed out to us that in the RFC for
async/await there was a mention of the `IntoFuture` trait that would be accepted
and we were like, oh, that's nice. Cool. Let's add it to `async-std`. Right? And
then someone from `tokio` project, or— I wrote a blog post about it, and someone
from `tokio` project saw it, and was like, yeah, that's indeed really nice, and
they put in the work to put it into, not just `futures-core`, but they just went
straight to compiler and were like, hey, here's the thing, and here's a patch,
and now it's, I think, either being merged or already merged.

__Ben__: Nice.

__Yoshua__: So, yeah, like we're all building these things, that's really cool.

__Ben__: And I guess, kind of the broader theme here is, now that, you know,
async/await is stable, it's kind of— maybe back up again. Back when, like, the
future trait was stabilized earlier this year, in summertime, people are like,
now we can finally use futures on Rust. Well, not really. You still gotta wait
for a while, and now it's kind of like, oh, async/await is here.
(_unintelligible— 22:32_) Can I use it now? Well, it depends on what you're—...

It seems like, when do you feel, like, the state of Rust itself, and all the
foundational library is gonna be such that people can just, without having to,
like, worry about things breaking under them, or too much changing, when is it
going to be actually great? Do you feel like— is it almost there? Is it really
far away?

__Yoshua__: Yeah, so we're really close. I think we're mostly there. The two
biggest things that we're sort of waiting on to be built, at all— something just
went through the headset, sorry, but— the two things that we're, like, waiting
on, really, is async closures, which are useful so you can borrow into a
closure, and give the borrow back, because you can't do that with closures and
async thing. And async traits, because implementing a trait requires an
associated future type that you return as a parameter. It's very complicated. It
would be really nice— once was these things truly exist then almost all of
synchronous ergonomic Rust would be expressable in asynchronous Rust as well.

__Ben__: Yeah, I've heard about async trait, and I can't think of it— right now
we have the— David Tolnay has a crate, where you can fake it—

__Yoshua__: Yeah.

__Ben__: Where you put this attribute on a trait method or in an impl. Or maybe
both, I forget. And then it implicitly boxes things, but it looks real nice.

__Yoshua__: Exactly.

__Ben__: But I haven't heard much about async closures. It sounds like it would
have been part of the original async/await RFC. Is that just not implemented? Is
it accepted?

__Yoshua__: So it used to be. Actually it used to be part of the same feature
flag, the async-await feature flag. And then it was decided that it wasn't ready
to stabilize yet, because of— it just wasn't. And so it's been moved to its own
feature flag, called `async_closure`. And, it's a separate feature. Sort of, the
idea there is, imagine you have an iterator, and you would like to call `filter`
on it, but an asynchronous filter so you don't consume the item, you get a
borrow into the item, and then you say, well, should this be continued? Yes or
no? So you return a bool. That, in asynchronous form, you can't give the
borrowed item into an async filter, just doesn't work today. So async— and
there's a few more, like an async version of map. I'm doing a shitty job of
explaining there, but there's a lot of patterns that we're still waiting on.
They're just not there.

__Ben__: I'm supposed to ask one more, kind of like, nitty gritty question in
this area. I know there is, like, there's the `Fn` trait. There's the `FnOnce`
trait, and the `FnMut` trait. Would that involve a new, like, `FnAsync` trait or
something?

__Yoshua__: I haven't talked to the lang team about this. And so this is not me
having inside information, this is just really, like, being like, I think the
answer is yes to all three of them. We'd have async versions of all three.

__Ben__: Oh, you would have, like, a async move fn and then async mut fn.

__Yoshua__: Yeah, exactly. `AsyncFn`, `AsyncFnOnce`, `AsyncFnMut`. I think. But
a cool thing, I think. Again, I might be entirely wrong because I haven't talked
to the lang team. They prove me wrong all the time. But you could implement
these for synchronous closures as well. So I could have a function called `map`,
that you can give an async closure, but you can also give a synchronous closure,
because going from a synchronous to asyncronous closure is just, wrap it inside
of an async block. So it's a very easy upgrade path. So, yeah, once we have
those, that that would be very nice. If this could work it'd be great.

__Ben__: I guess they— is the async/await RFC still up to date with the kind of
design, or is it gonna be like when they destabilized or made it its own
feature, do they kind of say, hey, we're gonna rethink this.

__Yoshua__: I think all of these will need their own RFCs for sure.

__Ben__: Okay. Cool. So look out for those in the future. I want to ask about—
speaking of upgrade paths, kind of, say someone is just writing their own
application, and they're like, oh, they get pretty far and like, oh, I need
async in here. And so, at that point, are they just going to, like, you know,
happily— import `async-std` and then re-map all of their, like, `std` types to
`async-std`, and it's all going to work out for them? Or do you think that— do
you also change signatures, say, of various things? I feel like you must have
to.

__Yoshua__: Well, yeah, we have had to, for sure, but not as much as you might
think we had to.

__Ben__: No?

__Yoshua__: Yeah. And most of the signatures that have been changed, are kind of
due to lack of language features. So all the async traits, we couldn't do one-
to-one mappings because you can't have `async fn` in the trait, right? Same for
like, async closure, right? It's all the streams, combinators, and all those
things. There are not quite async versions of it yet. There's some gotchas
there, but— oh, and the third one I guess, is stuff like `Mutex`, like poisoners
don't make sense in async context, because the way panics work is very
different. But I think, besides that, for most of the code, you could almost
write a code mod that adds, like, "replace std with async-std" and then "add
`.await` for all the calls and then you're done.

__Ben__: With regard to poisoning, I feel like there's a long term plan to, kind
of, replace the `Mutex` in `std` with `parking_lot`, so now it doesn't poison at
all and so maybe that's a decent dovetail. But also, I want to ask about— so if
you have an IO, like the— a file system API, do you have— do you try to, like,
have just `open`, and then in the `async-std` it returns a future?

__Yoshua__: Yes.

__Ben__: Or is there, like, an `open_async` version.

__Yoshua__: No! Just `open` returns a future, because it's a separate type.
Instead of, like, having both the synchronous and asynchronous on the same type,
we decided to create new types, because it would be a little bit clunky to be,
like, `file.async_open().await` inside of an async function becomes, like, you
see the word "async" everywhere. It's not as nice.

__Ben__: Well, then, what's this new type, then?

__Yoshua__: It's called `File`.

__Ben__: It's `File`, but it's `async_std::fs::File`.

__Yoshua__: Yes.

__Ben__: Okay. Interesting. Okay, that seems to make sense.

What's the next step for `async-std` now that futures, or async/await is
stabilized, and you have a release, I think next Monday, you said?

__Yoshua__: Yeah, tomorrow.

__Ben__: That's tomorrow. That's right. Yeah, so tomorrow there should be a—
we're not gonna have this, I guarantee you, ready to be edited by tomorrow, so
anyone listening will be like, oh, yeah, That's stable by now.

So now that that's done, what do you think the next, like, steps are?

__Yoshua__: Good question. Well, it's not done-done yet. We have a bit of a push
to go, to practically, like, release this. But from there on out, there, we have
a lot of things that are still marked as unstable, that require a feature flag
to enable. So our first pass is to, like, take a good look at that. Like, are
there any obvious candidates to stabilize? Right? Are there any things we're
unsure about and would like more feedback about? Is there any documentation that
we need to change, that kind of stuff.

__Ben__: How is documentation for `async-std`? If someone wanted to use it and
learn it, oh, it doesn't look very good. (_unintelligible— 29:26_)

__Yoshua__: I've spent many hours on it.

__Ben__: That sounds like a good thing, right?

__Yoshua__: Yeah.

__Ben__: There is some, and people can care about it, it seems, or at least you
care about it.

__Yoshua__: I'm gonna going to be a bit less modest there, and I'm going to say
our documentation is quite good.

__Ben__: Quite good.

__Yoshua__: Yes.

__Ben__: Excellent. All right. Perfect. It's good to know.

__Yoshua__: Yeah.

__Ben__: Because people don't want to just, like, go in there and be, like, you
know, I mean, look at the rust doc, and it's just signature and be like, nope, I
got no doc-comments, nothing.

__Yoshua__: Yeah, no, no, we have, like, examples for almost everything.

__Ben__: You want to examples, you want little "hello world"—

__Yoshua__: (_unintelligible— 29:56_), error types, all the—

__Ben__: Fantastic. Good to hear. It's very important for usability, especially
in Rust. We value that a lot. That's also— I had a different question. So today,
again, at Florian's talk, he mentioned that because of language changes in the
future, there is probably going to be a `async-std` 2.0, someday.

__Yoshua__: Yes.

__Ben__: And do you— can you talk more about like— what things are you
stabilizing in 1.0 that you think would need to change for a 2.0, or might
change, like you mentioned some things in the language, like the async `fn`
thing, but what would actually change about the `futures` interface?

__Yoshua__: Right. So I think it might be good to take a small step back and be
like, what does a 2.0— what does a major upgrade actually encompass? So,
breaking change. In our case, using a new dependency, like if `futures` 0.4
comes out, it's not an automatic upgrade, like, that is a breaking change,
right? New language features are breaking changes. But when people hear breaking
changes, they might be like, oh, it's a completely new thing. I need to rewrite
everything. And no, we're pretty much done with the interface. Like, these are
the details that wouldn't automatically work, and your build would break. But we
think our upgrade path— or we want the upgrade path to be super clear, right?
We're not going to change method names. We're not going to do all these things.
Maybe a few. Maybe we realize we've made mistakes, and it's a good chance to
change them. But the upgrade path should be, essentially for most people,
upgrade the version from 1.0 to 2.0, upgrade your compiler version to the right
one, and fix a couple lints here and there. Right?

__Ben__: Okay.

__Yoshua__: And that's it. Like, painless.

__Ben__: I think though— I mean, a lot of, like, anything to aspire to call
itself `std` has to worry about, like version compatibility, where you have two
projects, one's on this version, one's on that version, so have— do you foresee
that being a problem in the future?

__Yoshua__: No.

__Ben__: Okay.

__Yoshua__: No, not really. I mean, like, breaking changes are always a question
of, how do you upgrade? And I think if we can do the right communication from
the start, which we're trying to do, by the way, and provide good upgrade
guides, then we'll see, like, you know, there will be a small period where
things are— people are upgrading, its a little murky and then, we're upgraded
and we continue on.

__Ben__: Do you know of anyone, kind of, using `async-std` in a big capacity to
test, like— (_unintelligible— 32:12_), to pummel it for a while, run it through
its paces?

__Yoshua__: Well, we've been doing that ourselves, internally, trying to be
like, how do we stack up, right?

__Ben__: Doing what, though? Do you have, like, test suites, like big example
applications, anyone using it in any kind of production capacity? It's from
Ferrous Systems, and so is there, like— it's a company. Do they have any clients
that they're using it for? Or—

__Yoshua__: I don't know. I'm not part of Ferrous.

__Ben__: I see.

__Yoshua__: Right? But yeah, they are— they do client work with it. I know that
much.

__Ben__: Okay.

__Yoshua__: And we have lots of benchmarks and pretty hefty, like, testing going
on. But as always, there's, like, room to improve. But, overall, fairly
confident in it.

__Ben__: Excellent. All right. Is there anything else you want to talk about in
terms of, if somebody wanted to get involved, what are the best websites or chat
channels to get in touch with you on?

__Yoshua__: Our website is async.rs, which I'm pretty happy with that. Yeah, if
you're interested, you can check it out there. Otherwise, we're on Discord.
There's links to Discord from the GitHub. I think maybe even on the website
there's people online, If you have any questions. You can also hit us up on
Twitter. My twitter's, well— I can't spell that, so whatever, but we're on
async-rs on Twitter. Just ask around.

__Ben__: All right. Thanks a lot. Anything else you want to say?

__Yoshua__: Anything else I want to say? I'm just excited.

__Ben__: It's an exciting time right now.

__Yoshua__: Yeah, yeah. No, I'm just I'm just very excited for the future of
async Rust. I think this is a big milestone and things are definitely heading in
the right direction. And I'm just, yeah, want to see what comes next.

__Ben__: Well, thanks, Yoshua. Thanks for being on.

__Yoshua__: Yeah. Thanks for having me.

__Ben__: Great. See you around.

(Musical break)

#### Stjepan Glavina on Powerful Concurrency Primitives with `crossbeam`

__Ben__: Welcome to the Rustacean Station podcast. I am Ben Striegel, not live
from Rust Fest because you aren't here right now, unless you're hiding behind
that pillar over there. So, I am here with Stjepan J.?

__Stjepan Glavina__: Stjepan G.

__Ben__: G. Okay, Stjepan G. I will never get that correct. You are currently
the maintainer of `crossbeam`, I understand?

__Stjepan__: That's correct.

__Ben__: Excellent. And so, I want to just lead with, why don't you tell me,
what is crossbeam? Real quick high level overview?

__Stjepan__: Yeah, a lot of people asking this question, but I think the short
answer is, `crossbeam` is a library similar to `std::sync` module. Except, it's
battery-included. It's like an extension of the `std::sync` module. Which means
it includes more of concurrency and primitives like lock-free queues, channels.
We also have an epoch-based garbage collector, scope threads, Things like that.

__Ben__: Yeah. So that's actually quite an old project, I think, originally. So
`crossbeam`, I think, was— Aaron Turon made it many years ago. Back around Rust
1.0. And I remember reading blog posts about epoch-based garbage collection back
then. At what point did you get involved?

__Stjepan__: I believe Aaron started the project in 2016, and he was working on
it with some other contributors for a few years. But then he didn't have time to
maintain it any more. So he passed maintainership over to the community. But I
sort of stepped in as leader of the project because it was well suited to my
skill set, and I was really interested in it. And I had a vision for the
project.

__Ben__: And what was the vision? Back then.

__Stjepan__: The vision? So at that time, it had, like, a very basic set of
primitives like queues, a simple epoch-based garbage collector which had, like,
a number of flaws, I think even soundness issues. It also had scope threads, and
a Treiber stack, which is not super useful. But my vision was to expand the set
of primitives, to expand the APIs, and make primitives user friendly. So I
really wanted to bring this super-complex area of lock-free programming to the
wider audience. I wanted anyone to leverage the power of this weird advanced
stuff without much—

__Ben__: Yeah. I think there's a lot to unpack here, so let's try and take it
one thing at a time. Is it even possible to give a brief overview of what epoch-
based garbage collection is? Like, I thought, this is Rust. We don't even want
garbage collection. Why? What is this?

__Stjepan__: It's hard. Yeah, I'll try to be brief. So the thing is, in
concurrent programs, like in parallel programs, we have multiple threads, and
say you have a queue and you push things into the queue, and pop things out of
the queue, and if the queue dynamically allocates a node for each element inside
a queue, at some point when you pop stuff out of the queue, you will have to
deallocate that allocated slot where this element was stored. But the thing is,
a lot of threads could be accessing that particular slot allocated on the heap,
trying to see if there's something inside it. But if some thread concurrently
deletes, like, attempts to destroy that heap allocated objects, then other
threads are not allowed to read from it, because, you know, it might be dead. So
what we do with epoch-based garbage collection is, multiple threads
cooperatively can decide when heap allocated objects will never be accessed by
any threads any more. And only from that point on, we are allowed to destroy
those objects.

__Ben__: So I think a different way of saying it is, we already have— in Rust
today we have `sync::Arc`, which is—

__Stjepan__: Correct.

__Ben__: Essentially, it's reference counting, which is a form of garbage
collection. And so you can opt into this if you will have, for example, of some
kind of dynamically allocated thing being read and written to from multiple
threads. And so the reason that you need this is that Rust's normal ownership
rules kind of work in a tree-like hierarchy, very static, but thread access
patterns are very dynamic so that just doesn't work, and so your need something.

__Stjepan__: So `Arc`s would also work. But the thing about `Arc`s is, whenever
you clone an `Arc`, you have to update some kind of atomic reference counter.
And when you stop using an `Arc`, and you drop it, you have to decrement this
reference counter. And if you have a lot of threads constantly incrementing and
decrementing that counter, that's a lot of overhead. That makes things very
slow. So with epoch garbage collection, we avoid all that overhead, all that
contention. Unlike single reference counter, reserve, like, localize those
updates among threads so that each thread has, like— in the common case only
updates its thread-local storage. Like, a way of thinking of this is perhaps,
instead of having this single shared atomic reference counter be distributed
over threads so that each thread only updates its thread-local—

__Ben__: It's kind of sharded among threads.

__Stjepan__: Kind of. Yeah, you can think of it that way.

__Ben__: And then the super high level is, if you use an `Arc`, maybe you would
benefit from a lockless version of this kind of shared memory primitive.

__Stjepan__: Yeah, that's true.

__Ben__: But at the same time, there's going to be some kind of drawback to
this, right? There's always a tradeoff with these kinds of things. And so when
would you not want to use this and prefer an `Arc` instead?

__Stjepan__: Well, the trade off is that memory deallocation is deferred. So,
like, if an object has to be destroyed, it will be destroyed at some point in
the future, which means we might accumulate a lot of garbage data, which is
ready to be destroyed. But it, you know—

__Ben__: It's kind of the classic garbage collector tradeoff, where you have
reference counting, which eagerly deallocates, and you have a tracing garbage
collector, which does not. And they both have their advantages and
disadvantages.

__Stjepan__: Yes. So the main drawback is increased memory usage.

__Ben__: How it— could you compare it to, say, a concurrent garbage collector,
like, that Java might use, for example. Do they use lockless, epoch-based
approaches for their thing?

__Stjepan__: It's different, because in Java— Java uses a tracing garbage
collector, which means it will— it knows where pointers in the memory are, and
from time to time, it will trace those pointers to see what objects in memory
are still reachable and alive. With epochs, we don't do that. We use a
simplified version of that.

__Ben__: And you mentioned your background made you well-suited to understanding
this problem. It seems very thorny, very subtle. And so, what is your
background?

__Stjepan__: I did a lot of C++ before. Before getting involved in Rust, I did a
lot of research on concurrent programming and lock-free data structures. I
dabbled a lot in lock-free skip lists, and I spent, like, months and months
developing my own skip list in C++, and I wanted to transfer that knowledge over
to Rust. Okay, Did you actually end up writing a skip list in Rust? I did write
a lock-free skip list, the thing is, it's almost done, but we never published an
actual version on crates.io. We will get around to it someday.

__Ben__: And then, as far as `crossbeam` is concerned, it's not just this epoch-
based thing. It also involves, like, its own channels. So could you not use the
standard `sync` channels with a crossbeam pointer? Or, I guess I wouldn't call
it a pointer. So it's not quite— is the interface similar to Arc, where it's
like, `Arc::new`, give it some data, and then magic takes over? Or is it more
involved than that? How would I initialize some data and put it in the system?

__Stjepan__: You mean inside channels?

__Ben__: So one question I have is, in the `std::sync` module, there's both
`Arc`, and there's channels. But I don't think you need channels to use `Arc`,
and vice versa. You could use them independently. Is that true for crossbeam?
Could you use the standard channels with `crossbeam`'s types, and vice versa? Or
is it just that you want to provide alternatives that are faster in your way?
What are the benefits of using your own channels?

__Stjepan__: They are complementary. Like, channels in particular in crossbeam
are pretty much strictly better than channels in the standard library, in pretty
much every way.

__Ben__: Okay.

__Stjepan__: Like, they are more flexible, they are MPMC rather than MPSC
channels, which means you can clone receivers. They're more efficient. There is
also a selection interface, which means you can select over multiple channel
operations. I even wrote a proposal to include `crossbeam` based channels into
the standard library. Which might happen someday, hopefully.

__Ben__: Is the RFC still open?

__Stjepan__: This is still— like, there is an open proposal. I even wrote an
implementation which can be just copy-pasted into the standard library. But it
is up to the library team to make a decision of, whether to include that.

__Ben__: Okay, Interesting. And then hopefully, we'll see that someday if
actually— are there any trade offs? Like, you say it's all better. Is it more
memory usage, or doesn't work as well on—

__Stjepan__: No, there are really no tradeoffs.

__Ben__: Just kind of, you just made a better version.

__Stjepan__: Yeah. Yeah, pretty much. Yeah.

__Ben__: Is there a lot of research here, in terms of like, lock free data
structures?

__Stjepan__: Oh, there was a ton of research. I spent, like, years working on
those channels and channels might seem like a trivial thing. It's just a queue,
after all—

__Ben__: Just a queue.

__Stjepan__: Threads can push and pop data out of the queue, in and out of the
queue. But as soon as you add the selection, if you want to support these select
blocks, then that complicates things so much, and things get really, really
involved. I based `crossbeam` channels on work by Dmitry Vyukov, who is working
on the Go runtime. And he made a proposal to improve channels in Go, and wrote
this document. It's called "Go Channels on Steroids" and it's a really good
read. So I basically took his proposal and reimplemented in Rust, and then also
expanded it a little bit.

__Ben__: Excellent. So, I know one of the things that the standard channels are
missing is, kind of nice select interface, like maybe there's a macro? Or was at
some point? I forget—

__Stjepan__: There used to be a macro in the standard library. But it had, like,
its own quirks. There was also select struct for dynamic selections, which means
you don't have to statically decide which channels' operations you are selecting
over. But you can dynamically at runtime add those cases to a select. So that
interface in the standard library was always unstable, and the API was unsafe,
which is unfortunate.

__Ben__: And is it safe, the version in `crossbeam`?

__Stjepan__: Yes, in `crossbeam` it's completely safe.

__Ben__: Is it also a macro or is it a method?

__Stjepan__: There is a convenience macro, which is really nice to use, but you
can also dynamically add cases to select using the `Select` struct.

__Ben__: Wonderful. Very cool. What other parts of `crossbeam` are there,
besides the channels. You mentioned some things before, I feel like. The scope
threads, for example.

__Stjepan__: Yes, we also have scope threads. There also lock-free queues, which
are sort of like channels, but more lower-level. So if you want to build your
own channels, you would most likely use those queues. We also have work-stealing
deques. That is used by `rayon`, and also used by `async-std`. Those deques are
very useful for building your own schedulers, and things like that.

__Ben__: You said "deques?"

__Stjepan__: Deque, yes, like, double-ended queue.

__Ben__: Oh, okay, yeah. I was trying to think of like— I usually say "dee-
queue," but that's definitely not how it's pronounced. There's no good way of
pronouncing that word.

__Stjepan__: We also have some atomic primitives. Like, there's this thing
called `AtomicCell`, which is similar to types in the standard library called
`AtomicUsize`, `AtomicU32`, `AtomicI32`, and so on. But those in the standard
library are not that convenient because they require you to specify memory
orderings. Whereas `AtomicCell`, it just works, without specifying memory
orderings. But also, you can put, like, vectors in `AtomicCell`s, and arbitrary
kind of data.

__Ben__: Is that, kind of, I know there's a crate called `once_cell` that uses
`std::sync::Once` to initialize things exactly once. Is that kind of a
complement to that, or a replacement for that?

__Stjepan__: It's different. So `Once` is for initializing data once, whereas
`AtomicCell` is like a cell, like the `Cell` type from the standard library.
Except it's thread-safe, and you can update the contents of that cell as many
times as you want. So not just once.

__Ben__: Okay. When you took over the project, you said there were some things
that were unsound about some of the APIs?

__Stjepan__: Yes. There were some soundness issues in the epoch-based garbage
collector, but I really won't go into that because it's super subtle.

__Ben__: Do you feel like you've fixed those, since?

__Stjepan__: Yes, those have been fixed.

__Ben__: Okay. How do you even prove that kind of thing? I'm not going to ask
you for, like, an actual proof, but like, for your own satisfaction, when did
you feel like, okay, this is right now?

__Stjepan__: I don't know. It's a lot of work and looking into the APIs and
trying to find failure points. We also have this contributor, whose name is
Jeehoon Kang, and he is a PhD researcher in Korea, specifically studying memory
models and lock-free programming. And he made a proof of the correctness of our
garbage collector.

__Ben__: Very cool.

__Stjepan__: Yeah.

__Ben__: Excellent. That's great to have. I know back in the day, it was a big
question like, well, we'd like to maybe include crossbeam in `std` one day, but
we're not actually sure if it makes any sense, so it's fantastic to have that. I
wanted to ask about it's use in `rayon`. So `rayon` uses the queue, the
underlying queues, for its own purposes?

__Stjepan__: `rayon` uses deques, work-stealing deques for balancing the
workload among its own worker threads.

__Ben__: Cool. So anyone using `rayon` is currently using `crossbeam`.

__Stjepan__: Yes.

__Ben__: Because `rayon` is just fantastic. Exemplary library. And then you also
mentioned `async-std` is using `crossbeam`— I saw today, up in the presentation
that Florian gave, about `async-std` being faster than `crossbeam` even,
somehow? And then Yoshua told me to ask you about performance, in some way, and
said that you working on performance, very heavily. Do you want to talk about
that?

__Stjepan__: So in `crossbeam`, we have our own channels which are based on
`crossbeam` channels, in particular the bounded version of channels in
`crossbeam`. So the performance advantage of `crossbeam` channels are in that,
context switches on asynchronous tasks are much lower overhead than context
switches with threads. So if you're sending a lot of data between different
tasks, we can context switch between them much faster than with threads.

__Ben__: Excellent. And those are still MPMC?

__Stjepan__: Yeah, those are also MPMC.

__Ben__: Multi-producer, multi-consumer.

__Stjepan__: Yeah.

__Ben__: Fantastic. And is it the same, kind of— is it all the same
implementation underneath, for both threads and tasks? Or is it a totally brand
new thing that you had to write to support futures?

__Stjepan__: So the underlying concurrent queue is the same as in `crossbeam`,
but the, like— instead of notifying threads when send or receive operations can
proceed, we have to notify asyncronous tasks and use `Waker`s for that, so that
part is different.

__Ben__: Okay, Cool. But other than that, it all shares all the same code,
benefits from all the same bug testing—

__Stjepan__: Exactly.

__Ben__: Proofs, that sort of thing. Excellent. Okay. So, is there anything else
you want talk about with regard to `async-std` or `crossbeam` or— what's the
future hold for it?

__Stjepan__: These days are, I'm mostly focused on `async-std`, and like,
asynchronous programming in general. With regards to `crossbeam`, we have been
at, like, 0.something releases—

__Ben__: 0.9999999, where it's like, you want to get to 1.0, but you're not
quite there?

__Stjepan__: Yeah, that's with `async-std`. But also crossbeam has been at
0.something for way too long, and we really gotta push it over to 1.0.

__Ben__: What's required for that?

__Stjepan__: Not very much, actually. Just maybe some small fixes, but it's it's
ready for 1.0 for sure.

__Ben__: I would love to see a library like that reach 1.0. These foundational
sort of libraries. Is there anyone— if someone wanted to help with that, what
would you say, is there a chat channel they should see you on, or a forum?

__Stjepan__: We have a Discord channel. We also have a GitHub—

__Ben__: A `crossbeam` Discord channel.

__Stjepan__: We have a `crossbeam` Discord channel, yeah. So contributors are
welcome. Also at this RustFest, during impl days. I have a plan to work with a
few folks on `crossbeam`.

__Ben__: Fantastic.

__Stjepan__: So maybe we'll try to push it over 1.0.

__Ben__: Where would they find the link to that Discord?

__Stjepan__: It's in the `README`. Yeah.

__Ben__: In the `README` for `crossbeam`.

__Stjepan__: Exactly.

__Ben__: Great. Fantastic. All right, well, thanks for coming on. Thanks for
talking about it. Hopefully, we'll get more awareness of `crossbeam` and make
things stable and great for Rust.

__Stjepan__: Of course. Thank you for having me.

__Ben__: No problem.
