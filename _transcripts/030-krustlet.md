---
title: "WebAssembly on the Server with Krustlet"
file: https://audio.rustacean-station.org/file/rustacean-station/rustacean-station-e030-krustlet.mp3
---

__Jeremy Jung__: Hey, this is Jeremy Jung. This episode I'm talking to Taylor
Thomas about running WebAssembly on the server with Rust. He's an engineer on
the Azure team, the core maintainer of Helm, which is a package manager for
Kubernetes. And he's currently working on Krustlet, which runs WebAssembly
applications within Kubernetes. Also, during our conversation, you're going to
hear us talk about wasm; that's shorthand for WebAssembly. All right, I hope you
enjoy my talk with Taylor. Taylor, thanks for joining me today.

__Taylor Thomas__: Thank you for having me, Jeremy. This is my first Rust-
related podcast, so it's exciting for me. I'm a fairly new rustacean, all things
considered. So I'm happy to be here.

__Jeremy__: For people who aren't familiar with the world of Kubernetes and
containerization, all these different things. Could you start by explaining at a
high level what Kubernetes is?

__Taylor__: Yeah, so Kubernetes is a container orchestrator, and you've probably
at least heard of Docker if you're in the technology world, even if you haven't
used it. But Docker is a technology that made something called containers
popular and useful. Those technologies have been around for a while inside of
the Linux kernel. That's why they call it a container; everything is inside of
this thing, and contained in this process. It uses cgroups and kernel
namespaces. There's a couple different things under the hood that are going on,
but basically it allows you to create an artifact that can be bundled up into
something called an image, and the image can be passed around and then be used
multiple times. So often, people will compare those to VMs. VMs were a big
revelation because you didn't have to go literally put in a new blade if you
needed a new server or reboot something; you had to instead just say, okay, I
want a new VM. But you still had to install a whole operating system. It was
like spinning up a new computer. And so containers made that even more simple,
because instead of having to do that, it's using the same shared underlying
kernel calls and things underneath the hood. But everything's isolated, so if
you want to spin up three different instances of, let's say, like, an nginx
server, all you'd have to do is create three containers that are all running at
the same time, and those will all have the same specification that you basically
baked into it. They're an immutable artifact. If you want to create a new one,
it has a new hash and a new version, that allow it to use.

So this was really good for people, but the problem was, how do you orchestrate
it across everything? And that's where Kubernetes came in. So Kubernetes takes
that and says, okay, well, we have a huge fleet of nodes that's out there. How
do I schedule each of these containers properly so that they're either like, not
on the same place, or that they meet certain requirements. Or that I have a
certain number of them. And it takes care of all that, including some of the
underlying networking connections, so that you can connect all your your
containers to each other, in a distributed and actually self-healing way. It
goes through loops, and if something goes wrong, it will try to heal that
container and make it come back to a normal running state. And so it is a very
powerful technology. It's caught on— maybe it's caught on a little too much in
some people's opinions. But it's a useful tool for containers that came about,
and a lot of people are using it for underlying infrastructure projects.

__Jeremy__: It kind of reminds me a little bit of when you're using something
like AWS. And it has some form of auto scaling for VMs. And let's say that you
have an application, and it runs on virtual machines, and you would be able to
tell AWS, for example, as more people are accessing my application, I want you
to create new VMs, run new instances of my application. Something like
Kubernetes is able to do something similar, but maybe at a more generic level of
being able to figure out OK, how many machines do I have access to? And any time
I'm asked to run something, I'll go and find the right machine to run it on, and
it's always going to be in the context of these containers, it sounds like. Did
I kind of get that right?

__Taylor__: Yes, it's very much a generic tool across all these different
things. Nowadays, you can run it with with Windows or Linux or— mostly Windows
and Linux, but there are some limitations there. Yes, it's a very generic tool
in terms of being able to connect what you want and use what you want, to make
this distributed platform easy. And like you said, it will scale things. It's
just like those— if you've done something in AWS where you have the elastic
things where they'll scale, it's a similar thing. There's something in
Kubernetes that you can set up that will automatically scale to make sure that
you have the right amount of capacity for what you're doing.

__Jeremy__: And I think this sort of takes away the need for the developer to
need to understand where their applications are going to run. Its— you give some
kind of configuration to Kubernetes and say, here's my app, and then it just
figures out where to run it and how many instances to run and that sort of
thing.

__Taylor__: Yeah, it's really meant as a DevOps or SRE kind of tool, that
instead of it being a— they have to, like, custom-tailor machines, they already
have these Docker images in place and can just run them, like you said. You just
give it the configuration. And it is still involved. It's not like a magic
bullet there, but you don't have to care as much about where it goes. If you've
configured everything properly, it just kind of does it.

__Jeremy__: I wonder if you could paint a picture of where containers fit, in
between just running a full machine versus running a single process on a
computer.

__Taylor__: Essentially, a container is just a running process, a single
process. And because it's a single running process, you can run multiple of them
on a machine. The tools that you need installed, all the binaries, all those
different things are encapsulated inside of this container, and so that way, you
can run 10 of them on a machine instead of spinning up 10 servers. So it allows
a little bit more density. Obviously, you still have to be careful about, like,
noisy neighbor problems, and other things that normally happen in
infrastructure. But it allows for much more condensed areas, and the spin up is
much quicker. If you have a small image, you have to get— getting a new one, and
spinning it up is easily under 30 seconds every time. Bigger images can take
longer. But even then it's still faster than provisioning a full VM for what
you're trying to do. And so this fits for a lot of different kinds of services
that don't need, like, very large requirements on the system. And even if you do
have large requirements, you can use Kubernetes in a way that can be helpful.

__Jeremy__: And so you're talking about how these containers are a process
running on the system. So for example, if I were to, in Windows, look at the
task manager or in Linux, just run `ps`, I would see individual processes for
each of these containers that are being run.

__Taylor__: Yes, it really depends on the implementation, but essentially,
that's what's going on. With Docker, there's some other underlying details that
we don't need to get into, but essentially you would see processes that are spun
up, that are doing the work, but they are just processes underneath the hood,
instead of being a full operating system.

__Jeremy__: Next, I want to talk a little bit about WebAssembly, because I know
that's an important part of the Krustlet project that you work on. Could you
explain a little bit about what WebAssembly is at a high level?

