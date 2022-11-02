Minimal-ish example of editable vs normal POTENTIALLY WRONG conan2 flow for third-party libraries

# Flow as-is
## Scripts

- `scripts/run_conan_steps.sh` - "editable" flow. Doesn't clear the editable flag (you'll need to do that manually)
- `scripts/run_conan_install.sh` - used by the CMake to generate toolchain/package files for the host project.
  If conan is installed into the system/user and not into `.venv`, this can be avoided
- `scripts/conan_init.sh` - `.venv` initialization and hook installation

## Hooks
- `enforce_layout.py` - simple script to beat developers who are testing out-of-source third-party scripts without
  providing a proper layout. Without this it can easily end up with a tarball unpacked all over your conanfile.py

## Minor issues

- `CMakeUserPresets.json` is generated in the root folder near `CMakeLists.txt` and will break VSCode if build directory
  is removed. Can be worked around by moving conan logic into a subdirectory/included cmake file. Or conan should just
  stop generating stuff no one asked it for

# Missing documentation clarifications

- `editable` doesn't use `package()` call results. The point of the editable to use the build results as-is, without
  an installation, so you can make changes and recompile the editable package and immediately see/use results in a host
  or another third-party lib
- This means editable needs a potentially different layout (where includes, libs, etc are) than the one described by
  the normal `package_info()`
- `self.cpp.*` stuff you can set in layout is needed for editable. `.source` stuff is relative to the source directory,
  `.build` stuff is relative to the build directory.
  See `hello/conanfile.py` for some additional comments on how all those different infos interact
- You can also set `self.cpp.package` which in theory should be used to initialize `self.cpp_info`.
  But I didn't test that

In general, editable requires an additional setup and is a somewhat advanced thing. So it shouldn't be used as a default
package testing mechanism. By default, one should use `source`/`build`/`export-pkg`/`test` -> `create`. A build-sequence
script (similar to `scripts/run_conan_steps.sh`, but probably in python and using conan api, so it can be used in
vscode's `launch.conf`) can be used here as well. Those commands don't need the editable mode

Editable mode needs setup both in `conanfile.py` and in the host's cmake to merge the projects. AFAIK there is no
clear indication in the included targets that the target is in the editable mode, so you'll need to use some outside
registry for editable packages. Which is also a good idea, as `conan editable list` is rather useless

# Conclusions

- editable flow is not batteries included. It needs quite a lot of setup and external tooling. Also the different
  layouts can be quite confusing
- trying to move source-folder for out-of-source `conanfile.py`s somewhere else is a bad idea. It's basically hardcoded
  in more than one place in the conan code. So, the hook/api is your best shot at enforcing a correct layout
