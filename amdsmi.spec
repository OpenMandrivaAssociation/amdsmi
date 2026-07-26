Name:		amdsmi
Version:	7.14.0
# Upstream SOVERSION year.minor
%global sover 26.5.0
Release:	1
Summary:	AMD System Management Interface library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/amdsmi
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-7.14/amdsmi.tar.gz#/amdsmi-%{version}.tar.gz
# TheRock tarball omits esmi submodule; pin to tag used by amdsmi CMakeLists
Source1:	esmi_ib_library-5.2.1.1.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libnl-genl-3.0)
BuildRequires:	pkgconfig(libmnl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	python3

ExclusiveArch:	%{x86_64}

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

# Bundle esmi (ABF has no network for git clone of the submodule)
tar -xzf %{SOURCE1}
rm -rf esmi_ib_library
mv esmi_ib_library-esmi_pkg_ver-5.2.1.1 esmi_ib_library

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
%{_libdir}/libamd_smi.so.%{sover}
%{_libdir}/libamd_smi.so.26
%{_libexecdir}/amdsmi_cli/
%{_datadir}/amd_smi/
%exclude %{_docdir}/amd-smi-lib/*

%files devel
%{_includedir}/amd_smi/
%{_includedir}/e_smi/
%{_includedir}/rocm_smi/
%{_libdir}/libamd_smi.so
%{_libdir}/libamdsminic.a
%{_libdir}/cmake/amd_smi/
