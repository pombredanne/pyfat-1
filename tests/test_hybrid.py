import pytest
import subprocess
import os
import sys
import StringIO
import shutil

prefix = '.'
for i in range(0,3):
    if os.path.exists(os.path.join(prefix, 'pyfat.py')):
        sys.path.insert(0, prefix)
        break
    else:
        prefix = '../' + prefix

import pyfat

from common import *

def do_a_test(fat, tmpdir, check_func):
    testout = tmpdir.join("writetest.img")

    with open(str(testout), 'wb') as outfp:
        fat.write(outfp)

    check_func(fat, tmpdir, os.stat(str(testout)).st_size)

    fat2 = pyfat.PyFat()
    fat2.open(str(testout))
    check_func(fat2, tmpdir, os.stat(str(testout)).st_size)
    fat2.close()

def test_hybrid_rmfile(tmpdir):
    indir = tmpdir.mkdir("nofiles")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.rm_file("/FOO")

    do_a_test(fat, tmpdir, check_nofiles)

    fat.close()

def test_hybrid_onefile(tmpdir):
    indir = tmpdir.mkdir("onefile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])

    foo = tmpdir.join("foo")
    foo.write("foo\n")

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.add_file("/FOO", str(foo))

    do_a_test(fat, tmpdir, check_onefile)

    fat.close()

def test_hybrid_onedir(tmpdir):
    indir = tmpdir.mkdir("onedir")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.add_dir("/DIR1")

    do_a_test(fat, tmpdir, check_onedir)

    fat.close()

def test_hybrid_rmdir(tmpdir):
    indir = tmpdir.mkdir("rmdir")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    subprocess.call(["mmd", "-i", str(outfile), "DIR1"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.rm_dir("/DIR1")

    do_a_test(fat, tmpdir, check_nofiles)

    fat.close()

def test_hybrid_set_system_file(tmpdir):
    indir = tmpdir.mkdir("setsystemfile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.set_system("/FOO")

    do_a_test(fat, tmpdir, check_onefile_system)

    fat.close()

def test_hybrid_set_archive_file(tmpdir):
    indir = tmpdir.mkdir("setarchivefile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.set_archive("/FOO")

    do_a_test(fat, tmpdir, check_onefile_archive)

    fat.close()

def test_hybrid_set_hidden_file(tmpdir):
    indir = tmpdir.mkdir("sethiddenfile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.set_hidden("/FOO")

    do_a_test(fat, tmpdir, check_onefile_hidden)

    fat.close()

def test_hybrid_set_read_only_file(tmpdir):
    indir = tmpdir.mkdir("setread_onlyfile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.set_read_only("/FOO")

    do_a_test(fat, tmpdir, check_onefile_read_only)

    fat.close()

def test_hybrid_set_all_attr_file(tmpdir):
    indir = tmpdir.mkdir("setallattrfile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.set_read_only("/FOO")
    fat.set_archive("/FOO")
    fat.set_hidden("/FOO")
    fat.set_system("/FOO")

    do_a_test(fat, tmpdir, check_onefile_all_attr)

    fat.close()

def test_hybrid_set_no_attr_file(tmpdir):
    indir = tmpdir.mkdir("setnoattrfile")
    outfile = str(indir) + ".img"
    subprocess.call(["mkfs.msdos", "-C", str(outfile), "1440"])
    with open(os.path.join(str(indir), "foo"), "wb") as outfp:
        outfp.write("foo\n")
    subprocess.call(["mcopy", "-n", "-o", "-i", str(outfile), "foo", "::FOO"])

    fat = pyfat.PyFat()

    fat.open(outfile)

    fat.clear_read_only("/FOO")
    fat.clear_archive("/FOO")
    fat.clear_hidden("/FOO")
    fat.clear_system("/FOO")

    do_a_test(fat, tmpdir, check_onefile_no_attr)

    fat.close()
