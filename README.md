# Puro

[![Build Status](https://travis-ci.org/jvtm/puro.svg?branch=master)](https://travis-ci.org/jvtm/puro)
[![License](https://img.shields.io/pypi/l/puro.svg)](https://github.com/jvtm/puro)
[![Version](https://img.shields.io/pypi/v/puro.svg)](https://pypi.python.org/pypi/puro)
[![Python Versions](https://img.shields.io/pypi/pyversions/puro.svg)](https://pypi.python.org/pypi/puro)

Highly configurable data streams in Python 3.x.

Idea is to use _JSON schemas_ for selecting objects from _input sources_
and passing them to _action chains_.

Both sources and actions implement respective _plugin interface_, and they
can be re-used, configured and glued together in different order via config files.

Priority is to be usable, configurable and human friendly. But according to
initial benchmarks this can be also made _blazingly fast_ -- or at least as fast
as any custom processing would be.

Overall goal is to battle-tested functional core, easy but powerful configuration language
and extendable plugin API modelled after real life data handling scenarios.

These aspects will hopefully make this library worth using.

This is **not** a message queue. This is a component that sits _between_ message queues, datastores etc.

Also, only basic plugins will be provided here. While usable, they might not
adapt to _your_ use-case. Instead of being ready for all possible data formats
everywhere, the provided plugins will do just basic (data agnostic) actions.
Consider them just a bit more than Hello World examples.


## Core

_Python 3.x port, asyncio experiments on-going. Stay tuned!_


## Inputs

Various stream readers and examples will be provided (HTTP, Redis, SQS, Kombu, local dir, ...)


## Selectors

`jsonschema` + possibly others like `kmatch`


## Actions

Can either _data modifiers_ (modify, sanitize, filter, enrich)
or _data storers_ (Redis, disk, databases, message queues, ...)


## Work In Progress

This project is a full rewrite of an earlier, abandoned Python 2.x project.

Pieces will be committed here once things get ported into Python 3.6+ syntax,
and utilizing latest and greatest helper libraries.

Once the basic pieces exist, it is possible to extend the flow by having statistics,
throttling, logging, etc plugins too.
