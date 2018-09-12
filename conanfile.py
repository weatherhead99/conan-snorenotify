from conans import ConanFile, CMake, tools
import os

class SnorenotifyConan(ConanFile):
    name = "snorenotify"
    version = "0.7.0"
    license = "LGPL-v3"
    url = "https://github.com/weatherhead99/conan-snorenotify"
    description = "Snorenotify is a multi platform Qt notification framework."
    settings = "os", "compiler", "build_type", "arch"
    options = {"freedesktop" : [True,False],
               "snore_daemon" : [True,False]}
    default_options = "freedesktop=False", "snore_daemon=False"
    generators = "cmake"
    exports_sources = "build_with_conan.patch"
    requires="Qt/5.11.1@bincrafters/stable"
    build_requires="extra-cmake-modules/5.50.0@weatherhead99/testing"
    sha256 = "2e3f5fbb80ab993f6149136cd9a14c2de66f48cabce550dead167a9448f5bed9"
    
    def config_options(self):
        if self.settings.os != "Linux":
            del self.options.freedesktop

    def configure(self):
        self.options["Qt"].qtquickcontrols = True

    def source(self):
        tools.get("https://github.com/KDE/%s/archive/v%s.tar.gz"
                  % (self.name,self.version), sha256=self.sha256)
        tools.patch(patch_file="build_with_conan.patch")

    def build(self):
        cmake = CMake(self)
        sf = os.path.join(self.source_folder,"snorenotify-%s" % self.version)
        cmake.definitions["WITH_QT4"] = "OFF"
        if self.options["freedesktop"]:
            cmake.definitions["WITH_FREEDESKTOP_FRONTEND"] = "ON"
        else:
            cmake.definitions["WITH_FREEDESKTOP_FRONTEND"] = "OFF"

        if self.options["snore_daemon"]:
            cmake.definitions["WITH_SNORE_DAEMON"] = "ON"
        else:
            cmake.definitions["WITH_SNORE_DAEMON"] = "OFF"

        cmake.configure(source_folder=sf)
        cmake.build()

    def package(self):
        pass


