## enquire

### Goal

**Enquire** is a pet project with no ambitions. However, a bit of history might shed some light on the project goals.

> _It was a cold April morning and the dew on the grass was frozen like a tiny piece of glass._
> 
> _Eric Cartman_

I needed a modern cli prompt library to add some interactivity to my working projects.
[PyInquirer](https://github.com/CITGuru/PyInquirer) turned out to be the most easy-to-use 
and convenient among all the libs I could find.

Unfortunately, the latest version published on pypi had at least one critical bug: it completely ignored
the default value for `list` prompts. The GitHub version does not have that bug, however, it seems to be
abandoned for quite some years.

Since I only needed the basic, the radio button, and the checkbox types, these were implemented first.

---

_This documentation is a work in progress, check out the examples folder to get some usage tips_
