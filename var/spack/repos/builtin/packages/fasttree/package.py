# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Fasttree(Package):
    """FastTree infers approximately-maximum-likelihood phylogenetic
    trees from alignments of nucleotide or protein sequences.
    """

    homepage = "http://www.microbesonline.org/fasttree"
    url = "http://www.microbesonline.org/fasttree/FastTree-2.1.10.c"

    version(
        "2.1.10",
        sha256="54cb89fc1728a974a59eae7a7ee6309cdd3cddda9a4c55b700a71219fc6e926d",
        expand=False,
        url="http://www.microbesonline.org/fasttree/FastTree-2.1.10.c",
    )

    variant("openmp", default=True, description="Add openmp support to Fasttree.")

    def install(self, spec, prefix):
        cc = Executable(spack_cc)
        if "+openmp" in self.spec:
            cc(
                "-O3",
                self.compiler.openmp_flag,
                "-DOPENMP",
                "-finline-functions",
                "-funroll-loops",
                "-Wall",
                "-oFastTree",
                "FastTree-" + format(spec.version.dotted) + ".c",
                "-lm",
            )
        else:
            cc(
                "-O3",
                "-finline-functions",
                "-funroll-loops",
                "-Wall",
                "-oFastTree",
                "FastTree-" + format(spec.version.dotted) + ".c",
                "-lm",
            )

        mkdir(prefix.bin)
        install("FastTree", prefix.bin)

    @run_after("install")
    def create_fasttree_mp_symlink(self):
        with working_dir(prefix.bin):
            if "+openmp" in self.spec:
                symlink("FastTree", "FastTreeMP")
