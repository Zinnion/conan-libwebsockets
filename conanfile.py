import os
from conans import ConanFile, CMake, tools


class LibwebsocketsConan(ConanFile):
    name = "libwebsockets"
    version = "3.2.0"
    description = "Canonical libwebsockets.org websocket library"
    url = "https://github.com/zinnion/conan-libwebsockets"
    homepage = "https://github.com/warmcat/libwebsockets"
    license = "LGPL-2.1"
    topics = ("conan", "libwebsockets", "websocket")
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "lws_with_libuv": [True, False],
        "lws_with_libevent": [True, False],
        "lws_with_zlib": [True, False],
        "lws_with_ssl": [True, False]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'lws_with_libuv': False,
        'lws_with_libevent': False,
        'lws_with_zlib': False,
        'lws_with_ssl': False
    }

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def requirements(self):
        if self.options.lws_with_libuv:
            self.requires.add("libuv/1.29.1@zinnion/stable")
        if self.options.lws_with_libevent:
            self.requires.add("libevent/2.1.9@zinnion/stable")
        if self.options.lws_with_zlib:
            self.requires.add("zlib/1.2.11@zinnion/stable")
        if self.options.lws_with_ssl:
            self.requires.add("OpenSSL/1.1.1d@zinnion/stable")
        
    def source(self):
        sha256 = "5e731c536a20d9c03ae611631db073f05cd77bf0906a8c30d2a13638d4c8c667"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")
