---
episode: _episodes/029-redisjson.md
---

{%- include util.html -%}
[episode]: {{episode.url}}

__Jeremy Webb__: Okay. Welcome to the Rustacean Station. My name is Jeremy, and
I'm one of the editors and other hosts on the Rustacean Station here. Today, I'm
joined by Dr. Chrisoph Zimmermann, who is a solution architect at Redis Labs,
and also has a PhD in reflective OS design, which I definitely want to ask
about. He's a board member of miscellaneous sort of Linux things, and he's here
today to talk to us about a new project from Redis Labs, specifically RedisJSON.
Who are you? Christoph, Tell us a little bit about yourself.

__Chrisoph Zimmermann__: First of all, Hi, Jeremy. Thanks for having me on the
show. And before we continue, drop the "Doctor." Doing a PhD is nice, but
normally that has a medical connotation associated with it. I get asked about,
what can you do about my flu? I have a broken leg, can you fix that? That sort
of thing. So Chris is okay.

I'm a PhD by training. I did actually my PhD on something called an experimental
micro kernel architecture back in ninety— (_unintelligible— 00:40_) thesis at a
university called Trinity College Dublin. As the research team, we developed a
micro kernel architecture, comparable at the time to something like Mach 3,
which is actually close to something that Microsoft called NT, because quite a
few people went there. But I think the other half went to Apple, doing something
called, what is now OSX, as a next step. So the idea was, at the time, before I
diverge too much. The idea was to construct a kernel that was opening certain
mechanisms in a very controlled fashion to applications, so that applications
could reconfigure the behavior of these subsystems at runtime. So in contrast to
the then prominent approach, i.e. the operating system basically does tell the
application what to do, it was the other way around. And I wrote, actually, the
metadata architecture for this, something that later made its way into something
called the reflection API as part of the JDK 1.5. I wouldn't say they took it
literally, as in James Gosling and friends, but the concepts are pretty similar.
Unfortunately, I didn't patent the IPs, so I still have to work for a living,
instead of sitting on my Caribbean island powered by Oracle.

__Jeremy__: So how did you ow did you get into open source then? Obviously.

__Christoph__: Actually, I started open source even before I did the PhD. I
compiled my first version of Emacs on a Sun Solaris box in 87. That was the
first point in time when I came across the notion of open source, and we
developed the micro kernel architecture back in the day, just using open source
as a tool chain, if you will. That was also the first point in time, around
93-94, when I stumbled across something called Linux. Yes, which has been which
has been accompanying me ever since, more or less. Because we were looking for a
test system that we would use, in order to develop and QA the kernel, a micro-
kernel architecture. We came across (_unintelligible— 03:14_) because that's
what we used then, in order to write much of the QA framework, and often stuck
with open source for want of a better expression ever since.

__Jeremy__: Well, I guess it makes sense that why you ended up at Redis then,
being they're pretty big on open source and for everybody who's into databases
and things like that, they'll definitely know the name. At least of Redis. You
recently did a FOSDEM talk about RedisJSON. And obviously that's why we wanted
to have you on today, because this new Redis module is written in Rust, which is
presumably a first, to our knowledge at least. So obviously we should talk quite
a lot about that. But firstly, for anyone who doesn't exactly know what Redis
is, or what an in-memory database is useful for, could you give a quick
explanation about what that is?

__Christoph__: Before I do this, one important differentiation. Redis Labs, home
of Redis, is the company behind Redis, and Redis is the open source project.
Just to get this right, because there are quite a few service providers that
offer Redis. The hyperscalers come to mind. But only Redis Labs is actually
where the development of the project takes place. Some of the funding for the
codebase comes from all the rest of it. So let me shed some light on the history
of Redis, and also to some extent, without doing too much commercial promotions
here on Redis. About 10 years ago, a Italian developer by the name of Salvatore
Sanfilippo, was looking for a performant database, with certain real-time
aspects, for a web reporting project. He took a look at memcached, he took a
look at Postgres, he took a look at MySQL, but none of these projects were able
to satisfy his real-time requirements. So he ended up writing his own key— what
was then a key-value store. The first commit took place, I think, on the 21st of
March, wasn't even on GitHub them, but somewhere else before he basically took
the codebase from that platform to GitHub. And over the years, quite a few data
structures came to the original key-value association, because Redis started out
as a binary safe key-value store, pretty similar to the functionality of the
early memcached versions. Another popular key-value store, I might add. But over
the years, data structures have entered the code base, like sets, like sorted
sets, as in the ability to associate a score with set items, bit fields, lists
being probably the abstraction that can be found quite in a few programming
languages. In addition to something called streams, which essentially are a
scalable message burst.

__Jeremy__: First, what's a scalable message burst?

__Christoph__: Something similar to RabbitMQ. Maybe in the commercial world, MP
Series, or something called Kafka, by a company called Confluent. The idea is to
have message processing in main memory. So where Kafka basically use partitions
residing on disks and and other means, streams do it in main memory, with the
same abstractions, like consumer groups and so forth. So that gives you a
scalable infrastructure for your real-time requirements.

