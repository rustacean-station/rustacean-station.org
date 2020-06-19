---
title: "Compile-Time Evaluation, Interpreted Rust, and UB Sanitizing: Talking to Oliver Scherer about Miri"
file: https://audio.rustacean-station.org/file/rustacean-station/rustacean-station-e008-miri-oli-obk.mp3
---

__Ben Striegel__: All right, let me improvise an intro. Welcome to Rustacean
Station, live at RustFest. Well, I mean it's live for me, not for anyone
listening to this. We are here with some micro interviews, to just, I guess,
capitalize on the fact that we are surrounded by people who are themselves
embroiled in Rust everyday. Kind of just in the soup. And our first person, our
first ingredient in the Rust soup is oli_obk. I don't know your actual name.

__Oliver Scherer__: Uh, well, "Oli" comes from Oliver.

__Ben__: Okay.

__Oli__: "OBK" is just my hometown. Short.

__Ben__: Okay. Cool. So who are you?

__Oli__: Right now, I am working on improving privacy in big data analyses.
Making sure that cryptographically, that we can't do anything with your private
data. Other than that, I have been doing my PhD for last few years, and during
which I have been doing most of my Rust compiler work. And right now I'm also
working on the Rust compiler, mostly on `const-eval`.

__Ben__: `const-eval`. And I think today, I wanted to ask specifically about a
component called Miri, which I have heard a lot about, I think. I'm going to—
let's start from the beginning, because not everyone— I'd say actually, very few
people, kind of, understand the whole structure of the compiler and, like, where
MIR fits in and where const evaluation fits in. And so let's just go real quick.
What is const evaluation?

__Oli__: So const evaluation is the process of computing some kind of math or
other operation at compile time, most notably for computing the length of
arrays, or for computing the discriminant of an enum variant. So if you have a
C-like enum, all the discriminants can have integer values, but it can also have
values computed from more complex expressions.

__Ben__: Okay. And what would you do with const evaluation?

__Oli__: So I mostly do, like, whatever is kind of fun, and a little bit cursed.
But the main use case is actually to prove things at compile time instead of at
run time. So you move some information to compile time. For example, instead of
using a vector, you use arrays, because then you know the length at compile
time. And if your use case would be always vectors of the same length, that you
would know at compile time, you could use arrays. And the more powerful `const-
eval` gets, the more things you can do with it.

__Ben__: So kind of just moving operations from runtime to compile time, kind of
running parts of your program up front when you, the developer compile it, and
then like shipping that off to your users and then they get the benefit of all
that work, it's already done for them.

__Oli__: That is one part. You save runtime operations. But the other thing,
that is mainly why I got into it, is you can prove things at compile time by
simply not having errors. Because if you otherwise had some kind of runtime
error, that would happen once the user runs it. But if you do move things to
compile time, you get errors at compile time, and—

__Ben__: That sounds great. We love more compile-time errors around here.
Listening to this podcast, I'm sure that you are the same way.

Yeah, we'll talk more about proving things later, but I want to talk, before you
get into that, the whole the nitty gritty— what is the history of Miri? And so I
think for me, it's a pretty old-ish project, kind of, like began— I think Scott
Olsen or something was the person who— they were working on it as part of an
academic project for maybe their PhD or something. And you know more than that.

__Oli__: Correct, it was their master's thesis. And the project was actually
started right around when MIR was introduced to the compiler.

__Ben__: Around 2012, 2013— or, sorry, 2016, 2017 (_unintelligible— 3:56_)

__Oli__: Yeah. So when MIR was introduced, we still had an old const evaluator,
which is essentially, just like something working on the syntax tree of the
language, and like, the so-called constant folding. So it folds syntax
components to get— so if it sees, like, "2 + 2", it knows, okay, there's an
integer, there's an integer, and there's a plus, I can figure out that this is
4. It is very simple and is also very limited, because once you get into, like,
loops and local variables, it gets like, how do you even do that? It's like, we
never implemented it because it's very hard.

