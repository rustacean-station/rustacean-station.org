---
episode: _episodes/2019-09-15-rust-in-production-armin-ronacher.md
---

__Ben Striegel__: Howdy, folks. You're listening to Rustacean Station. Today's
episode is hosted by one of our volunteers. That's kind of what this whole
project is about, this crowd-sourced podcast of ours. And if you would like to
be a host or help out in any other way, please get in touch with us at our
Twitter, our Discord, our email. You can find these at rustacean-station.org.
Enjoy the show.

__Jeremy Jung__: Before I start, actually— how do you pronounce your last name?

__Armin Ronacher__: "Ronacher."

__Jeremy__: Oh, boy.

__Armin__: You can destroy it as you want.

__Jeremy__: Hey, this is Jeremy Jung, and you're listening to Software Sessions.
And today we pull into the Rustacean Station with Armin Ronacher. Armin is the
creator of Flask, one of the most popular Python web frameworks, a prolific open
source contributor, a conference speaker, and a partner at Sentry, where he
works in both Python and Rust. Welcome to the show.

__Armin__: Thank you for having me.

__Jeremy__: The first thing I want to start with is, you've been a big part of
the Python community for over a decade, and you've mentioned how it left a
profound impact on your life, and it even connected you with your wife. With
such a strong relationship to Python, what got you interested in Rust?

__Armin__: So what got me interested in Rust in the first place was the language
itself, very independent of, I would say, sort of a professional environment. So
I found the language long before 1.0, I don't know exactly when. And I also
don't really recollect anymore what the original motivation was behind me being
interested in it, but it had a lot to do with it being an exciting time to look
at language development. It was one of the few open source languages that were
happening at the time, and it had some features that I found really interesting.
So that was the initial way for me to become aware of the language, but then
relatively soon after, it also became pretty obvious that some of the features
of the language are really quite exciting. And in particular what made me
excited was that you could, at least on paper, write really good abstractions
where you didn't have to sacrifice performance. And so a lot of what limited my
ability to make nice APIs in Python was that you had to pay pretty much
everything at one time. So that's I guess what got me excited in the first
place. But then there was a lot more afterwards, like the community aspect— that
it was actually useful for problems that I had at work. So all of that came
after.

__Jeremy__: And could you give an example of, say, an abstraction that you said
would be very— the performance would not be good in Python, but you would be
able to kind of use the same or similar abstraction in Rust.

__Armin__: Sure. So a good example for this was what got me excited originally,
which was that I wanted to build, sort of larger, not necessarily distributed
systems, but systems where you could serialize some sort of message packing
potentially over the wire. So I actually wanted to build a system which
internally was based on, sort of, highly concurrent functionality, where you
would do a lot of message passing. And so, at the time in the Python community,
there was a lot of talk about asynchronous I/O, async I/O, and what was
happening there was a system called ASGI, which is sort of a asynchronous
version of WSGI, which is a web server standard of sorts, where applications can
have a standardized interface to talk to an HTTP server. And this async system
always looked like, at least on the Python side of things, that you could almost
only write this with a huge overhead. And so I was excited about this, like some
potential setups for how do you do asynchronous applications in Python. But it
also looks like you can almost impossibly write something that would perform in
the real world. And so on the Rust side of things, it looked like I don't
actually have to deal with async at all. I can just do threads. It has really
cool concurrent primitives. So it looked like you can build systems like this in
Rust, and and they would work. And I think for the most part that's true. And so
that's what got me in this, even though I didn't actually end up building a
system like this. That's what got me excited.

__Jeremy__: And you were saying that you found that within Rust, you felt that
async was maybe not needed. What kind of the difference in Rust where just using
threads was sufficient whereas in Python it wasn't?

__Armin__: So in Python, you basically can't use threads. Except for very
corner-casey situations where you can actually— so in Python you had the the
global interpreter lock. So the only way really to get concurrency out of it
where threads don't punish you for it, is if you manage to have execution
running in a thread that's effectively spawned outside the interpreter. So a
good example for this would be if you have linear algebra or some some mathy
kind of situations, where you could kick off a concurrent calculation on the C
side, then you don't really get anything out of threads. And in Rust that's
totally not the case. There is nothing that prevents you from spawning a lot of
threads. It turns out that you can spawn a ton of threads on most operating
systems, and it's just fine. So I think for the most part, how you program in
Rust and Python is just, as a result, very different, because doing lots of
threads in Rust is obvious to do, it's simple to do, but none of that is true
for Python.

__Jeremy__: And that's primarily because of the global interpreter lock.

__Armin__: That's a big part of it. But the other one is just that building
thread safe Python applications is as hard as in any other language. And Rust is
really good at teaching you how to do this better.

__Jeremy__: I see. And that's kind of related to the fact that Rust has sort of
the ownership and borrowing concepts that it catches at compile time.

__Armin__: Yes. So the fact that— so, Rust makes you a better programmer, or at
least that was my experience with it. It teaches you a bunch about how to better
build concurrent applications. Yeah, and so that was really exciting, and it's
still very exciting. And I think overall, almost every person that I've exposed
to Rust has felt that something about their mental model of programming has
fundamentally changed.

__Jeremy__: So I guess, would you say that maybe the thing that excited you most
about Rust is the concept of being able to catch concurrency problems at compile
time?

