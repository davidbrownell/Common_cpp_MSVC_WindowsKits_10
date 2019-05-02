# ----------------------------------------------------------------------
# |
# |  Activate_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2018-05-07 08:59:57
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2018-19.
# |  Distributed under the Boost Software License, Version 1.0.
# |  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# |
# ----------------------------------------------------------------------
"""Performs repository-specific activation activities."""

import os
import sys

sys.path.insert(0, os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"))
from RepositoryBootstrap.SetupAndActivate import CommonEnvironment, CurrentShell
from RepositoryBootstrap.Impl.ActivationActivity import ActivationActivity

del sys.path[0]

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# Ensure that we are loading custom data from this dir and not some other repository.
sys.modules.pop("_custom_data", None)

from _custom_data import _CUSTOM_DATA

# <Class '<name>' has no '<attr>' member> pylint: disable = E1101
# <Unrearchable code> pylint: disable = W0101
# <Unused argument> pylint: disable = W0613

# ----------------------------------------------------------------------
def GetCustomActions(
    output_stream,
    configuration,
    version_specs,
    generated_dir,
    debug,
    verbose,
    fast,
    repositories,
    is_mixin_repo,
):
    """
    Returns an action or list of actions that should be invoked as part of the activation process.

    Actions are generic command line statements defined in 
    <Common_Environment>/Libraries/Python/CommonEnvironment/v1.0/CommonEnvironment/Shell/Commands/__init__.py
    that are converted into statements appropriate for the current scripting language (in most
    cases, this is Bash on Linux systems and Batch or PowerShell on Windows systems.
    """

    actions = []

    if fast:
        actions.append(
            CurrentShell.Commands.Message(
                "** FAST: Activating without verifying content. ({})".format(_script_fullpath),
            ),
        )
    else:
        if CurrentShell.CategoryName == "Windows":
            # Verify install binaries
            for name, version, path_parts in _CUSTOM_DATA:
                this_dir = os.path.join(*([_script_dir] + path_parts))
                assert os.path.isdir(this_dir), this_dir

                actions += [
                    CurrentShell.Commands.Execute(
                        'python "{script}" Verify "{name}" "{dir}" "{version}"'.format(
                            script=os.path.join(
                                os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"),
                                "RepositoryBootstrap",
                                "SetupAndActivate",
                                "AcquireBinaries.py",
                            ),
                            name=name,
                            dir=this_dir,
                            version=version,
                        ),
                    ),
                ]

        if configuration != "Noop":
            library_version_info = version_specs.Libraries.get("Windows Kits", {})

            # Add the Windows Kit
            windows_kit_dir = os.path.join(_script_dir, "Libraries", "Windows Kits", "10")
            assert os.path.isdir(windows_kit_dir), windows_kit_dir

            actions += [
                # These values are typically set when activating a Visual Studio environment.
                CurrentShell.Commands.Set("WindowsSkdDir", windows_kit_dir),
                CurrentShell.Commands.Set("UniversalCRTSdkDir", windows_kit_dir),
                CurrentShell.Commands.Set("ExtensionSdkDir", os.path.join(windows_kit_dir, "Extension SDKs")),
            ]

            # Binaries
            windows_kit_bin_dir = ActivationActivity.GetVersionedDirectory(
                library_version_info,
                windows_kit_dir,
                "bin",
            )
            assert os.path.isdir(windows_kit_bin_dir), windows_kit_bin_dir

            windows_kit_bin_dir = os.path.join(windows_kit_bin_dir, configuration)
            assert os.path.isdir(windows_kit_bin_dir), windows_kit_bin_dir

            actions += [CurrentShell.Commands.AugmentPath(windows_kit_bin_dir), CurrentShell.Commands.AugmentPath(os.path.join(windows_kit_bin_dir, "ucrt"))]

            # Includes
            windows_kit_include_dir = ActivationActivity.GetVersionedDirectory(
                library_version_info,
                windows_kit_dir,
                "Include",
            )
            assert os.path.isdir(windows_kit_include_dir), windows_kit_include_dir

            new_includes = []

            for include_name in ["shared", "ucrt", "um"]:
                this_include_dir = os.path.join(windows_kit_include_dir, include_name)
                if os.path.isdir(this_include_dir):
                    new_includes.append(this_include_dir)

            if new_includes:
                actions.append(CurrentShell.Commands.Augment("INCLUDE", new_includes))

            # Libs
            windows_kit_lib_dir = ActivationActivity.GetVersionedDirectory(
                library_version_info,
                windows_kit_dir,
                "Lib",
            )
            assert os.path.isdir(windows_kit_lib_dir), windows_kit_lib_dir

            new_libs = []

            for lib_name in ["ucrt", "ucrt_enclave", "um"]:
                this_lib_dir = os.path.join(windows_kit_lib_dir, lib_name, configuration)
                if os.path.isdir(this_lib_dir):
                    new_libs.append(this_lib_dir)

            if new_libs:
                actions.append(CurrentShell.Commands.Augment("LIB", new_libs))

    return actions


# ----------------------------------------------------------------------
def GetCustomScriptExtractors():
    """
    Returns information that can be used to enumerate, extract, and generate documentation
    for scripts stored in the Scripts directory in this repository and all repositories
    that depend upon it.

    ****************************************************
    Note that it is very rare to have the need to implement 
    this method. In most cases, it is safe to delete it.
    ****************************************************

    There concepts are used with custom script extractors:

        - DirGenerator:             Method to enumerate sub-directories when searching for scripts in a
                                    repository's Scripts directory.

                                        def Func(directory, version_sepcs) -> [ (subdir, should_recurse), ... ] 
                                                                              [ subdir, ... ]
                                                                              (subdir, should_recurse)
                                                                              subdir

        - CreateCommands:           Method that creates the shell commands to invoke a script.

                                        def Func(script_filename) -> [ command, ...]
                                                                     command
                                                                     None           # Indicates not supported
        
        - CreateDocumentation:      Method that extracts documentation from a script.

                                        def Func(script_filename) -> documentation string

        - ScriptNameDecorator:      Returns a new name for the script.

                                        def Func(script_filename) -> name string

    See <Common_Environment>/Activate_custom.py for an example of how script extractors
    are used to process Python and PowerShell scripts.
    """

    return
