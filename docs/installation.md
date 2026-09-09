(installation)=

# Installation
## Prerequisites
This project requires Python 3.10 or newer. It is tested on Ubuntu, Windows and macOS
across Python 3.10-3.14.

## Stable release
To install the latest stable version with `pip`, run:
```bash
pip install -U mobile-env
```

## Development version
The development version can be installed after cloning the [GitHub repository](https://github.com/stefanbschneider/mobile-env):
```bash
pip install -e .
```

Optional extras: `.[test]` for the test suite, `.[docs]` to build this documentation, and
`.[rllib]` for the Ray RLlib wrapper.
