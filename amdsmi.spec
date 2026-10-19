Name:		amdsmi
Version:	10.1.0
# Upstream library VERSION (ROCm 10.1 / AMD SMI 27.1); SONAME stays .so.27
%global sover 27.1.0
Release:	1
Summary:	AMD System Management Interface library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/amdsmi
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-10.1/amdsmi.tar.gz#/amdsmi-%{version}.tar.gz
# TheRock tarball omits esmi; pin is ESMI_GIT_HASH in 10.1 CMakeLists.txt
Source1:	https://github.com/amd/esmi_ib_library/archive/d494a3194ceb4cc4dbb2debf9fcbe8773c6d3bef.tar.gz#/esmi_ib_library-d494a319.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libnl-genl-3.0)
BuildRequires:	pkgconfig(libmnl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	python3


%description
AMD SMI library (libamd_smi) and amd-smi CLI for monitoring AMD GPUs.
Successor to parts of rocm-smi for modern ROCm stacks.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for amdsmi.

%prep
%autosetup -n amdsmi -p1

# Bundle esmi (ABF has no network for FetchContent git clone).
# 10.1 re-fetches if esmi_ib_library/.git exists and HEAD != ESMI_GIT_HASH.
# Unpack without a .git so cmake reuses src/e_smi.c offline.
# Upstream enables ESMI only on x86_64; still unpack so header install GLOB works.
tar -xzf %{SOURCE1}
rm -rf esmi_ib_library
mv esmi_ib_library-d494a3194ceb4cc4dbb2debf9fcbe8773c6d3bef esmi_ib_library

# goamdsmi_shim is x86-only (-msse/-msse2) and links ESMI CPU symbols that
# are not built on non-x86; we never package the shim either.
sed -i -e '/add_subdirectory(goamdsmi_shim)/d' CMakeLists.txt
%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DBUILD_TESTS=OFF \
	-DBUILD_WRAPPER=OFF \
	-G Ninja
%build
%ninja_build -C build

%install
%ninja_install -C build
# Drop example sources and go shim for now (optional later)
rm -rf %{buildroot}%{_datadir}/amd_smi/example
rm -f %{buildroot}%{_libdir}/libgoamdsmi_shim64.so*
rm -f %{buildroot}%{_includedir}/goamdsmi.h
rm -f %{buildroot}%{_includedir}/amdsmi_go_shim.h
# Fix non-RPM-safe cmake versions if present
sed -i -e 's/PACKAGE_VERSION "[^"]*local[^"]*"/PACKAGE_VERSION "%{version}"/' \
	-e 's/= [0-9.]*.*-local.*/= %{version}/' \
	%{buildroot}%{_libdir}/cmake/amd_smi/*version*.cmake \
	%{buildroot}%{_libdir}/cmake/amd_smi/*config*.cmake 2>/dev/null || true

%files
%license LICENSE
%doc README.md
%{_bindir}/amd-smi
%{_libdir}/libamd_smi.so.*
%{_libexecdir}/amdsmi_cli/
%{_datadir}/amd_smi/
# 10.1 copies the importable module into site-packages when DESTDIR is set
%{python_sitearch}/amdsmi/
%exclude %{_docdir}/amd-smi-lib/*

%files devel
%{_includedir}/amd_smi/
%{_includedir}/e_smi/
%{_includedir}/rocm_smi/
%{_libdir}/libamd_smi.so
%{_libdir}/libamdsminic.a
%{_libdir}/cmake/amd_smi/
