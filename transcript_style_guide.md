
# Transcriptions Style Guide

This is a set of guidelines, that will help maintain a consistent style across
transcriptions done by multiple people.  Many are arbitrary, and possibly wrong.
Feel free to suggest changes or corrections.

## File formatting

Use standard markdown syntax as needed.  Titles probably aren't appropriate.

Before submitting a PR with a new, transcript, word-wrap the text to 80
characters.

## Names

Names should be shown in __Bold__.

The first time a speaker speaks, write their full name.  After that, each time
the speaker changes, write just the first name of the new speaker.  If they go
on for multiple paragraphs, only put their name at the start of the first
paragraph.

If a speaker mentions the name of another person, project, group, website, etc.,
try to make sure the spelling is correct.  If it's not possible to determine
what they're referring to, leave a (?) marker near the name.

## Editorial decisions

None of these have obviously correct answers.  Editorial judgment is called for.
Just do the best you can.

Many words and sounds can be omitted in the transcript:
- Filler words: "The answer is, uh, hm, six."
- False starts: "The answer should... the answer is six."
- Repeated words: "The answer is, is six."
All of these can be written "The answer is six."

Often the word "like" can be a filler word: "The, like, answer, like, is six."
It probably improves readability to remove it.  Be careful, though— sometimes
"like" is part of the meaning of the sentence, e.g. "They were like, this is
broken." (Where "like" indicates a thought or statement attributed to someone
else.)

How much to trim is ultimately a judgment call.  Try to leave the speaker's
style in place but also make the sentences readable.

Try to insert sentence breaks where needed; one sentence that goes on for too
long hurts readability.  If that means you need to start sentences with "And",
"But", "So", etc., that's still better than run-on sentences that go on forever.

If a speaker cuts themselves off mid-sentence, and jumps topics, or interrupts
or corrects themselves, use the UTF-8 em-dash character "—" to mark the break.
Example: "As you would expect, you can compile— the Rust compiler will use the
usual algorithms."

Also use an em-dash "—" to mark the point when a speaker stops suddenly (and
doesn't resume) or if a speaker is interrupted by someone else.

Don't try to fix sentences that are not grammatically correct.  If that's what
the speaker said, it's what should go in the transcript.  If it's not clear
whether they used the correct word (e.g. you can't tell whether they used the
right verb tense), by all means use the correct one by default.

## Hyperlinks

Links should generally be avoided, and instead inserted into the show notes if
they are missing from there.  One exception is if someone says, "we'll leave a
link to that in the show notes," link to the show notes as follows:

1. Ensure that at the top of the page, the following exists (it will compute
   the right link URL from the front matter):

       {%- include util.html -%}
       [episode]: {{episode.url}}

2. Add the hyperlink like this:

        We'll link that in the [show notes][episode] so you can find it.

Another exception to the avoid-links guideline might be if it is not at all
clear from the sentence what is going on (such as if the name of a feature is
given incorrectly).

## When to use `code` tags

Use the inline `code` style when it's clearly a Rust symbol, trait, type, macro,
etc. that's being referred to, e.g. `Option`, `Result`, `TryFrom`, etc.  Editor
search/replace isn't a good idea, because a speaker may talk about a result and
a `Result` in the same paragraph— only use `code` when it's referring to the
specific Rust element.

Also use `code` style for Rust numeric types like `u8`, `u32`, `f64`, etc.

It's fine (and usually helps readability) to translate certain things to Rust
syntax. For example, if someone says "vec of reference to str", it's OK to write
`Vec<&str>`, as long as it's clear that's what they meant.

It's usually much more readable to translate to `code` when the speaker is
spelling out Rust syntax character by character. I.e. if the speaker says
"bracket A comma B comma C", it's best to replace that with `[a, b, c]`.

When a macro is put in a `code` tag, add the exclamation point, e.g. `println!`

Use `code` when a crate is being named, e.g. `serde`.  If the crate name has a
dash (as displayed on crates.io),
then it's probably wise to use the dashed name when referring to the crate
(e.g. `num-traits`) but the underscored name when referring to it in Rust code,
e.g. `num_traits::clamp`.

Use `code` when a literal file name or path is being described, e.g.
`Cargo.lock`.

Most command-line tools should use `code`, e.g. `rustc` or `rustfmt`, or when a
command line is described, e.g. "cargo build dash dash release" should be
`cargo build --release`. Some tools use acronyms or names that are capitalized
differently than the command, so it's OK to refer to Cargo or RLS without the
`code` style.

Also use `code` tags to refer to symbols from other languages.

Put punctuation outside the `code block`, unless it's part of the syntax,
command, etc., for example `git init .` to refer to the current directory.

Sometimes it's not obvious which is correct; just do whatever seems best to
balance usefulness and readability.

## Table of Contents

If an episode contains different major sections (e.g. separate interviews with
different people), and you'd like a table of contents to link to the different
parts of the episode transcript, give each section an h4 title, using the
markdown syntax:
```
#### An Interview With Some Person

#### Another Interview With Someone Else
```

The actual table of contents will be automatically generated.  Just place this
at the top of the file:
```
* placeholder to generate bulleted TOC
{:toc}
```

## Music or other sounds

Don't add any text describing the opening or closing music.

If music is used to break up a multi-part interview, it's fine to write
"(Musical break)" or something like that.

Background noise that's not relevant to the show can be ignored.  If the
speakers respond to the noise, it might be helpful to describe the noise, e.g.
"(sound of duck quacking)" for context.

## Hard to understand words

If the transcriber can't figure out what was said, write (_unintelligible—
XX:XX_) where XX:XX is the timestamp in the audio file (to assist others in
possibly figuring it out).

## Things that need review

If you're not certain something is correct, tag it with something like
(_needs review_ XX:XX), and pester somebody to review it in a PR.
