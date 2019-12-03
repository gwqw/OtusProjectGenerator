#!/usr/bin/python3
"""
    Project generator for OTUS cpp lessons.
    Generates: CMakeLists, cpp and h files, .travis.yaml <- initial versions
"""

import os
import shutil

PROJECT_NAME = "%PROJECT_NAME%"
IS_TEST = "%IS_TEST%"
SOURCE_LIST = "%SOURCE_LIST%"
TEST_SOURCE_LIST = "%TEST_SOURCE_LIST%"

class ProjConfig:
    def __init__(self):
        self.path = ""
        self.project_name = "hello"
        self.source_list = ""
        self.test_source_list = ""
        self.is_test = False

    def create_files(self):
        self.generate_params()
        self.create_cmake_lists()
        self.get_source_lists()
        self.create_source_files()
        self.create_travis_yaml()

    def generate_params(self):
        if self.test_source_list:
            self.is_test = True
            self.test_option = "ON"
        else:
            self.test_option = "OFF"

    def create_cmake_lists(self):
        with open("CMakeLists_template.txt", 'r') as f:
            with open(self.path + "CMakeLists.txt", 'w') as g:
                for line in f:
                    if '%' not in line:
                        g.write(line)
                        continue
                    line = (line.replace(PROJECT_NAME, self.project_name).replace(IS_TEST, self.test_option).
                            replace(SOURCE_LIST, self.source_list).replace(TEST_SOURCE_LIST, self.test_source_list))
                    g.write(line)

    def get_source_lists(self):
        self.source_list = self.source_list.split()
        self.test_source_list = self.test_source_list.split()
        self.source_headers = [s for s in self.source_list if s[-1] == 'h']
        self.test_headers = [s for s in self.test_source_list if s[-1] == 'h']

    def create_source_files(self):
        self.created_sources = []
        if "main.cpp" in self.source_list:
            self.main = "main.cpp"
            self.create_main()
            self.created_sources.append("main.cpp")
        else:
            print("no main.cpp file")
        self.create_headers()
        self.create_other_sources()
        self.create_test_sources()

    def create_main(self):
        with open(self.path + self.main, 'w') as f:
            f.write("#include <iostream>\n\n")
            for h in self.source_headers:
                f.write(f'#include "{h}"\n')
            f.write("\nusing namespace std;\n\n")
            f.write("int main(int argc, char* argv[]) {\n")
            f.write("\treturn 0;\n")
            f.write("}\n")

    def create_headers(self):
        for h in self.source_headers:
            with open(self.path + h, 'w') as f:
                f.write("#pragma once\n")
        for h in self.test_headers:
            if h not in self.source_headers:
                with open(self.path + h, 'w') as f:
                    f.write("#pragma once\n")

    def create_test_sources(self):
        for s in self.test_source_list:
            if s in self.test_headers or s in self.created_sources: continue
            with open(self.path + s, 'w') as f:
                f.write("#define BOOST_TEST_MODULE %s_test_module\n" % (self.project_name))
                f.write("#include <boost/test/unit_test.hpp>\n\n")
                for h in self.source_headers:
                    f.write(f'#include "{h}"\n')
                f.write("\nusing namespace std;\n\n")
                f.write(f"BOOST_AUTO_TEST_SUITE({self.project_name}_test_suite)\n\n")
                f.write("\tBOOST_AUTO_TEST_CASE(test_) {\n\n")
                f.write("\t}\n\n")
                f.write("BOOST_AUTO_TEST_SUITE_END()\n")

    def create_other_sources(self):
        for s in self.source_list:
            if s in self.source_headers or s == self.main: continue
            with open(self.path + s, 'w') as f:
                for h in self.source_headers:
                    f.write(f'#include "{h}"\n')
                f.write("\nusing namespace std;\n\n")
            self.created_sources.append(s)

    def create_travis_yaml(self):
        with open(".travis_template.yml", 'r') as f:
            with open(self.path + ".travis.yml", 'w') as g:
                for line in f:
                    if '%' not in line:
                        g.write(line)
                        continue
                    line = (line.replace(PROJECT_NAME, self.project_name))
                    g.write(line)

    @staticmethod
    def read_from_cfg(filename):
        res = ProjConfig()
        with open(filename, 'r') as f:
            for line in f:
                if line and line[0] == '#': continue
                if '=' in line:
                    par_name, par_value = (w.strip() for w in line.split('='))
                    if par_name == "PATH":
                        res.path = par_value.replace('"', "")
                        if res.path and res.path[-1] != '/':
                            res.path += '/'
                    elif par_name == "PROJECT_NAME":
                        res.project_name = par_value
                    elif par_name == "SOURCE_LIST":
                        res.source_list = par_value
                    elif par_name == "TEST_SOURCE_LIST":
                        res.test_source_list = par_value
                    else:
                        print("Unknown parameter:", par_name, '=', par_value)
        return res

if __name__ == "__main__":
    if not os.path.exists("proj_gen.cfg"):
        print("Error: proj_gen.cfg is not in current dir")
        exit(1)
    if not os.path.exists("CMakeLists_template.txt"):
        print("Error: CMakeLists_template.txt is not in current dir")
        exit(1)
    if not os.path.exists(".travis_template.yml"):
        print("Error: .travis_template.yml is not in current dir")
        exit(1)
    cfg = ProjConfig.read_from_cfg("proj_gen.cfg")
    #print(cfg.path)
    cfg.create_files()
