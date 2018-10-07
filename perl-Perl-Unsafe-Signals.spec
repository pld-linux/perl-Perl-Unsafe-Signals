#
# Conditional build:
%bcond_without	tests	# do perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Perl
%define		pnam	Unsafe-Signals
Summary:	Perl::Unsafe::Signals - Allow unsafe handling of signals in selected blocks
Summary(pl.UTF-8):	Perl::Unsafe::Signals - pozwala na obsługę niebezpiecznych sygnałów we wskazanych blokach
Name:		perl-Perl-Unsafe-Signals
Version:	0.03
Release:	1
# "same as perl", but GPL in version 2+ is specified afterwards
License:	GPL v2+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Perl/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	3eced0ffa43e5f9978aa9f83a0e13562
URL:		http://search.cpan.org/dist/Perl-Unsafe-Signals/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Quoting perl581delta:

In Perl 5.8.0 the so-called "safe signals" were introduced. This means
that Perl no longer handles signals immediately but instead "between
opcodes", when it is safe to do so. The earlier immediate handling
easily could corrupt the internal state of Perl, resulting in
mysterious crashes.

It's possible since perl 5.8.1 to globally disable this feature by
using the PERL_SIGNALS environment variables (as specified in
"PERL_SIGNALS" in perlrun); but there's no way to disable it locally,
for a short period of time. That's however something you might want to
do, if, for example, your Perl program calls a C routine that will
potentially run for a long time and for which you want to set a
timeout.

This module therefore allows you to define UNSAFE_SIGNALS blocks in
which signals will be handled "unsafely".

Note that, no matter how short you make the unsafe block, it will
still be unsafe. Use with caution.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorarch}/Perl/Unsafe
%{perl_vendorarch}/Perl/Unsafe/Signals.pm
%dir %{perl_vendorarch}/auto/Perl/Unsafe
%dir %{perl_vendorarch}/auto/Perl/Unsafe/Signals
%attr(755,root,root) %{perl_vendorarch}/auto/Perl/Unsafe/Signals/Signals.so
%{_mandir}/man3/Perl::Unsafe::Signals.3pm*