__Armin__: I think it's the combination of so many things that made me excited
about Rust. I don't think, like, concurrency in itself would have made me
appreciate the language. I think it's just the sum of all the parts that did it.
I would say, like, in order of importance, probably the borrowing part is number
one, because it is the most fundamental. The ownership model and the borrowing
system is the most fundamental thing. But that in itself would not have made me
use the language. The ecosystem that developed around it, like the package
manager, and in particular the community. That is I think the most important
immediately following this. But that in itself would still not have made me pick
it for something that I would use professionally. The fact that we actually have
some really strong ecosystems on the Rust side was the ultimate reason I got
excited enough to actually use it in a commercial environment. So this is the
case for both— in our case, we do a lot of— essentially we do a lot of debug,
working with debug files, working with things that are roughly related to
compilers. And there is actually really good ecosystem and that's ultimately
what made me and us stick to it. So it's just the sum of all the things. I don't
think this the ownership alone would have been enough to be excited about the
language.

__Jeremy__: Right. It's kind of the whole package, sort of. You had all these
things come together and all those things combined was enough to make you really
take notice, and really want to use it professionally. You were talking about
how you're doing some work with things related to compilers and debugging and
things like that at Sentry. You joined Sentry about, I believe, four years ago.
Could you explain a little bit about what Sentry does, what their product does?

__Armin__: Yeah, so I joined Sentry more than four years ago now, but I also
knew many of the people, and in particular David, the founder, for a very long
time, and I used Sentry before that. So I've been exposed to Sentry, the
product, long before I joined the company. And what it does is it effectively is
an error reporting tool. And it's an open source product, which also happens to
have a quite well-functioning business built around it. And it consists of
multiple components. The most important component is the server, and the server
receives crash reports from the client SDKs. And what the server then does is it
takes this crash report, and it does some processing on it to produce an
individual error report, and then it's aggregates these together into a form so
that you can see how many individual errors are happening. And it does support
multiple languages and the one where Rust comes in the most is effectively
JavaScript, and all kinds of native languages like C, C++, Rust, Go. Every
language where you want to extract a stack trace out of either raw memory, or
where you want to take some memory addresses that you have for the stack trace,
and you want to find the correct functioning to it, at the location where in the
file the error happened. And this is where a lot of our Rust code comes in.

__Jeremy__: And if someone wanted to use Sentry, is this something where in
their own application, they would import a Sentry library, and that would kind
of hook into the memory of the application, or hook into the exception handling
of the application. Is that sort of how somebody would use Sentry?

__Armin__: Yeah, pretty much. So depending on the language, you either start
with a high-level SDK, like in JavaScript you pull in one of our clients. For
native crash reporting you have more options, one of which is to just use a
standardized crash handling library. On Windows there's a built-in function to
write a mini dump, which you can upload to us, or you can use Breakpad,
Crashpad, libraries like that. And so, it depends. Like, if you already have a
stack trace that comes out of some system, then you can probably throw it to us
and we will do something with it.

__Jeremy__: And then once you receive it, I believe you create some kind of
dashboard that shows people where all their errors are occurring, and sort of
the frequency, and sort of allow them to track. Okay. So how did you first
introduce Rust to Sentry?

__Armin__: So the initial, there were two approaches in which Rust appeared in
Sentry. The first one where we actually use Rust was a small project called
Sentry-CLI, which was a command line client to the API, and that client was just
written for fun. It was just an experiment to see how Rust works. The second
part where Rust actually ended up being quite crucial to how we do things, was
that we had a curious case of debugging, where in order to process JavaScript
stack traces, we need to work with source maps. And source maps are
fundamentally quite big and ever-growing JSON documents, that tell you more or
less at which line in the minified file you would find the same token in a non-
minified JavaScript file. So we'll tell you basically from this minified stack
trace where's the original thing. And this was written originally in Python, and
we look at various different ways to just cache the source map so that they're
faster to process. And I already had for some other purpose written a Rust
implementation of the algorithm needed to parse the source map and to map it.
And for fun we just plug this in as a module exported to Python, and it
tremendously improved the performance of the source map handling in Sentry. And
that also turned out to be relatively easy to expose to Sentry. Because Sentry
was written in Python, we already had this Rust library, all we had to do was
write the C wrapper around it, and then get it exposed via a Python wrapper that
we wrote called `milksnake` to effectively, the existing Sentry server, and that
was the gateway drug, basically, to get Rust into our code base.

__Jeremy__: So you mentioned how performance was a big motivator here. Were
there other things that, in terms of building the part that parsed the source
maps, that was easier in Rust than it was in Python?

__Armin__: I would say it was cleaner. I wouldn't say that it was easier to
write it in Rust than in Python. I can tell you why it wasn't another language.
It was basically Rust, because already had an implementation for this, and I
wrote the implementation because it was easy and fun. And the reason it was fun,
because since a lot of this is based on JSON, I just used `serde`, the already
existing serialization/deserialization library, to work with the base of the
format. And then as we started doing a little bit more correct handling of the
source maps, it also— the source code was relatively clean, because source maps
if you want to do them correctly, they have some really bizarre behaviors. Which
require you to count in UTF-16 offsets in a UTF-8 stream, and that also was
quite easy to do with the functionality you have out of the box in Rust.

__Jeremy__: So you mentioned `serde` helped with the serialization process. The
source map implementation, was that also something that existed as a library, or
was that something you created from scratch?

