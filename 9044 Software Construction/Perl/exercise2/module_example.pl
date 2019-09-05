#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au for COMP2041
#
# Use of a simple Perl module.
#
# The directory containing Example_Module.pm should be in environment variable PERL5LIB
# PERL5LIB is colon separated list of directory to search similar to PATH
#

use Example_Module qw/max/;

# As max is specified in our import list it can be used without the module name
print max(42,3,5), "\n";

# We don't import min explicitly so it needs the module name
print Example_Module::min(42,3,5), "\n";
