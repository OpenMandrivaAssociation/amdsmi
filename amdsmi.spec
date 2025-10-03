# Looks like the cmake files are too cluttered to make spotting debugsource
# files possible
%undefine _debugsource_packages

%define major 0
%define libname %mklibname amdsmi
%define devname %mklibname amdsmi -d

Name:		amdsmi
Version:	7.0.1
Release:	1
Source0:	https://github.com/ROCm/amdsmi/archive/refs/tags/rocm-%{version}.tar.gz
Summary:	AMD System Management Interface (SMI) for managing and monitoring GPUs
URL:		https://github.com/ROCm/amdsmi
License:	GPL
Group:		System/Libraries
BuildRequires:	cmake
BuildSystem:	cmake

%patchlist
amdsmi-7.0.1-compile.patch

%description
AMD System Management Interface (SMI) for managing and monitoring GPUs

%package -n %{libname}
Summary:	AMD System Management Interface (SMI) for managing and monitoring GPUs
Group:		System/Libraries

%description -n %{libname}
AMD System Management Interface (SMI) for managing and monitoring GPUs

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

AMD System Management Interface (SMI) for managing and monitoring GPUs

%files
%{_bindir}/*
%{_libexecdir}/amdsmi_cli
%{_datadir}/amd_smi
%doc %{_docdir}/amd-smi-lib

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/libgoamdsmi_shim64.so.*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/*