__Armin__: No, so that library we wrote, but the format is not very complicated,
so that was that was pretty simple to do.

__Jeremy__: And what things did you find were more difficult in Rust when
building this implementation?

__Armin__: For the source maps? I don't think there was anything harder. It was
just overall, the original Python module was obviously a lot less code than the
Rust one, just by it not doing error handling particularly well. It was just
parsing everything into a really not very efficient data structure. So this is
this is a case of second system syndrome. I can't really tell you how to compare
this tool because we already knew how to write the source map handling library
in Rust, so we obviously did it different the second time around. So they are
not very comparable.

__Jeremy__: I see. So you mentioned you started with the Sentry CLI, and that
was kind of just because— just for fun, just to kind of get more comfortable
with Rust, and see how it would work. And then that sort of moved into parsing
source maps with Rust, which really gave you a big performance benefit, and it
kind of proved out that this would be an effective tool, you know, to use with
Sentry, I guess in particular because of `serde` and because of, sort of, the
capabilities of Rust. What I kind of wanted to go into next is, you you gave a
conference talk, and it kind of went into how you wrote a Python extension in
Rust, and I believe— is this the the same project that we're referring to here?

__Armin__: Yeah, I believe that was the same. That was the first library we
exposed, but we also expose some others.

__Jeremy__: So in the conference talk, you mentioned that some people had come
to you and proposed that services should be written in Rust, and that it would
be better to have the Python communicate with Rust, with the Rust application
being written as a service. And you kind of pushed back on that a little bit, in
terms of saying that, perhaps it's better to actually write Python extensions in
Rust rather than building a separate application. Do you kind of still feel that
way or have your opinions changed?

__Armin__: I don't think my opinions have changed. I think there are times when
it's better to write a service and there are times when it's better to expose
something to an already existing language. Ultimately, I'm a strong believer of
only making individual services when there is no other way to do it. Or when the
cost of doing the extra service outweigh what the down side of it. I don't know
if that makes sense, but overall there were some reasons why we wrote this as a
separate service. But at the same time, it's important to know that even though
it is an independent service, almost all the code that runs in that service also
independently can be accessed in Sentry itself. So to make this more specific,
Symbolicator is an independent service which takes a mini dump or individual
stack trace addresses, and it resolves them in debug files and then gives you
back a proper stack trace. Now, in order to do that, it needs to open debug
files. And in order to work with these debug files. It also has an internal,
sort of, efficient cache format, which we call simcache, and it produces this on
the Symbolicator. But, for most people the source of the debug file will have to
be uploaded to Sentry in the first place. And so this uploading of the debug
file to Sentry actually goes to the main Sentry server, which is written in
Python. And so for you to get feedback on if that file is actually valid or not,
we do run the same library which Symbolicator uses, also on the side of Sentry,
to open the debug file to validate it, to make sure it's well formed, to index
it correctly. So a lot of the code that is in Symbolicator, which is the base
library called symbolic, also runs in Python exposed as a Python module. So even
though a lot of it runs in an independent service, almost all the code also gets
imported into a regular Python process for some functionality, which is better
done on the Sentry side. So basically, the answer here is, like, some of the
things looked better to put in an independent service, but we still wrote it in
a way where we actually have it embedded in the main Sentry system. I don't know
if that answers the question.

__Jeremy__: Yeah, I think so. You sort of are doing both, I guess. You wrote the
Rust code to act as a extension that you could call from Python. I guess you
found with Symbolicator, if I understand correctly, you're uploading the mini
dumps directly to Symbolicator?

__Armin__: So yeah, the way the flow works is that the client uploads the the
minidumps to Sentry. Sentry then immediately uploads it into— well, depending on
how the flow goes, and this might change, at the moment, it goes into Redis, and
then from Redis it's being picked up by another Python process that shows it to
Symbolicator. And then from this Redis to Symbolicator communication by HTTP, it
goes into some sort of polling system. And so it will try to poll Symbolicator
until the response is ready, and then it will go forward and do other things. I
would say from an architectural point of view, there is no reason this really
absolutely has to be a service. We could have built it as a not-service. The
reason why Symbolicator makes sense for us to be a service, is that we have a
lot of— we see a potential lot of value in independent people using
Symbolicator, even without Sentry. And the reason we hope that's the case is
because the total number of people that actually contribute, and find any
enjoyment in debug information files, like PDB, DWARF files, maybe source maps,
is very limited, but the complexity in those files is huge. PDB is a perfect
example. PDB is a Microsoft proprietary debug format. And a lot of companies
that have been attempting to reverse engineer it over the years, to build better
debugging tools. And Microsoft sort of open-sourced part of the specification a
couple of years ago, but there haven't been good open source implementation for
it until very recently. So our hope, in a way, is that by making Symbolicator a
useful service independently, we can actually encourage people to contribute to
an open source implementation of these debug formats. We already have these
pretty useful crates that do stuff for Rust. But unless you use Rust yourself,
there's a high chance you would not find them particularly useful. So by making
Symbolicator itself useful, we're hoping to encourage more development going
into these crates. So if we would have built Symbolicator into Sentry itself,
then you would have to run Sentry for that to be useful. But not everybody will
find Sentry in itself useful. Maybe someone just wants to do something else with
the debug files, and then Symbolicator might by itself might be useful for them.