__Taylor__: Yeah, so WebAssembly, as you can probably guess from the name, is a
tool that was originally designed for the web. Now that's— I think the original
creators didn't necessarily intended to be that way. But that's the name that it
has, and that's what it's used for. There's multiple companies— big websites
that use WebAssembly, and the idea behind WebAssembly is that you can create a
binary that can then be— so it's compiled code that can then be run in the
browser, so giving you the speed of compiled code, while also still being
sandboxed inside of the browser sandbox environment. So this allows for some
very performant things to be done. You have things like rendering tools. I know
one that I've seen, an example I always give as one, like Autodesk, which—
they're a maker of CAD tools and rendering tools. They have a lot of online
things that run WebAssembly, because it gives that the performance it needs to
be able to do those more complex tasks.

And so, that's where WebAssembly started. But the idea is, WebAssembly could be
used anywhere. And when you pull out WebAssembly from just the browser, it
allows you to have kind of a universal interface. And what this is called,
they've defined it and there's a working group, and it's still very much a work
in progress. But it's called WASI, which stands for WebAssembly System
Interface. And that interface is a definition of basically how it can interact
with the system. And the nice thing about it is, it's still that sandboxed
model, you have to grant explicit permission to do anything. So if you want it
to be able to access a file somewhere, you have to grant access to that file
ahead of time before you started. It's not there yet, but I assume when we get
to some of the networking socket support in there, it will also have those same
kind of things; you have to grant specific permission for it to do it. Whereas
opposed to containers, you have a little bit different security model because
you're still running, like, into the normal Linux security things that you have
to deal with. There's ways to break out of a container. There's not really a way
to break out of a WebAssembly module in the same way because you're not running
in these, like, you're running a compiled code thing somewhere, instead of
basically, like, a shim over specific binaries or things that are being run. So
that's the main difference, and this allows things to be run on any system.

One of the things that we saw with Docker, and that we were really hoping when
we had Docker was that it could run anywhere. But if we're being honest with
ourselves, it can't really run anywhere. Docker, and containers in general, are
a Linux tool. Now there's people who, at Microsoft and elsewhere, have made
Windows containers a thing. They work, they work well. There's some really cool
work they've done there, and there's nothing I have nothing to say against that.
They've done great work. But really, if you have a nginx container, you can't
run that on a Windows machine. You can run it on a Windows machine, but it's
technically running a Linux VM behind the scenes. Same thing on a Mac. And so it
isn't truly this ideal of write once, run anywhere.

Now obviously, there's still technical challenges that you can't do it
completely, but you can— so if I compile a WebAssembly module, a WASI-compatible
WebAssembly module on my Mac, I can pass it to you, and you can run it on a
Windows machine, on a Linux machine, on a Raspberry Pi. It doesn't matter,
because— and it will be the exact same code. So that is a very powerful thing
that we saw in WebAssembly that fits also fairly well inside of this container
space, and what we could do with it.

__Jeremy__: Help me to understand a little bit more about what WebAssembly
actually is, because— does WebAssembly itself have bytecode, or some kind of
language that you're passing to a runtime, like, for example, an example I can
think of is the Java virtual machine, where people can write many different
types of languages, such as, I believe Clojure and Scala. They can write a
language that generates Java bytecode, and is run by the Java virtual machine,
and so you can run those applications anywhere that you can run the Java virtual
machine. Is WebAssembly similar? Is there a language for WebAssembly that is the
target for, say, Rust or C or different languages that you want to run in
WebAssembly?

__Taylor__: That's a really good question. It is similar in the sense that it
does write code, then could be interpreted anywhere. And there are various wasm
runtimes. The ref implementation that we're using within the Krustlet project is
called Wasmtime. And that's the one that's following the WASI spec and is
essentially the reference implementation for the WASI specification. And that
one can run on any of these systems that you've mentioned. And it has a bytecode
that it interprets in that way. And there's a lot of technical details we could
dive into there, that I'm not a huge expert on. I know the basics, but there's
some that are just, like, JIT compilers, right? So just in time, there's some
that are, like, a pre-compilation step that can happen before. All of these
things can happen. But the thing is, this is much more lightweight and small and
constrained than the Java— the JVM would be in this case, right? So it's a much
smaller and compressed use case, but it does have the similarity that it is
bytecode being interpreted by some sort of runtime.

__Jeremy__: And this bytecode, because you've been talking about how there are
different, I guess, implementations of the WebAssembly runtime— You gave
Wasmtime as an example of that— Does that mean that as long as you target the
WebAssembly bytecode, that any of these different runtimes could run that code.
Is that how it works?

__Taylor__: Yeah, and that's why the WASI specification is kind of the thing
that's making it work on the server side, rather than just in the web, is
because we need those specifications for how to interface with different things
on the machine. And so, there's also this other thing called interface types,
which also defines, like, how you can interchange different data types in
between different parts of applications. To be clear, this is an area that's
still under heavy development. For example, Wasmtime and WASI in general hasn't
even finalized their network specification, so you have to kind of do
workarounds and things to get networking in place. Now that's coming, but, like,
this is very bleeding edge in that sense.

__Jeremy__: And so this bytecode can run in the browser, in whatever WebAssembly
runtime is built into the browser, and then it can also run outside the browser,
in a runtime such as Wasmtime. And it sounds like the distinction there is that,
when you're running outside of the browser, you need some kind of consistent API
to be able to access the file system, access network, things like that, which
would normally be handled by the browser. But once you take it outside of the
browser, you need some common interface that knows how to make system calls, to
open a file on Windows versus open a file on Linux. And that's what a runtime
like Wasmtime would do by implementing what WASI describes. Is that, sort of—
did I get that right there?

__Taylor__: Yeah, that's a great summary of how this works.

__Jeremy__: Cool. So one of the questions that I think people often have, is
when you work with languages like Rust or Go, they can be compiled ahead of
time. You can get a binary that you can run directly on your operating system.
For languages like those, what are the benefits of using WebAssembly to run an
application, versus just using that binary?

