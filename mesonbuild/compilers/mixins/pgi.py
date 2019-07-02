# Copyright 2019 The meson development team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstractions for the PGI family of compilers."""

import typing
import os

from ..compilers import clike_debug_args, clike_optimization_args

pgi_buildtype_args = {'plain': [],
                      'debug': [],
                      'debugoptimized': [],
                      'release': [],
                      'minsize': [],
                      'custom': [],
                      }


pgi_buildtype_linker_args = {'plain': [],
                             'debug': [],
                             'debugoptimized': [],
                             'release': [],
                             'minsize': [],
                             'custom': [],
                             }


class PGICompiler:
    def __init__(self, compiler_type):
        self.id = 'pgi'
        self.compiler_type = compiler_type

        default_warn_args = ['-Minform=inform']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args,
                          '3': default_warn_args}

    def get_module_incdir_args(self) -> typing.Tuple[str]:
        return ('-module', )

    def get_no_warn_args(self) -> typing.List[str]:
        return ['-silent']

    def get_pic_args(self) -> typing.List[str]:
        if self.compiler_type.is_osx_compiler or self.compiler_type.is_windows_compiler:
            return [] # PGI -fPIC is Linux only.
        return ['-fPIC']

    def openmp_flags(self) -> typing.List[str]:
        return ['-mp']

    def get_buildtype_args(self, buildtype: str) -> typing.List[str]:
        return pgi_buildtype_args[buildtype]

    def get_buildtype_linker_args(self, buildtype: str) -> typing.List[str]:
        return pgi_buildtype_linker_args[buildtype]

    def get_optimization_args(self, optimization_level: str):
        return clike_optimization_args[optimization_level]

    def get_debug_args(self, is_debug: bool):
        return clike_debug_args[is_debug]

    def compute_parameters_with_absolute_paths(self, parameter_list: typing.List[str], build_dir: str):
        for idx, i in enumerate(parameter_list):
            if i[:2] == '-I' or i[:2] == '-L':
                parameter_list[idx] = i[:2] + os.path.normpath(os.path.join(build_dir, i[2:]))

    def get_allow_undefined_link_args(self):
        return []

    def get_dependency_gen_args(self, outtarget, outfile):
        return []

    def get_always_args(self):
        return []