And so with with the advent of MIR there was a new opportunity for the tool now
known as Miri, which is MIR interpreter. So M-I-R-I, the I stands for
interpreter. Meaning, we are interpreting the MIR, sort of like a virtual
machine runs bytecode, but our bytecode is MIR. And MIR is different from the
usual syntax structure, (_unintelligible— 5:04_), display how your source code
looks, because there is no connection to the syntactical version anymore. It is
basically how later compiler stages like optimizers and so on process this data,
so you don't have things like loops anymore. It's basically just all full of
gotos and ifs. And that's it.

__Ben__: So MIR, I guess, kind of, even people who aren't even, like, at all
familiar with Rust compiler. It's just a language used internally in the
compiler, and your Rust code gets compiled to this, and then the Rust compiler
does various analyses on this, and at some point converts that into LLVM IR,
which is what LLVM wants to work on. Okay, and then, so we have an interpreter
in our compiler is what you're saying.

__Oli__: Right. So before we had an interpreter in our compiler, we had the Miri
Project, which was an external project to the Rust project, and what it did is,
it connected to the compiler API and used the MIR data structures to then
implement and interpret on top of that. And the next step after that was taking
parts of the Miri project, and putting them actually into the compiler. So
there's a core component of this virtual machine that is MIR interpreter, which
we want for the const evaluator. We don't want everything. For example, the full
Miri tool had support for doing FFI calls and that. And `const-eval` doing FFI
calls would be something very odd, and we don't want this. So we split out a
core component and moved this into the compiler, and then the compiler is using
this core MIR interpretation engine for the const evaluation.

And at the same time, Miri is using this engine. Since it's already using a
compiler API, it just uses now the engine from the compiler API instead of its
own. So there's a big shared piece of code between the Miri Tool and the const
evaluator. This is called the Miri engine.

__Ben__: Okay. And then, so not all of Miri is actually in the compiler.

__Oli__: No.

__Ben__: Are there other plans to eventually, kind of, move the entire thing, or
we're trying to move to a status where less things live in the rustc repository
directly, and kind of link against. Is it going to be a crate on crates.io? Or
is it gonna be kind of a submodule, private kind of thing, living in the Rust's
repository organization?

__Oli__: So Miri, right now, lives as a submodule inside the Rust project, but
mostly so CI notifies us if the compiler changes in ways that break Miri. Miri
is not actually, like, a core component of the Rust project. It is, although,
installable via `rustup`, so you don't actually need to compile it yourself.

__Ben__: I want to talk about that later, because you told me some cool things
that we could do with that.

__Oli__: Yeah.

__Ben__: But for now, just to finish off the history, how long have you been
working on the compiler in Miri?

__Oli__: Okay, so in Miri, I've only been working on for, like, two, two and a
half years I think. Before that, I was working on the old const evaluator. And
once Miri started taking off, I move completely over there and never touched the
old const evaluator again. So for a short time we actually had two— well, we had
three const evaluators in the compiler. So I was talking about how we have the
new one, the Miri based one. But we also had the old const folding const
evaluator. But there was also an LLVM based const evaluator, which was used for
statics. And this was a very odd situation to be in, to have these three const
evaluators that all had different feature sets. So they were non-overlapping in
some places, they were— everything had some features that the other parts
didn't, except for the Miri one, which had definitely all features that the
other two had. So at some point, once both of them were running in parallel, we
were checking them against each other to make sure that the new Miri const
evaluator did not change behavior. So we're basically running both and checking
the result. And once we were sure everything is good, we removed both of the old
one.

__Ben__: So it has parallels to, kind of, the new borrow checker, where we kept
the old one around for a long time. Kind of comparing with the new one. And once
we were pretty sure that everything was working out well, you remove the old
one.

__Oli__: Right.

__Ben__: This one seemed more transparent. There wasn't as much ceremony because
I haven't heard about this. What time frame was this happening in?