__Jeremy__: So building Symbolicator as a service was not so much because it
was— not because, like, from a technical perspective, you couldn't write it as a
Python extension, but it was more about being able to hopefully build a
community out of an isolated service. Something that, like you were saying,
people who don't necessarily use Sentry could still contribute to Symbolicator
if they were particularly interested in dealing with PDBs or other types of
debugging files.

__Armin__: Yeah. So there's also another thing that plays into this, which is
that we are effectively fighting for, well, we're fighting for a world that
doesn't exist currently, which is a world where companies and open source
people, open source communities, will find that there's value in debug files.
And to make this concrete, it's that even though we absolutely maybe— despise is
too strong of a word, but working with PDB files is not a lot of fun. Their
format was written with motivations that are very hard to to understand. It
appears to be a format that has been added more and more bloat over the years.
So as much as PDBs are not fun to work with, the other system that Microsoft
built is actually really good, which is the the symbol server protocol. The
ability to, if you have a crash and you can see what modules are referenced, you
can go to the Microsoft symbol server and you can ask, give me please the
executable which contains the unwind information. Please give me the debug file
which contains source code filename— well, filename location, maybe even
embedded source code. That doesn't exist in the open source community. It
doesn't even exist on Android, where you would expect it. It exists very little
on Apple systems. And so we're also hoping, in a way, that if there's a system
like Symbolicator, that there will be an appetite for building these types of
debug information indexes for other platforms, so that you can eventually,
maybe, debug your Android phone, or debug your Linux Ubuntu.

__Jeremy__: So that— yeah, that would be exciting. So trying to really build a
new sort of community. That's interested in working on this problem. And that's
something that could really benefit basically developers everywhere. And sort
of, Symbolicator is maybe the start, to trying to build that community.

__Armin__: Yeah, pretty much. That's the hope, and so Symbolicator doesn't just
do symbolication. It also assists you in abstracting over multiple different
potential storage systems, for symbol files, so it can connect to AWS. It can
connect to a Microsoft symbol server compatible system. It tries to help you
unpack different types of compressed debug files. So theoretically, even if all
you care about is getting a debug file for your debugger, you can just hit the
URL, and it will proxy to some remote source. So maybe someone could build a
plug-in file, a DB, or GDB to automatically download remote debug files through
it.

__Jeremy__: Another thing I'd like to talk a little bit about is, you had
mentioned you used something called `milksnake` to interact with Rust from
Python. Is that something that somebody who's interested in Python and Rust
interop, is that something that they should look into, or have things changed
from when you did that?

__Armin__: So `milksnake` is a library we wrote which helps you do just two
things: it helps you kick off `cargo` from a Python setup file, and it helps you
load a binary shared object, a dylib or something like that, with the Python
CFFI system. It doesn't do much around that. It doesn't automatically expose any
Rust functions to Python or anything like that. So it's a little bit more
cumbersome to use than some of the alternatives, which directly linking in
CPython. Our motivation for `milksnake` was twofold, one of which was that we
wanted to build wheels, which don't link against `libpython`. So we effectively
compile our Rust modules to regular shared object. Then we build a C binary—
sorry, C ABI into that binary, and we make a C header to it. So you can actually
load our Rust libraries from a C environment. And then we use CFFI via
`milksnake` to load these into Python. So that's maybe not the most convenient
workflow, and maybe also not the most high-performant one, but it gives you the
ability to pick and choose Python versions. So for instance, it doesn't matter
if you load this from Python 2.7 or Python 3.5 or Python 3.6 or 3.8— it doesn't
really matter. And it also just generally forces you to think a little bit about
how you approach a sensible layer of abstraction. And so that was our motivation
for doing this. And I think for a lot of people that model makes sense. Maybe
it's not the most sensible model for all things that you would do between Python
and Rust, but it definitely has its upsides.

__Jeremy__: And that's mainly, like you were saying, when you don't compile
against libpython, then you can use any Python distribution. And so you're sort
of—

__Armin__: Yes, so it does user either PyPy or CPython, for as long as it
supports CFFI, you can load this extension module. There are some alternative
approaches I'm toying around with, one of which is, there's a project called
Wasmer, where you could theoretically compile your Rust code into wasm module,
and then have this wasm module be loaded via Wasmer into Python. Now that
obviously is easier to do if you have, like, an algorithm that should run. It's
less easy to do if you also want to do, issue— I don't know, file open, or
something like that, where the wasm module would have to have an ABI that it can
call.

__Jeremy__: In your conference talk before, where you talked about using Python
and Rust together. You had mentioned that error handling was very painful. Has
that improved since then?

__Armin__: So we have a solution for that, where we basically have some macros
which translate errors. So we basically catch the result or panics at the
boundary, and then translate them into error codes. And then on the Python side
we have a wrapper that catches those error codes and re-raises them as Python
exceptions, and we have some code that auto-generates these mappings. We haven't
really built anything that makes this reusable, because we didn't have to. But
in a perfect world, there would be some way to standardize this. Now, there's a
lot of work going into this sort of stuff in the wasm community. So there are
systems like this that do automatic code generation between JavaScript and Rust.
This could theoretically also exist between Python and Rust. It's just that
nobody built this, and systems that are currently existing for wasm are not too
reusable unfortunately, so that's why not too much has changed between them. But
a little bit.

