from conans import ConanFile, CMake, tools
import os

class SnorenotifyConan(ConanFile):
    name = "snorenotify"
    version = "0.5.3"
    license = "LGPL-v3"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Snorenotify is a multi platform Qt notification framework."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires="Qt/5.11.1@bincrafters/stable"
    sha256 = "7d9b13f8994ac18c08ec7e5dcf5bd335e11a4f6203d61ab0765c9e4085b11e7e"
    
    def source(self):
        tools.get("https://github.com/KDE/%s/archive/v%s.tar.gz"
                  % (self.name,self.version), sha256=self.sha256)

    def build(self):
        cmake = CMake(self)
        sf = os.path.join(self.source_folder,"snorenotify-%s" % self.version)
        cmake.definitions["WITH_QT4"] = "OFF"
        cmake.configure(source_folder=sf)
        cmake.build()


    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