__Taylor__: It just depends on, I guess, the situation you're trying to do with
it, like, there's certain tools, like the idea is, what we have with with wasm
right now isn't meant to replace Docker entirely. I think it opens up new cases
for people who aren't already into Docker or need to— or have some specific
things, but also this makes— there's a certain amount of portability and
security that comes from using wasm. Obviously, if you build a binary and then
you build it for each system, you have the, like, native things, all built in,
all ready to go, which has a distinct advantage over something like having to
work through an interface. However, that security model is what gives us a lot
of hope for the future of this because you have to explicitly grant permissions.
And it's a compile-once. I don't have to compile my Windows version. I don't
have to— so you don't have to worry about cross-compiling toolchains, or the
different VMs that you have to spin up, to build one for Arm, and for Mac, and
for Linux, and for Windows. And you know, all those— all the different targets.
You don't have to worry about that with wasm. You just build the one binary and
it's ready to go.

It's also very, very small. If you do some— even without optimizations, you're
talking like a meg or two megs for a simple application. As opposed to a full
binary, when you build it— and Rust binaries are fairly small— Go binaries are
larger because they've compiled in the runtime. But like, Rust, even though
their binaries are small, this is even smaller. And if you strip it out, you
could get it under a meg, depending on what it's doing. Now that size really
matters with something like Kubernetes. So if you start with a container, and
you pull down an image, some of those images, even if you're using, like, the
very slim things are still 20, 30, 40 megs. Now, that's not a big deal, but
there's some of these bigger ones, especially when people are doing, some of the
bigger applications are close to a gig. Now that's not recommended. I know
people say, "but that's not a recommended practice." Yes, I know it's not. But
what actually happens in reality is, people will do that. And so when you pull
down, if you have a new version, even though they've cached certain layers, and
things are the same, it still takes a while to pull the new version, and start
it up. Whereas wasm is just these tiny modules. And even if we haven't done
something super big, But I'm guessing that even if it's only— even if it's huge,
it's only a few megs. And so then you're you're pulling this down, and this is
very quick and very fast and the added security benefits on top of that, where
you're not having to deal with the same security layers as what is available
inside of a container. That very explicit grant on your security surface is a
very powerful thing for us inside Kubernetes on the server side.

__Jeremy__: And that security piece is a little interesting. Is that when you're
building the WebAssembly application, that you're explicitly building in, this
application will have permissions to the file system at these paths. Or kind of,
what does that look like?

__Taylor__: So it's not built in at compile time. Now there is one, when we get
talking a little bit more about Krustlet, that we have another implementation.
And there's one was started by Capital One called waSCC, which is WebAssembly
Secure Capabilities Connector. There's lots of W's here in this space. And so
this this waSCC runtime actually does things called capabilities, where you can
explicitly— you're actually supposed to explicitly say, I need this capability,
and I'm signed to have this capability. But wasm by default, and the WASI spec,
you grant it at runtime, you say, I'm going to give you access to this file, or
I'm going to give you the permission to do this thing. So those things are done
at the very beginning of your runtime. Not when you're compiling in.

__Jeremy__: Interesting. And then so that would be some kind of configuration
file. Maybe that would say, okay, when you run this wasm application, only give
access to these permissions, and like you were saying before, that's much
simpler than something like a Docker container, where your permissions model is
actually based off of a Linux operating system.

__Taylor__: Yes, it's much simpler in that sense. I mean, you're still— there's
more overhead involved. If you were spinning this up completely manually, you
have to say, okay, I need to give it access to this directory, and I need to
give it access to this thing. But Kubernetes kind of takes care of that for you,
and we do that inside of Krustlet, with what we're doing, to kind of abstract
some of that away so you don't have to do it. So I mean, it's like most security
tradeoffs, right? Like the most secure thing is a server that's not connected to
the Internet, and is inside of a locked room, right? Like that's— and you can
only access it in that room with a badge. That's like the most secure you can
get. But that computer is kind of useless. So that's the idea behind the
security tradeoff is now, you're just being explicit about what you're granting
instead of just having all these implicit things of, oh, I can access the
network, and I can access this thing, and I can access this thing, which comes
by default as running a process on an operating system.

__Jeremy__: When you were talking about being able to run the wasm application
anywhere, that sounds like a benefit, because normally when you have a build
server for, for example, an open source project, you'll see that they have to
target all these different operating systems. They may have to build their
application for six or eight different OSes. And in the case of using
WebAssembly, they could just build it once, and it would technically run on any
of those, it sounds like.

We've been talking about WebAssembly on the server. Before we get into how
Krustlet runs wasm applications, if I had a wasm application and I just wanted
to run it on my machine, what does that look like? Is there some kind of package
manager, or how am I running these applications?

__Taylor__: So there's a couple different ways that these can be shared around.
There's no specific implementation right now. The thing that we started with,
inside of Krustlet itself, is we used the OCI specification, which is the exact
same thing that the containers use. It's just storing it as a different artifact
type. There's some work by the people working on waSCC. They have something
called Gantry. And there's a couple other people who are looking into how you're
supposed to store modules. So the idea behind all of this is we have to figure
out what exactly we want to do. So it's kind of a little bit in the air.

We have a tool that was built by somebody on the team called wasm-to-oci. And it
does the work of pushing that to a container registry that supports arbitrary
artifacts. And so what you can do is take that, and pull that down, and it just
pulls down the compiled module file. It's always something-dot-wasm. And then
you can use whatever runtime you want to use to run it, so you can download
Wasmtime and install that. You could do— there's Wasmer, there's wasm3, which is
kind of optimized for embedded devices. Those are the kinds of things that you
can do. You have to choose what runtime that you want to use. And then you have
to grab the module from somewhere, wherever that might be right now, which is
still, like I said, a little bit of a, loosey goosey kind of thing.

__Jeremy__: And if I was just in the context of running an application on my
computer without involving Kubernetes or anything like that, would it be where I
get a single file? That's the wasm application. And then I pass that into, say,
Wasmtime or something like that, just at the command line, and that's how I
would run it?

__Taylor__: Yeah, that's exactly how it would work locally. Now, obviously,
we're working on building this to make it even more fully-featured. The ideal
would be that then you can have an application that could be easily swapped
across machines. I mean, imagine if you had something like notepad, or some sort
of editor, and then you could do it there, and then just take that same
application and then have it somewhere else, without worrying about what kind of
system it is. You could have your Raspberry Pi 4 running a random desktop
somewhere, you could pass it over to a server, and do a virtual desktop session,
like, you could do anything crazy that you wanted to by passing that around.

