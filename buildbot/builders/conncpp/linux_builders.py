
################################# bld_linux_connector_oddbc ################################
def bld_linux_connector_cpp(name, kvm_image, cflags, cmake_params):
    linux_connector_cpp= BuildFactory()
    args= ["--port="+getport(), "--user=buildbot", "--smp=4", "--cpu=qemu64"]
    linux_connector_cpp.addStep(ShellCommand(
        description=["cleaning", "build", "dir"],
        descriptionDone=["clean", "build", "dir"],
        command=["sh", "-c", "rm -Rf ../build/*"]))
    linux_connector_cpp.addStep(ShellCommand(
        description=["rsyncing", "VMs"],
        descriptionDone=["rsync", "VMs"],
        doStepIf=(lambda(step): step.getProperty("slavename") != "bb01"),
        haltOnFailure=True,
        command=["rsync", "-a", "-v", "-L",
                 "bb01.mariadb.net::kvm/vms/"+kvm_image+"-build.qcow2",
                 "/kvm/vms/"]))
    linux_connector_cpp.addStep(Compile(
        description=["building", "linux-connctor_cpp"],
        descriptionDone=["build", "linux-connector_cpp"],
        timeout=3600,
        env={"TERM": "vt102"},
        command=["runvm", "--base-image=/kvm/vms/"+kvm_image+"-build.qcow2"] + args +["vm-tmp-"+getport()+".qcow2",
        "rm -Rf buildbot && mkdir buildbot",
        WithProperties("""
set -ex
if [ -e ~/libssl-dev*.deb ] ; then sudo dpkg -i ~/libssl-dev*.deb ; fi
git --version
rm -Rf build
export CFLAGS="${CFLAGS}"""+ cflags + """"
time git clone --depth 1 -b %(branch)s "https://github.com/MariaDB-Corporation/mariadb-connector-cpp.git" build
[-z "%(revision)s"] && git checkout %(revision)s
cd build
rm -rf ./test
git submodule init
git submodule update
cd libmariadb
git fetch --all --tags --prune
git log | head -n5
cd ..
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCONC_WITH_UNIT_TESTS=Off -DPACKAGE_PLATFORM_SUFFIX=$HOSTNAME""" + cmake_params + """ .
cmake --build . --config RelWithDebInfo --target package
"""),
        "= scp -r -P "+getport()+" "+kvm_scpopt+" buildbot@localhost:/home/buildbot/build/mariadb*tar.gz .",
        ]))
    linux_connector_cpp.addStep(SetPropertyFromCommand(
        property="bindistname",
        command=["sh", "-c", WithProperties("basename `ls mariadb*tar.gz`")],
        ))
    addPackageUploadStep(linux_connector_cpp, '"%(bindistname)s"')
    return {'name': name, 'builddir': name,
            'factory': linux_connector_cpp,
            "slavenames": connector_slaves,
            "category": "connectors"}
######################## bld_linux_connector_oddbc - END #####################

######################## Current GA/stable version builders ######################
#################$### Current GA/stable version builders - END ###################

######################## New (unstable) version builders ######################
bld_centos8_amd64_connector_cpp= bld_linux_connector_cpp("centos8_amd64-connector-cpp", "vm-centos8-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON ");
bld_stretch_amd64_connector_cpp= bld_linux_connector_cpp("stretch_amd64-connector-cpp", "vm-stretch-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON ");

bld_sles15_amd64_connector_cpp= bld_linux_connector_cpp("sles15-amd64-connector-cpp", "vm-sles150-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_xenial_x86_connector_cpp= bld_linux_connector_cpp("xenial-x86-connector-cpp", "vm-xenial-i386", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_xenial_amd64_connector_cpp= bld_linux_connector_cpp("xenial-amd64-connector-cpp", "vm-xenial-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");

bld_bionic_amd64_connector_cpp= bld_linux_connector_cpp("bionic-amd64-connector-cpp", "vm-bionic-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_focal_amd64_connector_cpp= bld_linux_connector_cpp("focal-amd64-connector-cpp", "vm-focal-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_groovy_amd64_connector_cpp= bld_linux_connector_cpp("groovy-amd64-connector-cpp", "vm-groovy-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_buster_amd64_connector_cpp= bld_linux_connector_cpp("buster-amd64-connector-cpp", "vm-buster-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_fedora32_amd64_connector_cpp= bld_linux_connector_cpp("fedora32-amd64-connector-cpp", "vm-fedora32-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_fedora33_amd64_connector_cpp= bld_linux_connector_cpp("fedora33-amd64-connector-cpp", "vm-fedora33-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");
bld_sles12_amd64_connector_cpp= bld_linux_connector_cpp("sles12-amd64-connector-cpp", "vm-sles123-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON");

######################## New (unstable) version builders ######################
bld_centos6_amd64_connector_cpp= bld_linux_connector_cpp("centos6_amd64-connector-cpp", "vm-centos6-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON ");
bld_centos6_x86_connector_cpp= bld_linux_connector_cpp("centos6_x86-connector-cpp", "vm-centos6-i386", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON ");
bld_centos7_amd64_connector_cpp= bld_linux_connector_cpp("centos7_amd64-connector-cpp", "vm-centos7-amd64", "", " -DWITH_SSL=OPENSSL -DWITH_OPENSSL=ON ");
##################### New (unstable) version builders - END ###################