__Jeremy__: The next thing I'd like to go a little more into is the web side of
Symbolicator. So why did you choose Actix web versus Rocket, or any of the other
Rust web framework projects?

__Armin__: So Symbolicator was built on Actix because— what's a good reason? I
mean, fundamentally there are not that many systems currently in Rust that are
stable. Actix at the time was the most stable system. And so we built this on
Actix 0.7. Now with the async/await thing coming up, it's actually not entirely
clear what's going to be the most sensible and stable solution going forward.
Internally, Symbolicator does a lot of things. It can download from external
sources. It can produce cache files. It can symbolicate based on cache files. It
can stack core minidumps. It does a lot of things. So the actor design made a
lot of sense. So that was the biggest reason, so actors seem sensible, the
platform seems stable. That was the decision for us, to go with Actix 0.7. Now,
we recently attempted to upgrade this to Actix 1.0. We didn't really succeed in
the upgrade, because of us running into memory leaks. What we believe is to be
in the Actix core itself. And since there are— this is quite a big of change
going on in the Rust async/await stabilization phase. This might actually be
something which we reconsider. Ultimately the Actix design for actors makes a
ton of sense for systems like Symbolicator. Maybe even the service design from
Actix 1.0 or the service design from `tokio-tower`. Feed well into this design
like this. The problem with all of this at the moment, is that async/await is
going to throw all of this into, like, a little bit of a chaos again, and it
doesn't necessarily seem like the community is moving into one clear direction.
In particular, Actix is turning a little bit into a silo, and the rest of the
community is also building new silos. So it's hard to say what this is going to
look like in a year from now. It might even turn out that we want to build
something like Actix on top of something else, which just does what we need, to
be a little bit more stable, and well-guarded for our use. Because this is not
the only thing we built on Actix. There is also a second system called Relay. So
it's unclear right now. The async/await thing is going to change a lot, and the
reason it's going to change a lot is because once async/await stabilizes,
certain things are going to work but other things that currently work really
well, will not work at all. So in particular, both Actix 1.0 and 0.7 is based on
manual futures a lot. So you have to do async/await. Async/await is only going
to work in functions and simple method implementations for now. But if you look
into how the service traits work, they actually require you to also define, sort
of this type hierarchy. For how you return futures from a service, and that's
not working at all with with impl future. And so for that reason, I'm actually
expecting that, initially at least, some other designs will emerge as being—
fitting better this design of the new features. Yeah, it's unclear. It's very
unclear right now. It feels again very unstable, overall. Where this whole thing
is moving.

__Jeremy__: So if someone was interested in building a web application in Rust
now, it sounds like the public API of these frameworks, maybe it's going to end
up start changing a lot, due to this all these changes being made in the
async/await ecosystem. Does that does that sound correct?

__Armin__: Yeah, that's that's how we feel right now, where we're waiting and
seeing where this whole thing is moving.

__Jeremy__: For someone who is interested in making a new web application in
Rust, would your advice maybe be to kind of wait and see a little bit, and see
how things turn out with async/await, or what would your sort of thought be?

__Armin__: My thoughts on this are very complex. I think it very much depends on
the type of application. So the only reason async/await even plays a role in
Symbolicator is because Symbolicator does something we normally don't really do.
It does a lot of HTTP downloads. Most of what it spends its time doing, other
than stack walking, which is CPU-bound, is going to different web services and
web servers and downloading stuff from there. So async made some sense to us
overall. But I'm not sure I know that many systems will actually need async,
like, most people will be fine with threads. So I'm not sure if async should be
the most motivating factor.

__Jeremy__: And would you say that async, is that most important with I/O
operations, like you were giving the example of Symbolicator making a lot of
HTTP calls, or you might have an application that's doing a lot of file reads or
writes. Is that kind of the primary use case for it?

__Armin__: I honestly have to say I'm not sure. I think async ultimately, right
now at least, is a question of preference. So composing things out of futures,
it doesn't matter if they're CPU-bound or if they are I/O bound, is something
that some parts of the Rust community decided is a good thing to do. And that's
why in certain environments, that appears to be the most logical thing to do.
And in particular Actix definitely has some situations where they say, well,
this is how you do stuff. So that's probably more the reason why we ended up
using async code, rather than it actually being the most sensible thing to do.
I'm pretty sure you could still use futures with mostly blocking code just to
compose the high-level workflow that we have. We could also have used some other
things, that would have probably been more sensible. But this is just how we
started with this, this seems overall to be quite okay as a design. I don't know
if it's the best design that we could have done. Like with the experience of
hindsight. There are a lot of things we did incorrectly with this design, where
we just probably didn't fully comprehend how painful async would actually be.

__Jeremy__: Could you maybe give some examples of things that you think might
have been done differently in hindsight?