__Jeremy__: Cool. Yeah, I mean, it's this idea of having a truly universal
binary, I guess. Having the ability to copy this application anywhere, and run
it without having to worry about, I guess, basically anything, you just need to
have a wasm runtime.

__Taylor__: Yeah, and that gives it some, quite a bit of power, right, because
you could jump from an edge device— I'm using edge in the loosest possible term,
because it could mean anything. But like any type of edge device all the way to
a server running in a data center. It could be anything along that whole
spectrum of different servers that can run this and you can pass it around, and
you can even start to think about how you could maybe hot-swap it, right, like
you could point at one running implementation of it. And then when you don't
have access to that because you lose Internet, you could point it at a local
instance of how to run this.

__Jeremy__: Very cool. Now maybe we should go a little bit more into Krustlet. I
know you've talked a little bit about what it is, but maybe you could go a
little more into detail about what Krustlet is.

__Taylor__: Yeah, So Krustlet stands for Kubernetes Rust Kubelet. Lots of K's.
The main idea behind Krustlet was we wanted to create— we wanted to re-implement
the kubelet, which, a kubelet is basically the binary that runs on a Kubernetes
node, that connects it to the cluster and runs it and joins. So that's a
kubelet. And we wanted to write it so we could do WebAssembly. And now the
reason we wrote it in Rust was for a couple reasons. Number one, since you're
probably listening to this because you like Rust and you do Rust, Rust has
probably the best WebAssembly support for server-side things.

Most languages at this point actually have WebAssembly support, but it's mostly
geared towards the browser. But WASI is something you can easily add in. It's
actually, you just use rustup and do `rustup target add wasm32-wasi`. And that's
how simple it is to start compiling for WASI-compatible wasm binaries in Rust,
And so, that is a very powerful and useful tool to have around, if you could do
it that easily. If you look at some of the other examples, like C or C++, you
have to customize clang properly, or download the already pre-configured
toolchain, and use that clang, and then also you have a couple other languages
that support it. But Rust was a fully featured language that we could use it
with, but also Rust has caught our attention for a while just because of its
application inside of distributed systems and compute— like normally, it's
looked at as a systems engineering language. But can we use it in these cloud
applications? This idea of "cloud native" is the buzz word right now. Can it be
used in a cloud native way? And so it was— a secondary goal here was to prove
that it could be done like that. Plus, you add on all the safety and security
and correctness features inside of Rust, and it really helps us out.

So we wrote several blog posts about that, that I can probably send around or
link around if you send out show notes. But the main idea is that— it has
prevented us from shooting ourselves in the foot. Go has really easy concurrency
things. Sometimes that's one of the things that I most miss about using Go for
some of this, is if I want to do concurrency work, it's quite simple to set up.
It's built into the language. It's very simple to do. But the thing is, is that
there are bugs that we got caught where you sit there and be like, where
everyone gets mad and like, why are you getting mad at me, borrow checker, like,
I've done everything— and then you're like, oh. It's caught that down the line,
I'm going to— if I were to do this, I'd have two people trying to read the same
data. And that has been very useful and exciting for us because it stopped us
from doing those things. And so the guarantee that when your Rust code compiles,
that it will be correct, even if it's not necessarily the right code, it's at
least correct, and you're not going to have weird data race access issues inside
of your code. And so that was the secondary reason that we found, it was just
very powerful for doing that.

And also, it's expressiveness with traits, and how generics work gave us a good
deal of flexibility inside of Kubernetes. Having dealt with both— extensively
with both the Kubernetes Rust client and the Kubernetes Go client, the
Kubernetes Rust client is much more ergonomic, due to how traits work and
generics. And so that was just something that we really enjoyed coming over. But
it also, like I said, the main thing was that it had such good wasm support
already built in. And really, most of the wasm runtimes are being written in
Rust right now. So it makes sense for us to be in this space. So that's why this
project was created, was to have the ability to easily run Rust things inside—
or, easily run wasm inside of Kubernetes. So that's why we used Rust, and why we
came up with Krustlet.

__Jeremy__: Yeah, that makes a lot of sense, because it reminds me of, I had a
conversation with Armin Ronacher in an earlier episode, and he works with Sentry
on different debugging tools and things like that. And the reason why they chose
to use Rust in parts of Sentry is because there are a lot of existing tools, or
a lot of existing crates in Rust related to compilers, or related to reading
debug files and things like that. And so in your case, the community had already
done a lot of work in WebAssembly, and that's why it made sense to choose Rust.
So I think it's interesting how there's these certain niches that people have
built up, and continue to cultivate and continue to bring additional projects
in, because of that base. It's very cool.

You had mentioned a little bit earlier about how Rust has really good support
for WebAssembly, and so it's easy to get something up and running in WebAssembly
using Rust. But you had also mentioned with WASI that there are only certain
features of the system that are implemented, like you had mentioned that there
aren't network calls implemented yet, and I wonder when you're writing a Rust
application, do you have to do anything special when you're trying to target
WASI, for example, if I were to make a network call in my Rust application, and
I try to compile it to be run in WebAssembly is the command line tool going to
tell me, you're trying to use an API that doesn't exist? Like, how does that
part work?

__Taylor__: That right now is a very rough edge. It just depends— I haven't
tried to direct compile in with a network call yet, but most of the time, if
you're doing something that can't be compiled, the compiler will go in and say,
like, I can't find a linked thing— like when it's trying to link and do things,
like I can't find anything that links this together, or that I'm able to compile
this in and it'll spit out an error, and sometimes it's very obtuse. It just
depends on what is. This is— like I said, it's a very rough edge right now
because it is so new, when you are compiling. But for the most part you actually
write things the same way. There's some things that you might need to pull in to
make sure that you don't do something incorrectly or that you've had the correct
things attached to the data structure, whatever it might be for the specific
case, there's actually some good examples inside of, like, Wasmtime and a couple
other places. But for the most part, you write code pretty much how you just
normally would.

__Jeremy__: So it sounds like currently, like you said, you pretty much write
code as normal. You run it through the command line utility, and then you may
get a helpful error message, or you may get one that's really hard to decode.
And then you basically start digging around the Internet trying to find out what
might be wrong.

