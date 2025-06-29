#  Copyright (C) 2025 Stratos Thivaios
#
#  This file is part of "VKLEDTS", a repository of instrument test scripts.
#
#  VKLEDTS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

##
##
##
## Use this file, to define resource identifiers and easily reuse them in the scripts.
## This is an example file! Copy this and remove the `example.` part from its filename.
## Below is an example instrument "entry". You should remove this and define your own.

lab_scope = "USB0::0x1AB1::0x04CE::DSXXXXXXXX::INSTR"

## Then, if you want to reuse this identifier in other scripts, add `import visares` at the top of your file,
# and then simply use the variable name used here, so with the one above just use `lab_scope`.