__Jeremy__: When you say in main memory for this application, you're obviously
imagining that all of the heavy lifting in the computer is being done on some
sort of server somewhere. So for main memory, does this mean the RAM of the
server, specifically on a hardware level? And that's the explanation for why
it's so performant? Or is it a hybridization of something like RAM, with maybe
cheaper sort of storage on the server end, like SSDs, that sort of thing?

__Christoph__: You hit the nail on the head. That's exactly how it works. The
idea behind the original implementation was, not to store data on disk,
persistence is offered but came later, but rather to do all the processing in
main memory. Where other databases, like the traditional SQL based ones which
start the data on disk and then having to retrieve it, and so forth. Redis does
it all in main memory. And this performance where Redis as a NoSQL database,
probably the leading NoSQL database in the area of main memory or free time
computing really shines.

__Jeremy__: In terms of the performance delta between one of the persistent ones
versus one of the in-memory ones, that you were just mentioning now, is that a
relatively similar performance delta to that, as if you just compared the raw
hardware, for example, maybe you're getting tens of gigabits per second out of
RAM, single digit gigabits out of a very modern SSD. And then maybe about a
tenth of that, if you were to go to a traditional magnetic spinning drive? Or is
it, once you move it into this database format with Redis or something, is it
relatively sort of a power of 10 or 20 every time you change hardware and
therefore the in-memory representation? Or is it something else?

__Christoph__: I mean, it's similar to the to the first comparison delta that
you mentioned, in terms of because if you stick to main memory, all this
overhead of first storing data on disk, then forgetting about it, because the OS
preempts this main memory, as part of the virtual storage memory management, and
then having to get the data back from disk, is pretty comparable. Traditional
SQL databases have come some way, let's put it this way: in terms of intentional
caching. But imagine the database that only does caching without having to go
through to the disk at any stage. Then you have it. Redis now offers
persistence, as I said. But this is optional and has to be configured
separately.

__Jeremy__: So naturally, if you want something to be super fast and super
performant, like I imagine a lot of people who target the— learning Rust is a
language want, Redis seems like a reasonably logical choice, without being too
commercial in the push, there.

__Christoph__: Yes, going back to the history of the project, Redis Labs was set
up in 2012 with the idea of offering Redis as a service. Then Salvatore joined
Redis Labs, I think in 2014-2015. So that was the point in time when the project
lead joined Redis Labs, has been with the company ever since. You'll see this
actually, in the— for example, in the GitHub commits. Many of the contributions,
many of the commits, for example, of the modules in RedisJSON 2, would be one of
them, come from Redis Labs. So Redis Labs, the entity behind Redis, funds the
development of the native server codebase, but also much of the ecosystem
surrounding it. So quite a few commits of the standard Java clients for Redis
come from, for example, from Redis Labs.

__Jeremy__: That's fantastic that he's been able to join the project again after
this time. You mentioned modules just now. So what's a Redis module?

__Christoph__: Redis modules came into existence, I think, about four years ago,
five years ago. The idea was that although the data structures offered by native
Redis are quite comprehensive, as I said in the beginning, application
programmers requested additional functionality— that's probably the best way to
do— how to describe this in terms of— okay, we have these native data types, but
what we'd really want in addition to these is, for example, a graph database or
is a document database, or is a time-series database, with the same performance
metrics offered by native Redis. I.e. the ability, for example, to store and to
retrieve a graph in main memory, rather than disk like the other graph databases
normally do it. A module from a technical perspective is an extension on the
server side, which you have to load during the server start up phase. So you
pull down the code from GitHub for Redis, compile it. That gives you native
Redis, out of the box, on your operating system of choice. Separately, you pull
down the module source code, you compile this, that gives you something
comparable to a shared object, to stick with the Linux parlance, and you will
then load this shared object when, as part of the server startup, based on your
particular configuration. After that, you have additional data types at your
disposal representing graphs and so forth. These low-level commands are great,
but most of the time this is not something that the application programmers are
looking for developers. So more often than not, these modules are accompanied by
client-side implementations, comparable to other client-side implementations
that are able to look after native Redis commands.

__Jeremy__: So another layer of abstraction to help the developer just be more
effective and be more productive?