__Taylor__: Yeah, that's kind of how it goes. Now luckily, people are very
responsive to this in the community, but we're working with them to work around
this, and there are possibilities of using networking. So the waSCC examples—
that's one of the reasons we chose to use waSCC, is because it has networking
support built in. Now the way it works is kind of just working around the
problem. You have a capability that's built for the native system, and so if
you're doing it on a on a Mac, there's— you can either load it from, like a
dylib file, or like an object file of some kind. Or you can have it compiled in,
which is what we do in Krustlet. And so when we build it for Windows, it gets
that compiled part for Windows. When we build it for Mac, it's going to have
that compiled thing in there. And so, like, it's just working around it by
creating a component of the system that is then linked by waSCC to be able to
talk— forward calls around. And so when something calls the networking thing,
that call gets forwarded to the WebAssembly module, which handles it and passes
it back out. There's not actual networking inside of the module itself, and so
it works around it. It's a bit different of a model. It's an actor model, as
opposed to the Wasmtime implementation in Krustlet, which is more of a— working
like a standard container. I use that term very, very loosely. It's more like, I
have a process, I'm running that process for as long as it wanted to, and then
it's done, as opposed to responding to specific, like, actor calls that come in
from a host.

__Jeremy__: So Wasmtime and waSCC are two different WebAssembly runtimes. When
you're talking about these processes running as actors, I guess, would that be,
this would be a case where if you want to run a number of processes and you want
them to communicate with one another, that's when you would choose waSCC. I'm
trying to understand when you would use one runtime versus the other.

__Taylor__: So right now, like if you were to go download Krustlet right now and
try it. Basically, you have— If you were going to be using Wasmtime, the only
way to communicate is by, like, data on files, because it can access files, so
you could mount a shared volume and then, like, pass it off, so it could do data
processing. But it can't do communication very well, until we get the— until
WASI finalizes how it's going to do networking. If you want to do a full thing
with waSCC— so the thing with waSCC is, you can use it entirely out of
Kubernetes as its own thing. It's almost— it's very similar to, like, a
functions as a service kind of tool. You write your things in whatever language,
compile into a wasm module, and then it handles connecting all those things
together and the capabilities model around it gives it a security, an additional
security layer, that you have— things are signed, so all your modules have to be
signed. And then you have to say that it has access to specific capabilities. So
whether it can access another capability that another WebAssembly module is
exposing or whatever. And you can glue all these together so that you could pass
calls around. And it also has actually an ad-hoc networking tool called Lattice
to connect multiple nodes together. So it can run entirely outside of
Kubernetes. But it also has a bunch of tooling and things around it. So when
you're going to do it, you're buying into that system, and you have to know that
that's what you're doing. Wasmtime is meant to be, like I said, following that
same WASI specification. So as soon as WASI gets networking, then we'll
implement the networking stuff. Just because we want to make sure that we have
the, more like, here's the vanilla option, how you glue it together. If you want
more of this, like, quick functions kind of thing than waSCC is an amazing tool.
And so we implemented that because we've been collaborating with them for a long
time. And so we've had that implementation there so that it can be, show another
way waSCC can be used, while also helping people who want to try this right now,
and hack around to do things with networking.

__Jeremy__: Does that mean there is some specific API call, I guess, that you're
using within your waSCC actors that allows it to communicate with the other
actors? But it's not like general network calls. It's a very constrained API. Is
that right?

__Taylor__: Yeah, there's an underlying thing they call waPC, W-A-P-C. So it's
WebAssembly protocol— I can't remember it. Basically, it's the protobuf of this
world. It's a message protocol. Here's how I'm sending a message back and forth.
And so each actor, is what it's called, is a WebAssembly module that can respond
to specific events, and so it registers specific event handlers for those
events. And when the underlying host that's running all these gets it, it
dispatches those events to the actors to run.

__Jeremy__: And so if you were using that with Krustlet, then the way that the
actors communicate with one another, or communicate with the host, that would be
configured automatically, by Krustlet, I guess, or what—

__Taylor__: To an extent.

__Jeremy__: Okay.

__Taylor__: That's why I was saying, that it can be used more fully-featured
outside of the Kubernetes world. But it has a distinct place inside of Krustlet
as well, and so Krustlet will do some of the configuration, to a point. Like, it
will make sure all the capabilities and stuff are configured, but we're, for
example, we're still trying to define, well, if somebody wants to add other
capabilities, how do they define that? Which normally you do— there's a
freestyle block inside of a Kubernetes configuration called an annotation. So
we're thinking, Well, do we do it with an annotation, or do we do it with
another tool? We don't know yet, but right now it does that base configuration,
like, if it, it'll set up— make sure you have, like, HTTP server access and that
you have access to do logging and that you have access to all those things it
sets up for you. But we have to still define a way of, what's a safe way for a
user to say, I need this capability.

__Jeremy__: When you've been developing Krustlet, you've mentioned how there's a
lot of existing WebAssembly capability in Rust or projects built in Rust. Are
there other parts of the Rust ecosystem, or specific crates that helped you
speed up your development a lot?

__Taylor__: Yeah, there are. In terms of development tools, I have really loved
`cargo expand` when I'm doing some of the macro stuff. Async things do a lot of,
like, additional macro things that, like, build stuff out or wrap things in. So
it's kind of nice to see that. I also learned about a bunch of different tools
around how to debug stack overflows because we were accidentally pinning some
stuff too early, and it was causing a stack overflow that we didn't discover
until Windows, because it has a smaller stack. And so there was some really
interesting things on the nightly compiler, like how to print type sizes. That
was really helpful in identifying things that could have gone wrong.

And looking at our other tools. We've really enjoyed the Kubernetes crate for
it. It's called `kube`, and that one has some really awesome, awesome tools in
it that are very helpful. I think a lot of them are things that people have
heard of. `serde` or "ser"—, I can never— I feel like that's a constant debate
in the Rust community.

__Jeremy__: I thought it was SER-DAY, but I don't know.

__Taylor__: I think it's SER-DAY because its serialize-deserialize, but anyway,
yeah, so that's there. That we've used a lot of, and has been very helpful.
Obviously, the `tokio` runtime has been helpful for us as well, but really,
like, it just depends. There's not, like, any other crazy tools we've used
outside of it. I mean, I do have to say a huge, huge thanks to those who are
those who are working on, like the `kube` crate, and some of these other things.
We've been able to contribute back, because we found bugs, and other stuff. I
love the `rustls` crate as well, which has been very helpful for Windows because
then we don't have to have an OpenSSL dependency. And so, those are the
different things that have been, I guess, really helpful to us, as I've, like,
looked through and seen all the different things that we've done in our code.