__Oli__: I started in October with, like, a huge pull request to add the—

__Ben__: You mean last month, October?

__Oli__: No, no, no, no, no, no, no. Sorry. This was October 2017, I guess.

__Ben__: Okay.

__Oli__: And once that was merged, I started immediately working on actually
using the new, const evaluator everywhere, which took another three months,
which was in March. And I managed to get it merged, after a few hundred commits
of fixing it up, just after a release. So we had another 12 weeks before it came
into stable, and that was very good, because in the next few weeks, we're
encountering all kinds of problems with it. They're all small problems, but
like, some people had some odd crates, that did curious things. And we had to
adjust for that to work again.

__Ben__: Okay, that sounds great. And certainly now we appreciate having more
const evaluation things. I know that, for example, the first thing that came to
stable Rust was the ability to write struct constructors. I think previously— or
maybe, no, it was being able to call functions, associated functions. And so
whereas previously, if you wanted to write a thing in a static context, you had
to just call the struct constructor. And if you had a private field of that
struct, you were out of luck. And so normally in Rust, you would write, like,
`String::new()`, or `Vec::new()`. But you couldn't call a `::new` thing in a
static, and so we were just kind of, eh. And the original impetus for this was
to allow that to happen, which I'm not sure if that was pre-Miri or post-Miri,
but certainly we have more things available these days.

__Oli__: That was actually pre-Miri for some types, and for some kind of
arguments, so you couldn't do, like, destructuring. You couldn't have local
variables. Some types, just like, you couldn't really work with references. And
so on. And with Miri, like, all of these limitations, they just went away
because, like, structurally they don't exist, we actually had to re-implement
some additional checks to not allow too much because Miri was so powerful.

__Ben__: Not allow too much. Why wouldn't you want to allow more things?

__Oli__: Well, we want to allow the things, and we slowly started removing these
checks again. But we wanted to take it slow. So there's some things where we
weren't sure, like, how they should be exactly designed. For example, Right now,
you cannot take mutable references inside constants and const functions, even if
it would technically be sound. If you look at it as a human, it's just like, we
want to make a nice analysis that permits you to do everything that's OK, but
not the things that are not okay, and this is work in progress.

__Ben__: So then, in terms of today, what can we do with Miri? What's like the
newest— like, so what is the newest stable stuff? I think I've seen some things
where, like, addition, works now on integers, for example, so we could have
like, const two— that's always worked (_unintelligible— 12:36_), that's just
constant folding. But like, what's the newer— I think maybe last December I saw
some of the, like, newest stuff.

__Oli__: So again, separating Miri the tool and the const evaluator, the const
evaluator, like very recently, like two days ago, you're able to take the length
of a string or of an array at compile time. And this by itself, what's already
interesting to a lot of people, because they could include bytes with the macro,
a file, and then get the length of the file at compile time.

__Ben__: Oh, very interesting.

__Oli__: And someone else was also experimenting with this, and implemented
string concatenation at compile time—

__Ben__: On static strings.

__Oli__: On static strings. It is very, very, very unstable and very, very much
undefined behavior, but you're doing it at compile time, so it's not as bad.

__Ben__: Let's actually segue into that: undefined behavior at compile time.
Yesterday at lunch or at dinner, you were talking to me very excitedly about
various things involving undefined behavior in Rust and Miri's use for detecting
undefined behavior. Now, I think in this case, was it Scott Olsen, who part of
his original thesis was the idea behind Miri originally, was to try and, like,
detect undefined behavior? Or am I just inventing that?

__Oli__: I believe at the beginning that was not the intention. I believe in the
beginning, it was mainly to be used as a new const evaluator. But here comes
along Ralf Jung, who then had a big vision of making sure we can prove that a
program has undefined behavior, by running it in Miri the tool. So this is
independent of the const evaluator. The const evaluator does not do a lot of
undefined behavior detection, but Miri the tool, if you run this on a program,
it will try to detect us much undefined behavior as it can. It is very hard to
actually do some kind of undefined behavior that it cannot detect. Yet.

