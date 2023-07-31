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


### Installation

```commandline
pip install enquire
```

### Basic usage

```python
from enquire.prompt import prompt
from enquire.question import Text

if __name__ == "__main__":
    questions = [
        Text("name", "What's your name?", default="Christian")
    ]

    answers = prompt(questions)
    print(answers)
```


### Question types

#### Text

**Text** is the most basic prompt type. It asks you a question and waits for you to type an answer.
If there is a default value it will be pre-typed for you.

**Params**

`name` - a unique key in the answers dict

`message` - a message to show to user

`validate` - an optional function accepting the current answers dict and the current answer being typed by a user. 
The function must return `True` if the answer is valid. There are built-in validation functions in 
the library like `is_int`, `is_number` etc.

#### Checkbox

**Checkbox** prompt generates a list of checkboxes and asks a user to pick 0..n options.
The resulting answer will be an array of picked values.

### Radio

**Radio** prompt presents a list of options and asks a user to pick exactly one of them.


### Boolean

**Boolean** is a special prompt which is pre-configured **Radio** with only two options - positive and negative.
You can choose how these are named (the defaults are _yes_ and _no_)

---

_This documentation is a work in progress, check out the examples folder to get some usage tips_

To run an example clone the repo, install the dependencies, and run

```commandline
PYTHONPATH="." python examples/text.py
```