__Christoph__: Exactly. That's exactly it. If you take a look at
[redis.io](https://redis.io/), you'll find that Redis natively supports about 50
programming languages, with more than 160 client-side implementations for the
native data types.

__Jeremy__: So just a few, just a few.

__Christoph__: Just a few, not that many, no. On top of these you get, as I
said, you get module-specific language bindings. But that also have the
advantages of, for example, with some modules implementing industry standards.
So, for example, if you take a look at graph, there has been a rough query
language been established, more or less as an industry standard called
openCypher, originally developed by Neo4j, which has but now become more or less
the standard for querying and manipulating graphs. So if you take a look at the
client-side implementation for RedisGraph, this offers basically open software
compatibility, and this is achieved through proper language binding based on
certain programming languages like Java, Python, Golang, and so forth. So only
this abstraction, in that particular case and others gives you the industry kind
of standardization out of the box, Which is important because you want to
develop applications that maybe can port to other graph databases as well.

__Jeremy__: Great explanation. In this case, we're not talking about graphs
though, we want to talk about JSON. You know, obviously the JavaScript Object
Notation. So RedisJSON is written in Rust. Let's just start with the obvious
question. Why did you do it in Rust?

__Christoph__: Okay. RedisJSON 2 is written in Rust. RedisJSON 1 is written in
C. Okay, C is the language that the native server is written in.

__Jeremy__: Okay, so 1 to 1 between the module—

__Christoph__: Exactly, 3-clause BSD, off you go. When Salvatore started to
design the module interface, he of course stuck to C, because that was the
language he knew best, and had used at the time for about five years to
implement the server codebase. So that was the natural SDK initially, and you'll
see this when you take a look at quite a few of the initial module
implementations, like graph, like RediSearch, like RedisJSON 1, they're all
written in C. Two main reasons because, yeah, the SDK was written in C. As the
software development kit that— or, the API that talks to the server, as part of
the module specification, and (B) would be performance, because C natively gives
you pretty good performance, but has a couple of drawbacks, that specifically
Rust addresses, like memory safety, QA, and so forth. But I'm sure we're gonna
go into more details on that later on.

__Jeremy__: Yes, definitely.

__Christoph__: So when engineering decided, as in the group who developed
RedisJSON 1 inside Redis Labs, decided to do a re-implementation, they went for
Rust rather than C, for RedisJSON 2.

__Jeremy__: So was the original version— was it a maintenance issue? Was it an
opportunity just to try out a new technology, on something that you otherwise
had a good version that you could always fall back on, if there was something
wrong? Can you unpack a bit more about this sort of "Why Rust?"

__Christoph__: Of course. The RedisJSON module was in for a functional overhaul
anyway. The C implementation was showing its age, And functional extensions were
clearly on the horizon, but also, the team that was in charge of developing this
and other modules also wanted to take a look at a newer technology, with a
couple of traits. For example, less QA effort in terms of, if you take a look at
your ordinary, C development used, you tend to spend, even if you have a good
understanding of how C works internally, you still spend a good amount of time,
basically, for example, fixing memory leaks. Because in C you all have to do it
manually. If you want to have some some memory, you ask the operating system.
You get back a pointer, and then it's up to you to do with the memory what you
want. You can store values in it. You can release it. You can re-allocate the
whole thing and so forth. The trouble of course starts, for example, if you
forget that you actually allocated it and never release it, because in that
case, memory will keep piling up or worse, you release it, but keep the pointer
dangling, and then some other parts of the application tries to access the
memory. In a good day, you get back false data, on a bad day you actually get a
segmentation validation, because you're trying to access a memory segment that
is no longer valid as part of page table of the corresponding application. On a
really bad day, you get something called an increase of the attack surface,
because you have a dangling pointer.

__Jeremy__: I've never heard this before. Increase of the attack surface?

__Christoph__: The attack surface is basically how you can break an application.
So if you manage to tweak a pointer, or if you encounter an invalid pointer that
points to something that is no longer in existence, you may be able, if you know
how this works internally, to exploit this fact.

__Jeremy__: Yes. Okay, so potential attack vector there, by not managing the
memory correctly—

Christoph. Exactly, and that of course, contributes to the overall attack
surface of an application. And that was the reason why they deliberately checked
out quite a few languages, and stuck with Rust, and then did the first
implementation of RedisJSON 2 in Rust. And I don't know if you've heard this
before, but there's a saying in the community that, in contrast to other
programming languages, if you can convince the Rust compiler to generate code,
you're almost there.

__Jeremy__: Yes, yes.

__Christoph__: Because this is exactly what Rust does, it takes apart your
source code, checks it out thoroughly, and put it back together again. The
effort that it takes to, for example, verify your handling of memory concepts
like borrowing, and the whole ownership of memory associated with a particular
variable comes to mind, including scope checking—

__Jeremy__: Lifetimes, as well.

__Christoph__: Lifetimes, exactly. Like scope-checking and so forth. And this
is, I think, one of the main benefits of Rust, because so much is done at
compile-time. The effort on the QA side, especially at runtime, basically, once
you have a build, and then you put it through its ordinary QA life cycle, tends
to shrink, depending on the particular code base, quite a lot, as a matter of
fact. I mean, I'm not revealing any secrets here. We're not the only ones, at
Redis Labs, not the only company seriously taking a look at Rust. I hear it's
the latest rage at Microsoft, too, for a reason. There was actually a
presentation that I recently saw, done by one of the chief Microsoft people, who
basically took about, what, 30 minutes, 45 minutes of his time to explain why
Microsoft is slowly moving away from C++ to Rust.

__Jeremy__: Yeah, for more safety, probably the number one reason, if we're
talking about the same article, which I think we are.

__Christoph__: Exactly. The conclusion, well we took a serious look at Rust
going forward.

__Jeremy__: I want to potentially unpack something that you were just saying
there, about the debugging issues before run time, at compile time, as supposed
to run time, and therefore it's shortening your QA cycle, and probably as a
result of that, overall, it makes your engineering team more effective. And I
want to give this a bit of a shout, and put a bit of a pin in this for a moment,
because I think it's something that doesn't get enough attention for Rust. I
mean, it's built on these three pillars of safety with a great memory model,
concurrency, and speed, i.e. very, very close to C++ish performance, but without
all of the drawbacks of memory management or shredding in any of that. But the
specific optimization for developer time is a huge cost to enterprise and
industry. And actually, if you've got engineers who are very enthusiastic about
wanting to use the new technology, you should try and push them towards Rust,
because it will save your company money in— if nothing else, other than, it will
make your engineers have to do less hours to get the same output.

__Christoph__: Absolutely, I couldn't have said it better. Even if you take a
look at your typical, what is called Pareto model or something, as in you spend
about 20% of the implementation— on the implementation of the initial codebase,
and then 80%, your mileage of course may vary, on ASM: application support and
maintenance, i.e. including new features in the codebase, fixing bugs, that sort
of thing. In Rust, again, that helps you because (A) it supports a very
interesting approach to packaging. First of all, the tools, the toolchain is
great. Plus, I think the namespaces, although quite comparable to other
programming languages, helps to structure possibly significant codebase quite a
lot. But similar to, I'm almost tempted to say Java, and other programming
languages. It does the checking of these at compile time, rather than at
runtime, like the likes of Python and so forth do it. This is the main benefit,
because if you incorporate a new piece of code or new piece of functionality in
your code base, you trigger a build. But at the end, should the build conclude
successfully, you can put this immediately into QA, which is then kind of a
lessened effort, because you can be certain that the compiler basically took the
new functionality apart, checked it, and put it back together again, and then
concluded it— and then included it in the existing code base. So again, you'll
gain on the QA effort. And especially if you're looking at the life cycle of a
project, and especially if you're dealing with a kind of complex project that
has been growing over over the last couple of years, if not decades, again, Rust
basically takes you by the hand and kind of— I'm almost tempted to say enforces
the whole thing, because Rust by itself offers a great QA framework.
Unfortunately, RedisJSON 2, for historical reasons, basically didn't avail of it
to the extent that the engineers could have done this, but also takes you by the
hand with doc strings and general documentation of your codebase. So the
technical debt that you enter when maintaining codebase is lessened, is
decreased in comparison to other programming languages. Which, of course, does
help with the overall effort you spend on maintaining and and extending a code
base.

__Jeremy__: Yeah, and I think there's other things as well in the Rust
toolchain, other than, for example, Cargo, which is just gonna do your building.
But there's also Rust has a very, very powerful testing framework built into it
from scratch. And I'm guessing from the sounds of things that you love to reduce
the load on QA. So presumably, when you were adding new functionality with each
build, you were really heavily leveraging the Rust testing framework?

__Christoph__: More and more so, yeah. But for initial reasons, the first rounds
of QA were done using the existing Python based framework, which is mostly
focusing on the client side, mainly for historical reasons. But going forward.
Yes, engineering will increase more and more the test coverage using native Rust
tooling.

__Jeremy__: How have you found Rust as a tool for interacting with other
languages?

__Christoph__: Funny you mention that, because one of the first things that the
group implementing RedisJSON 2 had to do was actually to write a crate that
would emulate the existing C bindings for the module SDK.

__Jeremy__: Lots of unsafe blocks, I guess in there.

__Christoph__: Yes, indeed. But otherwise you won't be able to interface with
existing codebase written in C. So that's OK. Was spent on getting things right,
as in, trying to keep the— and you'll see this actually on GitHub when you check
out the codebase, trying to keep the unsafe blocks to a minimum. So that you
would thus lay the foundation for an infrastructure that you can then use going
forward to implement more and more code bases in Rust natively.

__Jeremy__: In terms of implementing more things in the future, and just in
general development. There's a bit of a saying in the Rust community of, if
you're code's not working, then you should go to the unsafe blocks immediately.
I'm guessing you find that to be accurate?

__Christoph__: Depending on the use case. As I said, a lot of time was spent
analyzing the existing SDK with the C bindings, and then coming up with the
proper design, addressing that particular— what's the word I'm looking for—
transfer of control is probably not picturing it, but basically this migration.
Getting this migration right. From a safe codebase represented by Rust, from a
Rust perspective, unsafe code base, I.e. the language bindings representing the
SDK and ultimately talking to the server. As I said, quite a few hours, if not
days, were spent on getting things right there because it's so crucial, because
any room for error in this particular layer would then lead to challenges later
on with any Rust codebase you base on this SDK.

__Jeremy__: Yes, yes, of course. Has working with Rust, and its very opinionated
compiler, and its ideas about how to do memory management, and that sort of
thing— Do you think that is going to re- shape the way that you do memory
management of the lower level, the existing C implementation right now, the pure
Redis that you were talking about before. Do you think Rust might find its way
down to that metal?

__Christoph__: That would probably mean replacing the existing C based
implementation with Rust, of the server side. And that probably won't happen,
mainly driven by the road map of the project. If you take a look at the codebase
as it's found on GitHub, you notice that although it may, in comparison to other
projects, it may seem compact. But a lot of optimization has been flowing into
the C codebase already. So I don't see this migrating to Rust or similar
languages any time soon, but the modules are, of course, a different story.
That's exactly what happens, if that makes sense.

__Jeremy__: That's what happened with the modules, as in, as a result of the
RedisJSON 2 module that you've just done in Rust, that we've been talking about.
You think other modules might also be done in Rust from here going forward.

__Christoph__: There are no concrete plans for a— for the re-implementation of
other modules. Now—

__Jeremy__: It's OK if you can't say.

__Christoph__: No, but let me answer that question that way. Redis Labs,
especially the engineering people, are really taking a very close look at Rust
as a strategic choice of language going forward. If we think about a new module,
there must be very good reasons for implementing this in C. With the SDK crate,
we now have a foundation that is just ideally suited to do any other module
implementation, especially if we're talking about a new code base, simply in
Rust rather than C. Because the crate is there, it works in production with
RedisJSON 2, so it's an established codebase. And, as I said, the advantages
from the engineering perspective for us are clearly there, although I think the
feedback that was obtained from the engineering team and other and other people
I talked to, that Rust is probably not the easiest programming language to
learn.

__Jeremy__: Do you want to talk a bit about the teething issues, maybe when
you—?

__Christoph__: I'm not disclosing any secrets here, but I reckon the learning
curve in comparison to other languages— Python comes to mind, but also Perl or
something. The learning curve with Rust is pretty steep.

__Jeremy__: For the memory management stuff, lifetimes, borrow checker, that
sort of thing? Or—

__Christoph__: Exactly. These are concepts that totally make sense from Rust's
perspective. But coming from other programming languages that do not offer that
type of support for wonderful expression that so— that type of safety, let's put
it this way. I mean, Rust starts always with the strong type safety. It starts
there, and then it doesn't stop, add concepts of lifetime, the borrow checker,
the beloved borrow checker. Add memory management in general, and so forth. So
if you have done C or C++ programming for the last 20 years, you may have quite
a steep learning curve, grasping the concepts. I wouldn't particularly recommend
Rust as the language of choice, if you are just starting to learn to program.
Because first of all, you have to master that learning curve. In addition to
learning programming that might be a little bit over the top. So—

__Jeremy__: Interesting, interesting. I think that I wish I had started with
Rust, and the reason is if you assume the best, in the nature of things, and if
you assume competence, which I think is reasonable to do some of the time, in
the engineering world, you might start with a language, for example, maybe you
pick one of the easier languages like C Sharp, or something like that. And in
the process of learning it, maybe you start with simple data types and that sort
of thing, and then you move on to more complex data structures, and you move on
to complex control flow, and those sorts of things. As you're creating all of
these many projects, as you're learning, you are assuming that everything you
are compiling is safe, and it's not. And maybe from day one, recognizing that
you can be in a situation where you can program something that's dangerous. Like
at my company, we work with robots. So if you are messing around, and you, if
your program is not good, if your program is not safe, even in the memory
capacity or even has got undefined behavior or something like that, your code
can be very powerful. And maybe having that gravitas is actually something
that's probably good for new students.

__Christoph__: No, I see your point. On the other side, I mean, if you don't
know what a loop is, if you don't know what a variable is, if you don't know
what a scope or lifetime is, it may seem overly complex from the outside. If
you're just starting with the basics, as in programming 101—

__Jeremy__: In terms of— but I mean, if you hit `cargo new` and then you just
create a binary, for example, you'll get something that does "hello world" for
you instantaneously, right? And then, if you're using the right crates, you can
have a pretty similar experience to python. I mean, I'm thinking last week, for
some reason I had to replace an existing python tool from the operations team,
which is not something I usually do. But it was just this thing that checks
whether or not the company's website is up, and then emails people otherwise.
And just thanks to good crates being available, particularly the `lettre` crate,
which is not spelled the way that I would spell "letter." But it's it's kind of
funny in the way that it's misspelled, and I guess that makes it easier to
remember. I actually ended up writing a— well, it's almost like a script, but
it's not because it's a binary, but it's something like 20 lines of code,
whereas the Python one was 60 and had like 5 or 10 different libraries, and this
one is like 20 lines, with one library being pulled in. I mean, in some
applications where Rust has really saturated and the crate ecosystem is really
good, I think you can have a pretty similar experience to a scripting language
in a lot of ways. But you are right, that you do need to understand loops— at
some stage, you have to go through all of these things, like control flow or
conditionals, etcetera, etcetera, and learn the art of building a complex
behaving program out of very, very simple and easy to understand primitive
things, I guess. So yeah, that's an interesting debate, I think—

__Christoph__: Indeed, yes.

__Jeremy__: ...whether or not Rust is a good language as a first one. I think we
can all agree that it's probably better to learn Rust first, than it is to learn
assembly.

__Christoph__: True. The problem with languages are like, what technology I'm
looking for, like cars or or bikes. I mean, they all take you from A to B. They
all work similarly. The color may be different. The engine specification may be
different, but at the end of the day, looking at means for transport. But I
wouldn't, for example, recommend a learning driver to get behind the steering
wheel of a race car right away.

__Jeremy__: It's a good point, you know? But what's not a race car? I mean,
really. I mean, famously, the Instagram stack is predominantly Python, right?
Which is just mind blowing—

__Christoph__: Same goes for Dropbox, so I hear.

__Jeremy__: Yeah, well, Dropbox have been pretty aggressively moving into Rust,
it sounds like. Maybe interested in taking a— maybe they're taking a leaf out of
your book.

We should— maybe move back to the RedisJSON stuff. What might an application
look like, if somebody's using RedisJSON 2?

__Christoph__: Interesting question. And glad you that you asked it, because
RedisJSON is, whether 2 or 1, doesn't matter, is at the end of the day, a
document-oriented database extension for Redis. Meaning, if you have any sort of
document, so comparable to, in functionality to the likes of MongoDB, of
Couchbase. If you have any sort of document to store, to index, you would
normally do this using RedisJSON. Because documents more often than not, are
coded in the JavaScript object notation, as in JSON itself. So if you are a
application programmer, front-end portal solutions, any applications that
require the handling, the indexing, and so forth of documents, especially if
coded, if encoded rather, in JSON, RedisJSON is your choice, especially if you
look for performant document DB extension. Being an extension of Redis, it has
one particular feature. It does it all in main memory, similar to Redis itself,
because that's the focus of this NoSQL database. So any real-time aggregation
stuff comes to mind. Also, IOT applications, or IOT stacks that generate data,
in either a binary format, that which is then translated to JSON, or simply
generate JSON natively.

__Jeremy__: You said performant there. In terms of the new module versus its
predecessor. What— is there a performance delta that's observable? I mean, I've
watched your FOSDEM talk, so I know the answer to this question already, but for
our listeners, what's the performance delta—

__Christoph__: If you're interested in the technical details, yes. Check out my
FOSDEM talk.

__Jeremy__: I'll put the link in the description.

__Christoph__: Yes, thank you. But funny enough, yes, you do pay a performance
overhead, But funny enough, in comparison to the native C stack, it's not that
big. So yes, Rust adds a certain performance overhead. But you're not talking
orders of magnitude here. You're talking about kind of one, maybe two digit
percentages, if at all. Add the very benefit, to shift much of the effort from
runtime testing to compile-time builds.

__Jeremy__: Yeah, well, I would take a very, very, very long time for you to
lose all of the time that you would otherwise spend debugging. Calling get on
all of these values that you've stored in your database, right? If the Delta is,
you know, milliseconds each time you're calling that data back, then you
probably have to call some data trillions and trillions of time to get back an
hour of developer time that you've otherwise saved, right?

__Christoph__: Yeah. I mean, that's exactly it. We were quite aware off the fact
that Rust was going to add a certain performance overhead. But were quite
surprised at the low order of magnitude, that this was actually the case. You're
not looking at an awful lot, given the benefits that Rust offers as an
implementation language for our module.

__Jeremy__: I was pursuing a line here, if perhaps, that there is a small
performance overhead, but one, you can earn it back with developer time, and
two, do you think there's a potential for that overhead to go down, if you
leverage some of the things that Rust is very good at, for example, concurrency.

__Christoph__: Good question. At the moment, I do not see this dropping
significantly, but maybe over time, with the adding of new features, the
performance overhead will shrink in comparison to the complexity that you would
have introduced by maintaining the C based implementation. Because more often
than not, additional functionality introduces additional complexity in the
codebase, meaning that with the more lines of code that you include in the
module codebase, you also increase the complexity. Goes without saying. And I
reckon that going forward, C would just introduce more complexity, because it's
not as concise as Rust. Some of the stuff you get in Rust for free, like the
memory management, you have to do in C manually, and so forth. So going forward,
I would expect that the overhead will also further drop, that you pay for using
Rust. But to the order of magnitude, I do not know.

__Jeremy__: Like we alluded to earlier, Rust is sort of built on these three
pillars of memory safety and speed and concurrency. Do you think out there— and
it might not necessarily be specific to the RedisJSON module, it could be
relating to search, or it could be relating to graph. Probably, actually, it
would relate more. You could probably get better translations of Rust,
leveraging Rust's ability to do concurrency very well in the spaces of search,
or in the spaces of the graph stuff. And do you think that's an area of interest
for you guys going forward, for newer modules or refactoring of modules, like we
said earlier?

__Christoph__: Maybe. And let me give you the rationale behind this "maybe." If
you take a look at the native server implementation, I'm not talking about
modules here; I'm just talking about the server itself. The server has one
important trait: it's single-threaded. This is basically where it gains its
speed from. And the main disadvantage that you introduce with this approach is
actually, clients start blocking in terms of, any time that single thread is
executing something on the server side, any client side is blocked, although in
version 6 it's slightly more concurrent in terms of parallel. But Salvatore
designed this with the intention of, not introducing additional complexity,
additional kind of runtime performance, by explicitly making it multithreaded.
So the idea is to have an ultrafast database engine at your disposal that is
single threaded. If you take a look at the code paths of the codebase on GitHub,
you'll see that much of the code bases are quite short. As a matter of fact, if
you go to redis.io, you would see the complexity in O(N) notation for each of
the commands that the server offers.

__Jeremy__: Might it also be just by-product of the first Redis? Like you said
earlier, I think you said 1987, right? There wasn't exactly a large amount of
parallel machines and parallel compute going on that time, even moving into the
nineties, which is the next milestone that you mentioned again. Do you think
it'll move to a massively parallel architecture at some stage in the future?

__Christoph__: Very good question, going back to the single-threaded nature of
the original implementation. What quite a few modules— and, I think RedisGraph,
which would be the prominent example here— have introduced is a certain confined
level of parallelism on the module layer. The modules have most of the time one
important trait. They use the data types as offered by the server natively, as
their foundation for the implementation of their side. For example, if you take
a look at RediSearch, which is a full text search engine, much of the data types
used by the RediSearch implementation are hashes, something that is offered
natively by the server. So if you would introduce additional parallelism on a
module base, you would have to synchronize going back to the server-side
implementation each and every time you do this. Would introduced additional
overhead on the module level, because of locking. Simple. So I clearly see
parallelism increasing, depending on the particular use case. Now, in contrast,
RedisGraph is not so much relying on the native server data types because it
uses a compact binary format for storing and manipulating the graphs based on
GraphBLAS, which is an open source library that boils down to the handing of
graphs down to the manipulation of matrices. So it's ultra-performant, because
it can be done on a kind of sparse matrix basis. And that's exactly what
GraphBLAS is pretty good at. So RedisGraph only uses Redis to store and retrieve
these compact matrix representations from the engine. So what it does afterwards
is basically down to the model implementation. So that's the reason why you can
increase parallelism on the module side, where it makes sense.

And going back to your observation with regards to deploying multiple cores on
any given machine, what our community actually does, if they want to have better
throughput utilization of their multi-core architecture, they simply put a
couple of Redis servers, clustered it or not, on a single multi-core machine.
Meaning each and every core runs its own Redis instantiation.

__Jeremy__: The CUDA model, just tons and tons of kernels running—

__Christoph__: Yes. Something along these lines. Redis has a cluster
implementation also, as part of the open source codebase you can find on GitHub,
that allows you to separate, to subdivide the key space. And it does so, more or
less automatically. You still need cluster-aware client-side implementations for
this. But from an application perspective, the complexity offered by the cluster
is manageable, let's put it this way.

__Jeremy__: When the customer's spooling up the clusters, you're duplicating the
data between all of them, so you have multiple concurrent copies of the data?

__Christoph__: Only if you use something called high availability. There's a
center based approach. But that offers a typical— what's it called these days,
primary? Because we can't say master/slave anymore, because that's not
politically correct.

__Jeremy__: Yes, of course.

__Christoph__: The latest nomination is something called primaries and replicas,
or something like this. Don't quote me. It's on the website, so look it up. It's
redis.io, so for each primary you have at least one replica. Should that primary
fail, the cluster management will take care of promoting the replica to a new
primary, and will also re-create a new replica. But if you do not use Redis in
the high availability fashion, Redis as such is a shared-nothing architecture,
meaning that the key space is actually subdivided into so-called hash slots. And
these hash slots, based on the CRC16 computation, subdivide the key space. So
you know exactly what part of the keyspace is residing on what cluster node.
What cluster instance, let's put it this way.

__Jeremy__: Interesting, interesting. Because I want to— another thing that is
really underappreciated about Rust is its ability to give very, very easy access
to multi-threading for people. I mean, a classic example of this would be
perhaps the `rayon` crate. I don't know if you're familiar with it, but if you
have been programming for like two weeks, then you can write your first multi-
threaded program with relative ease. If you change `iter` to `par_iter` and
bring in the `rayon` crate. I don't know if other beginners in Rust can remember
their experience when they wrote their first parallel program, but for me, that
was pretty mind-blowing, the first time I just changed `iter` to `par_iter`, and
it worked. And not only did it work, but I was using it across a file directory,
that had something like 500,000 photos in it, and it was just, you know,
printing out the names or something like that, or moving them. It was a simple
backup tool that I was building, but I went from sort of multiple seconds of run
time to imperceivable amounts of run time. It's just mind-blowing that that's
not more widely leveraged, and more widely appreciated. I suspect the Rust
incumbents, the people who are really diehard about Rust are out there because
`rayon` is a hugely popular crate, and so is `crossbeam`, and some of the others
that it's built on. And obviously `tokio` is huge, which probably aligns more
with what you were saying earlier, about the architecture might do more blocking
in the future.

But yes, specifically, maybe we should move back to the JSON thing for a moment,
because there's a very, very, very popular crate that I'm thinking of, that I
won't say the name of for the moment, that's used in Rust for serializing and
deserializing JSON. It is able to do so in an incredibly performant matter as a
result of Rust's type system. And that's probably the last thing about Rust we
haven't talked much about: the type system. How much did you guys leverage that
in your implementation of RedisJSON 2?

__Christoph__: Take a look at the GitHub code base, if you're interested in the
details, I'm almost tempted to say. No, I mean, as I said, this is the reason
why we spent an awful lot of time in getting the SDK layer right, because
everything that runs on top of the SDK is type safe. As far as I know, you don't
have any unsafe code blocks in your RedisJSON 2 implementation. And other
implementations that are forthcoming, of modules in Rust. This is the reason why
so much effort went into properly designing the SDK codebase, and minimizing the
overall impact, in terms of unsafe code blocks and also performance overhead,
goes without saying, inside the crate. Because every microsecond that you spend
in the SDK doing superfluous tasks, that could have been either done on the
server side, or in your maybe parallelized module, you are spending too much.
And this is the reason why the SDK crate also doesn't tend to be
(_unintelligible— 44:33_) in terms of complexity and lines of code, because it's
similar to Redis, minimal in implementation, but designed properly and
engineered thoroughly, because of these reasons. Because everything that is
relying on the SDK shouldn't contain unsafe code blocks.

__Jeremy__: Yeah, well, I mean, there shouldn't be any unsafe code, in an ideal
world, but we can be more realistic, as supposed to less idealistic when it
comes to that, I think, given the state of things. Great, so I want to be
respectful of your time, obviously, and we're probably running up against it
here, but I will throw a link to your podcast, and your FOSDEM talk, and GitHub,
as mentioned earlier, in our [show notes][episode] and things like that. But before we wrap
up specifically talking about Rust, I want to ask you two purely opinion
questions which are: What's your Linux distro of choice? And what editor do you
use when you're working in the best programming language in the universe, Rust?

__Christoph__: I'm almost sounding probably a little bit biased here. Full
disclosure, I'm an Arch package maintainer. All the ARM cores that don't run
Android run, actually ALARM, which is Arch Linux for ARM. And the other machines
I use Ubuntu, Debian, Fedora, and CentOS.

__Jeremy__: All of the big ones.

__Christoph__: So its's a mixture of many distributions of choice, but I reckon
I'm not kind of disclosing any secrets here, for the production ARM cores, and
for the playground Intel-based, I'm using Arch. And the editor of choice, it's
tricky. It basically depends on the project at hand. Full disclosure, apart from
Rust, I do use other programming languages, too. So sometimes it's PyCharm,
sometimes it's IntelliJ. But if I program in Rust, if I'm doing this in an
embedded fashion, I would— you resort to Emacs, because Emacs runs everywhere.
And if it's as small as a SheevaPlug or something comparable. If I'm working on
a full blown GUI like Ubuntu, like CentOS, like Fedora, I would normally, I
reckon, the editor of choice would be Visual Studio Code, because the language
integration, even going beyond RLS, which I think is the next big thing for the
community, is just excellent.

__Jeremy__: I couldn't agree more. Well done. Excellent. Cool. Is there anything
else we should have talked about? It's interesting just now, that you mentioned
the ARM processors, actually. I guess you must be pretty stoked about Apple's
most recent news that they're going to be—

__Christoph__: A14? Yes.

__Jeremy__: It's been a long time coming.

__Christoph__: It's a fun fact that not that many people know. That actually
Apple now is coming back full circle, because the PowerPCs, as coming from IBM,
that was the latest rage before Intel were actually RISC architectures. Not
necessarily ARM-based ones like the A14 that Apple is currently targeting the
new generation of Macs with, but rather something coming from IBM, having its
origins in something called ROMP 802. You're going back to the 70s now. Because
Intel was— sorry, that IBM was probably the first company to take a serious look
at what can be done with regards to reducing the instruction set.

__Jeremy__: Yeah, it was IBM and those guys at Berkeley, David Paterson, really,
that kicked RISC off. And at the time, everybody was laughing at them, thinking
they were idiots, right?

__Christoph__: That's exactly it, yeah. ROMP, actually, I don't know if you know
what the 801 project— I can't remember the name, but somebody in New York State
took a very serious look at the typical usage of IBM 370 assembler instructions,
and came up with the conclusion that your only app stack, like COBOL or other,
or IMS, or other application stacks at the time, would only use 15 to 20% of the
overall code base. Hence this idea of doing it better and doing it faster. And
hence 801 was born, I think in 1975 or something. It's on Wikipedia, people,
look it up.

Yeah, one final plug, if I can squeeze in a shameless plug.

__Jeremy__: Squeeze all of the plugs in.

__Christoph__: There is, of course, the FOSDEM talk, there is redis.io. There is
also the community page on [redislabs.com](https://redislabs.com/). Just google
for it. With the documentation of all the modules. You'll find the codebase on
GitHub. And yes, I run a podcast, not Redis related,
[linuxinlaws.eu](https://linuxinlaws.eu/). So for a little bit of fun, for a
little bit of comedy, because I reckon it would be the first project— it would
be the first podcast, rather, that mingles or that combines humor and open
source, in a kind of, hopefully big way, go to
[linuxinlaws.eu](https://linuxinlaws.eu/). I've just uploaded the 11th episode
yesterday, of season number one. So we have been around for the last four
months, I think. But I think we have now a steady listenership of at least 5.5
people, if not 6.

__Jeremy__: Okay. I'll put a link to that in the [show notes][episode] as well.

__Christoph__: Hopefully, this plug changes this in a better way. It's
[linuxinlaws.eu](https://linuxinlaws.eu/).

__Jeremy__: In that case, thank you everybody for listening. Thank you,
Christoph, Chris, very, very, very much for coming on, and having an interesting
talk. I certainly learned a lot, because this is not anything at all related to
my area of expertise, but I'm sure this is an area, and the domain space, that
Rust can definitely have a strong hand in in the future. So hopefully everybody
enjoyed listening and we'll catch you all next time. Thanks very much,
Christoph.

__Christoph__: Thank you for having me. Take care.