__Armin__: I mean, this requires quite a bit of knowledge about how Symbolicator
works internally but to give you like a basic overview of how Symbolicator works
is, the API consumer sends some requests into Symbolicator, and Symbolicator
will attempt to work this down for some period of time. And if it's if it can't
fulfill your request in that period of time, it will give you back a request ID
and you can start polling on the result. That's sort of the base form of
communication that Symbolicator has with Sentry. Sentry will send requests to
Symbolicator. It will try to wait on them. If it takes too long, it will put it
into a queue, and then we'll start pulling it until the request is done. And
that abstraction, that is existing internally is basically a lot of futures. The
problem with all of these futures is that back pressure management is not clean
at all in Symbolicator. So the way we do this at the moment is not nice, and it
actually causes some problems, because if we overload the system it gets to a
point where it performs in ways in which well behaving system shouldn't perform.
And so we definitely want to change some parts about this design to make this
back pressure management more sensible, and more unified across this pipeline.
But the problem you end up with if you have this, is that you can— you have a
future somewhere, and the future does something. But from the outside, it's not
clear where this future should actually run, like, does this future do cpu-bound
tasks? Then you have to spawn it into some executor. It doesn't block the other
futures. Or is this feature actually just doing lots of I/O, and it's fine for
that future to share it's execution with— where all the other futures are
running. And so because these futures look the same on the outside, you can
easily spawn a future into the wrong thing. So you could spawn a future that
looks like it's I/O bound, but someone appended an `and_then` on to the future,
which is actually CPU-bound. And because it's so easy to get this wrong, we did
some mistakes in the Symbolicator design where some futures actually ended up
running on the wrong executor. And this lack of— because it's so easy to do
these mistakes, I'm not sure if that's the right abstraction to actually use.
Ultimately, all the problems are when you have async code that's running
somewhere, and then it has to do some CPU-bound task, and you would really like
that CPU-bound task to just be sync code, but what if that code again has to do
some async stuff? And then it gets all weird, and then no nice abstraction
currently existing in our code base. And I'm not even sure if there are some
good abstractions in the wider ecosystem right now, about how to design systems
like this. So yeah, I think there probably needs to be a better overall
framework to build something like this. Actix I think in 0.7, and both in 1.0
has some really good ideas, but it falls short in others. And because it doesn't
establish itself as the standard system, I'm not sure if it's going to actually
have the answers that it needs for people to build good systems on top. This is
too complex of a project to be just one or two people.

__Jeremy__: Actix specifically you mentioned, you're talking about?

__Armin__: Most projects in Rust are too few people, in that ecosystem. It
doesn't matter if it's Tower or if it's Actix. There would have to be a
community that understands, hey, this is this is how the pattern should be and
this is this is a framework that we're going to build that supports that.

__Jeremy__: In other languages are there ways that they deal with it, whether
that's in C or C++ or .NET, Java that sort of thing?

__Armin__: I mean there are definitely frameworks that are based on actor
systems, or something like that in various different programming languages. I
think Rust is at the moment not the language of choice for building services,
and that's why there's less demand for doing this. And I think that's why we
have not such a stable environment here. But I also don't think it's
fundamentally a problem right now. Even if even if our ecosystem isn't that
strong in actually building web services, most web services don't actually need
a lot of surface area. So I think in the next one or two years some standard
framework will emerge that can be a standardized framework that people build web
services on top.

__Jeremy__: It sounds like what you're thinking is that whatever that web
framework is it's going to need a much larger community than the existing ones
have, where it seems like the existing crates in the space— you said there's
only one or two main contributors. There's no Django, or no Rails of Rust at
this point.

__Armin__: So I think the problem is nobody wants a Django, or nobody wants a
Rails in Rust. People don't need another HTTP framework. What people actually
need is a system that answers how to do more complex applications. Because there
is Rocket. And Rocket is fine for what you do in Django, what you do in Rails,
which is, you can get an HTTP request, and you reply with a response. But the
things that people actually have some legitimate reasons for building in Rust
need more than that. They need— they effectively need something that gets closer
to an Erlang type of service, where you don't just have HTTP dispatching. You
also have internal message queues, you have maybe AMQP is involved, maybe some
distribution is involved. That is all more complex than Django is. I think you
can build Django-like applications just fine in Rust with the frameworks that
exist. But the ones that goes into more complex situations, you also don't have
a good answer in Python. You just also would never have probably built a system
like this in Python. So that's why that's specifically a problem in Rust at the
moment.

__Jeremy__: In your opinion, for an application that doesn't have these sort of
complex requirements of requiring internal message passing, or things like that,
somebody who is making an application that they would normally make in Flask, or
Rails, or Django, that sort of thing. Do you think at this point or even in the
future, that Rust may not be the best choice for that type of application?

__Armin__: I think Rust is fine for that. It really depends on what the
application does. Like, if the application has, I don't know, like— most
applications have a reason to exist and if the reason is, for instance, well, I
need to do some audio processing, I don't know— you could build as web service
if that's what you're processing. Then it would be absolutely sensible to build
this in Rust. If you have, I don't know, a web service which purpose it is to
write to a single Postgres database, maybe Rust is not necessarily choice here,
because Python gives you better debugability. There's a more rich ecosystem. So
it really depends on what you're doing. For us, it was obvious to build our
system in Rust because there is no other community right now of— or, there's no
other ecosystem where there is such a good support for working with debug
information files. Rust is pretty unique in that it has a really good ecosystem
here. The only alternative is C++, and I wouldn't know how to build a web
service in C++ either, and feel happy about it. So Rust is definitely a better
choice here. So it really depends on what is it that you're building, if Rust is
the choice or not.

__Jeremy__: So maybe the, sort of, web aspect in terms of, you know, being an
HTTP server that fields JSON requests and responses. That part is maybe not so
important but it's really what the application does. Like in your case, you said
something in the compiler space, there's a big Rust community. Or something
that's heavily CPU-bound, that you might have to normally write in C or
something like that. Maybe something like that would be a good fit for Rust.

