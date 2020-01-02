# ----------------------------------------------------------------------
# |
# |  _custom_data.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-08 12:01:04
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019-20
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Data used by both Setup_custom.py and Activate_custom.py"""

import os

import CommonEnvironment

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

_CUSTOM_DATA                                = [
    ("Windows Kits - 10.0.17763.0", "f8f19a7b35fe7d1c9d651512c9da3fbad9052713ab0f1fcad1252dca9c82dade", ["Libraries", "Windows Kits", "10"]),
]
