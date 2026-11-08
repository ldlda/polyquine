$RENDERERS->{'ps'} = sub { my $s = $_[0]; $s =~ s/'/''/g; "'" . $s . "'" };
