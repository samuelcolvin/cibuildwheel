---
title: Tips and tricks
---

### Troubleshooting

If your wheel didn't compile, check the list below for some debugging tips.

- A mistake in your config. To quickly test your config without doing a git push and waiting for your code to build on CI, you can test the Linux build in a Docker container. On Mac or Linux, with Docker running, try `cibuildwheel --platform linux`. You'll have to bring your config into the current environment first.

- Missing dependency. You might need to install something on the build machine. You can do this in `.travis.yml`, `appveyor.yml`, or `.circleci/config.yml`, with apt-get, brew or choco. Given how the Linux build works, you'll need to use the [`CIBW_BEFORE_BUILD`](options.md#before-build) option.

- Windows: missing C feature. The Windows C compiler doesn't support C language features invented after 1990, so you'll have to backport your C code to C90. For me, this mostly involved putting my variable declarations at the top of the function like an animal.

- MacOS: calling cibuildwheel from a python3 script and getting a `ModuleNotFoundError`? Due to a [bug](https://bugs.python.org/issue22490) in CPython, you'll need to [unset the `__PYVENV_LAUNCHER__` variable](https://github.com/joerick/cibuildwheel/issues/133#issuecomment-478288597) before activating a venv.

### Linux builds on Docker

Linux wheels are built in the [`manylinux` docker images](https://github.com/pypa/manylinux) to provide binary compatible wheels on Linux, according to [PEP 571](https://www.python.org/dev/peps/pep-0571/). Because of this, when building with `cibuildwheel` on Linux, a few things should be taken into account:

- Programs and libraries cannot be installed on the Travis CI Ubuntu host with `apt-get`, but can be installed inside of the Docker image using `yum` or manually. The same goes for environment variables that are potentially needed to customize the wheel building. `cibuildwheel` supports this by providing the `CIBW_ENVIRONMENT` and `CIBW_BEFORE_BUILD` options to setup the build environment inside the running Docker image. See [the options docs](options.md#build-environment) for details on these options.

- The project directory is mounted in the running Docker instance as `/project`, the output directory for the wheels as `/output`. In general, this is handled transparently by `cibuildwheel`. For a more finegrained level of control however, the root of the host file system is mounted as `/host`, allowing for example to access shared files, caches, etc. on the host file system.  Note that this is not available on CircleCI due to their Docker policies.

- Alternative dockers images can be specified with the `CIBW_MANYLINUX_X86_64_IMAGE` and `CIBW_MANYLINUX_I686_IMAGE` options to allow for a custom, preconfigured build environment for the Linux builds. See [options](options.md#manylinux-image) for more details.

### Building packages with optional C extensions

`cibuildwheel` defines the environment variable `CIBUILDWHEEL` to the value `1` allowing projects for which the C extension is optional to make it mandatory when building wheels.

An easy way to do it in Python 3 is through the `optional` named argument of `Extension` constructor in your `setup.py`:

```python
myextension = Extension(
    "myextension",
    ["myextension.c"],
    optional=os.environ.get('CIBUILDWHEEL', '0') != '1',
)
```
