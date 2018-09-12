from conans import ConanFile, CMake, tools
import os

class SnorenotifyConan(ConanFile):
    name = "snorenotify"
    version = "0.7.0"
    license = "LGPL-v3"
    url = "https://github.com/weatherhead99/conan-snorenotify"
    description = "Snorenotify is a multi platform Qt notification framework."
    settings = "os", "compiler", "build_type", "arch"
    options = {"snore_send" : [True,False],
               "snore_daemon" : [True,False],
               "snore_settings" : [True,False],
               "builtin_backend" : [True, False],
               "freedesktop_backend" : [True,False],
               "pushover" : [True,False]}
    default_options = "snore_send=False", \
                      "snore_daemon=False", \
                      "snore_settings=False" \
                      "builtin_backend=True" \
                      "freedesktop_backend=False" \
                      "pushover=False"
                      
    generators = "cmake"
    exports_sources = "build_with_conan.patch","qtime_fix.patch"
    requires="Qt/5.11.1@bincrafters/stable"
    build_requires="extra-cmake-modules/5.50.0@weatherhead99/testing"
    sha256 = "2e3f5fbb80ab993f6149136cd9a14c2de66f48cabce550dead167a9448f5bed9"
    
    def config_options(self):
        if self.settings.os != "Linux":
            del self.options.freedesktop

    def configure(self):
        if self.options.pushover:
            self.output.info("pushover option enabled, requiring qtwebkit")
            self.options["Qt"].qtwebsockets=True
        if self.options.freedesktop_backend:
            self.output.info("freedesktop option enabled, requiring qtdbus")
            self.options["Qt"].qtdbus=True
            
    def source(self):
        tools.get("https://github.com/KDE/%s/archive/v%s.tar.gz"
                  % (self.name,self.version), sha256=self.sha256)
        tools.patch(patch_file="build_with_conan.patch")
        tools.patch(patch_file="qtime_fix.patch")

    def build(self):
        cmake = CMake(self)
        sf = os.path.join(self.source_folder,"snorenotify-%s" % self.version)

        if self.options["snore_daemon"]:
            cmake.definitions["BUILD_daemon"] = "ON"
        else:
            cmake.definitions["BUILD_daemon"] = "OFF"

        if self.options["snore_send"]:
            cmake.definitions["BUILD_snoresend"] = "ON"
        else:
            cmake.definitions["BUILD_snoresend"] = "OFF"

        if self.options["snore_settings"]:
            cmake.definitions["BUILD_settings"] = "ON"
        else:
            cmake.definitions["BUILD_settings"] = "OFF"

        cmake.configure(source_folder=sf)
        cmake.build()

    def package(self):
        pass