__Jeremy__: At the start of the episode, you mentioned you're relatively new to
Rust. The languages you had used previously, would that be like, Go, or what are
some of the other languages you have a lot of experience with?

__Taylor__: Yeah, I am a rustacean by way of Go. I kind of like, moved all over
the place. So I've done a lot, I mean, I've done a lot of Python, like for glue
code, when I've done some more SRE work. I did Node back when it was starting to
become a thing, right, and then moved on to Go. And then we have— and then I've
been doing some Rust since then. So yeah, it's just— I come from Go, that's my
main background. Before this was a lot of Go, because I was in the Kubernetes
space, really heavily. Well, I still am, and so that's where I got my Go
experience from. So that's my background with it. Coming from Go to Rust is
really the current thing that's happened.

__Jeremy__: And since you have experience with Go, I'm wondering, are there
things that you miss from Go, either in the language itself, the runtime, or
even just the ecosystem that you wish that Rust had?

__Taylor__: Yeah, there's a few things we've run into here. Overall, I am very
pleased with Rust. And would choose it for a lot of different cloud projects,
depending on what I do— I think Go, this is totally personal opinion here, but I
think Go is very well suited for smaller, like, true microservices, or anything
similar. Very small constrained tools because it's quick to get started, it has
such a constrained vocabulary. And one of the things I appreciate particularly—
and some people hate this, and some people like it, but I like that generally
there is a way to do something in Go. There's sometimes two, sometimes three,
but most of the time, there is a way to do it, and when coming to Rust, there
was 40 different ways to do the exact same thing, and so that was something that
I missed.

The other thing I've said is that I really— I kind of mentioned, I said before—
that the concurrency story is much better in Go. And now, it doesn't provide the
same security— or not security, correctness that Rust provides. But it's so much
easier to get started and to spit things back and forth. And it's just been, as
a relatively new rustacean, I kind of get frustrated by the fact that there are
two, three, async implementations?

__Jeremy__: `tokio`, `async-std`.

__Taylor__: Yeah, those are the two that I know. I think there was one more,
right?

__Jeremy__: I think there's `smol`, I think is how you say it?

Taylor, Yeah, `smol`. It's supposed to be like a tiny— but yeah, it's so— and I
know that's a common complaint, and people have done a lot of work on those. But
it's very frustrating because you, like, get bought into that specific
implementation, and it's like, let's choose one and make it part of the standard
library, or make it the blessed crate, or whatever it is just so we can all
standardize, and not have to, like have weird hook ins to each runtime, and all
those kind of things. So that that's been fairly difficult to work with
sometimes.

Most of it's just otherwise, like ergonomics. I know that we're going to be
writing a blog post on this soon, but inside Krustlet we were doing a state
machine graph. It was more— it's kind of like a cross between, like, a
traditional state machine and walking a graph. That we were doing to be able to
encapsulate the logic inside of Krustlet a little bit better because they were
turning in to monster functions that were just ridiculous. And because of that,
we started to run into some of these things. In Go, You have their interfaces,
right? And these interfaces, you can just keep calling through and chaining
through. But because of how the type security that comes through the trait
system, and things here in Rust, it made it really difficult to find a way to
just iterate. We finally found a way around it. It was a little bit clunky and
well, like I said, we're going to write a blog post on it, kind of explain
everything. But there's just some of those things where the boundaries Rust puts
on you make some things very difficult to figure out, to make it work in a way
that's both rusty but also readable, to someone trying to write it, That was one
of those things, like, I just see some of those rough edges sometimes that just—
and I'm not sure if there's a way to solve that. That could just be me airing my
grievances, but like, that's something that I missed. There's a little bit more
flexibility that comes from the Go model, with some of the things that we've run
into here. But like I said, I feel that that's worth it, given the security and
things that we've gotten in return.

__Jeremy__: So you mentioned one of the things with Rust is that there's so many
different ways to do the same thing. And as you were learning the language, I
wonder, what was your approach to figuring out what is the ergonomic way to do
things, and I guess just how to pick up Rust in general?

__Taylor__: It was a combination of clippy, and I mean, everybody loves clippy.
Some people get really mad at clippy, but like clippy at least tells me like,
oh, hey, like, you're right. But this, you could do this more efficiently, or
you could avoid an extra allocation. Or you could do all those kind of things.
Learning to read the compiler messages. You get trained from reading other
compile— like, when other things fail, you look where the compile error failed,
what line. And then you go there because normally it doesn't give you very much
information. But with Rust, you have to go through and read, like, okay, it's
telling me this went out of scope here, or was passed here, and you need to go
do this, or you need to go do this, or you need to go do this. All those things
can be very useful when you're reading a Rust compiler error message. So those
were the other things.

The other thing I had to— and this is, I think, one of the bottlenecks, is that
I had to go to an experienced rustacean, who was— like a couple experienced ones
to go get the help. And that's what I love about the Rust community: people are
very willing to help. There's like the Rest Mentors page that I know was
mentioned at RustConf recently, that I hadn't heard about. But the big problem
is that that's still kind of a bottleneck, whereas with other languages, I've
been able to find, like a least semi-clear examples of, this is a good way to do
it. Or this is how these things were handled. I mean, an example of this is
`to_string` versus `to_owned`, which technically, they almost do the same thing
when you're doing it with, like, from— is there proper name for an ampersand-
string like, just like the strings slice, right? Those things, the `to_owned`
versus `to_string`. Really, what it turned into is, there used to be a
difference. But then there was— now it's just clear, like I just need this as a
string, then I use `to_string`, but if I'm using it in a case where I have one,
but I need an owned copy that I use `to_owned`, even though they're— I think
they, at this point, they call the same underlying logic.

And so, learning those kind of things, I had to learn from people. I didn't—
there wasn't, like, something that could say, hey, like, here's the history of
this, or even in the documentation, which Rust's documentation of the functions
is really good. It doesn't say, like, you should use this here or here. There's
no specific suggestions. And so if there's one thing that I hope we can improve
is maybe how we can document, like, that intermediate level because getting
started there's stuff, but then otherwise you're kind of bottlenecked at
specific, like asking other rustaceans, hey, how do I do this thing? And that
makes it a little bit harder for people.