__Armin__: Yeah, I would say that there are already some ecosystems where Rust
seems to be pretty obvious to use. If you have something where you have a
legitimate reason to expecting to run this in a browser, so if you want to have
your stuff compiled to wasm, Rust is a pretty obvious choice. If you have
anything in the crypto space, Rust is a pretty good choice. Anything in the
compiler space, Rust is a very good choice right now, both in handling debug
information files, as well as— there's cranelift. So if you're actually into
language design at this point, you might really consider doing this in Rust. But
I also think that Rust has already a pretty good overall establishment in in
anything where you would build something that is very CPU-bound, something where
you'll want to run over multiple CPU cores. And some of these things you
actually do want to expose to a web service. And in that case, why wouldn't you
do it in Rust? I mean, you could technically, probably do it in Rust, and then
expose it as a library, and then consume it in Go, and build a web service in
Go. And there are definitely some companies doing that. But you can also already
do this in Rust itself. So it really depends on what you're doing.

__Jeremy__: And in the current Rest ecosystem, are there— I mean we talked about
sort of a more robust actor system or being able to determine whether the thing
that you're running is I/O bound or CPU-bound, something improved for that. Is
there anything else within the Rust ecosystem, either a missing crate, or a
framework that you really wish Rust had right now?

__Armin__: Hmm, I have definitely one thing I wish was there. I wish
`std::Error` would carry a backtrace. The fact that the `std::Error` type
doesn't carry a backtrace right now is very frustrating. So that's that's the
biggest thing that's missing. I wish async/await would be stabilized, not
because I actually want to use async/await, but because I want the lower-level
HTTP and I/O libraries to stabilize, and until async/await is stable, I don't
think they will stabilize. It's also pretty obvious that even if you want to use
sync I/O the base libraries are most likely to be written in async fashion these
days, just because of how much more complex these protocols are becoming. HTTP2
is a pretty good example, where even if you only want to make an HTTP request
and get an HTTP response, internally the protocol has evolved in complexity to
the point where you actually need to write it in async style. This is only going
to get worse with HTTP3, where you basically get rid of all of TCP. So I really
want that ecosystem to stabilize. I also think that in terms of what's missing
in the ecosystem, there's some pretty— yeah, I don't know. I think there's some
pretty obvious shortcomings still in editor support. It's just like the entire
slowness of the compiler is a pretty big showstopper still. The fact that you
don't have— like, Rust needs IntelliSense, or something like this. And the fact
that RLS is still this slow is pretty annoying. I think once that gets better,
there will be some more obvious communities automatically picking up Rust.

__Jeremy__: One of the last things I'd like to go into is, in the past you've
wrote a lot of back-end code for games, and I believe— was that in Python and C
and C++?

__Armin__: Yeah, mostly Python.

__Jeremy__: Just out of curiosity, are there any projects you worked on in that
space in the past, where you could see Rust fitting in, or do you think that
that type of work mostly makes sense in Python?

__Armin__: I think game backends make a lot of sense in Rust. Now the question
is, where would use Python, versus where would you use Rust? So in particular,
when you look into something like a computer game that actually simulates a
world, where that has a very connected environment, people currently do this in
Java quite a lot. They do this in Go quite a lot. I think Rust has a pretty good
realistic expectation on being a language of choice, just because Rust makes a
lot of sense in other environments. If you're going to have to run code both on
the server of the game, and in the client, you want that to be the same code.
And that's why you have a lot of C++ code in the space at the moment. You have
some other games where the simulation is actually quite detached between client
and server, and then it might be in different environments or different
languages. But where it's about game simulation, Rust has a future. Where it's
more about, well, you want to store some inventory, or in-game currency, or like
statistic backends, I think there is no good reason why you would do this in
Rust at the moment.

__Jeremy__: Finally, is there anything else that you think I should have asked,
or anything else you'd like to add?

__Armin__: It's a good question. I think what would be interesting to explore in
the upcoming time will be, to see are there more communities where Rust becomes
a language of choice? Or where people would like to use Rust, but currently
can't for some reason or another. So when— I'm not surprised that the
cryptocurrency community embraces Rust, but I'm actually still quite surprised
that some communities are not picking up Rust where I would expect that. I would
have expected that there is generally a bigger push for web development for Rust
than there actually turns out to be. I was surprised about that. And I think the
big reason why there are fewer web projects going to be built in Rust is just a
fact of the compiler speed. It probably takes you too long. Or it's too hard to
expose protocols to Rust and other languages, like, you already have something
like Thrift or Protobuf, but it's actually not that convenient to build this in
Rust, compared to other languages. So I think it would be interesting for all of
us to to specifically talk to some of these communities, to find out what
actually the reasons are for not backing Rust. Because I really— I would have
expected at this point that there is more push for web development in the Rust
space than there is.

__Jeremy__: Have you talked with other companies that are using Rust for web
development? And you know, if you have, have you got any perspective on them, on
why they chose it or why, you know, they think maybe other people aren't
choosing it.

__Armin__: The biggest reason I've noticed, why people have very little interest
in Rust for web development, is because they already have other choices. And
because they feel like the ecosystem is not stable enough. So the chicken and
egg situation. Nobody has enough reason to work on stabilizing a web development
environment for Rust, because of other alternatives. At the same time, there is
just not enough development happening by itself to stabilize this. So I feel
like once it stabilizes by itself, by all the people that are already working on
it, there's going to be some reason for people to reevaluate it.