__Ben__: I want to kind of back up here, too, because it's kind of blowing my
mind, in some cases. Let's just talk about undefined behavior as a general
concept, like in C. So in C, part of the thing with undefined behavior is, hey,
here's a thing that we as a compiler as a language, you can't do legally. It is
illegal to do these things, but we can't ever tell if you do. At least not
tractably, or all the time. And so in C, there are things that you just
shouldn't do, because if you do, you are writing undefined C which is not like
compliant C, which happens all the time. It's just unavoidable. It's very easy
to do. In Rust, it should be harder to do. But if you have an `unsafe` block,
you can still do undefined things. But I think you were telling me that your
goal is to eventually make it so that Miri can detect 100% of undefined behavior
in Rust. So what does that even mean? Is it even undefined anymore? If we could
detect it 100% of the time?

__Oli__: So, we need to remember that Miri runs your program like it were a
virtual machine, so it will only detect if this specific run had undefined
behavior. It is not a general, your program is free of undefined behavior, if
Miri passes. It is, in this run Miri did not find any undefined behavior, and
except for the two or three edge cases that we know of, every kind of undefined
behavior would have been detected.

__Ben__: And those edge cases you're saying you have— you're working on making
those go away?

__Oli__: Right. But still, only for the specific input you gave to this specific
program run, you would have had detected undefined behavior. If you change the
input, you would have to re-run again to check if that input would cause
undefined behavior.

__Ben__: Interesting. So it's more like the sanitizers, kind of, that LLVM
provides, but tailored for Rust specifically. And I guess hopefully more
complete. You wouldn't need, like, both an address sanitizer and a thread
sanitizer, because that should just cover all undefined behavior for any given
run. Is it much slower, this virtual machine, then? You're laughing. That's a
good sign, right?

__Oli__: No, it is ridiculously slower. It is several orders of magnitude
slower.

__Ben__: Okay.

__Oli__: The idea is not to run, like, very large programs in it, but like, to
run your, for example, your entire test suite in it or something. But only the
unit tests, like only small, self-contained things. Mostly around your unsafe
code. You will try— at least cover the unsafe code because the safe code should
be fine. So you should be running your your tests inside Miri. Especially if the
source code that is employed has unsafe code.

__Ben__: And how you would do that is, you would use this rustup component which
you mentioned before. How would you (_unintelligible— 17:20_) "rustup install
miri" and then what?

__Oli__: `rustup component add miri`.

__Ben__: `rustup component add miri`.

__Oli__: Yeah. And then, you have a subcommand available, which is called
`cargo miri` and `cargo miri` takes care of everything for you, for running this
virtual machine. What you then can do, if you have a binary, you can do
`cargo miri run` and it will run your program as if you ran `cargo run`, so you
can actually pass arguments and, since it can open files and read files and
write files, it will do a lot of processing that you could normally do.

__Ben__: And could you compose that with `cargo test` somehow to automatically
use Miri on your entire test suite?

__Oli__: Exactly. We had `cargo miri run`, which runs a binary. And we have
`cargo miri test`, which just runs your entire test suite.

__Ben__: Okay, Nice. Very cool. And so, that sounds fantastic. With that, like,
would you recommend people do that today? Is it in a place where you think it
would work for plenty of programs?

__Oli__: So it works for plenty of programs, especially those that do not have
networking, that do not have threading and so on. So if it's very simple tests
that works, if you have just some tests that won't work, you can `cfg` them out
because there's a `#[cfg(miri)]` flag that you can use. And then you can just
comment out— or, not comment out, `cfg` out those tests that don't work. And
that way you can run your entire test suite through Miri. As we already
mentioned, it can be quite slow. That is one part, and there is lots of things
that Miri simply can't do. If you're calling an arbitrary C function, we don't
know that C function. Our virtual machine doesn't know that C function. Most
`libc` functions, we know them. So we implemented them to actually work. But, if
you have some custom C functions, that just doesn't work. You can still try to
run this by implementing the C function as a shim in your own Rust code.