__Jeremy__: Yeah, I'm not sure what the solution for that is, whether that's
like you said, some other intermediate guide, or— but then again, it's kind of
like, how do you determine what to put in there, and and how do people get
directed to that, versus the relationship you're talking about, where you're
talking to experienced people, and they just have all that context in their
head, and they can tell you. It's a hard problem to solve, for sure.

__Taylor__: Yeah, and like I said, the compiler is fantastic. A lot of times you
learned from the compiler messages. That's how I finally learned that when you
give a static constraint on a trait, that you're not saying it has to be static,
it just has to fit into a static which, like, I was, like, mind blown moment
right there. And I was like, oh, that's cool. Okay, I get it now. But before I'm
like, I don't want to make this static, that's going to bloat the size of this.
And I like, I can't have this allocated on the stack, like, this is huge. But
it's like, no, it's just saying, this needs to fit in a static, and I'm like,
okay, And I learned that, I think, from the compiler. I could be wrong, But I
think the compiler said, this doesn't fit in something, whatever, like, wait a
second. And I dug into it and found it. So I think that a lot of the work that—
people discussed this at RustConf, about making the compiler just kind of guide
you through things, and anticipate it, is quite impressive, and I'm very, very
happy with that. So maybe that is that intermediate way that it'll eventually
get there. But I'm just saying that I think that there's some tooling there. But
when people get in, that that learning curve is just a little bit— I like to
describe it as logarithmic, right? Like it's just, you have that initial punch
over the top. And then once you understand that, you can be quite capable of
producing things quickly.

__Jeremy__: You were talking about some of the issues you ran into, or
roadblocks where you needed to get more intermediate help or or talk to people
more experienced. I wonder, when you first started, how did you first start
learning Rust? Did you go through the Rust programming book? Did you start
making little small projects? I'm curious how you approached that.

__Taylor__: I did a combination of both. I tried to do some of the, like, Rust
By Example, the Rust Book, just some of the basics. And then I tried
implementing— I tried re-implementing some parts of different projects I'd had
in the past, or things I just wanted to try. And then I went on with trying to,
like, actually implement in a real project, which was Krustlet, and you can see,
if you actually look at the Krustlet code, you can see where like, oh, they must
have been new there. And we've been going through and cleaning that up as we go
along. But having that real project and something I could go towards, that's how
I learn best, is just having, like, an actual goal of either re-implementing
something or finding, like, an actual project to go dig into. And that's how I
work. But it's a little bit different for every person.

__Jeremy__: Was there a moment, I guess, where you felt like you were really
struggling, and then once you passed this point, that Rust clicked for you? Or
was it— did it feel pretty straightforward as you were going through the
process?

__Taylor__: It was a little bit gradual, more than like, a specific moment where
I was like, oh, everything clicked. I do have those moments, like I had
mentioned before, like when I understood what a static constraint on a trait
means, I was like, oh, mind blown, I finally get it. But it was more of— once I
started actually doing more complex traits, or trait bounds. I think when I
finally felt I was getting it was when I could do something like a "where T:
this plus this," and "N: this plus this," like with the long constraints at the
end of a function, and understood what it was doing and why I did it that way.
And I think also a combination of implementing some of the traits like `AsRef`,
`AsMutRef`, those kind of things that I could pull out or, like, convert or have
a wrapper type, and I'm like, okay, I'm finally getting how all this glues
together. That's when I noticed, I think, that okay, like, I can do this now. I
can put together some cool things.

But yeah, it comes— each thing comes with its own accomplishments. Like I had
mentioned before, we had the state machine that we've just finished and we're
cleaning up right now, and that state machine thing was, like, okay, we finally
got something that worked. I think it's recently where I felt like, okay, I feel
like I can actually be a good contributor to the community and maybe even start
mentoring others properly, because I have the knowledge to do it. Because now,
now we've created something new, that as far as we can tell, people haven't done
something like this in Rust before, outside of just toy things. And so, that's
why I'm excited. I wish we had it done today, so I could say, here's this blog
post. But I'm really excited for that because we're going to talk about, like,
all the work we built on from people in the community who had posted about it,
and all these things and it— okay, we managed to get something that works. It
still, like, has rough edges. It still has things that we've got something that
works well for us, and so I— that's been fairly recent, and so I think there's
just moments where, like, I keep understanding more. But for me it was more of a
gradual turning of like, oh. And then all of a sudden I realized like, oh no, I
think I've gotten to the point where I know it. It wasn't like a click like I
know it is, oh, I just realized I actually know what I'm doing now.

__Jeremy__: Yeah, yeah. No, that makes sense. You've been mentioning how
Krustlet has some rough edges. And I know on the project page it mentions how
it's highly experimental. What do you think are the big parts that are that are
currently missing for somebody who would want to go in and actually host their
application using Krustlet?

__Taylor__: Well, one of them is completely outside of our hands, which is
networking in WASI. We're trying to work with the community to do that, and
we're going to see if there's a way we can at least solidify and jump in and
work on that. But we're getting close. So this is— no one can hold us to this,
But we're hoping to get towards a 1.0 release towards the end of the year, or
beginning of next year. And so, like around the holiday season, things will slow
down, whatever. So that's why we don't know, it could be January, February.
That's what we're hoping for. And really the big things that we have are: we
have basic volume support, but we don't have cloud volume support, so we're
going to be looking at a way of how we can make sure every provider can use
this.

We're trying to solidify the API at the same time with that, because we have
people who are writing other providers. And a provider is just something that is
an implementation of a runtime. And so we've written ours for wasm. But we have
another person who's a core maintainer, his name is Kevin, and he's been
recently made a core maintainer of the project as well. And he's working on one
for containers. So he's just moving the container implementation stuff over to
Rust because of all the security benefits and things. And so we need volume
support for all the providers, and then we're going to try— and then we're going
to figure out a way we can abstract the networking, probably using the same
interfaces that Kubernetes has already defined, so that we can have networking
implementations more readily available, and connected into these things from the
rest of the Kubernetes world.

