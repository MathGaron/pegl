#!/usr/bin/env python3

'''EGL configuration management.'''

# Copyright © 2012 Tim Pederick.
#
# This file is part of PEGL.
#
# PEGL is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PEGL is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PEGL. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
from ctypes import POINTER, c_int, c_void_p

# Local imports.
from . import egl, error_check

MAX_CONFIGS = 256 # Arbitrary!
int_p = POINTER(c_int)

def get_configs(display, attribs=None):
    '''Get supported configurations for a given display.'''
    configs = (c_void_p * MAX_CONFIGS)()
    actual_count = int_p()
    actual_count.contents = c_int(0)

    if attribs is None:
        error_check(egl.eglGetConfigs(display, configs, MAX_CONFIGS,
                                      actual_count))
    else:
        error_check(egl.eglChooseConfig(display, attribs, configs, MAX_CONFIGS,
                                        actual_count))

    return tuple(Config(cfg, display) for cfg in configs[:actual_count[0]])

class Config:
    '''A set of EGL configuration options.'''
    def __init__(self, chandle, display):
        '''Initialise the configuration.'''
        self.chandle = chandle
        self.display = display

    def _attr(self, attr):
        '''Get the value of a configuration attribute.'''
        result = int_p()

        errorcheck(egl.eglGetConfigAttrib(self.display, self, attr, result))
        return result[0]