__Jeremy__: Do you think perhaps that might come after async/await becomes
stabilized, and maybe that will bring a lot of people off of the fence, and get
involved with web development?

__Armin__: I don't think async/await is going to be what kicks this off, because
once async/await stabilizes, there's still so many other things that needs to be
stabilized as well. Async/await stabilizing in combination with `impl Future`,
`impl` all of this stuff, is just part of it. We will still need— I'm afraid for
web frameworks to be really comfortable to use in Rust, we will still also need
to compose services, and composing services means that I can write existential
types, that's I think what they call it at the moment. But basically, I need— if
I return an `impl Future`, I need to name this type somewhere in an associated
type. So I will need to say like, hey, this is a service which produces a
`Future`. But I need to write what type of `Future` it is into the associated
type. And currently, I can't do that. And I'm afraid that just stabilizing
async/await is not going to— it's going to help us write async code on a low
level but it's still not going to help us compose services. And without that
ability, I don't think web services are going to be easier to write.

__Jeremy__: So that's more of the type of problem that, say, Erlang's VM, or the
Akka actor framework in Java, that— something like that, I guess for Rust,
you're thinking.

__Armin__: I think you will need something like this for people to be excited
about web development in Rust. Yeah, I do hope that the community forms that
says like, hey, this is actually— we have an idea of how it should look like,
and let's all join forces, because right now it feels like there are separate—
just too many separate attempts of doing something. And too many different ideas
of how it should work.

__Jeremy__: Yeah, so everyone sort of has their own idea, and we haven't yet
found a solution that everybody, I guess, thinks is good enough to kind of
gather around.

__Armin__: Yeah, I believe so.

__Jeremy__: If someone's interested in learning more about how to do web
development in Rust, what are sort of the the resources that you would suggest
they use?

__Armin__: Web development in Rust resources. Hmm. GitHub code search. I think
that's my answer right now. It's surprisingly good to use GitHub code search to
understand how people structure code. If you already have a framework that that
you want to use, like Actix or Tokio Tower or warp or whatever, or Rocket, to
search on GitHub for examples of how other people structure code is insanely
valuable. Because for the most part, right now, people don't have this written
down. It's not like there's a book that you can buy which says, like, this is
how you develop a web app in Rust. But what you can find are huge amounts of
open source libraries, or software that try to do different kinds of web
services in Rust, and you can find them if you search it.

__Jeremy__: And I suppose Symbolicator would be an example of that. Are there
any other specific projects that you think would be interesting for people to
take a look at?

__Armin__: We have a second service. Internally it's called semaphore,
externally it's called Relay. This is also an example, it's also an Actix 0.7
project, which I think has a pretty good design. We— what else do I know exists?
I'm not looking too much around what other people are doing, but every once in a
while, I'm looking for, like, specific patterns. Yeah, I'm not sure what else is
there.

__Jeremy__: With that, we can start wrapping up. So how can people follow you
and kind of learn more about what you're doing and follow the Symbolicator
project and can maybe get involved?

__Armin__: So actually, let me pitch some of my ideas here. I really want the
open source community to embrace debugging. Debug files. Everything that looks
like a symbol server. The project itself is on
github.com/getsentry/Symbolicator. We are also very actively contributing, not
to our own libraries, but to the Rust ecosystem as a whole in that space, for
the `pdb` crate, the `dwarf` and `gimli` crates. I want to assemble some sort of
community of people that have an interest in improving debug experience for
people. So right now we have— we're kind of starting a Slack channel for people
to talk about, sort of the experiences with this. We would also really encourage
Linux communities to start pushing for public symbol sources. I find it so
disappointing that right now, I can't use a build ID, even though they're
compiled into every library on Debian and Ubuntu and Red Hat Linux, but I can't
use a build ID to look up a debug file. That's so disappointing. So I really
wish that would happen. So I think you will hear more from us, actually pushing
people to do this, to give to give them incentives to host debug files. Because
everybody's experience would tremendously improve. Right now if you use Sentry
you can put your debug server into the list of sources, and you crash, and we
will search on your servers for debug files. And now there is an open source
implementation actually supports this. Best to reach out to me if you're
interested in this kind of stuff, on Twitter. My handle is mitsuhiko. You can
also tweet to getsentry or just send me an email. Anyone who has any sort of
interest in debug experience, especially for native C++, doesn't matter which
platform. Please write me I want to start making a community of people that care
about this sort of thing. Because it's really disappointing that there is not—
that there wasn't enough reason for people to invest in this sort of thing. I
think there's a huge development happiness improvement that could be there, if
we have this in the open source community.

__Jeremy__: Okay, great. So, hopefully anyone out there who is interested about
improving the debugging ecosystem can reach out to you, and really get this
started within the Rust community. So that's awesome.

__Armin__: And it's working with Rust out of the box. So Rust makes perfect
debug files. You can send them up to Sentry and Symbolicator and you can debug
production builds just fine.

__Jeremy__: Awesome. I think that's a great place to wrap up. Armin, it's been
great getting your perspective on Rust and its ecosystem. Thank you for joining
us.

__Armin__: Thank you for having me.