__Ben__: Cool. Um, And then, getting back to constant evaluation stuff. Does it
let us do anything special with the `unsafe` keyword in constant contexts?

__Oli__: So at the MIR level, we don't see `unsafe` anymore. It's just not there
anymore. So you can just run this, technically. We have some static checks that
prevent you from actually doing things that we don't like you to do. Not because
we want to forbid you from doing this, because some of these things can actually
break the type safety of the Rust compiler, if you do undefined behavior at
compile time. And they do this in very subtle ways. So there's more undefined
behavior at compile time then at runtime. One example would be, you cannot
compare pointer addresses at compile time, even though that's trivial at
runtime.

__Ben__: Because you have no address, there's no memory space.

__Oli__: Right.

__Ben__: Or I guess there is, but it's not a user's memory space.

__Oli__: Exactly. So we could compare it, and give you some random results. Even
if that were okay, the problem is, if you do the same comparison at runtime, you
get a different result. And now we have something where the compile-time gives
you a different result than the runtime. And this can actually be used to, like,
break array indexing checks and so on. So it's not something we want to do.

__Ben__: Okay. And then, in terms of upcoming— I know you said that Miri is
further along than const evaluation is, so const evaluation's kind of catching
up with features, where you gradually un-feature-flag them and add them. I think
you mentioned that loops are coming soon to constant evaluation through Miri?
Also branches, so `if`, that kind of thing. Is there anything else?

__Oli__: Right. So these two are, like, the big ones that unblock a lot of
things. And there is— almost all of the stumbling stones have been taken away
now. We basically just need to implement the analysis that allows you to feature
flag the things again. And after we have those, there's an active RFC for
allowing you to call trait methods at compile time. This will allow you to do
various curious things. For example, we can get part of the way there to running
`serde` at compile-time.

__Ben__: `serde`. Okay, yeah, interesting.

__Oli__: Which would allow you to, for example, parse TOML files or JSON files
at compile time, into a data structure, into a static. So your config files,
that you normally do, like, with a `lazy_static` or something, you could do that
at compile time. Which is especially interesting to embedded developers because
they can now use configuration files that were previously not— they previously
couldn't use.

__Ben__: So cool. And then let's also give shouts to everyone else who works on
Miri. So you want to give any names, people who help you out, or who to ask for
help if they had more questions, say?

__Oli__: Ralf Jung and I, who are merging pull requests, and Ralf is keeping it
up to date. So it's always working with the latest compiler. Christian Poveda is
implementing loads of new features into Miri. He, for example, he implemented
file reading and writing, which is a very cool feature. And on the compiler
side, Santiago Pastorino and Wesley Wiser are implementing loads of new MIR and
MIR optimization features, which often depend on const evaluation. So, for
example, constant propagation, optimizing runtime code. We do this by just
running the const evaluator on normal runtime functions and, like, letting it go
as far as it can.

__Ben__: In terms of getting more people to help you work on Miri, have you
been, like, onboarding people, or doing (_unintelligible— 23:00_) sponsorship of
people who want to tackle easy issues, or learn more about this kind of stuff?

__Oli__: So I'm mentoring a lot of issues about— both in the compiler and Miri,
if there's any interest, I'll happily take on more mentees. Right now I have,
like, three or four, but there's definitely space, time available to to do a
little bit more.

__Ben__: Great. I know plenty of people are looking forward to a lot of new
const stuff coming in the future, now that we have async/await, we got to have
new things to look forward to. So okay, thanks a lot for talking to us. It was
great hearing about this. Hopefully you get some more interest in this.
Otherwise, people just happen to know more about it, which is always good. All
right. Thanks for coming.

__Oli__: Thanks.
