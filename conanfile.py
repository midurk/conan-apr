#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class AprConan(ConanFile):
    name = "apr"
    version = "1.6.5"
    description = "The mission of the Apache Portable Runtime (APR) project is to create and maintain software libraries that provide a predictable and consistent interface to underlying platform-specific implementations."

    topics = ("apache", "portable", "runtime")
    url = "https://github.com/midurk/conan-apr"
    homepage = "https://apr.apache.org"
    author = "Michal Durkovic <michal.durkovic@innovatrics.com>"

    license = "Apache-2.0"
    exports = ["LICENSE.md"]

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    requires = ( "libuuid/1.0.3@bincrafters/stable", )

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "http://tux.rainside.sk/apache"
        tools.get("{0}/apr/apr-{1}.tar.gz".format(source_url, self.version), sha256="70dcf9102066a2ff2ffc47e93c289c8e54c95d8dda23b503f9e61bb0cbd2d105")
        extracted_dir = self.name + "-" + self.version
        
        os.rename(extracted_dir, self._source_subfolder)

        # see https://stackoverflow.com/questions/18091991/error-while-compiling-apache-apr-make-file-not-found
        tools.replace_in_file("{0}/configure".format(self._source_subfolder), '$RM "$cfgfile"', '$RM -f "$cfgfile"')

    def _build_with_autotools(self):
        build_env = AutoToolsBuildEnvironment(self)
        build_env.fpic = self.options.fPIC
        with tools.environment_append(build_env.vars):
            with tools.chdir(self._source_subfolder):
                configure_args = ['--prefix=%s' % self.package_folder]
                configure_args.append('--enable-shared' if self.options.shared else '--disable-shared')
                configure_args.append('--enable-static' if not self.options.shared else '--disable-static')
                build_env.configure(args=configure_args)
                build_env.make(args=["-s", "all"])
                build_env.make(args=["-s", "install"])

    def build(self):
        self._build_with_autotools()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('pthread')