And then after that, we need to have, like, real demos— like we have demos, but
we need, like some— I'm going to, like— here's a real application, in so far as
you could make it real. And take that, and put together some bootstrapping
thing, so it's easier for people to set it up. We want to make it as one-click
is possible to set it up. And so, those are kind of the things we're looking at,
and that people can look for rough edges. But if you want, for example, if you
wanted to trigger like data pipeline processing, you can use just waSCC, or you
can glue together waSCC and a WASI provider, which is the Wasmtime one. You can
glue both of those together, or have two of them running, and you can trigger a
data chain using an HTTP call and then process the data using— you can do that
right now.

We had an intern on our team over the summer, and she did some work on Raspberry
Pis, using a Raspberry Pi Kubernetes cluster, and then using Krustlet to read
soil sensors. You can do some fun things with it, it's just not all the way
there. And that's partially because of where things like— this is, this is
bleeding edge. And that's why we put, like, the big warning sign on the readme,
like, please don't run this in production. This is so new— not just the project
itself, but also the technology around it. And so that's what— those are kind of
like the steps we have. So at this point, I would say— I maybe would remove the
"highly" from Krustlet's description right now, if I was really wanting to,
because now it's just, this is an experimental project. That's kind of the goal
for the future here. But we're not that far out from having something where it's
a 1.0 where people can actually, people can start using it in a real way. Maybe
not perfectly, but in a real way.

__Jeremy__: Last year, Solomon, the CTO of Docker, he had tweeted that if WASI
and wasm had existed in 2008, then they wouldn't have needed to create Docker.
And I'm wondering, from your perspective, thinking about the future of wasm and
Krustlet, do you think that running applications in wasm could become the
default for server-side applications in the future?

__Taylor__: It's a possibility. I wouldn't peg it entirely for sure. I think it
will be a mix. People are just, like, getting on board with Kubernetes stuff and
containers, which sometimes, like I said, I think some people go way too far
into it, and don't think— they're just like, oh, they hear Kubernetes and
buzzword and want to do it. But people are still just barely getting to that
thing, so it'll be a long time if it does become the default. But I think it has
the ability to reach a very specific audience right now, and have that grow. A
lot of these constrained environments like edge computing, you can't run Docker
on there. It's too much, too much overhead. The— just can't handle it. But you
could run wasm modules. It also allows you to pack things in more tightly,
because if everything is a small process, that's just this tiny little thing and
tiny little bundles, you can run that with— we can run a lot more than you could
with containers right now. So I wouldn't say that it's going to— it's not a
container killer, nor is that our current goal, like, we didn't think that,
like— we don't want to disparage that other technology. That's something we
still use a lot and effectively. But I do think that there is going to be some
takeover of that space, at least in a small measure, with all this stuff from
wasm and WASI. Because if it's just portability and the ideal of, we'd be closer
to a write once, compile once, run anywhere kind of situation.

People say it's a pipe dream. I think we'll never get completely there. Even
with wasm, there's still constraints. There's still things that will be in
place, but this makes it easier and having— if every language gets to the point
where you could do it with Rust, or you just say, here's my WASI target and
build it, that to me sounds like a very powerful way of doing it, and not just
for server-side. I think that can reinvent a lot of things with normal
applications as well, just because of how portable they are and how then
applications could be tied to you, instead of just like being tied to a computer
or whatever it might be. So there's some really interesting ideas here. It's
just— those ones are a little bit further out, but I do think even in the short
term we'll start seeing some good applications where WASI will be— WASI
compatible wasm binaries will be a better choice than using a container.

__Jeremy__: And it sounds like maybe in the short term, you were talking about
edge computing, and that might be something like where you have a CDN running
application code at their their edge nodes. Something like Cloudflare's workers,
or Fastly has an equivalent. Are you thinking that might be where these things
start?

__Taylor__: I think that's where it's already started, in one sense, and that's
one of the reasons we chose Kubernetes. We think there's more beyond Kubernetes
and server side on my team. That's our belief, that we believe there's more to
that. But everybody is getting into trying to do Kubernetes and have this—
Kubernetes has become an API layer that people understand, that a lot of people
use. And enabling wasm through that API gives people a reason— We want people to
start using this and say, hey, like, why doesn't my (insert language of choice)
have the support for wasm, like WASI binaries? Can we please get that? And then,
as people do that, we start getting more motion around it.

__Jeremy__: I know when I talk to people about WebAssembly, sometimes what I'll
hear is, they'll say, well, I'm happy writing JavaScript in the browser. Why do
I care about WebAssembly? Right? And so, like you say, if there are more use
cases for running, other than just in the browser, then that might inspire other
languages like Python or Ruby or who knows what other languages, to focus on
getting them to work on WebAssembly. So I think that's pretty exciting.

So I think that's a good, good place to start wrapping up. If people want to
learn more about Krustlet, or about what you're working on, where should they
head?

__Taylor__: I would definitely start with the actual project site, so that's
[`deislabs/krustlet`](https://github.com/deislabs/krustlet) on GitHub. There is
also some posts that we have in various places. I wish there was, like, one
amalgamation of all of this, but you could look at the
[`deislabs.io/posts`](https://deislabs.io/posts/), I believe. Let me just double
check that.

__Jeremy__: And we can probably get the Krustlet-specific posts and then put
those in the show notes as well.

__Taylor__: Yeah, I can send those. But it's
[`deislabs.io/posts`](https://deislabs.io/posts/). That's posts for all of our
projects, but you'll see some, at least three blog posts there about Krustlet.
One was around our stack and heap allocation problems that we had, and some
lessons learned there. So those were some other places you can go. We have some
other posts that hopefully we can send in the show notes that kind of give an
overview of the different things, like the reasoning behind this. If you're more
interested, that's from a high level, like a business perspective. We have a
post for that. We have some other things about the security things we got from
it that we've posted around. So there's lots of sources of information there,
but if you really want to get started and look at the project and install it and
try it out, go ahead and check out
[`deislabs/krustlet`](https://github.com/deislabs/krustlet) on GitHub, and that
one will have the docs and everything you need to get started.

__Jeremy__: Very cool. Taylor, thank you so much for talking to me today. It's
been interesting learning about Krustlet, and wasm, Kubernetes and all that, and
I think it's going to be very interesting to see where it goes in the future.

__Taylor__: Well, thank you very much for having me. And hopefully everyone
finds at least some of this interesting and useful.

__Jeremy__: I hope you enjoyed the conversation with Taylor. Special thanks to
FFromm for giving me the idea for this episode in the Rustacean Station Discord.
All right, until next time, see you.
