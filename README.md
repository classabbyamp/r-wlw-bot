# r-wlw-bot, a Bot for Discord

[![Discord](https://discordapp.com/api/guilds/656888365886734340/widget.png?style=shield)](https://discord.gg/SwyjdDN)

A discord bot with ham radio functionalities.

## Running

### With Docker

See [README-DOCKER.md](./README-DOCKER.md)

### Without Docker

Requires Python 3.9 or newer.

Prep the environment. For more information on extra options, see the [quick-bot-no-pain Makefile documentation](https://github.com/0x5c/quick-bot-no-pain/blob/master/docs/makefile.md).

Install `libcairo` and `libjpeg` (package names may vary by distro or OS). Then run:

```
$ make install
```

Run. For more information on options, see the [quick-bot-no-pain run.sh documentation](https://github.com/0x5c/quick-bot-no-pain/blob/master/docs/run.sh.md).

```
$ run.sh
```

## Contributing

Check out the [development](/DEVELOPING.md) for more information about how to contribute to this project.

## Copyright

Copyright (C) 2021 classabbyamp

This program is released under the terms of the GNU General Public License,
version 2. See `COPYING` for full license text.
